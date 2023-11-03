from typing import NotRequired, TypedDict

import keyof
import keyof.compat


class Data(TypedDict):
    version: int
    command: str
    additional_data: NotRequired[str]


class OtherData(Data):
    other: float


DataKey = keyof.KeyOf[Data]
DataRequiredKey = keyof.RequiredKeyOf[Data]
DataNotRequiredKey = keyof.NotRequiredKeyOf[Data]

DataCompatKey = keyof.compat.KeyOf[Data]
DataCompatRequiredKey = keyof.compat.RequiredKeyOf[Data]
DataCompatNotRequiredKey = keyof.compat.NotRequiredKeyOf[Data]
