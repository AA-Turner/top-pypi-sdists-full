from rox.core.entities.rox_base import RoxBase
from rox.server.flags.flag_types import FlagTypes
from rox.core.context.merged_context import MergedContext
from rox.core.entities.default_flag_values import DefaultFlagValues
from rox.server.flags.normalize_flag_type import NormalizeFlagType


# Python does not have double type, only float
# Calling this RoxDouble instead of RoxFloat to keep it inline with the other SDKs
class RoxDouble(RoxBase):
    def __init__(self, default_value=DefaultFlagValues.FLOAT, options = []):
        super(RoxDouble, self).__init__(default_value, options, FlagTypes.FLOAT, NormalizeFlagType.normalize_float)

    def get_value(self, context=None):
        return self.get_double(context)

    def get_double(self, context=None):
        merged_context = MergedContext(self.parser.global_context if self.parser is not None else None, context)
        value = self._get_value(merged_context)

        self.send_impressions(value, merged_context)
        return value

