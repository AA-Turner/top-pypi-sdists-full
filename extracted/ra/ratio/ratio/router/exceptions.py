class InvalidRouteError(ValueError):
    pass


class PathAlreadyExistsError(ValueError):
    def __init__(self, path: str, regex: str | None = None):
        if regex is None:
            self.message = f"The following direct path already exists: '{path}'"
        else:
            self.message = f"The following dynamic path already exists, because the path '{path}' signature '{regex}' already exists.'"

        super().__init__(self.message)
