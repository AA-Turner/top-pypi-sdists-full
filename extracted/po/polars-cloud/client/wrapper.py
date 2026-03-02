# logging.basicConfig(format="%(levelname)s:%(filename)s %(name):  %(message)")

import polars_cloud._core.connect
import polars_cloud._core.rest.workspace

DOMAIN = "intense-mint-hookworm.ngrok-free.app"
polars_cloud._core.connect.ADDRESS = "localhost:3002"

polars_cloud._core.rest.workspace.DOMAIN = DOMAIN
polars_cloud._core.rest.workspace.BASE_URL = (
    f"https://{DOMAIN}/{polars_cloud._core.rest.workspace.BASE_PATH}"
)

polars_cloud._core.rest.aws.DOMAIN = DOMAIN
polars_cloud._core.rest.aws.BASE_URL = (
    f"https://{DOMAIN}/{polars_cloud._core.rest.aws.BASE_PATH}"
)

if __name__ == "__main__":
    from polars_cloud.__main__ import cli

    cli()
else:
    import polars_cloud
