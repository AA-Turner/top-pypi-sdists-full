class ChargehoundError(Exception):
    def __init__(self, error_response):
        super(ChargehoundError, self).__init__(error_response['message'])
        self.status = error_response['status']
        self.message = error_response['message']
        self.type = error_response.get('type')


class ChargehoundAuthenticationError(ChargehoundError):
    pass


class ChargehoundBadRequestError(ChargehoundError):
    pass


def create_chargehound_error(error_response):
    error = error_response['error']
    if error['status'] == 401:
        raise ChargehoundAuthenticationError(error)
    elif error['status'] == 403:
        raise ChargehoundAuthenticationError(error)
    elif error['status'] == 400:
        raise ChargehoundBadRequestError(error)
    else:
        raise ChargehoundError(error)
