import logging
from collections import defaultdict
from typing import Any

from abc import ABC, abstractmethod
from va.models import ReviewStatus, ReviewModal
from va.store.store import Store
from va.protos.orby.va.public.execution_messages_pb2 import ExecutionStatus


class ExecutionState:
    executed_steps: list[str] = []
    executing_steps: list[str] = []
    input: Any
    data: dict[str, Any] = dict()
    reviews: dict[str, ReviewModal] = dict()


class DebugMethod(ABC):
    def set_execution_input(self, execution_id: str, input: Any):
        pass

    @abstractmethod
    def set_review_status(
        self, execution_id: str, review_id: str, status: ReviewStatus
    ):
        pass

    @abstractmethod
    def set_review_data(self, execution_id: str, review_id: str, data: Any):
        pass


logger = logging.getLogger(__name__)


class InMemoryStore(Store, DebugMethod):
    execution_state: dict[str, ExecutionState]

    def __init__(self):
        self.execution_state = defaultdict(ExecutionState)

    def save_execution_data(self, execution_id: str, key: str, value: Any):
        logger.info(f"save_execution_data {key} {value}")
        self.execution_state[execution_id].data[key] = value

    def get_execution_data(self, execution_id: str, key: str):
        logger.info(f"get_execution_data {key}")
        return self.execution_state[execution_id].data[key]

    def get_execution_input(self, execution_id: str):
        logger.info("get_execution_input")
        return self.execution_state[execution_id].input

    def mark_step_executed(self, execution_id: str, step: str):
        logger.info(f"mark_step_executed {step}")
        execution_state = self.execution_state[execution_id]
        execution_state.executing_steps.remove(step)
        execution_state.executed_steps.append(step)

    def mark_step_executing(self, execution_id: str, step: str):
        logger.info(f"mark_step_executing {step}")
        self.execution_state[execution_id].executing_steps.append(step)

    def create_review(self, execution_id: str, review: ReviewModal):
        logger.info(f"create_review {review}")
        self.execution_state[execution_id].reviews[review.id] = review

    def get_review(self, execution_id: str, review_id: str):
        logger.info(f"get_review {review_id}")
        return self.execution_state[execution_id].reviews.get(review_id)

    def set_execution_input(self, execution_id: str, input: Any):
        logger.info(f"set_execution_input {input}")
        self.execution_state[execution_id].input = input

    def set_review_status(
        self, execution_id: str, review_id: str, status: ReviewStatus
    ):
        logger.info(f"set_review_status {review_id} {status}")
        self.execution_state[execution_id].reviews[review_id].status = status

    def set_review_data(self, execution_id: str, review_id: str, data: Any):
        logger.info(f"set_review_data {review_id} {data}")
        self.execution_state[execution_id].reviews[review_id].data = data

    def mark_start(self, execution_id: str) -> None:
        logger.info("mark_start")
        pass

    def mark_stop(
        self, execution_id: str, status: ExecutionStatus.ValueType = None
    ) -> None:
        logger.info("mark_stop")
        pass

    def mark_for_review(self, execution_id: str) -> None:
        logger.info("mark_for_review")
        pass

    def mark_resume(self, execution_id: str) -> None:
        logger.info("mark_resume")
        pass
