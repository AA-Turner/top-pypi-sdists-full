import json
import logging
import os
import shutil
from pathlib import Path

import yaml
from git import Repo

from tmo.types.entity import EntityType
from .evaluate_model import EvaluateModel
from .score_model import ScoreModel
from .train_model import TrainModel

MODEL_JSON = "model.json"
FEATURE_ENGINEERING_PATH = "feature_engineering_tasks"
MODEL_DEFINITIONS_PATH = "model_definitions"


class RepoManager(object):

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.logger = logging.getLogger(__name__)

    def add_model(
        self,
        model_id: str,
        model_name: str,
        model_desc: str,
        template: str,
        base_path: str = None,
    ):

        base_path = self.base_path if base_path is None else base_path
        model_path = os.path.join(base_path, MODEL_DEFINITIONS_PATH)

        if not os.path.isdir(model_path):
            try:
                os.makedirs(model_path)
            except Exception as e:
                raise IOError(f"Could not create models directory {model_path}: {e}")

        with open(os.path.join(template, MODEL_JSON), "r") as f:
            model = json.load(f)
            model["source_model_id"] = model["id"]
            model["id"] = model_id
            model["name"] = model_name
            model["description"] = model_desc

            name_path = model_name.strip().lower().replace(" ", "_")

            target_path = os.path.join(model_path, name_path)
            if os.path.isdir(target_path):
                raise ValueError(
                    f"Model path {name_path} already exists, please try another model"
                    " name"
                )

            try:
                shutil.copytree(template, target_path)
            except Exception as e:
                raise IOError(f"Could not copy model template to {target_path}: {e}")

            with open(os.path.join(target_path, MODEL_JSON), "w") as t:
                json.dump(model, t, indent=4)

    def add_task(self, template: str, task_name: str, base_path: str = None):

        base_path = self.base_path if base_path is None else base_path
        task_path = os.path.join(base_path, FEATURE_ENGINEERING_PATH)

        if not os.path.exists(task_path):
            try:
                os.makedirs(task_path)
            except Exception as e:
                raise IOError(
                    "Could not create feature engineering tasks directory"
                    f" {task_path}: {e}"
                )

        name_path = task_name.strip().lower().replace(" ", "_")

        target_path = os.path.join(task_path, name_path)
        if os.path.isdir(target_path):
            raise ValueError(
                f"Task path {name_path} already exists, please try another task name"
            )

        try:
            shutil.copytree(template, target_path)
        except Exception as e:
            raise IOError(f"Could not copy model template to {target_path}: {e}")

    def get_templates(
        self, entity_type: EntityType = EntityType.MODEL, source_path: str = None
    ) -> dict:

        source_path = (
            self.base_path if source_path is None else os.path.join(source_path, "")
        )
        templates_path = os.path.join(
            source_path,
            (
                MODEL_DEFINITIONS_PATH
                if entity_type == EntityType.MODEL
                else FEATURE_ENGINEERING_PATH
            ),
        )
        templates = {}

        if not os.path.isdir(templates_path):
            return templates

        if entity_type == EntityType.MODEL:
            templates = RepoManager._get_models_from_repo(templates_path)
        elif entity_type == EntityType.FEATURE_ENGINEERING_TASK:
            templates = RepoManager._get_tasks_from_repo(templates_path)

        return templates

    def init_model_directory(self, path: str = None):
        logging.info("Creating model directory")
        if path is None:
            path = os.path.join(os.path.abspath(os.getcwd()), "")

        self.logger.info("Creating model definitions")

        src = os.path.join(os.path.split(__file__)[0], "") + "metadata_files"
        src_folders = os.listdir(src)
        for folder in src_folders:
            full_folder_name = os.path.join(src, folder)
            if os.path.isfile(full_folder_name) and not os.path.exists(
                os.path.join(path, folder)
            ):
                shutil.copy(full_folder_name, path)

        Path(f"{path}{MODEL_DEFINITIONS_PATH}/").mkdir(parents=True, exist_ok=True)

        self.logger.info(f"model directory initialized at {path}")

        logging.info("Creating feature engineering tasks directory")
        Path(f"{path}{FEATURE_ENGINEERING_PATH}/").mkdir(parents=True, exist_ok=True)

        self.logger.info(f"feature engineering tasks directory initialized at {path}")

    def read_repo_config(self):
        self.repo_config_rename()
        path = os.path.join(self.base_path, ".tmo/config.yaml")
        if os.path.exists(path):
            with open(path, "r") as handle:
                return yaml.safe_load(handle)

        self.logger.warning("ModelOps repo config doesn't exist")
        return None

    def write_repo_config(self, config, path=None):
        path = path if path else self.base_path
        config_dir = os.path.join(path, ".tmo")
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        config_file = f"{config_dir}/config.yaml"

        with open(config_file, "w+") as f:
            yaml.dump(config, f, default_flow_style=False)

    def repo_config_exists(self, repo_path=None):
        path = repo_path if repo_path else self.base_path
        return Path(os.path.join(path, ".tmo")).is_file()

    def repo_config_rename(self, repo_path=None):
        path = repo_path if repo_path else self.base_path
        if Path(os.path.join(path, ".aoa")).is_file():
            os.rename(os.path.join(path, ".aoa"), os.path.join(path, ".tmo"))

    def train(self, model_id: str, data_conf: dict):
        trainer = TrainModel(self)
        trainer.train_model_local(
            model_id=model_id, rendered_dataset=data_conf, base_path=self.base_path
        )

    def evaluate(self, model_id: str, data_conf: dict):
        evaluator = EvaluateModel(self)
        evaluator.evaluate_model_local(
            model_id=model_id, rendered_dataset=data_conf, base_path=self.base_path
        )

    def batch_score_model_local(self, model_id: str, data_conf: dict):
        scorer = ScoreModel(self)
        scorer.batch_score_model_local(
            model_id=model_id, rendered_dataset=data_conf, base_path=self.base_path
        )

    @staticmethod
    def clone_repository(url, path, branch: str = "master"):
        repo = Repo.clone_from(url, path)
        repo.git.checkout(branch)

    @staticmethod
    def get_model_definitions_path() -> str:
        return MODEL_DEFINITIONS_PATH

    @staticmethod
    def get_feature_engineering_path() -> str:
        return FEATURE_ENGINEERING_PATH

    @staticmethod
    def _get_models_from_repo(templates_path: str = None) -> dict:
        if not os.path.isdir(templates_path):
            return {}

        models = {}

        for entity in sorted(os.listdir(templates_path)):
            if os.path.isfile(os.path.join(templates_path, entity)):
                continue

            model_metadata_dir = os.path.join(templates_path, entity)
            model_metadata_file = os.path.join(model_metadata_dir, MODEL_JSON)
            if os.path.isfile(model_metadata_file):
                with open(model_metadata_file, "r") as f:
                    model_metadata = json.load(f)
                    if model_metadata["language"] not in models:
                        models[model_metadata["language"]] = {}
                    models[model_metadata["language"]][model_metadata["id"]] = [
                        model_metadata["name"],
                        model_metadata_dir,
                    ]

        return models

    @staticmethod
    def _get_tasks_from_repo(templates_path: str = None) -> dict:
        if not os.path.isdir(templates_path):
            return {}

        tasks = {}

        for entity in sorted(os.listdir(templates_path)):
            from tmo.util.utils import get_files_in_path

            if os.path.isfile(os.path.join(templates_path, entity)):
                continue

            required_files = ["task.py", "requirements.txt"]
            task_dir = os.path.join(templates_path, entity)
            existing_files = get_files_in_path(task_dir)
            if set(required_files) == set(existing_files):
                tasks[entity] = task_dir

        return tasks
