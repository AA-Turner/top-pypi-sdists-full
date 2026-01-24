from http.client import HTTPException


class GalileoHTTPException(HTTPException):
    """Galileo HTTP exception to wrap all http exceptions."""

    def __init__(self, message: str, status_code: int, response_text: str) -> None:
        self.message = message
        self.status_code = status_code
        self.response_text = response_text
