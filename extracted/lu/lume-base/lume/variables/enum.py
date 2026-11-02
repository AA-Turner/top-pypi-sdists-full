import warnings
from typing import Any
from pydantic import field_validator, model_validator

from lume.variables.variable import Variable, ConfigEnum


class EnumVariable(Variable):
    """Variable for enumerated values.

    Attributes
    ----------
    default_value : Any | None
        Default value for the variable. Must be one of the allowed options.
    options : list[Any]
        List of allowed values for this variable.
    """

    default_value: Any | None = None
    options: list[Any]

    @field_validator("options", mode="before")
    @classmethod
    def validate_options(cls, value):
        if not value:
            raise ValueError("options must not be empty.")
        if not isinstance(value, (list, tuple)):
            raise ValueError("options must be a list or tuple.")
        return list(value)

    @model_validator(mode="after")
    def validate_default_value(self):
        if self.default_value is not None:
            self.validate_value(self.default_value, ConfigEnum.ERROR)
        return self

    def validate_value(self, value: Any, config: ConfigEnum = None):
        """Validates the given value.

        Parameters
        ----------
        value : Any
            The value to be validated.
        config : ConfigEnum, optional
            The configuration for validation. Defaults to None.
            Allowed values are "none", "warn", and "error".

        Raises
        ------
        TypeError
            If the value type does not match the option types.
        ValueError
            If the value is not in the list of allowed options.

        """
        # mandatory validation
        self._validate_value_is_in_options(value, config=config)

    def _validate_value_is_in_options(self, value: Any, config: ConfigEnum = None):
        """Validate that value is one of the allowed options.

        Parameters
        ----------
        value : Any
            The value to validate.
        config : ConfigEnum, optional
            The configuration for validation. Defaults to None.

        Raises
        ------
        ValueError
            If the value is not in the list of allowed options.
        """
        config = self._validation_config_as_enum(config)

        if value not in self.options:
            error_message = f"Value '{value}' of '{self.name}' is not one of the allowed options: {self.options}."
            if config == ConfigEnum.WARN:
                warnings.warn(error_message)
            else:
                raise ValueError(error_message)
