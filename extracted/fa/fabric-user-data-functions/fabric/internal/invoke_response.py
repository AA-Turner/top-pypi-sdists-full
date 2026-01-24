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


class UserDataFunctionInvokeResponse:
    def __init__(self):
        self.functionName: str = ""
        self.invocationId: str = ""
        self.status: StatusCode = StatusCode.SUCCEEDED
        self.output: object = ""
        self.errors: list[FormattedError] = []

    def add_error(self, error):
        self.errors.append(error)

    def to_json(self):
        def convert(o):
            if isinstance(o, StatusCode):
                return o.value
            elif isinstance(o, FormattedError):
                return o.to_json()
            return o.__dict__

        return json.dumps(
            self,
            default=convert)
