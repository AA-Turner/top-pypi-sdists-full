from http import HTTPStatus

from aws_lambda_powertools.event_handler import Response, content_types


def success_message(msg="ok", status_code=HTTPStatus.OK.value):
    return Response(
        status_code=status_code,
        content_type=content_types.APPLICATION_JSON,
        body={"message": msg},
    )


def success_response(body, status_code=HTTPStatus.OK.value):

    return Response(
        status_code=status_code,
        content_type=content_types.APPLICATION_JSON,
        body=body,
    )


def error_message(msg="error", data=None, status_code=HTTPStatus.BAD_REQUEST.value):
    return Response(
        status_code=status_code,
        content_type=content_types.APPLICATION_JSON,
        body={"message": msg, "data": data},
    )
