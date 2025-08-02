
from abc import ABCMeta, abstractmethod
from logging import Logger
from typing import List
from sidecar.sandbox_error import SandboxError


class StatusMaintainer:
    __metaclass__ = ABCMeta

    def __init__(self, logger: Logger):
        self._logger = logger

    @abstractmethod
    def update_qualiy_status(self, status: str):
        raise NotImplementedError

    @abstractmethod
    def add_sandbox_error(self, error: SandboxError):
        raise NotImplementedError


class IngressRouteRequest:
    def __init__(self, listener_port: int, path: str, host: str, app_port: int, app_name: str, color: str):
        self.listener_port = listener_port
        self.path = path
        self.host = host
        self.app_port = app_port
        self.app_name = app_name
        self.color = color