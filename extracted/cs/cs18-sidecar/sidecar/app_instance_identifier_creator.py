from abc import abstractmethod, ABCMeta
from logging import Logger

from sidecar.app_instance_identifier import AppInstanceIdentifier


class IAppInstanceIdentifierCreator:
    __metaclass__ = ABCMeta

    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    @abstractmethod
    def create(self, app_name: str, instance_id: str) -> AppInstanceIdentifier:
        raise NotImplementedError
