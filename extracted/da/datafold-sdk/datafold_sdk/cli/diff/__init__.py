import json
import os
import re
import concurrent
import time
import logging
from contextlib import nullcontext
from copy import deepcopy

from concurrent.futures import ThreadPoolExecutor, as_completed, CancelledError, BrokenExecutor
from typing import List, Optional, Dict, Tuple, Union
import keyring
import click
import pydantic
import rich
from rich.logging import RichHandler
from rich.prompt import Prompt
from rich.markdown import Markdown
from datafold_sdk.version import __version__
from datafold_sdk.cli.errors import (
    DataDiffCustomSchemaNoConfigError,
    DataDiffDbtProjectVarsNotFoundError,
    DataDiffNoDatasourceIdError,
)
from datafold_sdk.cli.cloud import DatafoldAPI, TCloudApiDataDiff, TCloudApiOrgMeta
from datafold_sdk.cli.dbt_parser import DbtParser, TDatadiffConfig
from datafold_sdk.cli.format import jsonify_error
from datafold_sdk.cli.config import apply_config_from_file

from datafold_sdk.cli.utils import (
    dbt_diff_string_template,
    getLogger,
    columns_added_template,
    columns_removed_template,
    no_differences_template,
    columns_type_changed_template,
    remove_password_from_url,
    run_as_daemon,
    truncate_error,
    print_version_info,
    LogStatusHandler,
)

from datafold_sdk import sdk_log

logger = logging.getLogger(__file__)
logger.addHandler(sdk_log.SDKLogHandler())

CLOUD_DOC_URL = "https://docs.datafold.com/development_testing/cloud"
DATAFOLD_TRIAL_URL = "https://app.datafold.com/org-signup"
DATAFOLD_INSTRUCTIONS_URL = "https://docs.datafold.com/development_testing/datafold_cloud"


class TDiffVars(pydantic.BaseModel):
    dev_path: List[str]
    prod_path: List[str]
    primary_keys: List[str]
    connection: Dict[str, Optional[str]]
    threads: Optional[int] = None
    where_filter: Optional[str] = None
    include_columns: List[str]
    exclude_columns: List[str]
    dbt_model: Optional[str] = None
    stats_flag: bool = False

def _get_log_handlers(is_dbt: Optional[bool] = False) -> Dict[str, logging.Handler]:
    handlers = {}
    date_format = "%H:%M:%S"
    log_format_rich = "%(message)s"

    # limits to 100 characters arbitrarily
    log_format_status = "%(message).100s"
    rich_handler = RichHandler(rich_tracebacks=True)
    rich_handler.setFormatter(logging.Formatter(log_format_rich, datefmt=date_format))
    rich_handler.setLevel(logging.WARN)
    handlers["rich_handler"] = rich_handler

    # only use log_status_handler in an interactive terminal session
    if rich_handler.console.is_interactive and is_dbt:
        log_status_handler = LogStatusHandler()
        log_status_handler.setFormatter(logging.Formatter(log_format_status, datefmt=date_format))
        log_status_handler.setLevel(logging.DEBUG)
        handlers["log_status_handler"] = log_status_handler

    return handlers

def _remove_passwords_in_dict(d: dict) -> None:
    for k, v in d.items():
        if k == "password":
            d[k] = "*" * len(v)
        elif k == "filepath":
            if "motherduck_token=" in v:
                d[k] = v.split("motherduck_token=")[0] + "motherduck_token=**********"
        elif isinstance(v, dict):
            _remove_passwords_in_dict(v)
        elif k.startswith("database"):
            d[k] = remove_password_from_url(v)

@click.group()
@click.pass_context
def manager(ctx):
    """Run datafold diff dbt --help for dbt development diffing."""

@manager.command(no_args_is_help=False)
@click.option("--version", is_flag=True, help="Print version info and exit")
@click.option(
    "-w",
    "--where",
    default=None,
    help="An additional 'where' expression to restrict the search space. Beware of SQL Injection!",
    metavar="EXPR",
)

@click.option(
    "--dbt-profiles-dir",
    envvar="DBT_PROFILES_DIR",
    default=None,
    metavar="PATH",
    help="Which directory to look in for the profiles.yml file. If not set, we follow the default profiles.yml location for the dbt version being used. Can also be set via the DBT_PROFILES_DIR environment variable.",
)
@click.option(
    "--dbt-project-dir",
    default=None,
    metavar="PATH",
    help="Which directory to look in for the dbt_project.yml file. Default is the current working directory and its parents.",
)
@click.option(
    "--select",
    default=None,
    metavar="SELECTION or MODEL_NAME",
    help="--select dbt resources to compare using dbt selection syntax in dbt versions >= 1.5.\nIn versions < 1.5, it will naively search for a model with MODEL_NAME as the name.",
)
@click.option(
    "--state",
    default=None,
    metavar="PATH",
    help="Specify manifest to utilize for 'prod' comparison paths instead of using configuration.",
)
@click.option(
    "-pd",
    "--prod-database",
    "prod_database",
    default=None,
    help="Override the dbt production database configuration within dbt_project.yml",
)
@click.option(
    "-ps",
    "--prod-schema",
    "prod_schema",
    default=None,
    help="Override the dbt production schema configuration within dbt_project.yml",
)
@click.pass_context
def dbt(ctx, **kw):
    log_handlers = _get_log_handlers()

    if kw["version"]:
        print(f"v{__version__}")
        return

    log_handlers["rich_handler"].setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG, handlers=list(log_handlers.values()))

    try:
        state = kw.pop("state", None)
        if state:
            state = os.path.expanduser(state)
        profiles_dir_override = kw.pop("dbt_profiles_dir", None)
        if profiles_dir_override:
            profiles_dir_override = os.path.expanduser(profiles_dir_override)
        project_dir_override = kw.pop("dbt_project_dir", None)
        if project_dir_override:
            project_dir_override = os.path.expanduser(project_dir_override)

        dbt_diff(
            api_key=ctx.obj.api_key,
            host_name=ctx.obj.host,
            log_status_handler=log_handlers.get("log_status_handler"),
            profiles_dir_override=profiles_dir_override,
            project_dir_override=project_dir_override,
            dbt_selection=kw["select"],
            state=state,
            where_flag=kw["where"],
            production_database_flag=kw["prod_database"],
            production_schema_flag=kw["prod_schema"],
        )
    except Exception as e:
        logging.error(e)
        raise

def dbt_diff(
    api_key: str,
    host_name: str,
    profiles_dir_override: Optional[str] = None,
    project_dir_override: Optional[str] = None,
    dbt_selection: Optional[str] = None,
    json_output: bool = False,
    state: Optional[str] = None,
    log_status_handler: Optional[LogStatusHandler] = None,
    where_flag: Optional[str] = None,
    stats_flag: bool = False,
    columns_flag: Optional[Tuple[str]] = None,
    production_database_flag: Optional[str] = None,
    production_schema_flag: Optional[str] = None,
) -> None:
    api = None
    print_version_info()
    dbt_parser = DbtParser(profiles_dir_override, project_dir_override, state)
    models = dbt_parser.get_models(dbt_selection)
    config = dbt_parser.get_datadiff_config()

    if not state and not (config.prod_database or config.prod_schema):
        doc_url = "https://docs.datafold.com/development_testing/open_source#configure-your-dbt-project"
        raise DataDiffDbtProjectVarsNotFoundError(
            f"""vars: data_diff: section not found in dbt_project.yml.\n\nTo solve this, please configure your dbt project: \n{doc_url}\n\nOr specify a production manifest using the `--state` flag."""
        )

    if isinstance(api_key, str) and isinstance(host_name, str):
        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        }
        api = DatafoldAPI(api_key=api_key, host=host_name, headers=headers, timeout=30)
    if not api:
        return
    org_meta = api.get_org_meta()
    if config.datasource_id is None:
        rich.print("[red]Data source ID not found in dbt_project.yml")
        raise DataDiffNoDatasourceIdError(
            f"Datasource ID not found. Please include it as a dbt variable in the dbt_project.yml. \nInstructions: {CLOUD_DOC_URL}\n\nvars:\n data_diff:\n   datasource_id: 1234"
        )

    data_source = api.get_data_source(config.datasource_id)
    dbt_parser.set_casing_policy_for(connection_type=data_source.type)
    rich.print("[green][bold]\nDiffs in progress...[/][/]\n")

    futures = {}

    with log_status_handler.status if log_status_handler else nullcontext(), ThreadPoolExecutor(
        max_workers=dbt_parser.threads
    ) as executor:
        for model in models:
            if log_status_handler:
                log_status_handler.set_prefix(f"Diffing {model.alias} \n")

            diff_vars = _get_diff_vars(
                dbt_parser,
                config,
                model,
                where_flag,
                stats_flag,
                columns_flag,
                production_database_flag,
                production_schema_flag,
            )

            # we won't always have a prod path when using state
            # when the model DNE in prod manifest, skip the model diff
            if (
                state and len(diff_vars.prod_path) < 2
            ):  # < 2 because some providers like databricks can legitimately have *only* 2
                diff_output_str = _diff_output_base(".".join(diff_vars.dev_path), ".".join(diff_vars.prod_path))
                diff_output_str += "[green]New model: nothing to diff![/] \n"
                rich.print(diff_output_str)
                continue

            if diff_vars.primary_keys:
                future = executor.submit(
                    _cloud_diff, diff_vars, config.datasource_id, api, org_meta, log_status_handler
                )
                futures[future] = model
            else:
                if json_output:
                    print(
                        json.dumps(
                            jsonify_error(
                                table1=diff_vars.prod_path,
                                table2=diff_vars.dev_path,
                                dbt_model=diff_vars.dbt_model,
                                error="No primary key found. Add uniqueness tests, meta, or tags.",
                            )
                        ),
                        flush=True,
                    )
                else:
                    rich.print(
                        _diff_output_base(".".join(diff_vars.dev_path), ".".join(diff_vars.prod_path))
                        + "Skipped due to unknown primary key. Add uniqueness tests, meta, or tags.\n"
                    )

    for future in as_completed(futures):
        model = futures[future]
        try:
            future.result()  # if error occurred, it will be raised here
        except (concurrent.futures.TimeoutError, BrokenExecutor, CancelledError, RuntimeError) as e:
            logger.error(f"An error occurred during the execution of a diff task: {model.unique_id} - {e}")

def _get_diff_vars(
    dbt_parser: "DbtParser",
    config: TDatadiffConfig,
    model,
    where_flag: Optional[str] = None,
    stats_flag: bool = False,
    columns_flag: Optional[Tuple[str]] = None,
    production_database_flag: Optional[str] = None,
    production_schema_flag: Optional[str] = None,
) -> TDiffVars:
    cli_columns = list(columns_flag) if columns_flag else []
    dev_database = model.database
    dev_schema = model.schema_
    dev_alias = prod_alias = model.alias
    primary_keys = dbt_parser.get_pk_from_model(model, dbt_parser.unique_columns, "primary-key")

    # prod path is constructed via configuration or the prod manifest via --state
    if dbt_parser.prod_manifest_obj:
        prod_database, prod_schema, prod_alias = _get_prod_path_from_manifest(model, dbt_parser.prod_manifest_obj)
    else:
        prod_database, prod_schema = _get_prod_path_from_config(config, model, dev_database, dev_schema)

    # cli flags take precedence over any project level config
    prod_database = production_database_flag or prod_database
    prod_schema = production_schema_flag or prod_schema

    if dbt_parser.requires_upper:
        dev_qualified_list = [x.upper() for x in [dev_database, dev_schema, dev_alias] if x]
        prod_qualified_list = [x.upper() for x in [prod_database, prod_schema, prod_alias] if x]
        primary_keys = [x.upper() for x in primary_keys]
    else:
        dev_qualified_list = [x for x in [dev_database, dev_schema, dev_alias] if x]
        prod_qualified_list = [x for x in [prod_database, prod_schema, prod_alias] if x]

    datadiff_model_config = dbt_parser.get_datadiff_model_config(model.meta)

    return TDiffVars(
        dbt_model=model.unique_id,
        dev_path=dev_qualified_list,
        prod_path=prod_qualified_list,
        primary_keys=primary_keys,
        connection=dbt_parser.connection,
        threads=dbt_parser.threads,
        # cli flags take precedence over any model level config
        where_filter=where_flag or datadiff_model_config.where_filter,
        include_columns=cli_columns or datadiff_model_config.include_columns,
        exclude_columns=[] if cli_columns else datadiff_model_config.exclude_columns,
        stats_flag=stats_flag,
    )


def _get_prod_path_from_config(config, model, dev_database, dev_schema) -> Tuple[str, str]:
    # "custom" dbt config database
    if model.config.database:
        prod_database = model.config.database
    elif config.prod_database:
        prod_database = config.prod_database
    else:
        prod_database = dev_database

    # prod schema name differs from dev schema name
    if config.prod_schema:
        custom_schema = model.config.schema_

        # the model has a custom schema config(schema='some_schema')
        if custom_schema:
            if not config.prod_custom_schema:
                raise DataDiffCustomSchemaNoConfigError(
                    f"Found a custom schema on model {model.name}, but no value for\nvars:\n  data_diff:\n    prod_custom_schema:\nPlease set a value or utilize the `--state` flag!\n\n"
                    + "For more details see: https://docs.datafold.com/development_testing/open_source"
                )
            prod_schema = config.prod_custom_schema.replace("<custom_schema>", custom_schema)
            # no custom schema, use the default
        else:
            prod_schema = config.prod_schema
    else:
        prod_schema = dev_schema
    return prod_database, prod_schema

def _get_prod_path_from_manifest(model, prod_manifest) -> Union[Tuple[str, str, str], Tuple[None, None, None]]:
    prod_database = None
    prod_schema = None
    prod_alias = None
    prod_model = prod_manifest.nodes.get(model.unique_id, None)
    if prod_model:
        prod_database = prod_model.database
        prod_schema = prod_model.schema_
        prod_alias = prod_model.alias
    return prod_database, prod_schema, prod_alias

# pylint: disable=too-many-branches,too-many-statements
def _cloud_diff(
    diff_vars: TDiffVars,
    datasource_id: int,
    api: DatafoldAPI,
    org_meta: TCloudApiOrgMeta,
    log_status_handler: Optional[LogStatusHandler] = None,
) -> None:
    if log_status_handler:
        log_status_handler.diff_started(diff_vars.dev_path[-1])
    diff_output_str = _diff_output_base(".".join(diff_vars.dev_path), ".".join(diff_vars.prod_path))
    payload = TCloudApiDataDiff(
        data_source1_id=datasource_id,
        data_source2_id=datasource_id,
        table1=diff_vars.prod_path,
        table2=diff_vars.dev_path,
        pk_columns=diff_vars.primary_keys,
        filter1=diff_vars.where_filter,
        filter2=diff_vars.where_filter,
        include_columns=diff_vars.include_columns,
        exclude_columns=diff_vars.exclude_columns,
    )

    error = None
    diff_id = None
    diff_url = None
    try:
        diff_id = api.create_data_diff(payload=payload)
        diff_url = f"{api.host}/datadiffs/{diff_id}/overview"
        rich.print(f"{diff_vars.dev_path[-1]}: {diff_url}")

        if diff_id is None:
            raise ValueError("API response did not contain a diff_id")

        diff_results = api.poll_data_diff_results(diff_id)

        rows_added_count = diff_results.pks.exclusives[1]
        rows_removed_count = diff_results.pks.exclusives[0]

        rows_updated = diff_results.values.rows_with_differences
        total_rows_table1 = diff_results.pks.total_rows[0]
        total_rows_table2 = diff_results.pks.total_rows[1]
        total_rows_diff = total_rows_table2 - total_rows_table1

        rows_unchanged = int(total_rows_table1) - int(rows_updated) - int(rows_removed_count)
        diff_percent_list = {
            x.column_name: f"{str(round(100.00 - x.match, 2))}%"
            for x in diff_results.values.columns_diff_stats
            if x.match != 100.0
        }
        columns_added = set(diff_results.schema_.exclusive_columns[1])
        columns_removed = set(diff_results.schema_.exclusive_columns[0])
        column_type_changes = diff_results.schema_.column_type_differs

        diff_output_str += f"Primary Keys: {diff_vars.primary_keys} \n"
        if diff_vars.where_filter:
            diff_output_str += f"Where Filter: '{str(diff_vars.where_filter)}' \n"

        if diff_vars.include_columns:
            diff_output_str += f"Included Columns: {diff_vars.include_columns} \n"

        if diff_vars.exclude_columns:
            diff_output_str += f"Excluded Columns: {diff_vars.exclude_columns} \n"

        if columns_removed:
            diff_output_str += columns_removed_template(columns_removed)

        if columns_added:
            diff_output_str += columns_added_template(columns_added)

        if column_type_changes:
            diff_output_str += columns_type_changed_template(column_type_changes)

        deps_impacts = {
            item["data_source_type"]: sum(1 for d in diff_results.deps.deps if d["data_source_type"] == item["data_source_type"])
            for item in diff_results.deps.deps
        }

        if any([rows_added_count, rows_removed_count, rows_updated]):
            diff_output = dbt_diff_string_template(
                total_rows_table1=total_rows_table1,
                total_rows_table2=total_rows_table2,
                total_rows_diff=total_rows_diff,
                rows_added=rows_added_count,
                rows_removed=rows_removed_count,
                rows_updated=rows_updated,
                rows_unchanged=str(rows_unchanged),
                deps_impacts=deps_impacts,
                is_cloud=True,
                extra_info_dict=diff_percent_list,
                extra_info_str="Value Changed:",
            )
            diff_output_str += f"\n{diff_url}\n {diff_output} \n"
            rich.print(diff_output_str)
        else:
            diff_output_str += f"\n{diff_url}\n{no_differences_template()}\n"
            rich.print(diff_output_str)

        if log_status_handler:
            log_status_handler.diff_finished(diff_vars.dev_path[-1])
    except BaseException as ex:  # pylint: disable=broad-exception-caught
        error = ex
    finally:
        if error:
            rich.print(diff_output_str)
            if diff_id:
                diff_url = f"{api.host}/datadiffs/{diff_id}/overview"
                rich.print(f"{diff_url} \n")
            logger.error(error)


def _diff_output_base(dev_path: str, prod_path: str) -> str:
    return f"\n[blue]{prod_path}[/] <> [green]{dev_path}[/] \n"
