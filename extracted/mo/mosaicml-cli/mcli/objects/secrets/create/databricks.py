"""Creators for databricks secrets"""
from typing import Optional

from mcli.models import SecretType
from mcli.objects.secrets import MCLIDatabricksSecret
from mcli.objects.secrets.create.base import SecretCreator
from mcli.utils.utils_interactive import secret_prompt, simple_prompt


class DatabricksSecretFiller():
    """Interactive filler for databricks secret data
    """

    @classmethod
    def fill_host(cls) -> str:
        return simple_prompt('What is your Databricks workspace URL / host?')

    @classmethod
    def fill_token(cls) -> str:
        return secret_prompt('What is your Databricks Personal Access Token?')


class DatabricksSecretCreator(DatabricksSecretFiller):
    """Creates databricks secrets for the CLI
    """

    def create(self,
               name: Optional[str] = None,
               host: Optional[str] = None,
               token: Optional[str] = None,
               **kwargs) -> MCLIDatabricksSecret:
        del kwargs

        # Get base secret
        base_creator = SecretCreator()
        secret = base_creator.create(SecretType.databricks, name)
        assert isinstance(secret, MCLIDatabricksSecret)

        secret.host = host or self.fill_host()
        secret.token = token or self.fill_token()

        return secret
