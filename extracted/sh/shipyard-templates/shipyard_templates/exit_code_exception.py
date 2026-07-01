def standardize_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ExitCodeException as error:
            raise ExitCodeException(error.message, error.exit_code) from error
        except Exception as error:
            raise ExitCodeException(
                f"Unknown Error occurred: {str(error)}", 1
            ) from error

    return wrapper


class ExitCodeException(Exception):
    def __init__(self, message, exit_code):
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code
