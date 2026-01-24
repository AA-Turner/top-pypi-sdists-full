class Timeout:

    FUNC_TIMEOUT_IN_SECONDS = 200


class SizeLimit:

    RESPONSE_SIZE_LIMIT_IN_MB = 30


class SpecConstants:
    LOCAL_HOST_URL = "http://localhost:7071/api/"
    PUBLIC_URL_DESC = "The public URL to invoke the User Data Function."
    SPEC_FUNCTION_NAME_JSON = "get_udf_oai_spec_json"
    SPEC_FUNCTION_NAME_YAML = "get_udf_oai_spec_yaml"


class UDFExceptionCodes:
    INVALID_INPUT = "InvalidInput"
    MISSING_INPUT = "MissingInput"
    RESPONSE_TOO_LARGE = "ResponseTooLarge"
    TIMEOUT = "Timeout"
    USER_THROWN = "UserThrown"
    INTERNAL_ERROR = "InternalError"
