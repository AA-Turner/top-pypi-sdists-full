class MissingEnvironmentKeysError(Exception):
    def __init__(self, missing_keys: set[str]):
        self.missing_keys = missing_keys


class NoEnvironmentVariablesFoundError(Exception):
    pass
