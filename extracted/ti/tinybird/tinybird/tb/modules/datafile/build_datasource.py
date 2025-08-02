import os
from copy import deepcopy
from dataclasses import asdict
from typing import Any, Dict, List, Optional

import click

from tinybird.datafile.common import PREVIEW_CONNECTOR_SERVICES, ImportReplacements
from tinybird.tb.client import DoesNotExistException, TinyB
from tinybird.tb.modules.feedback_manager import FeedbackManager


def new_ds(
    ds: Dict[str, Any],
    client: TinyB,
    user_token: Optional[str],
    force: bool = False,
    skip_confirmation: bool = False,
    current_ws=None,
    local_ws=None,
    fork_downstream: Optional[bool] = False,
    fork: Optional[bool] = False,
    build: Optional[bool] = False,
    is_vendor: Optional[bool] = False,
):
    ds_name = ds["params"]["name"]

    def manage_tokens():
        # search for token with specified name and adds it if not found or adds permissions to it
        t = None
        for tk in ds["tokens"]:
            token_name = tk["token_name"]
            t = client.get_token_by_name(token_name)
            if not t:
                token_name = tk["token_name"]
                # DS == token_origin.Origins.DATASOURCE
                client.create_token(token_name, [f"DATASOURCES:{tk['permissions']}:{ds_name}"], "DS", ds_name)
            else:
                scopes = [f"DATASOURCES:{tk['permissions']}:{ds_name}"]
                for x in t["scopes"]:
                    sc = x["type"] if "resource" not in x else f"{x['type']}:{x['resource']}"
                    scopes.append(sc)
                client.alter_tokens(token_name, scopes)

    datasource_exists = False
    try:
        existing_ds = client.get_datasource(ds_name)
        datasource_exists = True
    except DoesNotExistException:
        datasource_exists = False

    engine_param = ds["params"].get("engine", "")

    if (
        ds["params"].get("service") == "dynamodb"
        and engine_param != ""
        and engine_param.lower() != "replacingmergetree"
    ):
        raise click.ClickException(FeedbackManager.error_dynamodb_engine_not_supported(engine=engine_param))

    if engine_param.lower() == "join":
        deprecation_notice = FeedbackManager.warning_deprecated(
            warning="Data sources with Join engine are deprecated and will be removed in the next major release of tinybird-cli. Use MergeTree instead."
        )
        click.echo(deprecation_notice)

    if not datasource_exists or fork_downstream or fork:
        params = ds["params"]

        try:
            if (
                params.get("service") in PREVIEW_CONNECTOR_SERVICES
                and params.get("connector")
                and params.get("bucket_uri")
            ):
                bucket_uri = params.get("bucket_uri")
                extension = bucket_uri.split(".")[-1]
                if extension == "gz":
                    extension = bucket_uri.split(".")[-2]
                valid_formats = ["csv", "json", "jsonl", "ndjson", "parquet"]
                if extension not in valid_formats:
                    raise Exception(FeedbackManager.error_format(extension=extension, valid_formats=valid_formats))
                params["format"] = extension
            datasource_response = client.datasource_create_from_definition(params)
            datasource = datasource_response.get("datasource", {})

            if datasource.get("service") == "dynamodb":
                job_id = datasource_response.get("import_id", None)
                if job_id:
                    jobs = client.jobs(status=("waiting", "working"))
                    job_url = next((job["job_url"] for job in jobs if job["id"] == job_id), None)
                    if job_url:
                        click.echo(FeedbackManager.success_dynamodb_initial_load(job_url=job_url))

            if ds.get("tokens"):
                manage_tokens()

            if ds.get("shared_with") and not build:
                if not user_token:
                    click.echo(FeedbackManager.info_skipping_shared_with_entry())
                else:
                    share_and_unshare_datasource(
                        client,
                        datasource,
                        user_token,
                        workspaces_current_shared_with=[],
                        workspaces_to_share=ds["shared_with"],
                        current_ws=current_ws,
                    )
            if is_vendor and user_token and local_ws and current_ws:
                user_client: TinyB = deepcopy(client)
                user_client.token = user_token
                user_client.datasource_share(
                    datasource_id=datasource.get("id", ""),
                    current_workspace_id=current_ws.get("id", ""),
                    destination_workspace_id=local_ws.get("id", ""),
                )

        except Exception as e:
            raise click.ClickException(FeedbackManager.error_creating_datasource(error=str(e)))
        return

    if not force:
        raise click.ClickException(FeedbackManager.error_datasource_already_exists(datasource=ds_name))

    if ds.get("shared_with", []) or existing_ds.get("shared_with", []):
        if not user_token:
            click.echo(FeedbackManager.info_skipping_shared_with_entry())
        else:
            share_and_unshare_datasource(
                client,
                existing_ds,
                user_token,
                existing_ds.get("shared_with", []),
                ds.get("shared_with", []),
                current_ws,
            )

    alter_response = None
    alter_error_message = None
    new_description = None
    new_schema = None
    new_indices = None
    new_ttl = None

    try:
        if datasource_exists and ds["params"]["description"] != existing_ds["description"]:
            new_description = ds["params"]["description"]

        if datasource_exists and ds["params"].get("engine_ttl") != existing_ds["engine"].get("ttl"):
            new_ttl = ds["params"].get("engine_ttl", "false")

        # Schema fixed by the kafka connector
        if datasource_exists and (
            ds["params"]["schema"].replace(" ", "") != existing_ds["schema"]["sql_schema"].replace(" ", "")
        ):
            new_schema = ds["params"]["schema"]

        if datasource_exists:
            new = [asdict(index) for index in ds.get("params", {}).get("indexes_list", [])]
            existing = existing_ds.get("indexes", [])
            new.sort(key=lambda x: x["name"])
            existing.sort(key=lambda x: x["name"])
            if len(existing) != len(new) or any([(d, d2) for d, d2 in zip(new, existing) if d != d2]):
                new_indices = ds.get("params", {}).get("indexes") or "0"
        if (
            new_description
            or new_schema
            or new_ttl
            or ((new_indices is not None) and (not fork_downstream or not fork))
        ):
            alter_response = client.alter_datasource(
                ds_name,
                new_schema=new_schema,
                description=new_description,
                ttl=new_ttl,
                dry_run=True,
                indexes=new_indices,
            )
    except Exception as e:
        if "There were no operations to perform" in str(e):
            pass
        else:
            alter_error_message = str(e)

    if alter_response:
        click.echo(FeedbackManager.info_datasource_doesnt_match(datasource=ds_name))
        for operation in alter_response["operations"]:
            click.echo(f"**   -  {operation}")
        if alter_response["operations"] and alter_response.get("dependencies", []):
            click.echo(FeedbackManager.info_datasource_alter_dependent_pipes())
            for dependency in alter_response.get("dependencies", []):
                click.echo(f"**   -  {dependency}")

        if skip_confirmation:
            make_changes = True
        else:
            make_changes = click.prompt(FeedbackManager.info_ask_for_alter_confirmation()).lower() == "y"

        if make_changes:
            client.alter_datasource(
                ds_name,
                new_schema=new_schema,
                description=new_description,
                ttl=new_ttl,
                dry_run=False,
                indexes=new_indices,
            )
            click.echo(FeedbackManager.success_datasource_alter())
        else:
            alter_error_message = "Alter datasource cancelled"

    if alter_error_message:
        raise click.ClickException(
            FeedbackManager.error_datasource_already_exists_and_alter_failed(
                datasource=ds_name, alter_error_message=alter_error_message
            )
        )

    if datasource_exists and ds["params"].get("backfill_column") != existing_ds["tags"].get("backfill_column"):
        params = {
            "backfill_column": ds["params"].get("backfill_column"),
        }

        try:
            click.echo(FeedbackManager.info_update_datasource(datasource=ds_name, params=params))
            client.update_datasource(ds_name, params)
            click.echo(FeedbackManager.success_update_datasource(datasource=ds_name, params=params))
            make_changes = True
            alter_response = True
        except Exception as e:
            raise click.ClickException(FeedbackManager.error_updating_datasource(datasource=ds_name, error=str(e)))

    connector_data = None
    promote_error_message = None

    ds_params = ds["params"]
    service = ds_params.get("service")
    DATASOURCE_VALID_SERVICES_TO_UPDATE = ["bigquery", "snowflake"]
    if datasource_exists and service and service in [*DATASOURCE_VALID_SERVICES_TO_UPDATE, *PREVIEW_CONNECTOR_SERVICES]:
        connector_required_params = {
            "bigquery": ["service", "cron", "external_data_source"],
            "snowflake": ["connector", "service", "cron", "external_data_source"],
            "s3": ["connector", "service", "cron", "bucket_uri"],
            "s3_iamrole": ["connector", "service", "cron", "bucket_uri"],
            "gcs": ["connector", "service", "cron", "bucket_uri"],
        }.get(service, [])

        if not all(key in ds_params for key in connector_required_params):
            return

        connector = ds_params.get("connector", None)

        if service in PREVIEW_CONNECTOR_SERVICES:
            connector_id = existing_ds.get("connector", "")
            if not connector_id:
                return

            current_connector = client.get_connector_by_id(existing_ds.get("connector", ""))
            if not current_connector:
                return

            if current_connector["name"] != ds_params["connection"]:
                param = "connection"
                datafile_param = ImportReplacements.get_datafile_param_for_linker_param(service, param) or param
                raise click.ClickException(FeedbackManager.error_updating_connector_not_supported(param=datafile_param))

            linkers = current_connector.get("linkers", [])
            linker = next((linker for linker in linkers if linker["datasource_id"] == existing_ds["id"]), None)
            if not linker:
                return

            linker_settings = linker.get("settings", {})
            for param, value in linker_settings.items():
                ds_params_value = ds_params.get(param, None)
                if ds_params_value and ds_params_value != value:
                    datafile_param = ImportReplacements.get_datafile_param_for_linker_param(service, param) or param
                    raise Exception(
                        FeedbackManager.error_updating_connector_not_supported(param=datafile_param.upper())
                    )
            return

        connector_data = {
            "connector": connector,
            "service": service,
            "cron": ds_params.get("cron", None),
            "external_data_source": ds_params.get("external_data_source", None),
            "bucket_uri": ds_params.get("bucket_uri", None),
            "mode": ds_params.get("mode", "replace"),
            "query": ds_params.get("query", None),
            "ingest_now": ds_params.get("ingest_now", False),
        }

        try:
            client.update_datasource(ds_name, connector_data)
            click.echo(FeedbackManager.success_promoting_datasource(datasource=ds_name))
            return
        except Exception as e:
            promote_error_message = str(e)

    if alter_response and make_changes:
        # alter operation finished
        pass
    else:
        # removed replacing by default. When a datasource is removed data is
        # removed and all the references needs to be updated
        if (
            os.getenv("TB_I_KNOW_WHAT_I_AM_DOING")
            and click.prompt(FeedbackManager.info_ask_for_datasource_confirmation()) == ds_name
        ):  # TODO move to CLI
            try:
                client.datasource_delete(ds_name)
                click.echo(FeedbackManager.success_delete_datasource(datasource=ds_name))
            except Exception:
                raise click.ClickException(FeedbackManager.error_removing_datasource(datasource=ds_name))
            return
        else:
            if alter_error_message:
                raise click.ClickException(
                    FeedbackManager.error_datasource_already_exists_and_alter_failed(
                        datasource=ds_name, alter_error_message=alter_error_message
                    )
                )
            if promote_error_message:
                raise click.ClickException(
                    FeedbackManager.error_promoting_datasource(datasource=ds_name, error=promote_error_message)
                )
            else:
                click.echo(FeedbackManager.warning_datasource_already_exists(datasource=ds_name))


def share_and_unshare_datasource(
    client: TinyB,
    datasource: Dict[str, Any],
    user_token: str,
    workspaces_current_shared_with: List[str],
    workspaces_to_share: List[str],
    current_ws: Optional[Dict[str, Any]],
) -> None:
    datasource_name = datasource.get("name", "")
    datasource_id = datasource.get("id", "")
    workspaces: List[Dict[str, Any]]

    # In case we are pushing to a branch, we don't share the datasource
    # FIXME: Have only once way to get the current workspace
    if current_ws:
        # Force to get all the workspaces the user can access
        workspace = current_ws
        workspaces = (client.user_workspaces(version="v1")).get("workspaces", [])
    else:
        workspace = client.user_workspace_branches(version="v1")
        workspaces = workspace.get("workspaces", [])

    if workspace.get("is_branch", False):
        click.echo(FeedbackManager.info_skipping_sharing_datasources_branch(datasource=datasource["name"]))
        return

    # We duplicate the client to use the user_token
    user_client: TinyB = deepcopy(client)
    user_client.token = user_token
    if not workspaces_current_shared_with:
        for workspace_to_share in workspaces_to_share:
            w: Optional[Dict[str, Any]] = next((w for w in workspaces if w["name"] == workspace_to_share), None)
            if not w:
                raise Exception(
                    f"Unable to share datasource with the workspace {workspace_to_share}. Review that you have the admin permissions on this workspace"
                )

            user_client.datasource_share(
                datasource_id=datasource_id,
                current_workspace_id=workspace.get("id", ""),
                destination_workspace_id=w.get("id", ""),
            )
            click.echo(
                FeedbackManager.success_datasource_shared(datasource=datasource_name, workspace=w.get("name", ""))
            )
    else:
        shared_with = [
            w
            for w in workspaces
            if next((ws for ws in workspaces_current_shared_with if ws == w["id"] or ws == w["name"]), None)
        ]
        defined_to_share_with = [
            w for w in workspaces if next((ws for ws in workspaces_to_share if ws == w["id"] or ws == w["name"]), None)
        ]
        workspaces_need_to_share = [w for w in defined_to_share_with if w not in shared_with]
        workspaces_need_to_unshare = [w for w in shared_with if w not in defined_to_share_with]

        for w in workspaces_need_to_share:
            user_client.datasource_share(
                datasource_id=datasource_id,
                current_workspace_id=workspace.get("id", ""),
                destination_workspace_id=w.get("id", ""),
            )
            click.echo(
                FeedbackManager.success_datasource_shared(datasource=datasource["name"], workspace=w.get("name", ""))
            )

        for w in workspaces_need_to_unshare:
            user_client.datasource_unshare(
                datasource_id=datasource_id,
                current_workspace_id=workspace.get("id", ""),
                destination_workspace_id=w.get("id", ""),
            )
            click.echo(
                FeedbackManager.success_datasource_unshared(datasource=datasource_name, workspace=w.get("name", ""))
            )


def is_datasource(resource: Optional[Dict[str, Any]]) -> bool:
    if resource and resource.get("resource") == "datasources":
        return True
    return False
