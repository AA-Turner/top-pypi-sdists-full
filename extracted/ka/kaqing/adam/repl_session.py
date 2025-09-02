from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

class ReplSession:
    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ReplSession, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        if not hasattr(self, 'prompt_session'):
            self.prompt_session = PromptSession(auto_suggest=AutoSuggestFromHistory())