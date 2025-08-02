import asyncio
import logging
import time
from typing import Any, Optional

from .automation import Automation
from .models import ReviewStatus, ReviewModal
from .store import ReviewStore

logger = logging.getLogger(__name__)


class Review:
    """ "
    Review are attached to workflow executions.
    """

    store: ReviewStore
    execution_id: str
    review_id: str
    instruction: str

    def __init__(
        self,
        store: ReviewStore,
        execution_id: str,
        review_id: str,
        description: str,
        artifacts: Optional[list[Any]] = None,
    ):
        self.store = store
        self.execution_id = execution_id
        self.review_id = review_id
        self.instruction = description

        if self.store.get_review(execution_id, review_id) is None:
            new_review = ReviewModal(
                id=review_id,
                type="custom",
                instruction=description,
                artifacts=artifacts,
                status=ReviewStatus.PENDING,
                data=None,
            )
            self.store.create_review(execution_id, new_review)
            self.review_id = new_review.id

    async def wait(
        self, timeout: int = 900
    ):  # Default timeout equal to session timeout, i.e, 15 mins
        """Polls every 5 seconds until the review status is COMPLETED or timeout is reached."""
        automation = Automation.get_instance()
        automation.execution.mark_for_review()

        interval = 5  # seconds
        deadline = time.time() + timeout

        logger.info(
            f"review_requested {self.execution_id} {self.review_id} {self.instruction}"
        )

        while time.time() < deadline:
            status = self.status
            if status == ReviewStatus.READY:
                logger.info(
                    f"review {self.review_id} for execution ID {self.execution_id} is complete."
                )
                automation.execution.mark_resume()
                return
            await asyncio.sleep(interval)

        automation.execution.mark_resume()
        return f"Review '{self.review_id}' did not complete within {timeout} seconds."

    @property
    def status(self) -> ReviewStatus:
        return self.store.get_review(self.execution_id, self.review_id).status

    @property
    def data(self) -> Any:
        """Get the corrected data after review."""
        return self.store.get_review(self.execution_id, self.review_id).data


# shortcut for orby.review()
def review(key: str, instruction: str, artifacts: Optional[list[Any]] = None) -> Review:
    automation = Automation.get_instance()
    return Review(
        automation.store, automation.execution_id, key, instruction, artifacts
    )
