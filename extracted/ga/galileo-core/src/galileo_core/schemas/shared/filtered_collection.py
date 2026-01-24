from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import UUID4, BaseModel, Field, ValidationInfo, field_validator
from typing_extensions import Annotated


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
    between = "between"


class FilterBase(BaseModel):
    name: Optional[str]


StringOperator = Literal[Operator.eq, Operator.ne, Operator.contains]


class StringFilter(FilterBase):
    """
    Filters on a string field.
    """

    filter_type: Literal[FilterType.string] = FilterType.string
    value: str
    operator: StringOperator
    case_sensitive: bool = True


CollectionOperator = Literal[Operator.contains, Operator.not_in]


class CollectionFilter(FilterBase):
    """
    Filters for string items in a collection/list.
    """

    filter_type: Literal[FilterType.collection] = FilterType.collection
    value: str
    operator: CollectionOperator


MapOperator = Literal[Operator.one_of, Operator.not_in, Operator.eq, Operator.ne]


class MapFilter(FilterBase):
    """
    Filters for string items in a map / dictionary.
    """

    filter_type: Literal[FilterType.map] = FilterType.map
    operator: MapOperator
    key: str
    value: Union[str, List[str]]

    @field_validator("value", mode="before")
    def validate_value(cls, value: Union[str, List[str]], info: ValidationInfo) -> Union[str, List[str]]:
        operator = info.data.get("operator")
        if operator in (Operator.one_of, Operator.not_in):
            if not isinstance(value, list):
                raise ValueError(f"Value must be a list for operator {operator}.")
        elif operator in (Operator.eq, Operator.ne):
            if isinstance(value, list):
                raise ValueError(f"Value must be a string for operator {operator}.")
        return value


EnumOperator = Literal[Operator.eq, Operator.ne]


class EnumFilter(FilterBase):
    """
    Filters on a string field, with limited categories.
    """

    filter_type: Literal[FilterType.enum] = FilterType.enum
    value: str
    operator: EnumOperator


class IDFilter(FilterBase):
    """
    Filters on a UUID field.
    """

    filter_type: Literal[FilterType.id] = FilterType.id
    value: UUID4


DateOperator = Literal[Operator.eq, Operator.ne, Operator.gt, Operator.gte, Operator.lt, Operator.lte]


class DateFilter(FilterBase):
    """
    Filters on a datetime field.
    """

    filter_type: Literal[FilterType.date] = FilterType.date
    value: datetime
    operator: DateOperator


NumberOperator = Literal[
    Operator.eq, Operator.ne, Operator.gt, Operator.gte, Operator.lt, Operator.lte, Operator.between
]


class CustomNumberFilter(FilterBase):
    filter_type: Literal[FilterType.custom_number] = FilterType.custom_number
    value: Union[int, List[int]]
    operator: NumberOperator


class CustomBooleanFilter(FilterBase):
    filter_type: Literal[FilterType.custom_boolean] = FilterType.custom_boolean
    value: bool


class CustomUUIDFilter(FilterBase):
    filter_type: Literal[FilterType.custom_uuid] = FilterType.custom_uuid
    value: UUID4


QueryFilterV2 = Annotated[
    Union[
        CollectionFilter,
        CustomBooleanFilter,
        CustomNumberFilter,
        CustomUUIDFilter,
        DateFilter,
        EnumFilter,
        IDFilter,
        MapFilter,
        StringFilter,
    ],
    Field(discriminator="filter_type"),
]
