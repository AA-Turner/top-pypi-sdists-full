import json
import os

from google.oauth2 import service_account

from tinybird_cdk import config


def credentials():
    '''
    Encapsulates support for Google Cloud credentials.

    At least one of the two supported environment variables must be set:

        GOOGLE_APPLICATION_CREDENTIALS
        Path to a JSON file with the credentials.

        GOOGLE_APPLICATION_CREDENTIALS_JSON
        A JSON string with the credentials themselves.

    If both are set, GOOGLE_APPLICATION_CREDENTIALS_JSON takes precedence.
    '''
    if json_credentials := os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON'):
        return service_account.Credentials.from_service_account_info(json.loads(json_credentials))
    if filename := os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        return service_account.Credentials.from_service_account_file(filename)
    raise Exception('''
        Connecting to Google Cloud requires GOOGLE_APPLICATION_CREDENTIALS or
        GOOGLE_APPLICATION_CREDENTIALS_JSON to be set in the environment''')

def project_id():
    '''
    Returns the value of the GCP_PROJECT environment variable if set. Otherwise,
    the one in the credentials.
    '''
    if project := os.getenv("GCP_PROJECT"):
        return project
    return credentials().project_id

def gcs_bucket():
    return config.get('GCS_BUCKET')

def gcs_folder():
    folder = config.get('GCS_FOLDER', optional=True)
    if folder:
        folder = folder.strip("/")
    return folder
