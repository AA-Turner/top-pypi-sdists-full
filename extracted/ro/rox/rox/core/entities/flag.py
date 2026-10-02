from rox.core.entities.rox_base import RoxBase
from rox.server.flags.flag_types import FlagTypes
from rox.core.context.merged_context import MergedContext
from rox.core.entities.default_flag_values import DefaultFlagValues
from rox.server.flags.normalize_flag_type import NormalizeFlagType


class Flag(RoxBase):

    def __init__(self, default_value=DefaultFlagValues.BOOLEAN):
        super(Flag, self).__init__(
            NormalizeFlagType.FLAG_TRUE_VALUE if default_value else NormalizeFlagType.FLAG_FALSE_VALUE,
            [NormalizeFlagType.FLAG_FALSE_VALUE, NormalizeFlagType.FLAG_TRUE_VALUE],
            FlagTypes.BOOLEAN,
            NormalizeFlagType.normalize_boolean
        )

    def is_enabled(self, context=None):
        merged_context = MergedContext(self.parser.global_context if self.parser is not None else None, context)
        value = self._get_value(merged_context)

        self.send_impressions(value, merged_context)
        return value

    def _is_enabled(self, context, none_instead_of_default=False):
        return self._get_value(context, none_instead_of_default)

    def enabled(self, context, action):
        if self.is_enabled(context):
            action()

    def disabled(self, context, action):
        if not self.is_enabled(context):
            action()

    def get_value(self, context=None):
        merged_context = MergedContext(self.parser.global_context if self.parser is not None else None, context)
        value = self._get_value(merged_context)
        # get_value always returns a string, so map to the string value
        value_as_str = NormalizeFlagType.FLAG_TRUE_VALUE if value else NormalizeFlagType.FLAG_FALSE_VALUE
        self.send_impressions(value_as_str, merged_context)

        return value_as_str

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.default_value)

    def __str__(self):
        return "%s(%s, name=%s, condition=%s)" % (type(self).__name__, self.default_value, self.name, self.condition)
