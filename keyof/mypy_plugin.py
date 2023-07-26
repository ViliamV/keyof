from collections.abc import Callable, Sequence
from typing import Final

from mypy.errorcodes import TYPE_ARG
from mypy.plugin import AnalyzeTypeContext, Plugin, TypeAnalyzerPluginInterface
from mypy.types import (
    LiteralType,
    Type,
    TypeAliasType,
    TypedDictType,
    UninhabitedType,
    UnionType,
)

_MIN_MYPY_VERSION = (1, 0, 0)
_TYPE_NAME: Final = "KeyOf"
_TYPES_TO_ANALYZE: Final = frozenset(["keyof.KeyOf", "keyof.compat.KeyOf"])


def _create_string_literal(value: str, api: TypeAnalyzerPluginInterface) -> LiteralType:
    return LiteralType(value, api.named_type("builtins.str", []))


def _create_literal_type(values: Sequence[str], api: TypeAnalyzerPluginInterface) -> UnionType | LiteralType:
    if len(values) == 1:
        return _create_string_literal(values[0], api)
    return UnionType([_create_string_literal(value, api) for value in values])


def _analyze_typed_dict_key(ctx: AnalyzeTypeContext) -> Type:
    if (args_len := len(ctx.type.args)) != 1:
        ctx.api.fail(
            f'"{_TYPE_NAME}" expects 1 type argument, but {args_len} given',
            ctx.context,
            code=TYPE_ARG,
        )
        return UninhabitedType()
    argument = ctx.type.args[0]
    analyzed: Type | None = ctx.api.analyze_type(argument)
    if isinstance(analyzed, TypeAliasType):
        analyzed = analyzed.expand_all_if_possible()
    if not isinstance(analyzed, TypedDictType):
        ctx.api.fail(
            f'Argument 1 to "{_TYPE_NAME}" has incompatible type "{analyzed}"; expected "TypedDict"',
            ctx.context,
        )
        return UninhabitedType()
    return _create_literal_type(list(analyzed.items.keys()), ctx.api)


class CustomPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str) -> Callable[[AnalyzeTypeContext], Type] | None:
        if fullname in _TYPES_TO_ANALYZE:
            return _analyze_typed_dict_key
        return None


def _version_str_to_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.partition("+")[0].split("."))


def plugin(version: str) -> type[Plugin]:
    if _version_str_to_tuple(version) >= _MIN_MYPY_VERSION:
        return CustomPlugin
    return Plugin
