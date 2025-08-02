from dataclasses import dataclass, field, fields
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.mail.entities.mailers import Mailers
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Mail(BaseEntity):
    """
    Represents the mail configuration entity.
    Attributes:
        default (str): The default mailer transport to use.
        mailers (Mailers): The available mail transport configurations.
    Methods:
        __post_init__():
            Validates the integrity of the Mail instance after initialization.
            Raises OrionisIntegrityException if any attribute is invalid.
        toDict() -> dict:
            Serializes the Mail instance to a dictionary.
    """

    default: str = field(
        default = "smtp",
        metadata = {
            "description": "The default mailer transport to use.",
            "default": "smtp",
        }
    )

    mailers: Mailers | dict = field(
        default_factory = lambda: Mailers(),
        metadata = {
            "description": "The available mail transport configurations.",
            "default": lambda: Mailers().toDict()
        }
    )

    def __post_init__(self):
        """
        Post-initialization method to validate the 'default' and 'mailers' attributes.
        Ensures that:
        - The 'default' attribute is a string and matches one of the available mailer options.
        - The 'mailers' attribute is an instance of the Mailers class.
        Raises:
            OrionisIntegrityException: If 'default' is not a valid string option or if 'mailers' is not a Mailers object.
        """

        # Validate 'default' attribute
        options = [f.name for f in fields(Mailers)]
        if not isinstance(self.default, str) or self.default not in options:
            raise OrionisIntegrityException(
                f"The 'default' property must be a string and match one of the available options ({options})."
            )

        # Validate 'mailers' attribute
        if not isinstance(self.mailers, (Mailers, dict)):
            raise OrionisIntegrityException(
                "The 'mailers' property must be an instance of Mailers or a dictionary."
            )
        if isinstance(self.mailers, dict):
            self.mailers = Mailers(**self.mailers)