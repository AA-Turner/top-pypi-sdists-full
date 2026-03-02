import json
import logging
import os
from typing import Any, Callable

import yaml
from jinja2 import Template

MODEL_JSON_FILE = "/model.json"


class BaseModel(object):

    def __init__(self, repo_manager):
        self.repo_manager = repo_manager

    @staticmethod
    def get_model_ids(model_path: str, rtn_val=False) -> dict:
        catalog = {}
        index = 0
        model_ids = "Use one of the following models\n"

        for model_folder in os.listdir(model_path):
            if os.path.exists(model_path + model_folder + MODEL_JSON_FILE):
                with open(model_path + model_folder + MODEL_JSON_FILE, "r") as f:
                    model_definition = json.load(f)
                    catalog[index] = model_definition
                    index += 1

        for key in catalog:
            model_ids += "{1}: {0}\n".format(catalog[key]["id"], catalog[key]["name"])

        if rtn_val:
            return catalog

        raise ValueError(model_ids)

    @staticmethod
    def get_model_folders(model_path: str, rtn_val=False) -> dict:
        catalog = {}
        index = 0
        model_ids = "Use one of the following models\n"
        model_folder = None

        for model_folder in os.listdir(model_path):
            if os.path.exists(model_path + model_folder + MODEL_JSON_FILE):
                with open(model_path + model_folder + MODEL_JSON_FILE, "r") as f:
                    model_definition = json.load(f)
                    catalog[index] = model_definition
                    index += 1

        for key in catalog:
            model_ids += "{1}: {0}\n".format(model_folder, catalog[key]["name"])

        if rtn_val:
            return catalog

        raise ValueError(model_ids)

    @staticmethod
    def get_model_folder(model_path: str, model_id: str) -> str:
        for model_folder in os.listdir(model_path):
            if os.path.exists(model_path + model_folder + MODEL_JSON_FILE):
                with open(model_path + model_folder + MODEL_JSON_FILE, "r") as f:
                    model_definition = json.load(f)
                    if model_definition["id"] == model_id:
                        return model_folder

        raise ValueError("Could not find model path for model_id: {}".format(model_id))

    def __get_model_varargs(self, model_id: str) -> dict[str, str]:  # noqa #NOSONAR
        return {
            "model_id": model_id,
            "model_version": "cli",
            "model_table": "vmo_models_cli",
            "project_id": self.__get_project_id(),
            "job_id": "cli",
        }

    def __get_project_id(self) -> str:
        self.repo_manager.repo_config_rename(self.repo_manager.base_path)
        path = os.path.join(self.repo_manager.base_path, ".tmo/config.yaml")
        with open(path, "r") as handle:
            return yaml.safe_load(handle)["project_id"]

    @staticmethod
    def __template_sql_script(filename: str, jinja_ctx: Any) -> str:
        with open(filename) as f:
            template = Template(f.read(), autoescape=True)

        return template.render(jinja_ctx)

    def __execute_sql_script(self, filename: str, jinja_ctx: Any):  # noqa #NOSONAR
        from ..util.connections import execute_sql

        script = self.__template_sql_script(filename, jinja_ctx)

        stms = script.split(";")

        for stm in stms:
            stm = stm.strip()
            if stm:
                logging.info("Executing statement: {}".format(stm))

                try:
                    execute_sql(stm)
                except Exception as e:
                    if stm.startswith("DROP"):
                        logging.warning("Ignoring DROP statement exception")
                    else:
                        raise e

    @staticmethod
    def __get_engine(  # noqa #NOSONAR
        model_definition: dict[str, Any], mode: str
    ) -> dict:
        if "automation" in model_definition:

            if (
                mode in model_definition["automation"]
                and "engine" in model_definition["automation"][mode]
            ):
                return model_definition["automation"][mode]["engine"]

            # legacy
            if "trainingEngine" in model_definition["automation"]:
                return model_definition["automation"]["trainingEngine"]

        return model_definition["language"]

    def __run_r_model(  # noqa #NOSONAR
        self, model_id: str, model_dir: str, data_conf: dict, mode: str
    ):
        import tempfile
        import subprocess

        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(json.dumps(data_conf).encode())

        pkg_path, _ = os.path.split(__file__)
        cmd = (
            f"{pkg_path}/run_model.R"
            f" {model_id} {self.__get_project_id()} {mode} {fp.name} {model_dir}"
        )
        subprocess.check_call(cmd, shell=True)

    def _execute_model(  # noqa
        self,
        model_definitions_path: str,
        model_id: str,
        rendered_dataset: dict,
        automation_mode: str,
        execute_callback: Callable,
    ):
        """
        Método común para ejecutar modelos (score, evaluate, etc).

        Args:
            model_definitions_path: Ruta al directorio de definiciones de modelos
            model_id: ID del modelo
            rendered_dataset: Dataset renderizado
            automation_mode: Modo de automatización (DEPLOY, EVALUATE, etc)
            execute_callback: Función callback que ejecuta la lógica específica.
                             Recibe (engine, context, model_dir, model_definition,
                                     model_conf, rendered_dataset, cli_model_kwargs)
        """
        from tmo.context.model_context import ModelContext, DatasetInfo
        from tmo.types.job import JobRunnerEngine

        model_dir = model_definitions_path + BaseModel.get_model_folder(
            model_definitions_path, model_id
        )

        with open(f"{model_dir}/model.json", "r") as f:
            model_definition = json.load(f)

        with open(f"{model_dir}/config.json", "r") as f:
            model_conf = json.load(f)

        logging.getLogger(__name__).info("Loading and executing model code")

        cli_model_kwargs = self.__get_model_varargs(model_id)

        context = ModelContext(
            dataset_info=DatasetInfo.from_dict(rendered_dataset),
            hyperparams=model_conf["hyperParameters"],
            artifact_input_path="artifacts/input",
            artifact_output_path="artifacts/output",
            **cli_model_kwargs,
        )

        engine = JobRunnerEngine(self.__get_engine(model_definition, automation_mode))

        execute_callback(
            engine=engine,
            context=context,
            model_dir=model_dir,
            model_definition=model_definition,
            model_conf=model_conf,
            rendered_dataset=rendered_dataset,
            cli_model_kwargs=cli_model_kwargs,
        )
