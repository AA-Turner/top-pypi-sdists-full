from operator import truediv
from rox.core.entities.default_flag_values import DefaultFlagValues

# Static functions for noramlising flag types (i.e. string->other type) - each accepts a:
# - string-value: the string representation of the value.
# - default_value: the value to be returned if normalisation fails (i.e. the string data is not valid for that type)
class NormalizeFlagType:
    FLAG_TRUE_VALUE = 'true'
    FLAG_FALSE_VALUE = 'false'

    @staticmethod
    def normalize_string(string_value, default_value=DefaultFlagValues.STRING):
        return string_value

    @staticmethod
    def normalize_int(string_value, default_value=DefaultFlagValues.INT):
        try:
            return int(string_value)
        except ValueError:
            return default_value

    @staticmethod
    def normalize_float(string_value, default_value=DefaultFlagValues.FLOAT):
        try: 
            return float(string_value)
        except ValueError:
            return default_value

    @staticmethod
    def normalize_boolean(string_value, default_value=DefaultFlagValues.BOOLEAN):
        if type(string_value) == bool:
            return string_value
        if string_value == NormalizeFlagType.FLAG_TRUE_VALUE:
            return True
        if string_value == NormalizeFlagType.FLAG_FALSE_VALUE:
            return False
        return default_value
