import importlib
import json
import logging
import os
import sys

from tmo.cli.base_model import BaseModel
from tmo.cli.model_utils import cleanup_artifacts, ARTIFACTS_PATH
from tmo.context.model_context import ModelContext, DatasetInfo
from tmo.types.job import JobRunnerEngine, JobAutomationMode


class ScoreModel(BaseModel):

    def __init__(self, repo_manager):
        super().__init__(repo_manager)
        self.logger = logging.getLogger(__name__)

    def batch_score_model_local(
        self, model_id: str = None, rendered_dataset: dict = None, base_path: str = None
    ):
        base_path = (
            self.repo_manager.model_catalog_path
            if base_path is None
            else os.path.join(base_path, "")
        )
        model_definitions_path = f"{base_path}model_definitions/"

        if not os.path.exists(model_definitions_path):
            raise ValueError(f"model directory {model_definitions_path} does not exist")

        model_artefacts_path = f".artefacts/{model_id}"

        if not os.path.exists(f"{model_artefacts_path}/output"):
            raise ValueError("You must run training before trying to run scoring.")

        try:
            cleanup_artifacts()

            os.makedirs(ARTIFACTS_PATH)

            os.symlink(
                f"../{model_artefacts_path}/output/",
                f"{ARTIFACTS_PATH}/input",
                target_is_directory=True,
            )
            os.symlink(
                "../{}/output/".format(model_artefacts_path),
                f"{ARTIFACTS_PATH}/output",
                target_is_directory=True,
            )

            def execute_score(
                engine,
                context,
                model_dir,
                model_definition,
                model_conf,
                rendered_dataset,
                cli_model_kwargs,
            ):
                if engine == JobRunnerEngine.PYTHON:
                    sys.path.append(model_dir)
                    scoring = importlib.import_module(
                        ".scoring", package="model_modules"
                    )

                    scoring.score(
                        context=context,
                        data_conf=rendered_dataset,
                        model_conf=model_conf,
                        **cli_model_kwargs,
                    )

                elif engine == JobRunnerEngine.SQL:
                    raise ValueError("SQL engine not supported")

                elif engine == JobRunnerEngine.R:
                    self._BaseModel__run_r_model(  # noqa
                        model_id, model_dir, rendered_dataset, "score.batch"
                    )

                else:
                    raise ValueError(
                        f"Unsupported language: {model_definition['language']}"
                    )

            self._execute_model(
                model_definitions_path=model_definitions_path,
                model_id=model_id,
                rendered_dataset=rendered_dataset,
                automation_mode=JobAutomationMode.DEPLOY,
                execute_callback=execute_score,
            )

            cleanup_artifacts()
        except ModuleNotFoundError:
            model_dir = model_definitions_path + BaseModel.get_model_folder(
                model_definitions_path, model_id
            )
            cleanup_artifacts()
            self.logger.error(
                "Missing required python module, try running following command first:"
            )
            self.logger.error(
                f"pip install -r {model_dir}/model_modules/requirements.txt"
            )
            raise
        except:
            cleanup_artifacts()
            self.logger.exception("Exception running model code")
            raise
