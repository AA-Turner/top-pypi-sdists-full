# Copyright 2023 Agnostiq Inc.

import base64
from typing import Optional

from covalent_cloud import get_client
from covalent_cloud.shared.classes.settings import Settings, settings


def store_secret(name: str, value: str, settings: Optional[Settings] = settings):
    """
    Stores a new secret in the Covalent Cloud. This function is used to securely save sensitive information like API keys, passwords, or other confidential data. Each secret is identified by a unique name.

    .. note:: There is a limit of 100 secrets per user account.

    Args:
        name (str): The name of the secret to be stored.
        value (str): The value of the secret.
        settings (Settings, optional): Configuration settings for connecting to the Covalent Cloud. Defaults to None, which uses the default settings.

    Returns:
        None: This function does not return any value but raises an error if the operation is unsuccessful.

    Examples:
        .. highlight:: python
        .. code-block:: python

            import covalent_cloud as cc

            # Store a new secret
            cc.store_secret(name="MY_SECRET_NAME", value="MY_SECRET_VALUE")
            # A secret with the name "MY_SECRET_NAME" and value "MY_SECRET_VALUE" is stored.
    """
    client = get_client(settings)
    body = {
        "name": name,
        "value": base64.b64encode(value.encode("utf-8")).decode("utf-8"),
    }
    r = client.post("/api/v2/secrets", request_options={"json": body})
    r.raise_for_status()


def list_secrets(settings: Optional[Settings] = settings):
    """
    Retrieves a list of all stored secrets in the Covalent Cloud. This function is useful for managing and verifying the secrets stored within the user's environment.

    Args:
        settings (Settings, optional): Configuration settings for connecting to the Covalent Cloud. Defaults to None, which uses the default settings.

    Returns:
        List[str]: A list containing the names of all stored secrets.

    Examples:
        .. highlight:: python
        .. code-block:: python

            import covalent_cloud as cc

            # Retrieve a list of all stored secrets
            secret_names = cc.list_secrets()
            # Returns a list of names of all secrets stored in the user's environment.
    """
    client = get_client(settings)
    r = client.get("/api/v2/secrets")
    r.raise_for_status()
    return r.json()["names"]


def delete_secret(name: str, settings: Optional[Settings] = settings):
    """
    Deletes a specific secret from the Covalent Cloud. Use this function to remove secrets that are no longer needed or should be updated.

    Args:
        name (str): The name of the secret to be deleted.
        settings (Settings, optional): Configuration settings for connecting to the Covalent Cloud. Defaults to None, which uses the default settings.

    Returns:
        None: This function does not return any value but raises an error if the operation is unsuccessful.

    Examples:
        .. highlight:: python
        .. code-block:: python

            import covalent_cloud as cc

            # Optionally, delete a secret if no longer needed
            cc.delete_secret(name="MY_SECRET_NAME")
            # Deletes the secret named "MY_SECRET_NAME".
    """
    client = get_client(settings)

    r = client.delete(f"/api/v2/secrets/{name}")
    r.raise_for_status()
