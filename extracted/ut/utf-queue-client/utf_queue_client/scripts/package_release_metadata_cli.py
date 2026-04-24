import json
import os
from dataclasses import dataclass, field
from typing import Optional

import click
from opentelemetry import trace
from otel_extensions import instrumented
from package_release_metadata_client import (
    ManifestClient,
    ManifestCreate,
    ManifestRead,
    QualityStatusClient,
    QualityStatusCreate,
)
from package_release_metadata_client.wrapper._base import DEV_URL

from utf_queue_client import DISABLE_SSL_VERIFICATION_DEFAULT
from utf_queue_client.scripts import setup_telemetry

STATUS_CHOICES = click.Choice(["pass", "fail", "aborted"])


def _make_manifest_client(dev: bool = False) -> ManifestClient:
    client = ManifestClient(dev=dev)
    if (
        os.environ.get("DISABLE_SSL_VERIFICATION", DISABLE_SSL_VERIFICATION_DEFAULT)
        == "true"
    ):
        client._api_client.configuration.verify_ssl = False
    return client


def _make_quality_status_client(dev: bool = False) -> QualityStatusClient:
    client = QualityStatusClient(dev=dev)
    if (
        os.environ.get("DISABLE_SSL_VERIFICATION", DISABLE_SSL_VERIFICATION_DEFAULT)
        == "true"
    ):
        client._api_client.configuration.verify_ssl = False
    return client


# ---------------------------------------------------------------------------
# pkgrelease_manifest_read
# ---------------------------------------------------------------------------

_MANIFEST_READ_HELP = """\
Get the latest manifest for a package release.

Returns the manifest resolved for the given release_name. If build_number is
omitted, the service returns the manifest for the highest known build.

\b
Required fields:
  --release-name   Release identifier, e.g. '2.4.1'.

\b
Optional fields:
  --build-number   Build number; defaults to the latest for the release.

\b
Response body type: ManifestRead
  manifest_id      str   — UUID of the manifest.
  release_name     str
  build_number     int
  artifactory_url  str | null
  created_at       str
"""


@click.command(name="pkgrelease_latest_manifest_read", help=_MANIFEST_READ_HELP)
@click.option(
    "--release-name", required=True, help="Release identifier, e.g. '2026.6.0'."
)
@click.option(
    "--dev",
    is_flag=True,
    default=False,
    help=f"Target the dev environment ({DEV_URL}).",
)
def manifest_read_cli_entrypoint(release_name, dev):
    result = manifest_read(release_name=release_name, dev=dev)
    print(json.dumps(result.to_dict(), indent=2, default=str))


def manifest_read(
    release_name: str,
    dev: bool = False,
) -> ManifestRead:
    with setup_telemetry():
        client = _make_manifest_client(dev)
        return _get_latest_manifest(client, release_name)


@instrumented
def _get_latest_manifest(
    client: ManifestClient,
    release_name: str,
) -> ManifestRead:
    span = trace.get_current_span()
    span.set_attribute("release_name", release_name)
    response = client.get_latest_manifest(release_name)
    span.set_attribute("manifest_id", response.data.manifest_id)
    return response.data


# ---------------------------------------------------------------------------
# pkgrelease_manifest_write
# ---------------------------------------------------------------------------

_MANIFEST_WRITE_HELP = """\
Create a new manifest for a package release.

Returns 409 if a manifest for the same (release_name, build_number) already exists.

\b
Required fields:
  --release-name   Release identifier, e.g. '2.4.1'.
  --build-number   Build number integer.

\b
Optional fields:
  --artifactory-url  URL to the manifest artifact in Artifactory.

\b
Response body type: ManifestRead
  manifest_id      str   — UUID of the created manifest.
  release_name     str
  build_number     int
  artifactory_url  str | null
  created_at       str
"""


@click.command(name="pkgrelease_manifest_write", help=_MANIFEST_WRITE_HELP)
@click.option("--release-name", required=True, help="Release identifier, e.g. '2.4.1'.")
@click.option("--build-number", required=True, type=int, help="Build number integer.")
@click.option(
    "--artifactory-url",
    default=None,
    help="(optional) URL to the manifest artifact in Artifactory.",
)
@click.option(
    "--dev",
    is_flag=True,
    default=False,
    help=f"Target the dev environment ({DEV_URL}).",
)
def manifest_write_cli_entrypoint(release_name, build_number, artifactory_url, dev):
    result = manifest_write(
        release_name=release_name,
        build_number=build_number,
        artifactory_url=artifactory_url,
        dev=dev,
    )
    print(json.dumps(result.to_dict(), indent=2, default=str))


def manifest_write(
    release_name: str,
    build_number: int,
    artifactory_url: Optional[str] = None,
    dev: bool = False,
) -> ManifestRead:
    with setup_telemetry():
        client = _make_manifest_client(dev)
        payload = ManifestCreate(
            release_name=release_name,
            build_number=build_number,
            artifactory_url=artifactory_url,
        )
        return _create_manifest(client, payload)


@instrumented
def _create_manifest(client: ManifestClient, payload: ManifestCreate) -> ManifestRead:
    span = trace.get_current_span()
    span.set_attribute("release_name", payload.release_name)
    span.set_attribute("build_number", payload.build_number)
    response = client.create_manifest(payload)
    span.set_attribute("manifest_id", response.data.manifest_id)
    return response.data


# ---------------------------------------------------------------------------
# pkgrelease_quality_status_update
# ---------------------------------------------------------------------------

_UPDATE_HELP = """\
Create a new quality_status row for a package release.

Resolves the manifest from release_name + build_number and inserts a new row.
Returns 404 if the manifest does not exist.
Returns 409 if a row with the same (stack_name, manifest_id, job_url) already exists.

\b
Required fields:
  --release-name      Release identifier, e.g. '2.4.1'.
  --build-number      Build number integer.
  --job-url           CI job URL that produced this result.
  --stack-name        Stack identifier, e.g. 'zigbee'.
  --test-result-type  Category of test, e.g. 'sanity'.
  --status            Outcome: pass | fail | aborted.
  --run-num           Run/attempt number.

\b
Optional fields:
  --sub-stack         Sub-stack name.
  --total-cnt         Total test count.
  --pass-cnt          Passing test count.
  --fail-cnt          Failing test count.
  --skip-cnt          Skipped test count.
  --blocked-cnt       Blocked test count.
  --pass-pct          Pass percentage (0–100).
  --start-time        Test run start time (ISO 8601), e.g. '2024-01-15T10:30:00'.

\b
Response body type: QualityStatusRead
  id               int    — Row primary key.
  manifest_id      str    — UUID of the resolved manifest.
  stack_name       str
  test_result_type str
  status           str | null
  run_num          int | null
  job_url          str | null
  sub_stack        str | null
  total_cnt        int | null
  pass_cnt         int | null
  fail_cnt         int | null
  skip_cnt         int | null
  blocked_cnt      int | null
  pass_pct         float | null
  start_time       str | null
"""


@dataclass
class QualityStatusOptions:
    sub_stack: Optional[str] = field(default=None)
    total_cnt: Optional[int] = field(default=None)
    pass_cnt: Optional[int] = field(default=None)
    fail_cnt: Optional[int] = field(default=None)
    skip_cnt: Optional[int] = field(default=None)
    blocked_cnt: Optional[int] = field(default=None)
    pass_pct: Optional[float] = field(default=None)
    start_time: Optional[str] = field(default=None)


@click.command(name="pkgrelease_quality_status_update", help=_UPDATE_HELP)
@click.option("--release-name", required=True, help="Release identifier, e.g. '2.4.1'.")
@click.option("--build-number", required=True, type=int, help="Build number integer.")
@click.option("--job-url", required=True, help="CI job URL that produced this result.")
@click.option("--stack-name", required=True, help="Stack identifier, e.g. 'zigbee'.")
@click.option(
    "--test-result-type", required=True, help="Category of test, e.g. 'sanity'."
)
@click.option(
    "--status",
    required=True,
    type=STATUS_CHOICES,
    help="Outcome: pass | fail | aborted.",
)
@click.option("--run-num", required=True, type=int, help="Run/attempt number.")
@click.option("--sub-stack", default=None, help="(optional) Sub-stack name.")
@click.option(
    "--total-cnt", default=None, type=int, help="(optional) Total test count."
)
@click.option(
    "--pass-cnt", default=None, type=int, help="(optional) Passing test count."
)
@click.option(
    "--fail-cnt", default=None, type=int, help="(optional) Failing test count."
)
@click.option(
    "--skip-cnt", default=None, type=int, help="(optional) Skipped test count."
)
@click.option(
    "--blocked-cnt", default=None, type=int, help="(optional) Blocked test count."
)
@click.option(
    "--pass-pct", default=None, type=float, help="(optional) Pass percentage (0–100)."
)
@click.option(
    "--start-time",
    default=None,
    help="(optional) Test run start time (ISO 8601), e.g. '2024-01-15T10:30:00'.",
)
@click.option(
    "--dev",
    is_flag=True,
    default=False,
    help=f"Target the dev environment ({DEV_URL}).",
)
def update_cli_entrypoint(**kwargs):
    options = QualityStatusOptions(
        sub_stack=kwargs.pop("sub_stack"),
        total_cnt=kwargs.pop("total_cnt"),
        pass_cnt=kwargs.pop("pass_cnt"),
        fail_cnt=kwargs.pop("fail_cnt"),
        skip_cnt=kwargs.pop("skip_cnt"),
        blocked_cnt=kwargs.pop("blocked_cnt"),
        pass_pct=kwargs.pop("pass_pct"),
        start_time=kwargs.pop("start_time"),
    )
    result = quality_status_update(**kwargs, options=options)
    print(json.dumps(result.to_dict(), indent=2, default=str))


def quality_status_update(
    release_name: str,
    build_number: int,
    job_url: str,
    stack_name: str,
    test_result_type: str,
    status: str,
    run_num: int,
    options: Optional[QualityStatusOptions] = None,
    dev: bool = False,
):
    opts = options or QualityStatusOptions()
    with setup_telemetry():
        client = _make_quality_status_client(dev)
        payload = QualityStatusCreate(
            release_name=release_name,
            build_number=build_number,
            job_url=job_url,
            stack_name=stack_name,
            test_result_type=test_result_type,
            status=status,
            run_num=run_num,
            sub_stack=opts.sub_stack,
            total_cnt=opts.total_cnt,
            pass_cnt=opts.pass_cnt,
            fail_cnt=opts.fail_cnt,
            skip_cnt=opts.skip_cnt,
            blocked_cnt=opts.blocked_cnt,
            pass_pct=opts.pass_pct,
            start_time=opts.start_time,
        )
        return _create_quality_status(client, payload)


@instrumented
def _create_quality_status(client: QualityStatusClient, payload: QualityStatusCreate):
    span = trace.get_current_span()
    span.set_attribute("release_name", payload.release_name)
    span.set_attribute("build_number", payload.build_number)
    span.set_attribute("status", payload.status)
    span.set_attribute("job_url", payload.job_url)
    response = client.create_quality_status(payload)
    span.set_attribute("quality_status.id", response.data.id)
    return response.data


# ---------------------------------------------------------------------------
# pkgrelease_quality_status_enquiry
# ---------------------------------------------------------------------------

_ENQUIRY_HELP = """\
Query quality_status records for a package release.

release_name is required. The API invoked depends on the additional parameters:

\b
  release_name only, or release_name + build_num only:
    → GET /api/v1/quality_status/latest
    Returns the latest *passed* result per (stack_name, sub_stack, test_result_type)
    for the release. build_num defaults to the highest known build for that release.

  release_name + stack_name and/or test_result_type:
    → GET /api/v1/quality_status  (filtered list)
    Returns all matching rows. If build_num is omitted the latest build is used.

\b
Response body type — latest endpoint: LatestQualityStatusResponse
  release_name  str
  build_number  int
  stacks        list[StackSummary]
    Each StackSummary: stack_name (str), results (list[StackResult])
      Each StackResult: sub_stack (str|null), test_result_type (str), status (str)

\b
Response body type — list endpoint: List[QualityStatusRead]
  Each item:
    id               int
    manifest_id      str
    stack_name       str
    test_result_type str
    status           str | null
    run_num          int | null
    job_url          str | null
    sub_stack        str | null
    total_cnt        int | null
    pass_cnt         int | null
    fail_cnt         int | null
    skip_cnt         int | null
    blocked_cnt      int | null
    pass_pct         float | null
    start_time       str | null
"""


@click.command(name="pkgrelease_quality_status_enquiry", help=_ENQUIRY_HELP)
@click.option("--release-name", required=True, help="Release identifier (required).")
@click.option(
    "--build-num",
    default=None,
    type=int,
    help="(optional) Build number; defaults to the latest for the release.",
)
@click.option(
    "--stack-name",
    default=None,
    help="(optional) Filter by stack name. Triggers the list API.",
)
@click.option(
    "--test-result-type",
    default=None,
    help="(optional) Filter by test result type. Triggers the list API.",
)
@click.option(
    "--dev",
    is_flag=True,
    default=False,
    help=f"Target the dev environment ({DEV_URL}).",
)
def enquiry_cli_entrypoint(release_name, build_num, stack_name, test_result_type, dev):
    result = quality_status_enquiry(
        release_name=release_name,
        build_num=build_num,
        stack_name=stack_name,
        test_result_type=test_result_type,
        dev=dev,
    )
    if isinstance(result, list):
        print(json.dumps([r.to_dict() for r in result], indent=2, default=str))
    else:
        print(json.dumps(result.to_dict(), indent=2, default=str))


def quality_status_enquiry(
    release_name: str,
    build_num: Optional[int] = None,
    stack_name: Optional[str] = None,
    test_result_type: Optional[str] = None,
    dev: bool = False,
):
    with setup_telemetry():
        client = _make_quality_status_client(dev)
        if stack_name is not None or test_result_type is not None:
            return _list_quality_status(
                client, release_name, build_num, stack_name, test_result_type
            )
        return _get_latest_quality_status(client, release_name, build_num)


@instrumented
def _get_latest_quality_status(
    client: QualityStatusClient,
    release_name: str,
    build_number: Optional[int],
):
    span = trace.get_current_span()
    span.set_attribute("release_name", release_name)
    span.set_attribute("build_number", build_number or "")
    span.set_attribute("query_type", "latest")
    response = client.get_latest_quality_status(
        release_name=release_name,
        build_number=build_number,
    )
    return response.data


@instrumented
def _list_quality_status(
    client: QualityStatusClient,
    release_name: str,
    build_number: Optional[int],
    stack_name: Optional[str],
    test_result_type: Optional[str],
):
    span = trace.get_current_span()
    span.set_attribute("release_name", release_name)
    span.set_attribute("build_number", build_number or "")
    span.set_attribute("stack_name", stack_name or "")
    span.set_attribute("test_result_type", test_result_type or "")
    span.set_attribute("query_type", "list")
    response = client.list_quality_status(
        release_name=release_name,
        build_number=build_number,
        stack_name=stack_name,
        test_result_type=test_result_type,
    )
    return response.data


if __name__ == "__main__":
    update_cli_entrypoint()
