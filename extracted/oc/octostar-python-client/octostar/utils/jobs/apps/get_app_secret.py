import os
from warnings import warn
from dotenv import get_key, find_dotenv, load_dotenv
from ....client import Client


def sync(key: str, client: Client = None) -> str:
    """
    # Reads an application secret value

    Retrieves the value of an application secret based on the provided key.

    ## Arguments

    - `key`: The key for the application secret.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns

    The corresponding secret value.

    ## Raises

    - `ValueError`: If the key is not valid.
    - `RuntimeError`: If the secrets file could not be read.

    ## Example

    ```python
    secret_value = sync("my_secret_key")
    print(secret_value)
    ```
    """
    if not key or not isinstance(key, str):
        raise ValueError("key must be a non-empty string")
    if not key.strip():
        raise ValueError("key must be non-empty")

    sanitized_key = (
        key.replace("/", "_").replace(".", "_").replace("-", "_").replace(" ", "_")
    )

    if f"{os.getenv('OS_DEV_MODE')}".lower() == "true":
        if not os.getenv(sanitized_key):
            dotenv_value = get_key(find_dotenv(usecwd=True), sanitized_key)
            if dotenv_value is not None:
                os.environ[sanitized_key] = dotenv_value
                warn(
                    "Loading secret from .env file. This is fine for development but not for production!",
                    stacklevel=2,
                )
        if os.getenv(sanitized_key) is not None:
            warn(
                f"App secret {sanitized_key} has been loaded in plaintext from environment variables. This is fine for development but it should not happen in production!",
                Warning,
                stacklevel=2,
            )
            return os.environ[sanitized_key]

    path = "/etc/secrets/" + sanitized_key

    if not os.path.isfile(path):
        raise RuntimeError(f"Secret file not found at {path}")

    try:
        with open(path, "r") as file:
            line = file.readline()
            if not line:
                raise ValueError(f"Secret file {path} is empty")
            return line.strip()
    except Exception as e:
        raise RuntimeError(f"Error reading secret file {path}: {e}")


async def asyncio(key: str, client: Client = None) -> str:
    """
    # Reads an application secret value asynchronously

    Retrieves the value of an application secret based on the provided key asynchronously.

    ## Arguments

    - `key`: The key for the application secret.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns

    The corresponding secret value.

    ## Raises

    - `ValueError`: If the key is not valid.
    - `RuntimeError`: If the secrets file could not be read.

    ## Example

    ```python
    secret_value = await asyncio("my_secret_key")
    print(secret_value)
    ```
    """
    return sync(key, client)
