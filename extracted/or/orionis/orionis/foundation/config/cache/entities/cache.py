from dataclasses import dataclass, field
from orionis.foundation.config.cache.entities.stores import Stores
from orionis.foundation.config.cache.enums import Drivers
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.services.environment.env import Env
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Cache(BaseEntity):
    """
    Represents the cache configuration for the application.

    Attributes:
        default (Drivers | str): The default cache storage type. Can be a member of the Drivers enum or a string
            (e.g., 'memory', 'file'). Defaults to the value of the 'CACHE_STORE' environment variable or Drivers.MEMORY.
        stores (Stores): The configuration for available cache stores. Defaults to a Stores instance with a file store
            at the path specified by the 'CACHE_PATH' environment variable or "storage/framework/cache/data".

    Methods:
        __post_init__():
            - Validates that 'default' is either a Drivers enum member or a string.
            - Converts 'default' from string to Drivers enum if necessary.
            - Validates that 'stores' is an instance of Stores.
    """

    default: Drivers | str = field(
        default_factory = lambda : Env.get("CACHE_STORE", Drivers.MEMORY.value),
        metadata = {
            "description": "The default cache storage type. Can be a member of the Drivers enum or a string (e.g., 'memory', 'file').",
            "default": Drivers.MEMORY.value
        },
    )

    stores: Stores | dict = field(
        default_factory = lambda: Stores(),
        metadata = {
            "description": "The configuration for available cache stores. Defaults to a file store at the specified path.",
            "default": lambda: Stores().toDict()
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization method for validating and normalizing cache configuration.

        Ensures that:
        - The `default` attribute is either an instance of `Drivers` or a string representing a valid driver name.
        - If `default` is a string, it is converted to the corresponding `Drivers` enum member after validation.
        - The `stores` attribute is an instance of `Stores`.

        Raises:
            OrionisIntegrityException: If `default` is not a valid driver or if `stores` is not an instance of `Stores`.
        """

        # Validate the 'default' attribute to ensure it is either a Drivers enum member or a string
        if not isinstance(self.default, (Drivers, str)):
            raise OrionisIntegrityException("The default cache store must be an instance of Drivers or a string.")

        options_drivers = Drivers._member_names_
        if isinstance(self.default, str):
            _value = self.default.upper().strip()
            if _value not in options_drivers:
                raise OrionisIntegrityException(f"Invalid cache driver: {self.default}. Must be one of {str(options_drivers)}.")
            else:
                self.default = Drivers[_value].value
        else:
            self.default = self.default.value

        # Validate the 'stores' attribute to ensure it is an instance of Stores
        if not isinstance(self.stores, (Stores, dict)):
            raise OrionisIntegrityException("The stores configuration must be an instance of Stores or a dictionary.")
        if isinstance(self.stores, dict):
            self.stores = Stores(**self.stores)