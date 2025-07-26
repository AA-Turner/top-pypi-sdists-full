"""
Exceptions raised by Typed Settings.
"""

from ._compat import PY_311


if not PY_311:
    from exceptiongroup import ExceptionGroup


class TsError(Exception):
    """
    **Basse class** for all typed settings exceptions.
    """


class UnknownFormatError(TsError):
    """
    Raised when no file format loader is configured for a given config file.
    """


class ConfigFileNotFoundError(TsError):
    """
    Raised when a mandatory config file does not exist.
    """


class ConfigFileLoadError(TsError):
    """
    Raised when a config file exists but cannot be read or parsed/loaded.
    """


class InvalidOptionsError(TsError):
    """
    Raised when loaded settings contain an option that is not defined in the
    settings class.
    """


class InvalidValueError(TsError):
    """
    Raised the value of an option cannot be converted to the correct type.
    """


class InvalidSettingsError(TsError, ExceptionGroup):
    """
    Raised when the loaded settings cannot be converted to an instances of the
    settings class.

    This is a subclass of both, :exc:`TsError` and :exc:`ExceptionGroup`.

    .. versionadded:: 25.0.0
    """
