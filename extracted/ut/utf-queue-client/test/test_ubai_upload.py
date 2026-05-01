import os
import subprocess
import sys
import tempfile

import pytest
from otel_extensions import inject_context_to_env, instrumented
from ubai_client.apis import ArtifactApi, SearchApi
from ubai_client.models import ArtifactStorage

from utf_queue_client.scripts.ubai_upload_cli import MULTIPART_SIZE_THRESHOLD, cli


@pytest.fixture
def metadata():
    yield [
        ("app_name", "ubai_unit_test"),
        ("branch", "master"),
        ("stack", "ble"),
        ("build_number", "b140"),
        ("target", "brd4180b"),
    ]


@instrumented
@pytest.mark.parametrize(
    "set_environment_variable",
    [("DISABLE_SSL_VERIFICATION", "true"), ("DISABLE_SSL_VERIFICATION", "false")],
    indirect=True,
)
@pytest.mark.parametrize("use_queue", [True, False])
def test_ubai_upload_cli(request, metadata, set_environment_variable, use_queue):
    file = os.path.join(os.path.dirname(__file__), "test.hex")

    username = os.environ["UTF_QUEUE_USERNAME"]
    password = os.environ["UTF_QUEUE_PASSWORD"]
    client_id = request.node.name

    @inject_context_to_env
    def call_cli():
        cli(file, metadata, username, password, client_id, queue=use_queue)

    call_cli()


@instrumented
@pytest.mark.parametrize(
    "set_environment_variable",
    [("DISABLE_SSL_VERIFICATION", "true"), ("DISABLE_SSL_VERIFICATION", "false")],
    indirect=True,
)
@pytest.mark.parametrize("use_queue", [True, False])
def test_ubai_upload_cli_large_file(
    request, metadata, set_environment_variable, use_queue
):
    with tempfile.TemporaryDirectory() as temp_dir:
        file = os.path.join(temp_dir, "test_large.hex")
        with open(file, "wb") as f:
            f.write(os.urandom(MULTIPART_SIZE_THRESHOLD * 2))

        username = os.environ["UTF_QUEUE_USERNAME"]
        password = os.environ["UTF_QUEUE_PASSWORD"]
        client_id = request.node.name

        @inject_context_to_env
        def call_cli():
            cli(file, metadata, username, password, client_id, queue=use_queue)

        call_cli()

        # delete our file
        metadata_dict = {}
        for key, value in metadata:
            metadata_dict[key] = value
        search_api = SearchApi()
        search_api.api_client.configuration.discard_unknown_keys = True
        search_spec = ArtifactStorage(
            extension=".hex",
            name="test_large",
            metadata=metadata_dict,
        )
        search_results = search_api.find_all_artifacts(search_spec)
        artifact_api = ArtifactApi()
        for result in search_results:
            artifact_api.delete_artifact(result.id)


@pytest.mark.parametrize("use_queue", [True, False, None])
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
def test_ubai_upload_cli_script(
    request, metadata, use_queue, set_environment_variables
):
    file = os.path.join(os.path.dirname(__file__), "test.hex")
    base_dir = os.path.dirname(os.path.dirname(__file__))

    client_id = request.node.name
    args = ["--file-path", file, "--client-id", client_id]
    for k, v in metadata:
        args += ["--metadata", k, v]
    if use_queue is not None:
        args += ["--queue" if use_queue else "--no-queue"]

    @inject_context_to_env
    def call_cli_script():
        assert "TRACEPARENT" in os.environ
        process = subprocess.Popen(
            [
                sys.executable,
                os.path.join(
                    base_dir, "utf_queue_client", "scripts", "ubai_upload_cli.py"
                ),
            ]
            + args,
        )
        process.communicate()
        assert process.poll() == 0

    call_cli_script()
