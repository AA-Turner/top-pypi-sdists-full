"""Implementations for APIGW and ELB"""
from typing import Mapping, Dict, Tuple, Callable, Any, Union, Type, cast, TYPE_CHECKING
import io


from .base import StartResponse
from .wsgienv import environ

if TYPE_CHECKING:
    from aws_lambda_powertools.utilities.typing import LambdaContext


class StartResponseGW(StartResponse):
    """APIGW sepcifics"""

    def response(self, output: Union[bytes, io.BytesIO]) -> Mapping[str, Union[bool, str, int, Mapping[str, str]]]:
        """Create the response dict"""
        resp = cast(Dict[str, Union[bool, str, int, Mapping[str, str]]], super().response(output))
        resp["statusCode"] = int(cast(str, resp["statusCode"]))
        return resp


class StartResponseELB(StartResponse):
    """ELB specifics"""

    def response(self, output: Union[bytes, io.BytesIO]) -> Mapping[str, Union[bool, str, int, Mapping[str, str]]]:
        """Create the response dict"""
        resp = cast(Dict[str, Union[bool, str, int, Mapping[str, str]]], super().response(output))
        resp["statusCode"] = int(cast(str, resp["statusCode"]))
        resp["statusDescription"] = self.status_line
        return resp


# FIXME: define the types for the environ callable
def select_impl(event: Mapping[str, Any], _context: "LambdaContext") -> Tuple[Callable[..., Any], Type[StartResponse]]:
    """Select correct StartResponse implementation"""
    if "elb" in event.get("requestContext", {}):
        return environ, StartResponseELB
    return environ, StartResponseGW
