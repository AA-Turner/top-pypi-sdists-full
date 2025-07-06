from typing import Any, Dict

from .._tasks import _Tasks


class TasksInfo:
    """
    Class which provides metadata about available tasks from the Tempo Tasks tab
    """

    def __init__(self, tasks: _Tasks):
        self.__tasks = tasks

    def get_all_available_tasks(self, locust_request_label: str = "Tasks.MainMenu.GetAllAvailable") -> Dict[str, Any]:
        """
        Retrieves all the available "tasks" and associated metadata from "Appian-Tempo-Tasks"

        Args:
            locust_request_label (str): Label locust should associate with the request

        Returns (dict): List of tasks and associated metadata

        Examples:

            >>> tasks_info.get_all_available_tasks()

        """
        return self.__tasks.get_all(locust_request_label=locust_request_label)

    def get_task_info(self, task_name: str, exact_match: bool = True) -> Dict[str, Any]:
        """
        Get the information about specific task by name.

        Args:
            task_name (str): Name of the action
            exact_match (bool): Should action name match exactly or to be partial match. Default : True

        Returns (dict): Specific Task's info

        Raises: In case of task is not found in the system, it throws an "Exception"

        Example:
            If full name of task is known:

            >>> task_info.get_task_info("task_name", exact_match=True)

            If only the display name is known, or part of the display name:

            >>> task_info.get_task_info("task")

        """
        return self.__tasks.get_task(task_name=task_name, exact_match=exact_match)
