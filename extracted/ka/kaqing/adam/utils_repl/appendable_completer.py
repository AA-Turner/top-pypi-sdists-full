from abc import abstractmethod

class AppendableCompleter:
    @abstractmethod
    def append_completions(self, key: str, value: dict[str, any]):
        pass