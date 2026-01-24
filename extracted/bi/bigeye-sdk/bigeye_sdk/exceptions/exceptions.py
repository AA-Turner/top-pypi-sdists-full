class FileLoadException(Exception):
    def __init__(self, message: str):
        self.message = message


class FileNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message


class AttributeTypeException(Exception):
    def __init__(self, message: str):
        self.message = message


class InvalidConfigurationException(Exception):
    def __init__(self, message: str):
        self.message = message


class ConfigNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message


class ConfigParseException(Exception):
    def __init__(self, message: str):
        self.message = message


class BrowserAuthException(Exception):
    def __init__(self, message: str):
        self.message = message


class BigConfigValidationException(Exception):
    def __init__(self, message: str):
        self.message = message


class NoSourcesFoundException(Exception):
    def __init__(self, message: str):
        self.message = message


class TableNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message


class BigconfigIncompleteException(Exception):
    def __init__(self, message: str):
        self.message = message


class WorkspaceNotSetException(Exception):
    def __init__(self, message: str):
        self.message = message


class DeltaUnhealthyException(Exception):
    def __init__(self, message: str):
        self.message = message


class MetricUnhealthyException(Exception):
    def __init__(self, message: str):
        self.message = message


class AuthenticationFailedException(Exception):
    def __init__(self, message: str):
        self.message = message

class CollectionNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message