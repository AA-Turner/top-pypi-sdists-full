"""Test related utilities"""


def http_error_message(url: str, status_code: int) -> str:
    """Generate default HTTP error messages from URI and status code"""
    client_error = ""
    match status_code:
        case 400:
            client_error = "Bad Request"
        case 401:
            client_error = "Unauthorized"
        case 404:
            client_error = "Not Found"
        case 429:
            client_error = "Too Many Requests"
        case _:
            pass

    return f"Client error '{status_code} {client_error}' for url '{url}'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{status_code}"
