import os

from python_agent.common.constants import PREFIXES, MESSAGES_CANNOT_BE_NONE

# Aliases for environment variable suffixes that use underscore-separated naming
# instead of the camelCase convention used by ConfigData attributes.
# Maps uppercase suffix (after stripping prefix) -> canonical ConfigData attribute name.
# e.g. SL_LAB_ID -> strip prefix -> LAB_ID -> alias -> labId
ENV_ALIASES = {
    "LAB_ID": "labId",
    # v3-style footprints aliases. The BE exposes three external names;
    # internal fields stay identical to today. The matching env var styles
    # are SL_FOOTPRINTS_SEND_INTERVAL_SECS etc. — they are uppercased by the
    # resolver before lookup, so the key below is already upper-cased and
    # underscore-separated.
    "FOOTPRINTS_SEND_INTERVAL_SECS": "intervalSeconds",
    "FOOTPRINTS_COLLECT_INTERVAL_SECS": "_add_coverage_interval_seconds",
    "FOOTPRINTS_BUFFER_THRESHOLD_MB": "footprintsBufferThresholdMB",
    # camelCase variants (SL_FOOTPRINTSSENDINTERVALSECS uppercased strips
    # underscores) are covered by the normal dir(ConfigData) lookup for
    # footprintsBufferThresholdMB, but the other two need explicit aliases
    # because their internal field names differ.
    "FOOTPRINTSSENDINTERVALSECS": "intervalSeconds",
    "FOOTPRINTSCOLLECTINTERVALSECS": "_add_coverage_interval_seconds",
    # SL_TEST_NAME_FORMAT is the documented spelling for --testNameFormat.
    # Underscore-separated is the convention for new parameters; the camelCase
    # SL_TESTNAMEFORMAT also resolves through the ordinary dir(ConfigData)
    # lookup, but is neither documented nor tested.
    "TEST_NAME_FORMAT": "testNameFormat",
}


class EnvironmentVariablesResolver(object):
    """
    This class resolves Sealights Related environment variables.
    """

    def __init__(self, int_properties, target_object):
        if target_object is None:
            raise Exception("'target_object'" + MESSAGES_CANNOT_BE_NONE)

        self.key_to_case_sensitive_key = {}
        self.int_properties = int_properties or []

        keys = dir(target_object)
        for case_sensitive_key in keys:
            # Windows have upper case keys, so we keep a mapping between upper key (ie, 'APPNAME') to case sensitive one (ie, 'appName').
            self.key_to_case_sensitive_key[case_sensitive_key.upper()] = (
                case_sensitive_key
            )

    def resolve(self):
        result = {}
        for prefix in PREFIXES:
            result.update(self.resolve_with_prefix(prefix))
        return result

    def resolve_with_prefix(self, prefix):
        result = {}
        for key in os.environ.keys():
            if key.lower().startswith(prefix.lower()):
                value = os.environ[key]
                uppercase_key = key[len(prefix) :].upper()
                if not self.key_to_case_sensitive_key.get(uppercase_key):
                    # Check aliases for alternative naming conventions (e.g. SL_LAB_ID -> labId)
                    aliased_attr = ENV_ALIASES.get(uppercase_key)
                    if aliased_attr:
                        uppercase_key = aliased_attr.upper()
                    else:
                        # could be an external environment variable that isn't in the target object
                        continue
                case_sensitive_key = self.key_to_case_sensitive_key[uppercase_key]
                if case_sensitive_key in self.int_properties:
                    value = int(value)
                # Update the underlying dictionary. We assume object use the case sensitive keys
                result.update({case_sensitive_key: value})
        return result
