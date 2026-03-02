import inspect
import logging
import os
import runpy
import shutil
import subprocess
import types

from tmo.cli.base_task import BaseTask
from tmo.context.model_context import ModelContext, DatasetInfo

ARTIFACTS_PATH = "./artifacts"


class RunTask(BaseTask):

    def __init__(self, repo_manager):
        super().__init__(repo_manager)
        self.logger = logging.getLogger(__name__)

    def run_task_local(self, base_path: str, task_name: str = None, func: str = None):

        base_path = os.path.join(base_path, "")
        task_path = base_path + "feature_engineering_tasks/"

        if not os.path.exists(task_path):
            raise ValueError(
                f"feature engineering task directory {task_path} does not exist"
            )

        catalog = BaseTask.get_task_folders(task_path)  # noqa

        cli_task_kwargs = self._BaseTask__get_task_varargs()  # noqa

        if not task_name or task_name not in catalog:
            print("")
            print(
                "Task name not found. Please select one from the list below or"
                " press Ctrl+C to quit."
            )
            task_name = self.__input_select(
                "task",
                catalog,
                "Available feature engineering tasks:",
            )

        task_file_path = os.path.join(task_path, task_name, "task.py")

        task_artefacts_path = f".artefacts/{task_name}/"  # noqa
        task_artefacts_abs_path = os.path.abspath(task_artefacts_path)
        task_artefacts_output_path = os.path.join(task_artefacts_path, "output/")
        if os.path.exists(task_artefacts_path):
            self.logger.debug(
                f"Cleaning local task artefact path: {task_artefacts_path}"
            )
            shutil.rmtree(task_artefacts_path)

        os.makedirs(task_artefacts_output_path)

        try:
            if os.path.exists(ARTIFACTS_PATH):
                os.remove(ARTIFACTS_PATH)

            if os.name == "nt":
                subprocess.run(
                    ["cmd", "/c", "mklink", "/J", "artifacts", task_artefacts_abs_path],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            else:
                os.symlink(
                    task_artefacts_path, ARTIFACTS_PATH, target_is_directory=True
                )

            context = ModelContext(
                artifact_output_path="artifacts/output",
                dataset_info=DatasetInfo.from_dict({}),
                hyperparams={},
                **cli_task_kwargs,
            )

            task_module = runpy.run_path(task_file_path)

            if not func or not (
                func in task_module
                and isinstance(task_module[func], types.FunctionType)
            ):
                function_names = [
                    name
                    for name, value in task_module.items()
                    if isinstance(value, types.FunctionType)
                    and inspect.getfile(value) == task_file_path
                ]
                print("")
                print(
                    "Function name not found. Please select one from the list below or"
                    " press Ctrl+C to quit."
                )
                func = self.__input_select(
                    "function", function_names, "Available functions:"
                )

            print("")

            self.logger.info("Loading and executing task code")
            task_module[func](context=context)

            self.logger.info(f"Artefacts can be found in: {task_artefacts_output_path}")
            self.__cleanup()
            return task_name, func
        except ModuleNotFoundError:
            self.__cleanup()
            self.logger.error(
                "Missing required python module, try running the following command"
                " first:"
            )
            self.logger.error(f"pip install -r {task_path}requirements.txt")
            raise
        except:
            self.__cleanup()
            self.logger.exception("Exception running feature engineering task code")
            raise

    @staticmethod
    def __cleanup():
        if os.path.exists(ARTIFACTS_PATH):
            os.remove(ARTIFACTS_PATH)

    @staticmethod
    def __print_underscored(message):  # TODO: should be moved to utils
        print(message)
        print("-" * len(message))

    def __input_select(
        self, name, values, label="", default=None
    ) -> str | None:  # TODO: should be moved to utils
        if len(values) == 0:
            return None

        if label != "":
            self.__print_underscored(label)

        for ix, item in enumerate(values):  # noqa
            default_text = " (default)" if default and default == item else ""
            print(f"[{ix}] {item}" + default_text)

        tmp_index = (
            input(f"Select {name} by index (or leave blank for the default one): ")
            if default
            else input(f"Select {name} by index: ")
        )

        if default and default in values and tmp_index == "":
            tmp_index = values.index(default)
        elif (tmp_index == "" and not default) or (
            not tmp_index.isnumeric() or int(tmp_index) >= len(values)
        ):
            print(
                "Wrong selection, please try again by selecting the index number on the"
                " first column."
            )
            print("You may cancel at anytime by pressing Ctrl+C.")
            print("")
            return self.__input_select(name, values, label, default)

        return values[int(tmp_index)]
