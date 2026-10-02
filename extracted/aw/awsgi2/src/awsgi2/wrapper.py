"""The WSGI wrapper for APIGW/ELB events"""
from typing import Any, Mapping, Optional, Union, TYPE_CHECKING


from .impl import select_impl
from .base import StrSetSrcTypes

if TYPE_CHECKING:
    from aws_lambda_powertools.utilities.typing import LambdaContext


def response(
    app: Any,
    event: Mapping[str, Any],
    context: "LambdaContext",
    base64_content_types: Optional[StrSetSrcTypes] = None,
    base64_content_encodings: Optional[StrSetSrcTypes] = None,
) -> Mapping[str, Union[bool, str, int, Mapping[str, str]]]:
    """Wrap event to WSGI things and have the app process it"""
    environ, got_class = select_impl(event, context)

    instance = got_class(
        base64_content_types=base64_content_types,
        base64_content_encodings=base64_content_encodings,
    )
    output = app(environ(event, context), instance)
    return instance.response(output)
