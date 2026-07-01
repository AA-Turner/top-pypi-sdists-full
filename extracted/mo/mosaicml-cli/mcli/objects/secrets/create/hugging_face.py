"""Creators for hugging face secrets"""
from typing import Optional

from mcli.models import SecretType
from mcli.objects.secrets.create.base import SecretCreator
from mcli.objects.secrets.create.generic import FileSecretFiller
from mcli.objects.secrets.env_var import HuggingFaceSecret
from mcli.utils.utils_interactive import secret_prompt


class HuggingFaceSecretFiller(FileSecretFiller):
    """Interactive filler for hugging face secret data
    """

    @staticmethod
    def fill_token() -> str:
        return secret_prompt("What is your Hugging Face token?", validate=HuggingFaceSecretFiller.validate_token)

    @staticmethod
    def validate_token(token: str) -> bool:
        return token.startswith("hf_")


class HuggingFaceSecretCreator(HuggingFaceSecretFiller):
    """Creates HuggingFace secrets for the CLI
    """

    def create(self, name: Optional[str] = None, token: Optional[str] = None) -> HuggingFaceSecret:
        base_creator = SecretCreator()
        secret = base_creator.create(SecretType.hugging_face,
                                     name=name or 'hugging-face',
                                     make_name_unique=name is not None)
        assert isinstance(secret, HuggingFaceSecret)

        if not token or not HuggingFaceSecretFiller.validate_token(token):
            token = HuggingFaceSecretFiller.fill_token()

        secret.token = token
        return secret
