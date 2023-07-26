# KeyOf

[Mypy](https://mypy-lang.org/) plugin for static type checking of [TypedDict](https://peps.python.org/pep-0589/) keys
inspired by TypeScript's [`keyof` type operator](https://www.typescriptlang.org/docs/handbook/2/keyof-types.html).

## Requirements

- `python>=3.11`
- `mypy>=1.0.1`

## Installation

```shell
pip install keyof
```

### Mypy plugin

Add `keyof.mypy_plugin` to the list of plugins in your [mypy config file](https://mypy.readthedocs.io/en/latest/config_file.html)
(for example `pyproject.toml`)

```toml
[tool.mypy]
plugins = ["keyof.mypy_plugin"]
```

## Usage

```python
from typing import TypedDict

from keyof import KeyOf


class Data(TypedDict):
    version: int
    command: str


def get_data(data: Data, key: KeyOf[Data]) -> int | str:
    return data[key]


data = Data(version=1, command="foo")

get_data(data, "version")  # OK

get_data(data, "not_existing_key") # error
# Argument 2 to "get_data" has incompatible type "Literal['not_existing_key']"; expected "Literal['version', 'command']"
```
