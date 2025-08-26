from functools import wraps

from qwak.exceptions import QwakException
from qwak.feature_store.validations.validation_response import SuccessValidationResponse


def silence_backend_specific_validation_exceptions(*error_messages_to_silence):
    """
    A decorator that catches specific backend validation exceptions and returns a standardized
    validation success response encapsulating the exception details. Used to skip the validation
    process for certain backend exceptions. hopefully will be removed soon after validations will be supported on
    all environment types.

    Parameters:
        *error_messages_to_silence: Variable length argument list
            Messages that, if present in the exception message, should trigger the
            standardized validation success response instead of propagating the exception.

    Returns:
        function
            The wrapped function that will catch specified backend validation exceptions
            and return a standardized validation success response if any of the specified
            error messages are found in the exception message.

    Usage:
    ------
    @silence_backend_specific_validation_exceptions(
        "Validating DataSource is not supported for self-hosted environments",
        "Validating DataSource is not supported for SAAS environments"
    )
    def validate_data_source():
        # Your function implementation

    When 'validate_data_source_blocking' raises a QwakException containing one of the specified error messages,
    it will return a SuccessValidationResponse, including the
    exception's representation in stderr and in the sample as a dataframe with a warning column.
    If the exception message does not contain any of the specified error messages, the exception is raised normally.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, silence_specific_exceptions: bool = True, **kwargs):
            try:
                return func(*args, **kwargs)
            except QwakException as e:
                is_to_silent_error = silence_specific_exceptions and any(
                    error_message in repr(e)
                    for error_message in error_messages_to_silence
                )
                if not is_to_silent_error:
                    raise e

                try:
                    import pandas as pd
                except ImportError as exc:
                    raise QwakException("Missing required Pandas dependency") from exc

                return (
                    SuccessValidationResponse(
                        sample=pd.DataFrame({"errors": [repr(e)]}),
                        features=[],
                        stdout="",
                        stderr=repr(e),
                    ),
                    None,
                )

        return wrapper

    return decorator
