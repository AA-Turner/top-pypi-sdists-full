import json

# flake8: noqa: R505
class StatusCode:
    BAD_REQUEST = "BadRequest"
    TIMEOUT = "Timeout"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    RESPONSE_TOO_LARGE = "ResponseTooLarge"


class FormattedError:
    def __init__(self, error_code: str, message: str, properties: dict = None):
        self.errorCode: str = error_code
        self.message: str = message
        if properties is None:
            self.properties = {}
        else:
            self.properties = properties

    def add_or_update_property(self, key, value):
        self.properties[key] = value

    def to_json(self):
        return self.__dict__

class BatchItemResult:
    """Represents the result of a single item in a batch execution."""
    def __init__(self, output=None, errors=None):
        self.output = output
        self.errors = errors if errors is not None else []
    
    def to_dict(self):
        """Convert to dict, only including fields that have populated values."""
        result = {}
        
        if self.errors:
            # Has errors - only include errors field
            result['errors'] = [e.to_json() if isinstance(e, FormattedError) else e for e in self.errors]
        else:
            # No errors - include output field (even if None)
            result['output'] = self.output
        
        return result


class UserDataFunctionInvokeResponse:
    def __init__(self):
        self.functionName: str = ""
        self.invocationId: str = ""
        self.status: StatusCode = StatusCode.SUCCEEDED
        self.output: object = ""
        self.batchOutput: list = None
        self.errors: list[FormattedError] = []

    def add_error(self, error):
        self.errors.append(error)

    def to_json(self):
        def convert(o):
            if isinstance(o, StatusCode):
                return o.value
            elif isinstance(o, FormattedError):
                return o.to_json()
            # Coerce values from common data libraries that are not natively
            # JSON serializable and do not expose a usable __dict__ (e.g. numpy
            # scalars, pyarrow scalars). Falling back to o.__dict__ on these
            # raised AttributeError and failed the whole response.
            item = getattr(o, "item", None)
            if callable(item):
                try:
                    return item()  # numpy scalar -> native python scalar
                except Exception:
                    pass
            as_py = getattr(o, "as_py", None)
            if callable(as_py):
                try:
                    return as_py()  # pyarrow scalar -> native python value
                except Exception:
                    pass
            # Branch on __dict__ first so we don't eagerly evaluate str(o)
            # (which could raise from a custom __str__) when __dict__ exists.
            d = getattr(o, "__dict__", None)
            if d is not None:
                return d
            return str(o)

        response_dict = self.__dict__.copy()
        
        if self.batchOutput is not None:
            # Batch mode: exclude output field
            response_dict.pop('output', None)
        else:
            # Scalar mode: exclude batchOutput field
            response_dict.pop('batchOutput', None)
        
        return json.dumps(response_dict, default=convert)
