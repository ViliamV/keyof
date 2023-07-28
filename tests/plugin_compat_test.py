from typing import TypedDict
from keyof.compat import KeyOf
import pytest


class Data2(TypedDict):
    version: int
    command: str


def get_data2(data: Data2, key: KeyOf[Data2]) -> int | str:
    return data[key]


@pytest.mark.mypy_testing
def mypy_test_uc1() -> None:
    data = Data2(version=1, command="foo")
    get_data2(data, "version")  # OK


@pytest.mark.mypy_testing
def mypy_test_uc2() -> None:
    data = Data2(version=1, command="foo")
    with pytest.raises(KeyError):
        get_data2(data, "foo")  # E: [arg-type]
