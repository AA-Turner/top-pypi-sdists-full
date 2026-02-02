from argparse import Namespace
from collections import defaultdict
import json
from pathlib import Path
from typing import Any, List, Dict, Set, Optional

import attrs
import yaml
from pydantic import BaseModel

from packaging.version import parse as parse_version

from datafold_sdk.cli.dbt_config_validators import ManifestJsonConfig, RunResultsJsonConfig
from datafold_sdk.cli.errors import (
    DataDiffDbtCoreNoRunnerError,
    DataDiffDbtNoSuccessfulModelsInRunError,
    DataDiffDbtRunResultsVersionError,
    DataDiffDbtSelectNoMatchingModelsError,
    DataDiffDbtSelectUnexpectedError,
    DataDiffSimpleSelectNotFound,
)

from datafold_sdk.cli.utils import getLogger
from datafold_sdk import sdk_log

logger = getLogger(__name__)
logger.addHandler(sdk_log.SDKLogHandler())


# getting this dbt_runner will only succeed in dbt-core>=1.5
# it's needed for `--select` functionality
def try_get_dbt_runner():
    try:
        from dbt.cli.main import dbtRunner # pylint: disable=import-outside-toplevel
    except ImportError:
        dbtRunner = None

    if dbtRunner is not None:
        dbt_runner = dbtRunner()
    else:
        dbt_runner = None

    return dbt_runner


def try_set_dbt_flags() -> None:
    try:
        from dbt.flags import set_flags # pylint: disable=import-outside-toplevel
        set_flags(Namespace(MACRO_DEBUGGING=False))
    except: #pylint: disable=bare-except
        pass


RUN_RESULTS_PATH = "target/run_results.json"
MANIFEST_PATH = "target/manifest.json"
PROJECT_FILE = "dbt_project.yml"
PROFILES_FILE = "profiles.yml"
LOWER_DBT_V = "1.0.0"
UPPER_DBT_V = "1.8.0"


# https://github.com/dbt-labs/dbt-core/blob/c952d44ec5c2506995fbad75320acbae49125d3d/core/dbt/cli/resolvers.py#L6
def default_project_dir() -> Path:
    paths = list(Path.cwd().parents)
    paths.insert(0, Path.cwd())
    return next((x for x in paths if (x / PROJECT_FILE).exists()), Path.cwd())


# https://github.com/dbt-labs/dbt-core/blob/c952d44ec5c2506995fbad75320acbae49125d3d/core/dbt/cli/resolvers.py#L12
def default_profiles_dir() -> Path:
    return Path.cwd() if (Path.cwd() / PROFILES_FILE).exists() else Path.home() / ".dbt"


def legacy_profiles_dir() -> Path:
    return Path.home() / ".dbt"


class TDatadiffModelConfig(BaseModel):
    where_filter: Optional[str] = None
    include_columns: List[str] = []
    exclude_columns: List[str] = []


class TDatadiffConfig(BaseModel):
    prod_database: Optional[str] = None
    prod_schema: Optional[str] = None
    prod_custom_schema: Optional[str] = None
    datasource_id: Optional[int] = None


@attrs.define(frozen=False, init=False)
class DbtParser: # pylint: disable=too-many-instance-attributes
    dbt_runner: Optional[Any]  # dbt.cli.main.dbtRunner if installed
    project_dir: Path
    connection: Dict[str, Any]
    project_dict: Dict[str, Any]
    dev_manifest_obj: ManifestJsonConfig
    prod_manifest_obj: Optional[ManifestJsonConfig]
    dbt_user_id: Optional[str]
    dbt_version: str
    dbt_project_id: Optional[str]
    requires_upper: bool
    threads: Optional[int]
    unique_columns: Dict[str, Set[str]]
    profiles_dir: Path

    def __init__(
        self,
        profiles_dir_override: Optional[str] = None,
        project_dir_override: Optional[str] = None,
        state: Optional[str] = None,
    ) -> None:
        super().__init__()

        try_set_dbt_flags()
        self.dbt_runner = try_get_dbt_runner()
        self.project_dir = Path(project_dir_override or default_project_dir())
        self.connection = {}
        self.project_dict = self.get_project_dict()
        self.dev_manifest_obj = self.get_manifest_obj(self.project_dir / MANIFEST_PATH)
        self.prod_manifest_obj = None
        if state:
            self.prod_manifest_obj = self.get_manifest_obj(Path(state))

        self.dbt_user_id = self.dev_manifest_obj.metadata.user_id
        self.dbt_version = self.dev_manifest_obj.metadata.dbt_version
        self.dbt_project_id = self.dev_manifest_obj.metadata.project_id
        self.requires_upper = False
        self.threads = None
        self.unique_columns = self.get_unique_columns()

        if profiles_dir_override:
            self.profiles_dir = Path(profiles_dir_override)
        elif parse_version(self.dbt_version) < parse_version("1.3.0"):
            self.profiles_dir = legacy_profiles_dir()
        else:
            self.profiles_dir = default_profiles_dir()

    def get_datadiff_config(self) -> TDatadiffConfig:
        data_diff_vars = self.project_dict.get("vars", {}).get("data_diff", {})
        prod_database = data_diff_vars.get("prod_database")
        prod_schema = data_diff_vars.get("prod_schema")
        prod_custom_schema = data_diff_vars.get("prod_custom_schema")
        datasource_id = data_diff_vars.get("datasource_id")
        config = TDatadiffConfig(
            prod_database=prod_database,
            prod_schema=prod_schema,
            prod_custom_schema=prod_custom_schema,
            datasource_id=datasource_id,
        )
        logger.info(f"config: {config}")
        return config

    def get_datadiff_model_config(self, model_meta: dict) -> TDatadiffModelConfig:
        where_filter = None
        # include_columns = []
        include_columns: List[str] = []
        exclude_columns: List[str] = []

        if "datafold" in model_meta and "datadiff" in model_meta["datafold"]:
            config = model_meta["datafold"]["datadiff"]
            where_filter = config.get("filter")
            include_columns = config.get("include_columns") or []
            exclude_columns = config.get("exclude_columns") or []

        return TDatadiffModelConfig(
            where_filter=where_filter, include_columns=include_columns, exclude_columns=exclude_columns
        )

    def get_models(self, dbt_selection: Optional[str] = None):
        dbt_version = parse_version(self.dbt_version)
        if dbt_selection:
            if (dbt_version.major, dbt_version.minor) >= (1, 5):
                if self.dbt_runner:
                    return self.get_dbt_selection_models(dbt_selection)
                raise DataDiffDbtCoreNoRunnerError(
                    "datafold-sdk is using a dbt-core version < 1.5, update the environment's dbt-core version via pip install 'dbt-core>=1.5' in order to use `--select`"
                )
                # Naively get node named <dbt_selection>
            logger.warning(
                f"Full `--select` support requires dbt >= 1.5. Naively searching for a single model with name: '{dbt_selection}'."
            )
            return self.get_simple_model_selection(dbt_selection)
        return self.get_run_results_models()

    def get_dbt_selection_models(self, dbt_selection: str) -> List[Optional[ManifestJsonConfig.Nodes]]:
        # log level and format settings needed to prevent dbt from printing to stdout
        # ls command is used to get the list of model unique_ids
        if not self.dbt_runner:
            raise DataDiffDbtCoreNoRunnerError(
                "datafold-sdk is using a dbt-core version < 1.5, update the environment's dbt-core version via pip install 'dbt-core>=1.5' in order to use `--select`"
            )
        results = self.dbt_runner.invoke(
            [
                "--log-format",
                "json",
                "--log-level",
                "none",
                "ls",
                "--select",
                dbt_selection,
                "--resource-type",
                "model",
                "--output",
                "json",
                "--output-keys",
                "unique_id",
                "--project-dir",
                self.project_dir,
            ]
        )
        if results.exception:
            raise results.exception

        if results.success and results.result:
            model_list = [json.loads(model)["unique_id"] for model in results.result]
            models = [self.dev_manifest_obj.nodes.get(x) for x in model_list]
            return models

        if not results.result:
            raise DataDiffDbtSelectNoMatchingModelsError(f"No dbt models found for `--select {dbt_selection}`")

        logger.debug(str(results))
        raise DataDiffDbtSelectUnexpectedError("Encountered an unexpected error while finding `--select` models")

    def get_simple_model_selection(self, dbt_selection: str):
        model_nodes = dict(filter(lambda item: item[0].startswith("model."), self.dev_manifest_obj.nodes.items()))
        model_unique_key_list = [k for k, v in model_nodes.items() if v.name == dbt_selection]

        # name *should* always be unique, but just in case:
        if len(model_unique_key_list) > 1:
            logger.warning(
                f"Found more than one model with name '{dbt_selection}' {model_unique_key_list}, using the first one."
            )
        elif len(model_unique_key_list) < 1:
            raise DataDiffSimpleSelectNotFound(
                f"Did not find a model node with name '{dbt_selection}' in the manifest."
            )

        model = model_nodes.get(model_unique_key_list[0])

        return [model]

    def get_run_results_models(self) -> List[Optional[ManifestJsonConfig.Nodes]]:
        with open(self.project_dir / RUN_RESULTS_PATH, encoding='utf-8') as run_results:
            logger.info(f"Parsing file {RUN_RESULTS_PATH}")
            run_results_dict = json.load(run_results)
        run_results_validated = RunResultsJsonConfig.model_validate(run_results_dict)

        dbt_version = parse_version(run_results_validated.metadata.dbt_version)

        if dbt_version < parse_version(LOWER_DBT_V):
            raise DataDiffDbtRunResultsVersionError(
                f"Found dbt: v{dbt_version} Expected the dbt project's version to be >= {LOWER_DBT_V}"
            )
        if dbt_version >= parse_version(UPPER_DBT_V):
            logger.warning(
                f"{dbt_version} is a recent version of dbt and may not be fully tested with datafold-sdk!"
            )

        success_models = [x.unique_id for x in run_results_validated.results if x.status == x.Status.success]

        models = [self.dev_manifest_obj.nodes.get(x) for x in success_models]
        if not models:
            raise DataDiffDbtNoSuccessfulModelsInRunError(
                "Expected > 0 successful models runs from the last dbt command."
            )

        return models

    def get_manifest_obj(self, path: Path) -> ManifestJsonConfig:
        with open(path, encoding='utf-8') as manifest:
            logger.info(f"Parsing file {path}")
            manifest_dict = json.load(manifest)
            manifest_obj = ManifestJsonConfig.model_validate(manifest_dict)
        return manifest_obj

    def get_project_dict(self):
        with open(self.project_dir / PROJECT_FILE, encoding='utf-8') as project:
            logger.info(f"Parsing file {PROJECT_FILE}")
            project_dict = yaml.safe_load(project)
        return project_dict

    def get_pk_from_model(self, node, unique_columns: dict, pk_tag: str) -> List[str]:
        try:
            # Get a set of all the column names
            column_names = {name for name, params in node.columns.items()}
            # Check if the tag is present on a table level
            if pk_tag in node.meta:
                # Get all the PKs that are also present as a column
                pks = [pk for pk in (node.meta[pk_tag] if not isinstance(pk_tag, bool) else []) if pk in column_names]
                # pks = [pk for pk in pk_tag in node.meta[pk_tag] if pk in column_names]
                if pks:
                    # If there are any left, return it
                    logger.debug("Found PKs via Table META: %s", str(pks))
                    return pks

            from_meta = [name for name, params in node.columns.items() if pk_tag in params.meta] or None
            if from_meta:
                logger.debug(f"Found PKs via META [{node.name}]: %s", str(from_meta))
                return from_meta

            from_tags = [name for name, params in node.columns.items() if pk_tag in params.tags] or None
            if from_tags:
                logger.debug(f"Found PKs via Tags [{node.name}]: %s", str(from_tags))
                return from_tags
            if node.unique_id in unique_columns:
                from_uniq = unique_columns.get(node.unique_id)
                if from_uniq is not None:
                    logger.debug(f"Found PKs via Uniqueness tests [{node.name}]: {str(from_uniq)}")
                    return list(from_uniq)

        except (KeyError, IndexError, TypeError) as e:
            raise e

        logger.debug("Found no PKs")
        return []

    def process_node(self, manifest, node, cols_by_uid) -> None:
        if not (node.resource_type == "test" and hasattr(node, "test_metadata")):
            return

        if not node.depends_on or not node.depends_on.nodes:
            return

        uid = node.depends_on.nodes[0]

        if uid.startswith("source."):
            return

        model_node = manifest.nodes[uid]
        if node.test_metadata:
            if node.test_metadata.name == "unique":
                column_name: str = node.test_metadata.kwargs["column_name"]
                for col in self._parse_concat_pk_definition(column_name):
                    if model_node is None or col in (model_node.columns or {}).keys():
                        cols_by_uid[uid].add(col)

            elif node.test_metadata.name == "unique_combination_of_columns":
                for col in node.test_metadata.kwargs["combination_of_columns"]:
                    cols_by_uid[uid].add(col)


    def get_unique_columns(self) -> Dict[str, Set[str]]:
        manifest = self.dev_manifest_obj
        cols_by_uid: Dict[str, Set] = defaultdict(set)
        for node in manifest.nodes.values():
            try:
                self.process_node(manifest, node, cols_by_uid)
            except (KeyError, IndexError, TypeError) as e:
                logger.warning("Failure while finding unique cols: %s", e)

        return cols_by_uid

    def _parse_concat_pk_definition(self, definition: str) -> List[str]:
        definition = definition.strip()
        if definition.lower().startswith("concat(") and definition.endswith(")"):
            definition = definition[7:-1]  # Removes concat( and )
            columns = definition.split(",")
        else:
            columns = definition.split("||")

        stripped_columns = [col.strip('" ()') for col in columns]
        return stripped_columns

    def set_casing_policy_for(self, connection_type: str):
        """
        Set casing policy for identifiers: database, schema, table, column, etc.
        Correct policy depends on the type of the database, because some databases (e.g. Snowflake)
        use upper case identifiers by default, while others (e.g. Postgres) use lower case.
        """
        self.requires_upper = connection_type == "snowflake"
