from typing import List, Union

import click
from pydantic import BaseModel
from retry import retry
from ubai_client.apis import ArtifactApi
from ubai_client.models import ArtifactStorage

from utf_queue_client.scripts import setup_telemetry


class RetentionSpec(BaseModel):
    branch: str
    build_number_min: int
    build_number_max: int
    retention_days: int


@retry(Exception, delay=5, backoff=2, max_delay=30, tries=6)
def update_artifact_retention(
    retention_specs: Union[RetentionSpec, List[RetentionSpec]],
    artifact_api: ArtifactApi,
) -> int:
    if isinstance(retention_specs, RetentionSpec):
        retention_specs = [retention_specs]
    num_updated = 0
    for retention_spec in retention_specs:
        for i in range(
            retention_spec.build_number_min, retention_spec.build_number_max + 1
        ):
            spec = ArtifactStorage(
                retention_days=retention_spec.retention_days,
                metadata=dict(branch=retention_spec.branch, build_number=str(i)),
            )
            print(f"Updating {spec.metadata}")
            resp = artifact_api.update_artifacts(spec)
            print(f"{resp.num_updated} records updated")
            num_updated += resp.num_updated
    return num_updated


@click.command()
@click.option(
    "--branch", type=str, required=True, help="Branch name, e.g. release/23q2"
)
@click.option("--build_number", type=int, required=True, help="Build number, e.g. 104")
@click.option(
    "--retention_days",
    type=int,
    required=True,
    help="Number of days to retain.  Set to negative value to retain permanently.",
)
def cli_entrypoint(branch, build_number, retention_days):
    cli(branch, build_number, retention_days)


def cli(branch: str, build_number: int, retention_days: int) -> int:
    with setup_telemetry():
        artifact_api = ArtifactApi()
        artifact_api.api_client.configuration.verify_ssl = False
        artifact_api.api_client.configuration.assert_hostname = False

        retention_specs = [
            RetentionSpec(
                branch=branch,
                build_number_min=build_number,
                build_number_max=build_number,
                retention_days=retention_days,
            ),
        ]
        return update_artifact_retention(retention_specs, artifact_api)


if __name__ == "__main__":
    cli_entrypoint()
