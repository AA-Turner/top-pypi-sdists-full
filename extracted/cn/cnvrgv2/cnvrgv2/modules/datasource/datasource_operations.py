import shutil
import time
from datetime import datetime
from cnvrgv2.config import error_messages
from dateutil.tz import tzlocal
from cnvrgv2.errors import CnvrgAlreadyClonedError


def handle_dir_exist(force: bool, path: str) -> None:
    """
    Handle the case where a directory already exists.

    @param force: If True, forcefully delete the directory.
    @type force: bool
    @param path: The path to the directory.
    @type path: str
    @raise CnvrgAlreadyClonedError: If the directory already exists and force is False.
    """
    if force:
        shutil.rmtree(path)
    else:
        raise CnvrgAlreadyClonedError(error_messages.DATASOURCE_ALREADY_CLONED)


def format_credentials(creds: dict) -> dict:
    """
    Format the credentials for use with boto3.

    @param creds: The raw credentials.
    @type creds: dict
    @return: The formatted credentials.
    @rtype: dict
    """
    expiration = creds.get('expiration', 129600)
    return {
        "access_key": creds['access_key_id'],
        "secret_key": creds['secret_access_key'],
        "token": creds.get('session_token'),
        "expiry_time": datetime.fromtimestamp(time.time() + expiration, tz=tzlocal()).isoformat(),
    }


def get_refreshable_credentials_function(datasource):
    """
    Get a function to refresh credentials for the given data source.

    @param datasource: The data source instance.
    @type datasource: Datasource
    @return: A function to refresh credentials.
    @rtype: function
    """

    def refresh():
        creds = datasource._get_credentials()
        return format_credentials(creds)

    return refresh
