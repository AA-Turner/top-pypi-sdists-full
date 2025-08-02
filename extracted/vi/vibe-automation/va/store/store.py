from typing import Any
from abc import ABC, abstractmethod

from va.models import ReviewModal
from va.protos.orby.va.public.execution_messages_pb2 import ExecutionStatus


class ExecutionStore(ABC):
    @abstractmethod
    def mark_start(self, execution_id: str) -> None:
        pass

    @abstractmethod
    def mark_stop(
        self, execution_id: str, status: ExecutionStatus.ValueType = None
    ) -> None:
        pass

    @abstractmethod
    def mark_for_review(self, execution_id: str) -> None:
        pass

    @abstractmethod
    def mark_resume(self, execution_id: str) -> None:
        pass

    @abstractmethod
    def mark_step_executed(self, execution_id: str, step: str) -> None:
        pass

    @abstractmethod
    def mark_step_executing(self, execution_id: str, step: str) -> None:
        pass

    @abstractmethod
    def get_execution_input(self, execution_id: str) -> Any:
        pass

    @abstractmethod
    def save_execution_data(self, execution_id: str, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def get_execution_data(self, execution_id: str, key: str) -> Any:
        pass


class ReviewStore(ABC):
    @abstractmethod
    def create_review(self, execution_id: str, review: ReviewModal) -> None:
        pass

    @abstractmethod
    def get_review(self, execution_id: str, review_id: str) -> ReviewModal:
        pass


class Store(ExecutionStore, ReviewStore):
    pass
