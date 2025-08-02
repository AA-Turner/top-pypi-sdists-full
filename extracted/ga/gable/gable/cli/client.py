from typing import Union

import click
from gable import GableClient
from gable.api.client import GableAPIClient


class GableCliClient:
    """
    CLI wrapper for GableClient

    This is meant to be a thin wrapper around GableClient that we use for the CLI. It
    catches exceptions and raises ClickExceptions with the error message and allows us
    to handle errors in a way that is specific to the CLI.
    """

    def __init__(
        self, endpoint: Union[str, None] = None, api_key: Union[str, None] = None
    ) -> None:
        # TODO: eventually, we want to entirely migrate to the "external" client
        self.internal_client = GableAPIClient(endpoint=endpoint, api_key=api_key)
        self.external_client = GableClient(api_endpoint=endpoint, api_key=api_key)

    @property
    def api_key(self):
        return self.external_client.api_key

    @property
    def endpoint(self):
        return self.external_client.api_endpoint

    @api_key.setter
    def api_key(self, value):
        self.internal_client.api_key = value
        try:
            self.internal_client.validate_api_key()
        except ValueError as e:
            raise click.ClickException(str(e))

    @endpoint.setter
    def endpoint(self, value):
        self.internal_client.endpoint = value
        try:
            self.internal_client.validate_endpoint()
        except ValueError as e:
            raise click.ClickException(str(e))

    @property
    def ui_endpoint(self):
        return self.internal_client.ui_endpoint

    def __getattr__(self, name: str):
        try:
            attr = getattr(self.external_client, name)
        except AttributeError:
            attr = getattr(self.internal_client, name)

        if callable(attr):

            def wrapper(*args, **kwargs):
                try:
                    return attr(*args, **kwargs)
                except Exception as e:
                    raise click.ClickException(str(e))

            return wrapper
        else:
            return attr  # If it's not callable, return the attribute directly
