from pydantic import model_validator
import numpy as np

from lume.variables.variable import Variable, ConfigEnum


class BoolVariable(Variable):
    """Variable bool bool values.

    Attributes
    ----------
    default_value : bool | None
        Default value for the variable.
    """

    default_value: bool | None = None

    @model_validator(mode="after")
    def validate_default_value(self):
        if self.default_value is not None:
            self.validate_value(self.default_value, ConfigEnum.ERROR)
        return self

    def validate_value(self, value: bool, config: ConfigEnum = None):
        """Validates the given value.

        Parameters
        ----------
        value : bool
            The value to be validated.
        config : ConfigEnum, optional
            The configuration for validation. Defaults to None.
            Allowed values are "none", "warn", and "error".

        Raises
        ------
        TypeError
            If the value is not of type bool.
        ValueError
            If the value is out of the valid range or does not match the default value
            for constant variables.

        """
        # mandatory validation
        self._validate_value_type(value)

        # optional validation
        config = self._validation_config_as_enum(config)

        if config != ConfigEnum.NULL:
            self._validate_value_is_within_range(value, config=config)

    @staticmethod
    def _validate_value_type(value: bool):
        if not isinstance(value, (bool, np.bool)):
            raise TypeError(
                f"Expected value to be of type {bool} or {np.bool}, but received {type(value)}."
            )

    def _validate_value_is_within_range(self, value: bool, config: ConfigEnum = None):
        config = self._validation_config_as_enum(config)
        # Additional validation here
