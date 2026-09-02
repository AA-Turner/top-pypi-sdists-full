from base64 import b64encode


def get_key(client_id: str, client_secret: str) -> str:
    """Reads Client ID and API Key from and returns a basic auth string for the DealCloud API

    Returns:
    auth_string (str): The b64 encoded basic auth string
    """

    decoded_auth_string = f"{client_id}:{client_secret}"

    auth_string = b64encode(str.encode(decoded_auth_string)).decode("utf-8")

    return auth_string
