"""Creators for docker secrets"""
from enum import Enum
from typing import Optional

from mcli.models import SecretType
from mcli.objects.secrets import MCLIDockerRegistrySecret
from mcli.objects.secrets.create.base import SecretCreator
from mcli.utils.utils_interactive import choose_one, secret_prompt, simple_prompt


class ContainerRegistries(Enum):
    DOCKERHUB = ("DockerHub", "https://index.docker.io/v1/")
    GHCR = ("Github (GHCR)", "https://ghcr.io")
    OTHER = ("Other", "")

    def __init__(self, display: str, url: str):
        self.display = display
        self.url = url


class DockerSecretFiller():
    """Interactive filler for docker secret data
    """

    @classmethod
    def fill_username(cls) -> str:
        return simple_prompt('What is your username?')

    @classmethod
    def fill_password(cls) -> str:
        return secret_prompt('What is your password/API token?')

    @classmethod
    def fill_server(cls) -> str:
        chosen = choose_one(message="Which container registry would you like to use?",
                            options=list(ContainerRegistries),
                            formatter=lambda o: o.display,
                            default=ContainerRegistries.DOCKERHUB)
        server = chosen.url
        if chosen is ContainerRegistries.OTHER:
            server = simple_prompt('What is the URL for this registry?')
        return server


class DockerSecretCreator(DockerSecretFiller):
    """Creates docker secrets for the CLI
    """

    def create(self,
               name: Optional[str] = None,
               username: Optional[str] = None,
               password: Optional[str] = None,
               email: Optional[str] = None,
               server: Optional[str] = None,
               **kwargs) -> MCLIDockerRegistrySecret:
        del kwargs

        # Get base secret
        base_creator = SecretCreator()
        secret = base_creator.create(SecretType.docker_registry, name)
        assert isinstance(secret, MCLIDockerRegistrySecret)

        secret.server = server or self.fill_server()
        secret.username = username or self.fill_username()
        secret.password = password or self.fill_password()
        secret.email = email

        return secret
