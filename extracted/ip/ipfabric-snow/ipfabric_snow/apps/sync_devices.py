import datetime
import typing
from importlib import metadata

import typer
import typing_extensions
from ipfabric_snow.apps.env_setup import ensure_environment_is_setup
from ipfabric import IPFClient
from rich import print
from ipfabric_snow.utils.etl import ETLUtility
from loguru import logger
from ipfabric_snow.utils.servicenow_client import Snow

sync_devices_app = typer.Typer()

# IPF_IGNORE_CLOUD_DEVICES_FILTER = {'or': [{'vendor': ['eq', 'azure']}, {'vendor': ['eq', 'aws']}, {'vendor': ['eq', 'gcp']}]}


def get_snow_auth(env_vars):
    token = env_vars.get("SNOW_TOKEN")
    username = env_vars.get("SNOW_USER")
    password = env_vars.get("SNOW_PASS")

    if token:
        return token
    elif username and password:
        return username, password
    else:
        raise ValueError("Incomplete authentication credentials")


def verify_or_create_vendors_and_locations(devices, sn_model: Snow):
    unique_vendors = set(device["vendor"] for device in devices if "vendor" in device)
    unique_locations = set(
        device["location"] for device in devices if "location" in device
    )

    snow_locations = sn_model.vendors.get_all()
    snow_vendors = sn_model.location.get_all()

    for vendor in unique_vendors:
        if vendor not in snow_vendors:
            sn_model.vendors.create_vendor(vendor)

    for location in unique_locations:
        if location not in snow_locations:
            sn_model.location.create_location(location)


def insert_devices_into_staging_table(all_devices, sn_client: Snow, staging_table_name, staging_table_insert_limit):
    if len(all_devices) > staging_table_insert_limit:
        start_idx = 0
        while start_idx < len(all_devices):
            logger.info(f"Inserting records {start_idx} to {start_idx + staging_table_insert_limit}")
            end_idx = min(start_idx + staging_table_insert_limit, len(all_devices))
            devices_to_insert = all_devices[start_idx:end_idx]
            sn_client.request_client.insert_staging_record(
                staging_table_name, {"records": devices_to_insert}
            )
            start_idx += staging_table_insert_limit
    else:
        sn_client.request_client.insert_staging_record(
            staging_table_name, {"records": all_devices}
        )


@sync_devices_app.command("devices", help="Sync devices from IP Fabric to ServiceNow")
def sync_devices(
    staging_table_name: typing_extensions.Annotated[
        typing.Optional[str],
        typer.Argument(
            help="The name of the ServiceNow staging table to use.",
            rich_help_panel="Core Arguments"
        ),

    ] = "x_1249630_ipf_devices",
    show_diff: bool = typer.Option(False, help="Display the data difference", rich_help_panel="Diffing Options"),
    diff_source: str = typer.Option(
        "IPF", help="Specify the main source for diff, either IPF or SNOW", rich_help_panel="Diffing Options"
    ),
    write_diff: bool = typer.Option(
        False, help="Enable or disable writing the diff to a file", rich_help_panel="Diffing Options"
    ),
    diff_file: str = typer.Option(
        "data/{date_time}_diff_{diff_source}.json",
        help="Path to save the diff file, if desired",
        rich_help_panel="Diffing Options"
    ),
    dry_run: bool = typer.Option(
        False, help="Perform a dry run without making any changes"
    ),
    ipf_snapshot: str = typer.Option(
        "$last", help="IP Fabric snapshot ID to use for the sync", rich_help_panel="IP Fabric Options"
    ),
    cmdb_table_name: str = typer.Option(
        default="cmdb_ci_netgear",
        help="Name of the cmdb table to pull data from. Defaults to cmdb_ci_netgear",
        hidden=True,
        rich_help_panel="Service Now Options"
    ),
    timeout: int = typer.Option(10, help="timeout for httpx requests"),
    record_limit: int = typer.Option(
        default=1000,
        help="Limit the number of records to pull from ServiceNow. Defaults to 1000",
        rich_help_panel="Service Now Options"
    ),
    output_verbose: bool = typer.Option(
        False,
        help="adds more detail to the output. Identifies which keys changed per device",
        rich_help_panel="Diffing Options"
    ),
    staging_table_insert_limit: int = typer.Option(
        9999,
        help="Limit the number of records to insert into the staging table",
        rich_help_panel="Service Now Options"
    ),
    include_switch_stacks: bool = typer.Option(
        False,
        help="Include switch stacks in the sync. Inserts the stack members as separate records in the staging table",
        rich_help_panel="IP Fabric Options"
    ),
    include_fex: bool = typer.Option(
        False,
        help="Include FEX devices in the sync. Inserts the FEX devices as separate records in the staging table",
        rich_help_panel="IP Fabric Options"
    ),
):
    """
    Sync devices from IP Fabric to ServiceNow
    """
    etl_utility, diff = sync_devices_func(
        staging_table_name=staging_table_name,
        show_diff=show_diff,
        diff_source=diff_source,
        write_diff=write_diff,
        dry_run=dry_run,
        ipf_snapshot=ipf_snapshot,
        cmdb_table_name=cmdb_table_name,
        timeout=timeout,
        record_limit=record_limit,
        output_verbose=output_verbose,
        staging_table_insert_limit=staging_table_insert_limit,
        include_switch_stacks=include_switch_stacks,
        include_fex=include_fex,
        for_cli=True,
    )

    if show_diff:
        print(diff)

    if write_diff:
        diff_file = diff_file.format(
            date_time=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
            diff_source=diff_source,
        )
        etl_utility.write_diff_to_file(diff, diff_file)
        logger.info(f"Diff saved to {diff_file}")


def sync_devices_func(
        show_diff: bool,
        diff_source: str,
        write_diff: bool,
        dry_run: bool,
        ipf_snapshot: str,
        timeout: int,
        record_limit: int,
        output_verbose: bool,
        cmdb_table_name: str = 'cmdb_ci_netgear',
        staging_table_name: str = 'x_1249630_ipf_devices',
        staging_table_insert_limit: int = 9999,
        for_cli: bool = False,
        include_switch_stacks: bool = False,
        include_fex: bool = False,
        ):
    if staging_table_name is None and not dry_run:
        logger.error(
            "No staging table name provided. Either provide a staging table name or enable dry run mode."
        )
        raise typer.Exit(code=1)
    all_vars = ensure_environment_is_setup()
    if all_vars.get("IPF_TOKEN"):
        auth = all_vars["IPF_TOKEN"]
    elif all_vars.get("IPF_USER") and all_vars.get("IPF_PASS"):
        auth = (all_vars["IPF_USER"], all_vars["IPF_PASS"])
    else:
        logger.error("No authentication credentials provided for IPFClient.")
        raise typer.Exit(code=1)

    ipf = IPFClient(base_url=all_vars["IPF_URL"], auth=auth, snapshot_id=ipf_snapshot)
    ipf._client.headers['user-agent'] += f'; python-ipfabric-snow/{metadata.version("ipfabric-snow")}'
    auth = get_snow_auth(all_vars)
    sn_client = Snow(auth=auth, url=all_vars["SNOW_URL"], httpx_timeout=timeout)

    current_snow_data = sn_client.request_client.get_all_records(
        cmdb_table_name, limit=record_limit
    )
    all_snow_devices = current_snow_data["result"]
    logger.info(f"Found {len(all_snow_devices)} devices in ServiceNow")

    all_devices = ipf.inventory.devices.all()
    # if we need to ignore cloud items from the inventory, we can add this filter
    # all_devices_to_ignore = ipf.inventory.devices.all(filters=IPF_IGNORE_CLOUD_DEVICES_FILTER)
    # all_devices = [device for device in ipf.inventory.devices.all() if device not in all_devices_to_ignore]
    logger.info(f"Found {len(all_devices)} devices in IP Fabric")

    main_source = diff_source.upper()

    if not dry_run:
        insert_devices_into_staging_table(
            all_devices,
            sn_client,
            staging_table_name,
            staging_table_insert_limit
        )
        if include_switch_stacks or include_fex:
            if include_switch_stacks:
                switch_stacks_members = ipf.fetch_all("/technology/platforms/stack/members")
                insert_devices_into_staging_table(
                    switch_stacks_members,
                    sn_client,
                    "x_1249630_ipf_switch_stacks",
                    staging_table_insert_limit
                )
                logger.info("Inserted Switch Stack data into Switch Stack Staging table")
            if include_fex:
                fex_devices = ipf.fetch_all("/technology/platforms/fex/fex-modules")
                insert_devices_into_staging_table(
                    fex_devices,
                    sn_client,
                    "x_1249630_ipf_fex",
                    staging_table_insert_limit
                )
                logger.info("Inserted FEX data into FEX Staging table")
    else:
        logger.info("Dry run enabled, no data will be sent to ServiceNow")

    if show_diff or write_diff:
        etl_utility = ETLUtility(
            all_devices,
            all_snow_devices,
            data_source=main_source,
            verbose=output_verbose,
            check_env=False,
            env_vars=all_vars,
        )

        etl_utility.transform_data()
        diff = etl_utility.compute_diff()
        return etl_utility, diff
    else:
        logger.info("No diff requested, exiting.")
        if for_cli:
            raise typer.Exit(code=0)
        else:
            return None, None
