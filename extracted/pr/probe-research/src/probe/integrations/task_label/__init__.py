"""The dataset fields that key and name an RL task, and the reader every integration shares."""

from .task_label import TASK_DESCRIPTION_FIELD, TASK_ID_FIELD, TASK_NAME_FIELD, get_task_label

__all__ = ["TASK_DESCRIPTION_FIELD", "TASK_ID_FIELD", "TASK_NAME_FIELD", "get_task_label"]
