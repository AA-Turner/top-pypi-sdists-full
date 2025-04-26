import json
from http import HTTPStatus

from aws_lambda_powertools.event_handler import Response, content_types
from aws_lambda_powertools.event_handler.exceptions import BadRequestError

from aws_packages.auth.auth_backend_abc import AuthBackendBase
from aws_packages.auth.models import AuthenticationRequest, LoginResponse


def process_authenticate_request(request_body, auth_backend: AuthBackendBase):
    if request_body is None:
        raise BadRequestError("No request body provided")

    request_obj = AuthenticationRequest(**json.loads(request_body))

    try:
        auth_user = auth_backend.authenticate(request_obj)
    except Exception as e:
        # TODO: Raise error instead of response
        return Response(
            status_code=HTTPStatus.BAD_REQUEST.value,
            content_type=content_types.APPLICATION_JSON,
            body={"message": str(e)},
        )

    return Response(
        status_code=HTTPStatus.OK.value,
        content_type=content_types.APPLICATION_JSON,
        body=LoginResponse(
            access_token=auth_backend.get_access_token(auth_user)
        ).as_dict(),
    )
