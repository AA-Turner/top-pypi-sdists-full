from abc import abstractmethod


class CloudCopier:
    @abstractmethod
    def upload(self, source_local_file: str, target_file: str) -> None:
        pass
