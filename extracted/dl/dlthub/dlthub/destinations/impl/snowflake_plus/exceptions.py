from dlt.common.destination.exceptions import DestinationTerminalException


# TODO: This is a similar exception to dlt.destinations.exceptions.InvalidFilesystemLayout
# Keep MissingPlaceholderException in dlthub until we have a generalized InvalidFilesystemLayout
class MissingPlaceholderException(DestinationTerminalException):
    """Raised when a placeholder in the template is missing from extra_placeholders."""

    def __init__(self, missing_placeholder: str, template: str):
        self.missing_placeholder = missing_placeholder
        self.template = template
        message = (
            f"Placeholder '{{{missing_placeholder}}}' in base_location template '{template}' "
            f"is not provided in extra_placeholders. Please add this placeholder to your "
            f"configuration."
        )
        super().__init__(message)
