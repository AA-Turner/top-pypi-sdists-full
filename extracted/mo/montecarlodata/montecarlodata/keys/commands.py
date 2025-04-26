from typing import Optional

import click

from montecarlodata.integrations.keys import IntegrationKeyService
from montecarlodata.keys.airflow import AirflowService

_AIRFLOW_CALLBACKS_SCOPE = "AirflowCallbacks"


@click.group(help="Manage Integration Gateway Keys")
def keys():
    pass


@keys.command(name="add-airflow", help="Add a new Airflow Integration Key")
@click.pass_obj
@click.option(
    "--name",
    required=False,
    help="Name of the Airflow Connection, required to disambiguate "
    "if multiple Airflow connections are defined",
)
@click.option("--description", required=True, help="Description for the key")
def add_airflow_integration_key(ctx, name: Optional[str] = None, description: Optional[str] = None):
    config = ctx["config"]
    resource_uuid = AirflowService(
        config=config,
        command_name="keys add_airflow_integration_key",
    ).get_airflow_resource_uuid(name=name)
    IntegrationKeyService(
        config=config,
        command_name="keys add_airflow_integration_key",
    ).create(
        description=description,
        scope=_AIRFLOW_CALLBACKS_SCOPE,
        warehouse_ids=[resource_uuid],
    )


@keys.command(name="list-airflow", help="List existing Airflow Integration Keys in the account")
@click.pass_obj
@click.option(
    "--name",
    required=False,
    help="Show keys only for the Airflow Connection with this name",
)
def list_airflow_integration_keys(ctx, name: Optional[str] = None):
    resource_uuid = (
        AirflowService(
            config=ctx["config"],
            command_name="keys list_airflow_integration_keys",
        ).get_airflow_resource_uuid(name=name)
        if name
        else None
    )
    IntegrationKeyService(
        config=ctx["config"],
        command_name="keys list_airflow_integration_keys",
    ).get_all(scope=_AIRFLOW_CALLBACKS_SCOPE, resource_uuid=resource_uuid)


@keys.command(name="delete-airflow", help="Delete an existing Airflow Integration Key")
@click.pass_obj
@click.option("--key-id", required=True, help="Id of the key to delete")
def delete_airflow_integration_key(ctx, key_id: str):
    IntegrationKeyService(
        config=ctx["config"],
        command_name="keys delete_airflow_integration_key",
    ).delete(key_id=key_id)
