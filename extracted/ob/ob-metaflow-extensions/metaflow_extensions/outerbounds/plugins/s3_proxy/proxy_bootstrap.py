from .s3_proxy_manager import S3ProxyManager
from metaflow._vendor import click
from metaflow import JSONType
import json


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--integration-name", type=str, help="The integration name", required=True
)
@click.option("--write-mode", type=str, help="The write mode")
@click.option("--debug", type=bool, help="The debug mode", default=False)
@click.option(
    "--uc-proxy-cfg-write-path",
    type=str,
    help="The path to write the user code proxy config",
    required=True,
)
@click.option(
    "--proxy-status-write-path",
    type=str,
    help="The path to write the proxy status",
    required=True,
)
def bootstrap(
    integration_name,
    write_mode,
    debug,
    uc_proxy_cfg_write_path,
    proxy_status_write_path,
):
    manager = S3ProxyManager(
        integration_name=integration_name,
        write_mode=write_mode,
        debug=debug,
    )
    user_code_proxy_config, proxy_pid, config_path, binary_path = manager.setup_proxy()
    with open(uc_proxy_cfg_write_path, "w") as f:
        f.write(json.dumps(user_code_proxy_config))
    with open(proxy_status_write_path, "w") as f:
        f.write(
            json.dumps(
                {
                    "proxy_pid": proxy_pid,
                    "config_path": config_path,
                    "binary_path": binary_path,
                }
            )
        )


if __name__ == "__main__":
    print("[@s3_proxy] Jumpstarting the proxy....")
    cli()
