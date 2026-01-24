import typer

from ipfabric_snow.apps.env_setup import env_setup_app
from ipfabric_snow.apps.sync_devices import sync_devices_app
from ipfabric_snow.utils.logger import setup_logging

app = typer.Typer()
app.add_typer(env_setup_app, name="env", help="Setup environment variables")
app.add_typer(sync_devices_app, name="sync", help="Sync Inventory data with ServiceNow")


@app.callback()
def logging_configuration(
    log_level: str = typer.Option("INFO", help="Log level"),
    log_to_file: bool = typer.Option(True, help="Log to file"),
    log_file_name: str = typer.Option("ipf_serviceNow.log", help="Log file name"),
    log_json: bool = typer.Option(False, help="Log in JSON format"),
):
    setup_logging(log_level, log_to_file, log_file_name, log_json)


def main():
    app()


if __name__ == "__main__":
    main()
