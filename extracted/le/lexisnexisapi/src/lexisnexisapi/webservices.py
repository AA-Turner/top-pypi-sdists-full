import base64
import json
import os
from os.path import exists

from datetime import datetime
from time import sleep

import requests
import xmltodict
from lexisnexisapi import credentials as cred

__version__ = "3.0.3.3"
__author__ = "Robert Cuffney & Ozgur Aycan, " "CS Integration Consultants @ LexisNexis"


def APIEndpoints(endpointName):
    endpoint = f"https://services-api.lexisnexis.com/v1/{endpointName}?"
    return endpoint


def error_handler(func):
    """
    generic error handling
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred in function: '{func.__name__}'")
            print(f"error: {e}")
            print(f"args:{args}")
            print(f"kwargs:{kwargs}")
            raise  # Re-raise the exception to propagate it further

    return wrapper


def token():
    """Gets Authorization token to use in other requests."""
    client_id = cred.get_Key("WSAPI_CLIENT_ID")
    secret = cred.get_Key("WSAPI_SECRET")
    auth_url = "https://auth-api.lexisnexis.com/oauth/v2/token"
    payload = {
        "grant_type": "client_credentials",
        "scope": "http://oauth.lexisnexis.com/all",
    }
    auth = requests.auth.HTTPBasicAuth(client_id, secret)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(auth_url, auth=auth, headers=headers, data=payload)
    response.raise_for_status()  # Raise exception for bad status codes
    json_data = response.json()
    return json_data["access_token"]


@error_handler
def call_api(access_token, endpoint, **kwargs):
    """Call the API with the provided token and endpoint"""
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    url = APIEndpoints(endpoint)
    with requests.Session() as session:
        response = session.get(headers=headers, url=url, **kwargs)
        response.raise_for_status()  # Raise exception for bad status codes
        api_data = response.json()
        return api_data


def loop(access_token, endpoint, sleepTime=5, **kwargs):
    parameters = kwargs["params"]
    i = 0
    skip = 0
    remaining_count = 1
    while skip < remaining_count:
        data = call_api(access_token, endpoint=endpoint, params=parameters)
        # define some parameters from the first call only:
        if i == 0:
            num_docs = parameters.pop("$top")
            skip = parameters.get("$skip", num_docs)
            remaining_count = data["@odata.count"]
            dir = datetime.now().strftime("%Y-%m-%d-%H%M")
            if not exists(dir):
                os.makedirs(dir)
        else:
            skip = skip + num_docs  # define skip for the call after that.
        parameters["$skip"] = (
            skip  # set the number of documents to skip to for the next call
        )
        file_path = os.path.join(dir, f"export_{i}.json")
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)  # save the api response to json file:
        i += 1
        sleep(sleepTime)
    print(f"Complete, JSON exports are saved in the following directory: {dir}")


def get_base64(message):
    base64_message = base64.urlsafe_b64encode(message.encode("ascii")).decode("ascii")
    # Remove padding "=" characters
    base64_message_without_padding = base64_message.rstrip("=")
    return base64_message_without_padding


def convert_xml_content(data):
    """
    conversts the content section of the document to a
    python dictionary
    """
    for c in data["value"]:
        myDoc = c["Document"]["Content"]
        ordDict = xmltodict.parse(
            myDoc
        )  # parse out the xml, and convert to ordered dictionary
        newDict = json.loads(
            json.dumps(ordDict)
        )  # convert to regular dictionary ('unnecessary')
        c["Document"]["Content"] = newDict
    return data
