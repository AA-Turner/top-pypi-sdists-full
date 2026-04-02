class FlipSideRateLimitError(Exception):
    def __init__(self):
        message = "FlipSide ratelimit exceeded, for more information visit"
        super().__init__(message)


class FlipSideQueryError(Exception):
    def __init__(self, e):
        message = f"Your FlipSide query is malformed: {e.message}"
        super().__init__(message)


class FlipSideApiError(Exception):
    def __init__(self, e):
        message = f"An api error occurred: {str(e)}"
        super().__init__(message)


class PostgresConstraintError(Exception):
    pass


class APIError(Exception):
    def __init__(self, e):
        message = f"An error in calling api: {str(e)}"
        super().__init__(message)
