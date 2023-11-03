import pytest

from keyof import KeyOf, NotRequiredKeyOf, RequiredKeyOf

from .conftest import (
    DataCompatKey,
    DataCompatNotRequiredKey,
    DataCompatRequiredKey,
    DataKey,
    DataNotRequiredKey,
    DataRequiredKey,
    OtherData,
)


@pytest.mark.mypy_testing
def test_key() -> None:
    _key: DataKey = "version"
    _key = "foo"  # E: [assignment]
    _key = 123  # E: [assignment]


@pytest.mark.mypy_testing
def test_compat_key() -> None:
    _key: DataCompatKey = "version"
    _key = "foo"  # E: [assignment]
    _key = 123  # E: [assignment]


@pytest.mark.mypy_testing
def test_required_key() -> None:
    _key: DataRequiredKey = "version"
    _key = "command"
    _key = "additional_data"  # E: [assignment]
    _key = "foo"  # E: [assignment]


@pytest.mark.mypy_testing
def test_compat_required_key() -> None:
    _key: DataCompatRequiredKey = "version"
    _key = "command"
    _key = "additional_data"  # E: [assignment]
    _key = "foo"  # E: [assignment]


@pytest.mark.mypy_testing
def test_not_required_key() -> None:
    _key: DataNotRequiredKey = "additional_data"
    _key = "command"  # E: [assignment]
    _key = "version"  # E: [assignment]
    _key = "foo"  # E: [assignment]


@pytest.mark.mypy_testing
def test_compat_not_required_key() -> None:
    _key: DataCompatNotRequiredKey = "additional_data"
    _key = "command"  # E: [assignment]
    _key = "version"  # E: [assignment]
    _key = "foo"  # E: [assignment]


@pytest.mark.parametrize("cls", (KeyOf, RequiredKeyOf, NotRequiredKeyOf))
def test_runtime_behavior(cls: type) -> None:
    with pytest.raises(TypeError):
        cls()
    with pytest.raises(TypeError):

        class _SubClass(cls):
            ...


@pytest.mark.mypy_testing
def test_subclassing() -> None:
    _key: KeyOf[OtherData] = "other"
    _key = "command"
    _key = "version"
    _key = "foo"  # E: [assignment]
