from typing import TYPE_CHECKING, Any, TypeAlias

if TYPE_CHECKING:
    KeyOf: TypeAlias = Any
    RequiredKeyOf: TypeAlias = Any
    NotRequiredKeyOf: TypeAlias = Any
else:
    from keyof import KeyOf, NotRequiredKeyOf, RequiredKeyOf  # noqa: F401
