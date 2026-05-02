import re
from acceldata_sdk.constants import MIN_TORCH_BACKEND_VERSION_FOR_RULE_ID_API
from semantic_version import Version, SimpleSpec


class APIVersionUtils:

    def __init__(self):
        pass

    @staticmethod
    def _has_leading_zero(value: str) -> bool:
        """Checks if the version component has a leading zero."""
        return value and value[0] == '0' and value.isdigit() and value != '0'

    @staticmethod
    def extract_actual_version(torch_version) -> str:
        """Extracts the actual version from the given torch_version object."""
        version_string = torch_version.buildVersion
        if version_string:
            version_pattern = r'^(\d+)(?:\.(\d+)(?:\.(\d+))?)?(?:-(.*))?$'
            match = re.match(version_pattern, version_string)

            if not match:
                raise ValueError(f'Invalid version string: {version_string}')

            major, minor, patch, _ = match.groups()

            # Validate no leading zeroes in version parts
            for part_name, part in zip(['major', 'minor', 'patch'], [major, minor, patch]):
                if APIVersionUtils._has_leading_zero(part):
                    raise ValueError(f"Invalid leading zero in {part_name} part of version: {version_string}")

            # Convert to integers, treating missing parts as zeros
            major, minor, patch = int(major), int(minor or 0), int(patch or 0)
            actual_version = f'{major}.{minor}.{patch}'
            return actual_version
        else:
            raise ValueError('Torch version is not available.')


    @staticmethod
    def validate_torch_version_for_rule_id_api(actual_version: str):
        """Validates if the given Torch version supports the rule ID API."""
        if Version(MIN_TORCH_BACKEND_VERSION_FOR_RULE_ID_API) not in SimpleSpec(f'<={actual_version}'):
            raise ValueError(f'The rule ID API is not supported for Torch version {actual_version}.')
