import re
import warnings
from pydantic import field_validator, model_validator

from lume.variables.variable import Variable, ConfigEnum


class StrVariable(Variable):
    """Variable for str values.

    Attributes
    ----------
    default_value : str | None
        Default value for the variable.
    min_length : int | None
        Minimum allowed string length (inclusive). Ignore if set to `None`.
    max_length : int | None
        Maximum allowed string length (inclusive). Ignore if set to `None`.
    regex : str | None
        Regex pattern the string must fully match. Ignore if set to `None`.
    """

    default_value: str | None = None
    min_length: int | None = None
    max_length: int | None = None
    regex: str | None = None

    @field_validator("min_length", "max_length", mode="before")
    @classmethod
    def validate_length_bounds(cls, value):
        if value is not None and value < 0:
            raise ValueError(f"Length bound must be non-negative, got {value}.")
        return value

    @model_validator(mode="after")
    def validate_length_range(self):
        if self.min_length is not None and self.max_length is not None:
            if self.min_length > self.max_length:
                raise ValueError(
                    f"min_length ({self.min_length}) must be less than or equal to"
                    f" max_length ({self.max_length})."
                )
        return self

    @model_validator(mode="after")
    def validate_default_value(self):
        if self.default_value is not None:
            self.validate_value(self.default_value, ConfigEnum.ERROR)
        return self

    def validate_value(self, value: str, config: ConfigEnum = None):
        """Validates the given value.

        Parameters
        ----------
        value : str
            The value to be validated.
        config : ConfigEnum, optional
            The configuration for validation. Defaults to None.
            Allowed values are "none", "warn", and "error".

        Raises
        ------
        TypeError
            If the value is not of type str.
        ValueError
            If the value length is outside the valid range or does not match the regex.

        """
        # mandatory validation
        self._validate_value_type(value)

        # optional validation
        config = self._validation_config_as_enum(config)

        if config != ConfigEnum.NULL:
            self._validate_value_is_within_range(value, config=config)

    @staticmethod
    def _validate_value_type(value: str):
        if not isinstance(value, str):
            raise TypeError(
                f"Expected value to be of type {str}, but received {type(value)}."
            )

    def _validate_value_is_within_range(self, value: str, config: ConfigEnum = None):
        config = self._validation_config_as_enum(config)
        self._validate_str_length(value, config=config)
        self._validate_str_regex(value, config=config)

    def _validate_str_length(self, value: str, config: ConfigEnum = None):
        config = self._validation_config_as_enum(config)
        length = len(value)

        if self.min_length is not None and length < self.min_length:
            msg = (
                f"Value of '{self.name}' has length {length}, which is below"
                f" min_length ({self.min_length})."
            )
            if config == ConfigEnum.WARN:
                warnings.warn(msg)
            else:
                raise ValueError(msg)

        if self.max_length is not None and length > self.max_length:
            msg = (
                f"Value of '{self.name}' has length {length}, which exceeds"
                f" max_length ({self.max_length})."
            )
            if config == ConfigEnum.WARN:
                warnings.warn(msg)
            else:
                raise ValueError(msg)

    def _validate_str_regex(self, value: str, config: ConfigEnum = None):
        config = self._validation_config_as_enum(config)

        if self.regex is not None and not re.fullmatch(self.regex, value):
            msg = (
                f"Value '{value}' of '{self.name}' does not match"
                f" the required pattern: {self.regex!r}."
            )
            if config == ConfigEnum.WARN:
                warnings.warn(msg)
            else:
                raise ValueError(msg)
