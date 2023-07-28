from collections.abc import Callable
from typing import Final, cast

from mypy.errorcodes import TYPE_ARG
from mypy.nodes import TypeInfo
from mypy.plugin import AnalyzeTypeContext, Plugin, TypeAnalyzerPluginInterface
from mypy.typeanal import TypeAnalyser
from mypy.types import (
    AnyType,
    LiteralType,
    Type,
    TypeAliasType,
    TypedDictType,
    TypeOfAny,
    UnboundType,
    UnionType,
)

_MIN_MYPY_VERSION = (1, 0, 1)
_TYPES_TO_ANALYZE: Final = frozenset(
    [
        "keyof.KeyOf",
        "keyof.RequiredKeyOf",
        "keyof.NotRequiredKeyOf",
        "keyof.compat.KeyOf",
        "keyof.compat.RequiredKeyOf",
        "keyof.compat.NotRequiredKeyOf",
    ]
)


def _create_string_literal(value: str, api: TypeAnalyzerPluginInterface) -> LiteralType:
    return LiteralType(value, api.named_type("builtins.str", []))


def _default_type_analysis(api: TypeAnalyser, type_: UnboundType) -> Type:
    symbol_table_node = api.lookup_qualified(type_.name, type_)
    if symbol_table_node is None:
        return AnyType(TypeOfAny.special_form)
    node = symbol_table_node.node
    if isinstance(node, TypeInfo):
        return api.analyze_type_with_type_info(node, type_.args, type_)
    return AnyType(TypeOfAny.special_form)


def _analyze_typed_dict_key(ctx: AnalyzeTypeContext) -> Type:
    api = cast(TypeAnalyser, ctx.api)
    type_name = ctx.type.name
    if (args_len := len(ctx.type.args)) != 1:
        api.fail(
            f'"{type_name}" expects 1 type argument, but {args_len} given',
            ctx.context,
            code=TYPE_ARG,
        )
        return _default_type_analysis(api, ctx.type)
    argument = ctx.type.args[0]
    analyzed: Type | None = ctx.api.analyze_type(argument)
    if isinstance(analyzed, TypeAliasType):
        analyzed = analyzed.expand_all_if_possible()
    if not isinstance(analyzed, TypedDictType):
        api.fail(
            f'Argument 1 to "{type_name}" has incompatible type "{analyzed}"; expected "TypedDict"',
            ctx.context,
        )
        return _default_type_analysis(api, ctx.type)
    match type_name:
        case "KeyOf":
            keys = set(analyzed.items.keys())
        case "RequiredKeyOf":
            keys = analyzed.required_keys
        case "NotRequiredKeyOf":
            keys = set(analyzed.items.keys()) - analyzed.required_keys
        case _:
            raise RuntimeError(f"Unexpected type name: {type_name!r}")
    return UnionType.make_union([_create_string_literal(key, api) for key in keys])


class KeyOfPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str) -> Callable[[AnalyzeTypeContext], Type] | None:
        if fullname in _TYPES_TO_ANALYZE:
            return _analyze_typed_dict_key
        return None


def _version_str_to_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.partition("+")[0].split("."))


def plugin(version: str) -> type[Plugin]:
    if _version_str_to_tuple(version) >= _MIN_MYPY_VERSION:
        return KeyOfPlugin
    return Plugin
