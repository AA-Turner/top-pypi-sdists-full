from enum import Enum


class ListHttpTriggersResponse200ItemAuthenticationMethod(str, Enum):
    API_KEY = "api_key"
    BASIC_HTTP = "basic_http"
    CUSTOM_SCRIPT = "custom_script"
    NONE = "none"
    SIGNATURE = "signature"
    WINDMILL = "windmill"

    def __str__(self) -> str:
        return str(self.value)
