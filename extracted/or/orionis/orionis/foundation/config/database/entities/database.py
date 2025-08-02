from dataclasses import dataclass, field, fields
from orionis.foundation.config.database.entities.connections import Connections
from orionis.services.environment.env import Env
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Database(BaseEntity):
    """
    Data class to represent the general database configuration.

    Attributes
    ----------
    default : str
        The name of the default database connection to use.
    connections : Connections
        The different database connections available to the application.
    """
    default: str = field(
        default_factory = lambda: Env.get("DB_CONNECTION", "sqlite"),
        metadata={
            "description": "Default database connection name",
            "default": "sqlite"
        }
    )

    connections: Connections | dict = field(
        default_factory = lambda: Connections(),
        metadata={
            "description": "Database connections",
            "default": lambda: Connections().toDict()
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization method for validating and normalizing the 'default' and 'connections' attributes.
        Validates that the 'default' attribute is either a valid string corresponding to a member of DatabaseConnections
        or an instance of DatabaseConnections. If 'default' is a valid string, it is converted to its corresponding value.
        If 'default' is not valid, raises an OrionisIntegrityException.
        Also ensures that the 'connections' attribute is an instance of Connections and is not empty.
        Raises an OrionisIntegrityException if the validation fails.
        """

        # Validate default attribute
        options = [field.name for field in fields(Connections)]
        if isinstance(self.default, str):
            if self.default not in options:
                raise OrionisIntegrityException(f"The 'default' attribute must be one of {str(options)}.")
        else:
            raise OrionisIntegrityException(f"The 'default' attribute cannot be empty. Options are: {str(options)}")

        # Validate connections attribute
        if not self.connections or not isinstance(self.connections, (Connections, dict)):
            raise OrionisIntegrityException("The 'connections' attribute must be an instance of Connections or a non-empty dictionary.")
        if isinstance(self.connections, dict):
            self.connections = Connections(**self.connections)