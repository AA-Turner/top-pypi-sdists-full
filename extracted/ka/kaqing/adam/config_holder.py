from typing import TypeVar

T = TypeVar('T')

class ConfigReadable:
    def is_debug() -> bool:
        pass

    def get(self, key: str, default: T) -> T:
        pass

class ConfigHolder:
    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ConfigHolder, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        if not hasattr(self, 'config'):
            # set by Config
            self.config: 'ConfigReadable' = None
            # only for testing
            self.is_display_help = True
            # set by ReplSession
            self.append_command_history = lambda entry: None