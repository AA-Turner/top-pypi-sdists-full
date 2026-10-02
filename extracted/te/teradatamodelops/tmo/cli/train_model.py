import importlib
import json
import logging
import os
import shutil
import subprocess
import sys

from tmo.cli.base_model import BaseModel
from tmo.context.model_context import ModelContext, DatasetInfo
from tmo.types.job import JobRunnerMode, JobRunnerEngine, JobAutomationMode

ARTIFACTS_PATH = "./artifacts"
MODELS_PATH = "./models"


class TrainModel(BaseModel):

    def __init__(self, repo_manager):
        super().__init__(repo_manager)
        self.logger = logging.getLogger(__name__)

    def train_model_local(self, model_id: str, rendered_dataset: dict, base_path: str):

        base_path = (
            self.repo_manager.model_catalog_path
            if base_path is None
            else os.path.join(base_path, "")
        )
        model_definitions_path = f"{base_path}model_definitions/"

        if not os.path.exists(model_definitions_path):
            raise ValueError(f"model directory {model_definitions_path} does not exist")

        model_artefacts_path = f".artefacts/{model_id}/"  # noqa
        model_artefacts_abs_path = os.path.abspath(model_artefacts_path)
        model_artefacts_output_path = os.path.join(model_artefacts_path, "output/")
        if os.path.exists(model_artefacts_path):
            self.logger.debug(
                f"Cleaning local model artefact path: {model_artefacts_path}"
            )
            shutil.rmtree(model_artefacts_path)

        os.makedirs(model_artefacts_output_path)

        try:
            if os.path.exists(ARTIFACTS_PATH):
                os.remove(ARTIFACTS_PATH)

            if os.name == "nt":
                subprocess.run(
                    [
                        "cmd",
                        "/c",
                        "mklink",
                        "/J",
                        "artifacts",
                        model_artefacts_abs_path,
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            else:
                os.symlink(
                    model_artefacts_path, ARTIFACTS_PATH, target_is_directory=True
                )

            model_dir = model_definitions_path + BaseModel.get_model_folder(  # noqa
                model_definitions_path, model_id
            )

            with open(f"{model_dir}/model.json", "r") as f:
                model_definition = json.load(f)

            with open(f"{model_dir}/config.json", "r") as f:
                model_conf = json.load(f)

            self.logger.info("Loading and executing model code")

            cli_model_kwargs = self._BaseModel__get_model_varargs(model_id)  # noqa

            context = ModelContext(
                dataset_info=DatasetInfo.from_dict(rendered_dataset),
                hyperparams=model_conf["hyperParameters"],
                artifact_output_path="artifacts/output",
                **cli_model_kwargs,
            )

            engine = JobRunnerEngine(
                self._BaseModel__get_engine(  # noqa
                    model_definition, JobAutomationMode.TRAIN
                )
            )
            if engine == JobRunnerEngine.PYTHON:
                sys.path.append(model_dir)
                training = importlib.import_module(".training", package="model_modules")
                training.train(
                    context=context,
                    data_conf=rendered_dataset,
                    model_conf=model_conf,
                    **cli_model_kwargs,
                )

            elif engine == JobRunnerEngine.SQL:
                self.__train_sql(
                    context, model_dir, rendered_dataset, model_conf, **cli_model_kwargs
                )

            elif engine == JobRunnerEngine.R:
                self._BaseModel__run_r_model(  # noqa
                    model_id,
                    model_dir,
                    rendered_dataset,
                    JobRunnerMode.TRAIN.value.lower(),
                )

            else:
                raise ValueError(f"Unsupported engine: {engine}")

            self.logger.info(
                f"Artefacts can be found in: {model_artefacts_output_path}"
            )
            self.__cleanup()
        except ModuleNotFoundError:
            model_dir = model_definitions_path + BaseModel.get_model_folder(
                model_definitions_path, model_id
            )
            self.__cleanup()
            self.logger.error(
                "Missing required python module, try running following command first:"
            )
            self.logger.error(
                f"pip install -r {model_dir}/model_modules/requirements.txt"
            )
            raise
        except:
            self.__cleanup()
            self.logger.exception("Exception running model code")
            raise

    @staticmethod
    def __cleanup():
        if os.path.exists(ARTIFACTS_PATH):
            os.remove(ARTIFACTS_PATH)
        if os.path.exists(MODELS_PATH):
            os.remove(MODELS_PATH)

    def __train_sql(
        self,
        context: ModelContext,
        model_dir: str,
        data_conf: dict,
        model_conf: dict,
        **kwargs,
    ):
        from tmo.util import tmo_create_context
        from teradataml import remove_context

        self.logger.info("Starting training...")

        tmo_create_context()  # noqa

        sql_file = f"{model_dir}/model_modules/training.sql"
        jinja_ctx = {
            "context": context,
            "data_conf": data_conf,
            "model_conf": model_conf,
            "model_table": kwargs.get("model_table"),
            "model_version": kwargs.get("model_version"),
            "model_id": kwargs.get("model_id"),
        }

        self._BaseModel__execute_sql_script(sql_file, jinja_ctx)  # noqa

        remove_context()

        self.logger.info("Finished training")

        self.logger.info("Saved trained model")

        remove_context()
