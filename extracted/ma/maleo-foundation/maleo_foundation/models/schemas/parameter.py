import re
import urllib.parse
from pydantic import BaseModel, Field, field_validator
from maleo_foundation.constants import SORT_COLUMN_PATTERN, DATE_FILTER_PATTERN
from maleo_foundation.enums import BaseEnums
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.types import BaseTypes
from maleo_foundation.extended_types import ExtendedTypes

class BaseParameterSchemas:
    class IdentifierType(BaseModel):
        identifier: BaseEnums.IdentifierTypes = Field(..., description="Data's identifier type")

    class IdentifierValue(BaseModel):
        value: BaseTypes.IdentifierValue = Field(..., description="Data's identifier value")

    class OptionalListOfIds(BaseModel):
        ids: BaseTypes.OptionalListOfIntegers = Field(None, description="Specific Ids")

    class OptionalListOfUuids(BaseModel):
        uuids: BaseTypes.OptionalListOfUUIDs = Field(None, description="Specific Uuids")

    class Filters(BaseModel):
        filters: BaseTypes.ListOfStrings = Field([], description="Filters for date range, e.g. 'created_at|from::<ISO_DATETIME>|to::<ISO_DATETIME>'.")

        @field_validator("filters")
        @classmethod
        def validate_date_filters(cls, values):
            if isinstance(values, list):
                decoded_values = [urllib.parse.unquote(value) for value in values]
                #* Replace space followed by 2 digits, colon, 2 digits with + and those digits
                fixed_values = []
                for value in decoded_values:
                    #* Look for the pattern: space followed by 2 digits, colon, 2 digits
                    fixed_value = re.sub(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+) (\d{2}:\d{2})', r'\1+\2', value)
                    fixed_values.append(fixed_value)
                final_values = [value for value in fixed_values if DATE_FILTER_PATTERN.match(value)]
                return final_values

    class DateFilters(BaseModel):
        date_filters: ExtendedTypes.ListOfDateFilters = Field([], description="Date filters to be applied")

    class OptionalListOfStatuses(BaseModel):
        statuses: BaseTypes.OptionalListOfStatuses = Field(None, description="Data's status")

    class OptionalListOfCodes(BaseModel):
        codes: BaseTypes.OptionalListOfStrings = Field(None, description="Specific Codes")

    class OptionalListOfKeys(BaseModel):
        keys: BaseTypes.OptionalListOfStrings = Field(None, description="Specific Keys")

    class OptionalListOfNames(BaseModel):
        names: BaseTypes.OptionalListOfStrings = Field(None, description="Specific Names")

    class Search(BaseModel):
        search: BaseTypes.OptionalString = Field(None, description="Search string.")

    class Sorts(BaseModel):
        sorts: BaseTypes.ListOfStrings = Field(["id.asc"], description="Sorting columns in 'column_name.asc' or 'column_name.desc' format.")

        @field_validator("sorts")
        @classmethod
        def validate_sorts(cls, values):
            return [value for value in values if SORT_COLUMN_PATTERN.match(value)]

    class SortColumns(BaseModel):
        sort_columns: ExtendedTypes.ListOfSortColumns = Field([BaseGeneralSchemas.SortColumn(name="id", order=BaseEnums.SortOrder.ASC)], description="List of columns to be sorted")

    class Expand(BaseModel):
        expand: BaseTypes.OptionalListOfStrings = Field(None, description="Expanded field(s)")

    class Data(BaseModel):
        data: BaseTypes.StringToAnyDict = Field(..., description="Data")