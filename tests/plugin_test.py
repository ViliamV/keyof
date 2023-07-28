from typing import TypedDict
from keyof import KeyOf
import pytest


class Data(TypedDict):
    version: int
    command: str


def get_data(data: Data, key: KeyOf[Data]) -> int | str:
    return data[key]


@pytest.mark.mypy_testing
def mypy_test_verify_1() -> None:
    # just to make sure mypy plugin testing works as expected
    foo = "abc"
    foo = 123  # E: [assignment]


@pytest.mark.mypy_testing
@pytest.mark.xfail
def mypy_test_verify_2() -> None:
    # just to make sure mypy plugin testing works as expected
    foo = "abc"
    foo = 123


@pytest.mark.mypy_testing
def mypy_test_uc1() -> None:
    data = Data(version=1, command="foo")
    get_data(data, "version")  # OK


@pytest.mark.mypy_testing
def mypy_test_uc2() -> None:
    data = Data(version=1, command="foo")
    with pytest.raises(KeyError):
        get_data(data, "foo")  # E: [arg-type]
