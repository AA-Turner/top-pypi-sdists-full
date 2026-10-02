class Timeout:

    FUNC_TIMEOUT_IN_SECONDS = 200


class SizeLimit:

    RESPONSE_SIZE_LIMIT_IN_MB = 30


class SpecConstants:
    LOCAL_HOST_URL = "http://localhost:7071/api/"
    PUBLIC_URL_DESC = "The public URL to invoke the User Data Function."
    SPEC_FUNCTION_NAME_JSON = "get_udf_oai_spec_json"
    SPEC_FUNCTION_NAME_YAML = "get_udf_oai_spec_yaml"


class HeaderConstants:
    IS_BATCH = "x-ms-fabric-isbatch"


class BatchConstants:
    """Constants for batch execution validation."""
    MIN_BATCH_SIZE = 1
    MAX_BATCH_SIZE = 900
    DEFAULT_BATCH_SIZE = MAX_BATCH_SIZE


class BatchInternalKeys:
    """Internal kwargs keys for batch execution state."""
    IS_BATCH = '__is_batch__'
    BATCH_SIZE = '__batch_size__'
    BATCH_ITEMS = '__batch_items__'
    BATCH_VALIDATION_ERROR = '__batch_validation_error__'


class UDFExceptionCodes:
    INVALID_INPUT = "InvalidInput"
    MISSING_INPUT = "MissingInput"
    RESPONSE_TOO_LARGE = "ResponseTooLarge"
    TIMEOUT = "Timeout"
    USER_THROWN = "UserThrown"
    INTERNAL_ERROR = "InternalError"


class BatchErrorMessages:
    """Error messages for batch execution validation."""
    BATCH_TOO_SMALL = "Batch must contain at least {min_required} item(s)"
    BATCH_TOO_LARGE = "Batch size {batch_size} exceeds maximum allowed size of {max_allowed}"
    BATCH_ARRAY_EXPECTED = "This function is configured for batch execution and expects an array of items as input. The provided data is not an array."
