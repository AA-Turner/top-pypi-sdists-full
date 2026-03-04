from datetime import datetime
from enum import Enum
from typing import Annotated, ClassVar, Generic, Literal, TypeVar

from pydantic import (
    UUID4,
    BaseModel,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)


class Operator(str, Enum):
    eq = "eq"
    ne = "ne"
    contains = "contains"
    one_of = "one_of"
    not_in = "not_in"
    gt = "gt"
    gte = "gte"
    lt = "lt"
    lte = "lte"
    between = "between"


class FilterType(str, Enum):
    boolean = "boolean"
    number = "number"
    string = "string"
    enum = "enum"
    collection = "collection"
    map = "map"
    custom_number = "custom_number"
    custom_boolean = "custom_boolean"
    custom_uuid = "custom_uuid"
    id = "id"
    date = "date"
    function = "function"


class FilterBase(BaseModel):
    name: str | None


BooleanOperator = Literal[Operator.eq, Operator.ne]


class BooleanFilter(FilterBase):
    """
    Filters on a boolean field.
    """

    filter_type: ClassVar[Literal[FilterType.boolean]] = FilterType.boolean
    operator: BooleanOperator = Field(default=Operator.eq)
    value: bool


StringOperator = Literal[Operator.eq, Operator.ne, Operator.contains, Operator.one_of, Operator.not_in]


class StringFilter(FilterBase):
    """
    Filters on a string field.
    """

    filter_type: ClassVar[Literal[FilterType.string]] = FilterType.string
    operator: StringOperator
    value: str | list[str]
    case_sensitive: bool = True

    @model_validator(mode="after")
    def validate_operator_value(self) -> "StringFilter":
        operator = self.operator
        value = self.value
        match operator:
            case Operator.one_of | Operator.not_in:
                if not isinstance(value, list):
                    raise ValueError(f"Value must be a list for operator {operator}.")
            case Operator.eq | Operator.ne | Operator.contains:
                if isinstance(value, list):
                    raise ValueError(f"Value must be a string for operator {operator}.")
            case _:
                raise ValueError(f"Invalid operator {operator}.")
        return self


CollectionOperator = Literal[Operator.eq, Operator.contains, Operator.not_in]


class CollectionFilter(FilterBase):
    """
    Filters for string items in a collection/list.
    """

    filter_type: ClassVar[Literal[FilterType.collection]] = FilterType.collection
    operator: CollectionOperator
    value: str | list[str]
    case_sensitive: bool = True

    @model_validator(mode="after")
    def validate_operator_value(self) -> "CollectionFilter":
        operator = self.operator
        value = self.value
        match operator:
            case Operator.not_in:
                if not isinstance(value, list):
                    raise ValueError(f"Value must be a list for operator {operator}.")
            case Operator.eq | Operator.contains:
                if not isinstance(value, str):
                    raise ValueError(f"Value must be a string for operator {operator}.")
            case _:
                raise ValueError(f"Invalid operator {operator}.")
        return self


MapOperator = Literal[Operator.one_of, Operator.not_in, Operator.eq, Operator.ne]


class MapFilter(FilterBase):
    """
    Filters for string items in a map / dictionary.
    """

    filter_type: ClassVar[Literal[FilterType.map]] = FilterType.map
    operator: MapOperator
    key: str
    value: str | list[str]

    @model_validator(mode="after")
    def validate_operator_value(self) -> "MapFilter":
        operator = self.operator
        value = self.value
        if operator in (Operator.one_of, Operator.not_in):
            if not isinstance(value, list):
                raise ValueError(f"Value must be a list for operator {operator}.")
        elif operator in (Operator.eq, Operator.ne):
            if isinstance(value, list):
                raise ValueError(f"Value must be a string for operator {operator}.")
        return self


EnumOperator = Literal[Operator.eq, Operator.ne, Operator.one_of, Operator.not_in]

E = TypeVar("E", bound="Enum")


class EnumFilter(FilterBase, Generic[E]):
    """
    Filters on a string field, with limited categories.
    """

    filter_type: ClassVar[Literal[FilterType.enum]] = FilterType.enum
    operator: EnumOperator
    value: Annotated[
        E | list[E],
        Field(
            json_schema_extra={
                "anyOf": [
                    {
                        "type": "string",
                        "example": "ENUM_VALUE",
                        "description": "Single enum value - specific options depend on the concrete enum type used",
                    },
                    {
                        "type": "array",
                        "items": {"type": "string", "example": "ENUM_VALUE"},
                        "example": ["ENUM_VALUE_1", "ENUM_VALUE_2"],
                        "description": "Array of enum values",
                    },
                ]
            }
        ),
    ]


IDOperator = Literal[Operator.eq, Operator.ne, Operator.one_of, Operator.not_in, Operator.contains]


class IDFilter(FilterBase):
    """
    Filters on a UUID field.
    """

    filter_type: ClassVar[Literal[FilterType.id]] = FilterType.id
    operator: IDOperator = Field(default=Operator.eq)
    value: UUID4 | list[UUID4 | str] | str

    @field_validator("value", mode="before")
    def validate_value(
        cls, value: UUID4 | list[UUID4 | str] | str, info: ValidationInfo
    ) -> UUID4 | list[UUID4 | str] | str:
        operator = info.data.get("operator", Operator.eq)
        match operator:
            case Operator.one_of | Operator.not_in:
                if not isinstance(value, list):
                    raise ValueError(f"Value must be a list for operator {operator}.")
            case Operator.eq | Operator.ne:
                if isinstance(value, list):
                    raise ValueError(f"Value must be a single UUID for operator {operator}.")
            case Operator.contains:
                if not isinstance(value, str):
                    raise ValueError(f"Value must be a string for operator {operator}.")
            case _:
                raise ValueError(f"Invalid operator {operator}.")
        return value


DateOperator = Literal[Operator.eq, Operator.ne, Operator.gt, Operator.gte, Operator.lt, Operator.lte]


class DateFilter(FilterBase):
    """Filters on a datetime field."""

    filter_type: ClassVar[Literal[FilterType.date]] = FilterType.date
    operator: DateOperator
    value: datetime


NumberOperator = Literal[
    Operator.eq,
    Operator.ne,
    Operator.gt,
    Operator.gte,
    Operator.lt,
    Operator.lte,
    Operator.between,
]


class CustomNumberFilter(FilterBase):
    filter_type: ClassVar[Literal[FilterType.custom_number]] = FilterType.custom_number
    operator: NumberOperator
    value: int | float | list[int] | list[float]


class CustomBooleanFilter(FilterBase):
    filter_type: ClassVar[Literal[FilterType.custom_boolean]] = FilterType.custom_boolean
    value: bool


class CustomFunctionFilter(FilterBase):
    filter_type: ClassVar[Literal[FilterType.function]] = FilterType.function


class CustomUUIDFilter(FilterBase):
    filter_type: ClassVar[Literal[FilterType.custom_uuid]] = FilterType.custom_uuid
    value: UUID4


QueryFilterV2 = Annotated[
    CollectionFilter
    | CustomBooleanFilter
    | CustomNumberFilter
    | CustomUUIDFilter
    | DateFilter
    | EnumFilter
    | IDFilter
    | MapFilter
    | StringFilter
    | BooleanFilter
    | CustomFunctionFilter,
    Field(discriminator="filter_type"),
]
