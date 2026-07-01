"""Base creator for secrets"""
import logging
import uuid
from typing import Optional

from mcli.api.exceptions import ValidationError
from mcli.models import Secret, SecretType
from mcli.objects.secrets import SECRET_CLASS_MAP
from mcli.utils.utils_interactive import simple_prompt
from mcli.utils.utils_logging import FAIL
from mcli.utils.utils_string_functions import validate_secret_name

logger = logging.getLogger(__name__)


class SecretValidationError(ValidationError):
    """Secret could not be configured with the provided values
    """


def validate_secret_name_rfc(name: str) -> bool:

    result = validate_secret_name(name)
    if not result:
        raise SecretValidationError(result.message)
    return True


class SecretCreator:
    """Creates base secrets for the CLI
    """

    @staticmethod
    def create_base_secret(name: str, secret_type: SecretType) -> Secret:
        secret_class = SECRET_CLASS_MAP.get(secret_type)
        if not secret_class:
            raise SecretValidationError(f'{FAIL} The secret type: {secret_type} does not exist.')

        return secret_class(name, secret_type)

    def create(
        self,
        secret_type: SecretType,
        name: Optional[str] = None,
        make_name_unique: bool = False,
        **kwargs,
    ) -> Secret:

        del kwargs

        if name:
            if make_name_unique:
                name = f'{name[:58]}-{str(uuid.uuid4())[:4]}'
            validate_secret_name(name)

        name = name or simple_prompt('What would you like to name this secret?', validate=validate_secret_name_rfc)
        return self.create_base_secret(name, secret_type)
