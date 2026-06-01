import logging
from uuid import UUID

from picsellia.sdk.user import User
from picsellia.sdk.worker import Worker
from picsellia.types.enums import WorkerType

logger = logging.getLogger("picsellia")


def parse_user_weights_to_assignees(
    assignees: list[tuple[Worker | User | UUID, float | int]],
    expected_worker_type: WorkerType | None = None,
):
    users = []
    for user, weight in assignees:
        if isinstance(user, Worker):
            logger.warning(
                "You should not use Worker anymore, instead use User or UUID for an user id"
            )
            if expected_worker_type and user.type != expected_worker_type:
                raise ValueError(f"Assignee {user} cannot be used for this campaign.")
            user_id = user.user_id
        elif isinstance(user, User):
            user_id = user.id
        else:
            # Assume it's a user id and not a worker_id anymore
            user_id = user
        users.append({"user_id": user_id, "weight": weight})

    return users
