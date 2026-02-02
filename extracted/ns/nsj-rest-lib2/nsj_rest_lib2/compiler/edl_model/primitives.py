import enum

from typing import Annotated, List, Union
from pydantic import StringConstraints

REGEX_EXTERNAL_REF = r"^(\w+)\/(\w+)$"
REGEX_EXTERNAL_COMPONENT_REF = r"^(\w+)\/(\w+)\/([\w\/#]+)$"
REGEX_INTERNAL_REF = r"^#\/components\/([\w\/#]+)$"

ExternalRefType = Annotated[str, StringConstraints(pattern=REGEX_EXTERNAL_REF)]
ExternalComponentRefType = Annotated[
    str, StringConstraints(pattern=REGEX_EXTERNAL_COMPONENT_REF)
]
InternalRefType = Annotated[str, StringConstraints(pattern=REGEX_INTERNAL_REF)]


class PrimitiveTypes(enum.Enum):
    # TODO Validar esses tipos
    STRING = "string"
    TEXT = "text"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    UUID = "uuid"
    CURRENCY = "currency"
    QUANTITY = "quantity"
    CPF = "cpf"
    CNPJ = "cnpj"
    CPF_CNPJ = "cpf_cnpj"
    EMAIL = "email"
    DATE = "date"
    DATETIME = "datetime"
    DURATION = "duration"


PropertyType = Union[
    PrimitiveTypes, ExternalRefType, ExternalComponentRefType, InternalRefType
]

MAPPING_PRIMITIVE_TYPES_TO_PYTHON = {
    PrimitiveTypes.STRING: "str",
    PrimitiveTypes.TEXT: "str",
    PrimitiveTypes.NUMBER: "float",
    PrimitiveTypes.INTEGER: "int",
    PrimitiveTypes.BOOLEAN: "bool",
    PrimitiveTypes.UUID: "uuid.UUID",
    PrimitiveTypes.CURRENCY: "float",
    PrimitiveTypes.QUANTITY: "float",
    PrimitiveTypes.CPF: "str",
    PrimitiveTypes.CNPJ: "str",
    PrimitiveTypes.CPF_CNPJ: "str",
    PrimitiveTypes.EMAIL: "str",
    PrimitiveTypes.DATE: "datetime.date",
    PrimitiveTypes.DATETIME: "datetime.datetime",
    PrimitiveTypes.DURATION: "relativedelta",
}

BasicTypes = int | bool | float | str
DefaultTypes = BasicTypes | List[BasicTypes]

STR_BASED_TYPES = {
    PrimitiveTypes.STRING,
    PrimitiveTypes.TEXT,
    PrimitiveTypes.EMAIL,
    PrimitiveTypes.CPF,
    PrimitiveTypes.CNPJ,
    PrimitiveTypes.CPF_CNPJ,
}


class CardinalityTypes(enum.Enum):
    C1_1 = "1_1"
    C1_N = "1_N"
    CN_N = "N_N"
