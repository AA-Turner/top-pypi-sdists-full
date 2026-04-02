import httpx

from higgsfield_client.exceptions import HiggsfieldClientError


def extract_error_message(response: httpx.Response) -> str:
    try:
        data = response.json()
        return (
            data.get('detail') or
            data.get('details') or
            data.get('message') or
            data.get('error') or
            response.text
        )
    except (ValueError, TypeError, AttributeError):
        return response.text


def raise_for_status(response: httpx.Response) -> None:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exception:
        message = extract_error_message(response)
        raise HiggsfieldClientError(message) from exception
