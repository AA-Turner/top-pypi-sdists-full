from cnvrgv2.config import error_messages
from cnvrgv2.context import Context
from cnvrgv2.errors import CnvrgLoginError
from cnvrgv2.config import Config


def verify_login():
    # TODO: Prettify function, there is duplication between line 11 and line 13
    try:
        # Attempt to log in using credentials (from config files)
        credentials_variables = Config().get_credential_variables()
        # If cannot log in using config credentials, try using env variables
        auth_variables = credentials_variables if all(credentials_variables) else (Context().get_env_variables())
        if not all(auth_variables):
            raise CnvrgLoginError(error_messages.CREDENTIALS_MISSING)
    except CnvrgLoginError:
        raise CnvrgLoginError(error_messages.CREDENTIALS_MISSING)
