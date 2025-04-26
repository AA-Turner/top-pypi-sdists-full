import base64
import os
import subprocess
import sys

import pytest
from otel_extensions import inject_context_to_env, instrumented
from ubai_client.apis import ArtifactApi, SearchApi
from ubai_client.model.artifact_input import ArtifactInput
from ubai_client.models import ArtifactStorage

from utf_queue_client.scripts.ubai_copy_cli import cli


@pytest.fixture
def copy_metadata():
    yield [
        ("app_name", "ubai_unit_test"),
        ("branch", "master"),
        ("stack", "dmp"),
        ("build_number", "b140"),
        ("target", "brd4180b"),
    ]


@pytest.fixture
def artifact_id():
    artifact_api = ArtifactApi()
    base64_content = base64.b64encode(os.urandom(1000)).decode("utf-8")
    metadata = {
        "app_name": "ubai_unit_test",
        "branch": "master",
        "stack": "ot",
        "build_number": "b140",
        "target": "brd4180b",
    }
    payload = ArtifactInput(
        base64_content=base64_content, extension=".hex", metadata=metadata, name="test"
    )
    response = artifact_api.upload_artifact(payload)
    yield response.id
    artifact_api.delete_artifact(response.id)


@pytest.fixture
def copy_name():
    yield "copy_test"


@pytest.fixture
def copy_extension():
    yield ".hex"


@instrumented
@pytest.mark.parametrize(
    "set_environment_variable",
    [("DISABLE_SSL_VERIFICATION", "true"), ("DISABLE_SSL_VERIFICATION", "false")],
    indirect=True,
)
def test_ubai_copy_cli(
    artifact_id, copy_name, copy_extension, copy_metadata, set_environment_variable
):
    @inject_context_to_env
    def call_cli():
        cli(artifact_id, copy_name, copy_extension, copy_metadata)

    call_cli()

    # delete our file
    metadata_dict = {}
    for key, value in copy_metadata:
        metadata_dict[key] = value
    search_api = SearchApi()
    search_api.api_client.configuration.discard_unknown_keys = True
    search_spec = ArtifactStorage(
        extension=copy_extension,
        name=copy_name,
        metadata=metadata_dict,
    )
    search_results = search_api.find_all_artifacts(search_spec)
    artifact_api = ArtifactApi()
    for result in search_results:
        artifact_api.delete_artifact(result.id)


@pytest.mark.parametrize(
    "set_environment_variables",
    [
        [],
        [
            (
                "OTEL_EXPORTER_OTLP_ENDPOINT",
                "https://otel-collector-http-wrong.silabs.net",
            )
        ],
    ],
    indirect=True,
)
@instrumented
def test_ubai_copy_cli_script(
    artifact_id, copy_name, copy_extension, copy_metadata, set_environment_variables
):
    base_dir = os.path.dirname(os.path.dirname(__file__))

    args = [
        "--artifact_id",
        artifact_id,
        "--name",
        copy_name,
        "--extension",
        copy_extension,
    ]
    for k, v in copy_metadata:
        args += ["--metadata", k, v]

    @inject_context_to_env
    def call_cli_script():
        assert "TRACEPARENT" in os.environ
        process = subprocess.Popen(
            [
                sys.executable,
                os.path.join(
                    base_dir, "utf_queue_client", "scripts", "ubai_copy_cli.py"
                ),
            ]
            + args,
        )
        process.communicate()
        assert process.poll() == 0

    call_cli_script()
