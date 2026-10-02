from rox.server.flags.normalize_flag_type import NormalizeFlagType
from rox.core.utils.type_utils import is_string


class EvaluationResult:
    def __init__(self, value):
        self.value = value

    def bool_value(self):
        if self.value is None:
            return False

        if isinstance(self.value, bool):
            return self.value

        return None

    def string_value(self):
        if is_string(self.value):
            return self.value

        if isinstance(self.value, bool):
            return NormalizeFlagType.FLAG_TRUE_VALUE if self.value else NormalizeFlagType.FLAG_FALSE_VALUE

        return None
