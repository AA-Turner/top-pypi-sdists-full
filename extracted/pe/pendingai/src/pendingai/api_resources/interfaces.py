#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from abc import abstractmethod
from typing import Generic, TypeVar

from pendingai.api_resources.object import ListObject, Object
from pendingai.auth import AuthSession
from pendingai.requestor.requestor import Requestor

T = TypeVar("T", bound=Object)


class ResourceInterface:
    def __init__(self, requestor: Requestor, session: AuthSession) -> None:
        self._requestor: Requestor = requestor
        self._session: AuthSession = session


class ListResourceInterface(Generic[T], ResourceInterface):
    @abstractmethod
    def list(self, *args, **kwargs) -> list[T] | ListObject[T]: ...  # FIXME: Remove list


class CreateResourceInterface(Generic[T], ResourceInterface):
    @abstractmethod
    def create(self, *args, **kwargs) -> T: ...


class RetrieveResourceInterface(Generic[T], ResourceInterface):
    @abstractmethod
    def retrieve(self, *args, **kwargs) -> T: ...


class UpdateResourceInterface(Generic[T], ResourceInterface):
    @abstractmethod
    def update(self, *args, **kwargs) -> T: ...


class DeleteResourceInterface(Generic[T], ResourceInterface):
    @abstractmethod
    def delete(self, *args, **kwargs) -> T: ...
