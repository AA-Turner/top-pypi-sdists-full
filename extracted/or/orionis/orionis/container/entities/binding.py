from dataclasses import dataclass, field
from orionis.container.enums.lifetimes import Lifetime
from orionis.container.exceptions import OrionisContainerTypeError
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Binding(BaseEntity):

    contract: type = field(
        default=None,
        metadata={
            "description": "Contract of the concrete class to inject.",
            "default": None
        }
    )

    concrete: type = field(
        default=None,
        metadata={
            "description": "Concrete class implementing the contract.",
            "default": None
        }
    )

    instance: object = field(
        default=None,
        metadata={
            "description": "Concrete instance of the class, if provided.",
            "default": None
        }
    )

    function: callable = field(
        default=None,
        metadata={
            "description": "Function invoked to create the instance.",
            "default": None
        }
    )

    lifetime: Lifetime = field(
        default=Lifetime.TRANSIENT,
        metadata={
            "description": "Lifetime of the instance.",
            "default": Lifetime.TRANSIENT
        }
    )

    enforce_decoupling: bool = field(
        default=False,
        metadata={
            "description": "Indicates whether to enforce decoupling between contract and concrete.",
            "default": False
        }
    )

    alias: str = field(
        default=None,
        metadata={
            "description": "Alias for resolving the dependency from the container.",
            "default": None
        }
    )

    def __post_init__(self):
        """
        Validates the types of specific instance attributes after object initialization.

        This method ensures that:
        - The 'lifetime' attribute is an instance of the `Lifetime` enum.
        - The 'enforce_decoupling' attribute is a boolean.
        - The 'alias' attribute is either a string or None.

        If any of these conditions are not met, an `OrionisContainerTypeError` is raised to prevent improper usage.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It raises an exception if validation fails.

        Raises
        ------
        OrionisContainerTypeError
            If 'lifetime' is not an instance of `Lifetime`.
        OrionisContainerTypeError
            If 'enforce_decoupling' is not of type `bool`.
        OrionisContainerTypeError
            If 'alias' is not of type `str` or `None`.
        """

        # Validate that 'lifetime' is an instance of Lifetime enum if provided
        if self.lifetime and not isinstance(self.lifetime, Lifetime):
            raise OrionisContainerTypeError(
                f"The 'lifetime' attribute must be an instance of 'Lifetime', but received type '{type(self.lifetime).__name__}'."
            )

        # Validate that 'enforce_decoupling' is a boolean
        if not isinstance(self.enforce_decoupling, bool):
            raise OrionisContainerTypeError(
                f"The 'enforce_decoupling' attribute must be of type 'bool', but received type '{type(self.enforce_decoupling).__name__}'."
            )

        # Validate that 'alias' is either a string or None
        if self.alias and not isinstance(self.alias, str):
            raise OrionisContainerTypeError(
                f"The 'alias' attribute must be of type 'str' or 'None', but received type '{type(self.alias).__name__}'."
            )