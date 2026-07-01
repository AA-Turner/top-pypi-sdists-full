import json
import os

__version__ = "3.0.3.3"
__author__ = (
    "Robert Cuffney & Ozgur Aycan, "
    "CS Integration Consultants @ LexisNexis"
)

def set_Key(**kwargs):
    """
    Send kwargs to be stored as JSON object
    """
    try:
        cred = get_Credentials()
        cred.update(kwargs)
        f = cred_file_path()
        with open(f, "w") as outfile:
            json.dump(cred, outfile, indent=4)
    except Exception as e:
        print(f"Error occurred: {e}")


def get_Key(key):
    """
    Send parameter 'key' to return value lf 'key':'value' 
    from myCredentials JSON object.
    """
    try:

        def input_Key():
            var = input(f"Please enter your {key}")
            return var

        cred = get_Credentials()
        if key in get_Credentials():
            key_value = cred[key]
        else:
            key_value = input_Key()
            dict = {key: key_value}
            set_Key(**dict)
        return key_value
    except Exception as e:
        print(f"Error occurred: {e}")


def get_Credentials():
    """
    get all credentials from myCredentials JSON object.
    """
    try:
        check_file_exists()
        f = cred_file_path()
        with open(f, "r") as outfile:
            dict = json.load(outfile)
        return dict
    except Exception as e:
        print(f"Error occurred: {e}")


def check_file_exists():
    """
    ensures the JSON object exists, if not it creates a blank JSON object
    """
    try:
        from os.path import exists

        f = cred_file_path()
        file_exists = exists(f)
        if not file_exists:
            with open(f, "w") as outfile:
                json.dump({}, outfile)
    except Exception as e:
        print(f"Error occurred: {e}")


def cred_file_path():
    try:
        # Get the user's home directory
        home_dir = os.path.expanduser("~")

        # Create a unique directory path
        unique_dir = os.path.join(home_dir, ".lnapi")

        # Create the unique directory if it doesn't exist
        if not os.path.exists(unique_dir):
            os.makedirs(unique_dir)

        # Define the path to the .cred file inside the unique directory
        cred_file_path = os.path.join(unique_dir, ".cred")

        # return .cred file path
        return cred_file_path
    except Exception as e:
        print(f"Error occurred: {e}")
