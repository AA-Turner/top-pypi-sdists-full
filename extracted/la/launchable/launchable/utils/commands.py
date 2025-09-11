from enum import Enum


class Command(Enum):
    VERIFY = 'VERIFY'
    RECORD_TESTS = 'RECORD_TESTS'
    RECORD_BUILD = 'RECORD_BUILD'
    RECORD_SESSION = 'RECORD_SESSION'
    SUBSET = 'SUBSET'
    COMMIT = 'COMMIT'
    FLAKE_DETECTION = 'FLAKE_DETECTION'

    def display_name(self):
        return self.value.lower().replace('_', ' ')
