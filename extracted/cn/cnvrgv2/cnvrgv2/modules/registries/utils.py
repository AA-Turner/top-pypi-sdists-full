import re

from cnvrgv2.config import error_messages
from cnvrgv2.errors import CnvrgArgumentsError

URL_VALIDATION_REGEX = re.compile(r"\A[\w.-]+(?:\.[\w\.-]+)+[\w\-\._%~:\/?#\[\]@!\$&'\(\)\*\+,;=.]+\Z")


class RegistryTypes:
    CNVRG = "cnvrg"
    INTEL = "intel"
    HABANA = "habana"
    DOCKERHUB = "dockerhub"
    NVIDIA = "nvidia"
    GCR = "gcr"
    ECR = "ecr"
    ACR = "acr"
    OTHER = "other"

    @classmethod
    def validate_type(cls, registry_type):
        if registry_type is None:
            return True

        registry_types = [cls.__dict__[var] for var in vars(cls) if not var.startswith("__")]
        return registry_type in registry_types


def validate_registry_params(title=None, url=None, username=None, password=None):
    if title is not None and not isinstance(title, str):
        raise CnvrgArgumentsError(error_messages.REGISTRY_BAD_TITLE)

    if url is not None and not isinstance(url, str):
        raise CnvrgArgumentsError(error_messages.REGISTRY_BAD_URL)

    if isinstance(url, str) and not re.match(URL_VALIDATION_REGEX, url):
        raise CnvrgArgumentsError(error_messages.REGISTRY_BAD_URL_FORMAT)

    if username is not None and not isinstance(username, str):
        raise CnvrgArgumentsError(error_messages.REGISTRY_BAD_USERNAME)

    if password is not None and not isinstance(password, str):
        raise CnvrgArgumentsError(error_messages.REGISTRY_BAD_PASSWORD)
