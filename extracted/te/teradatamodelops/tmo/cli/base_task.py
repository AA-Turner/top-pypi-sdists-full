import os

import yaml

REQUIREMENTS_FILE = "/requirements.txt"
TASK_PY_FILE = "/task.py"


class BaseTask(object):

    def __init__(self, repo_manager):
        self.repo_manager = repo_manager

    def __get_task_varargs(self):  # noqa # NOSONAR
        return {"project_id": self.__get_project_id(), "job_id": "cli"}

    def __get_project_id(self):
        self.repo_manager.repo_config_rename(self.repo_manager.base_path)
        path = os.path.join(self.repo_manager.base_path, ".tmo/config.yaml")
        with open(path, "r") as handle:
            return yaml.safe_load(handle)["project_id"]

    @staticmethod
    def get_task_folders(task_path: str) -> list[str]:
        catalog = []
        for task_folder in os.listdir(task_path):
            if os.path.exists(
                task_path + task_folder + REQUIREMENTS_FILE
            ) and os.path.exists(task_path + task_folder + TASK_PY_FILE):
                catalog.append(task_folder)

        return catalog
