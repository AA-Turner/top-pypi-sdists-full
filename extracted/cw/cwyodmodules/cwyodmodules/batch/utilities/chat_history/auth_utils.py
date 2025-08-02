import base64
import json

from ...utilities.helpers.env_helper import EnvHelper
from mgmt_config import logger

# Use default logging configuration for decorators
DEFAULT_LOG_EXECUTION = True
DEFAULT_LOG_ARGS = True
DEFAULT_LOG_RESULT = True

@logger.trace_function(log_execution=DEFAULT_LOG_EXECUTION, log_args=DEFAULT_LOG_ARGS, log_result=DEFAULT_LOG_RESULT)
def get_authenticated_user_details(request_headers):
    user_object = {}

    # check the headers for the Principal-Id (the guid of the signed in user)
    if "X-Ms-Client-Principal-Id" not in request_headers.keys():
        # if it's not, assume we're in development mode and return a default user
        try:
            from . import sample_user
            raw_user_object = sample_user.sample_user
        except (ImportError, AttributeError):
            # Fallback for test environments where relative imports fail
            raw_user_object = {
                "X-Ms-Client-Principal-Id": "00000000-0000-0000-0000-000000000000",
                "X-Ms-Client-Principal-Name": "testusername@constoso.com",
                "X-Ms-Client-Principal-Idp": "aad",
                "X-Ms-Token-Aad-Id-Token": "test_token",
                "X-Ms-Client-Principal": "test_principal"
            }
    else:
        # if it is, get the user details from the EasyAuth headers
        raw_user_object = {k: v for k, v in request_headers.items()}

    user_object["user_principal_id"] = raw_user_object.get("X-Ms-Client-Principal-Id")
    user_object["user_name"] = raw_user_object.get("X-Ms-Client-Principal-Name")
    user_object["auth_provider"] = raw_user_object.get("X-Ms-Client-Principal-Idp")
    user_object["auth_token"] = raw_user_object.get("X-Ms-Token-Aad-Id-Token")
    user_object["client_principal_b64"] = raw_user_object.get("X-Ms-Client-Principal")
    user_object["aad_id_token"] = raw_user_object.get("X-Ms-Token-Aad-Id-Token")

    return user_object
