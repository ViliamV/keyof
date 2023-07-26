from typing import Any, Generic, NoReturn, TypeVar

_T = TypeVar("_T")


class KeyOf(Any, Generic[_T]):
    def __new__(cls, *_args: Any, **_kwargs: Any) -> NoReturn:
        raise TypeError("Type KeyOf cannot be instantiated.")

    def __init_subclass__(cls, *_args: Any, **_kwargs: Any) -> NoReturn:
        raise TypeError("Cannot subclass KeyOf")
