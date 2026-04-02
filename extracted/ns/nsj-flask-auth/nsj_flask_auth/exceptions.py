class MissingAuthorizationHeader(Exception):
    pass


class Unauthorized(Exception):
    pass


class Forbidden(Exception):
    pass

class InternalUnauthorized(Exception):
    pass

class UnknowAuthorizationException(Exception):
    pass
