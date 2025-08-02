import click


class AlreadyExistsException(click.ClickException):
    pass


class ParseException(Exception):
    def __init__(self, err: str, lineno: int = -1):
        self.lineno: int = lineno
        super().__init__(err)


class IncludeFileNotFoundException(Exception):
    def __init__(self, err: str, lineno: int = -1):
        self.lineno: int = lineno
        super().__init__(err)


class ValidationException(Exception):
    def __init__(self, err: str, lineno: int = -1) -> None:
        self.lineno: int = lineno
        super().__init__(err)
