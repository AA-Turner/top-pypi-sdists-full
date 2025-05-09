# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .employee_wage import EmployeeWage
import pydantic
from .error import Error
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class GetEmployeeWageResponse(UncheckedBaseModel):
    """
    A response to a request to get an `EmployeeWage`. The response contains
    the requested `EmployeeWage` objects and might contain a set of `Error` objects if
    the request resulted in errors.
    """

    employee_wage: typing.Optional[EmployeeWage] = pydantic.Field(default=None)
    """
    The requested `EmployeeWage` object.
    """

    errors: typing.Optional[typing.List[Error]] = pydantic.Field(default=None)
    """
    Any errors that occurred during the request.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
