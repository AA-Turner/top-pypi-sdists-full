from http import HTTPStatus


class NotReadyYetError(Exception):
    def __init__(self,
                 message: str = 'NOT_READY',
                 status: HTTPStatus = HTTPStatus.CONFLICT):
        self.message = message
        self.status = status
