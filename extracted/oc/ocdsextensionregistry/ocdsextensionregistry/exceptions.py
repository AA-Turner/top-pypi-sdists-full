class OCDSExtensionRegistryError(Exception):
    """Base class for exceptions from within this package."""


class DoesNotExist(OCDSExtensionRegistryError):  # noqa: N818
    """Raised if an object wasn't found for the given parameters."""


class MissingExtensionMetadata(OCDSExtensionRegistryError):  # noqa: N818
    """Raised if a method call requires extensions metadata, with which the extension registry was not initialized."""


class NotAvailableInBulk(OCDSExtensionRegistryError):  # noqa: N818
    """Raised if files are required to be available in bulk, but are not."""


class UnknownLatestVersion(OCDSExtensionRegistryError):  # noqa: N818
    """Raised if the latest version of an extension can't be determined."""


class UnsupportedSchemeError(OCDSExtensionRegistryError):
    """Raised if a URI scheme is unsupported."""


class CommandError(OCDSExtensionRegistryError):
    """Errors from within this package's CLI."""


class SphinxError(OCDSExtensionRegistryError):
    """Raised if Sphinx produces a warning."""


class OCDSExtensionRegistryWarning(UserWarning):
    """Base class for warnings from within this package."""


# The attributes are used by lib-cove-ocds.
class ExtensionWarning(OCDSExtensionRegistryWarning):
    """Used when an extension file can't be read."""

    def __init__(self, extension, exc):
        self.extension = extension
        self.exc = exc

    def __str__(self):
        cls = type(self.exc)
        return f"{self.extension}: {cls.__module__}.{cls.__name__}: {self.exc}"


# The attributes are used by lib-cove-ocds.
class ExtensionCodelistWarning(OCDSExtensionRegistryWarning):
    """Used when a codelist file can't be read."""

    def __init__(self, extension, codelist, exc):
        self.extension = extension
        self.codelist = codelist
        self.exc = exc

    def __str__(self):
        cls = type(self.exc)
        return f"{self.extension}({self.codelist}): {cls.__module__}.{cls.__name__}: {self.exc}"


class VersionedReleaseWarning(OCDSExtensionRegistryWarning):
    """Base class for warnings while creating a versioned release."""


class VersionedReleaseTypeWarning(VersionedReleaseWarning):
    """Used when a type is unexpected or unrecognized while creating a versioned release."""

    def __init__(self, pointer, types, schema):
        self.pointer = pointer
        self.types = types
        self.schema = schema

    def __str__(self):
        return f"{self.pointer} has unrecognized type {self.types}"


class VersionedReleaseRefWarning(VersionedReleaseWarning):
    """Used when a subschema has no ``type`` or ``$ref``, while creating a versioned release."""

    def __init__(self, pointer, schema):
        self.pointer = pointer
        self.schema = schema

    def __str__(self):
        return f"{self.pointer} has no type and no $ref"


class VersionedReleaseItemsWarning(VersionedReleaseWarning):
    """Used when an array has no ``items`` or ``items`` is an array, while creating a versioned release."""

    def __init__(self, pointer, schema):
        self.pointer = pointer
        self.schema = schema

    def __str__(self):
        return f"{self.pointer}/items is not set or is an array"
