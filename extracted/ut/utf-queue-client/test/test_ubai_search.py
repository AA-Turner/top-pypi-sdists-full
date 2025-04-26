import os
import subprocess
import sys

import pytest
from otel_extensions import inject_context_to_env, instrumented

from utf_queue_client.scripts.ubai_search_cli import cli


@instrumented
@pytest.mark.parametrize(
    "set_environment_variable",
    [("DISABLE_SSL_VERIFICATION", "true"), ("DISABLE_SSL_VERIFICATION", "false")],
    indirect=True,
)
def test_ubai_search_cli(set_environment_variable):
    metadata = [
        ("app_name", "ubai_unit_test"),
        ("branch", "master"),
        ("stack", "ble"),
        ("build_number", "b140"),
        ("target", "brd4180b"),
        ("compiler", "gcc"),
    ]

    @inject_context_to_env
    def call_cli():
        results = cli("test", ".hex", metadata)
        assert len(results) == 1
        results = cli(None, None, metadata)
        assert len(results) == 1
        results = cli("test", None, metadata)
        assert len(results) == 1
        results = cli(None, ".hex", metadata)
        assert len(results) == 1

    call_cli()


@pytest.mark.parametrize(
    "set_environment_variable",
    [("DISABLE_SSL_VERIFICATION", "true"), ("DISABLE_SSL_VERIFICATION", "false")],
    indirect=True,
)
@pytest.mark.parametrize(
    "args",
    [
        ["--name", "test", "--extension", ".hex"],
        ["--extension", ".hex"],
        ["--name", "test"],
    ],
)
@instrumented
def test_ubai_search_cli_script(args, set_environment_variable):
    metadata = [
        ("app_name", "ubai_unit_test"),
        ("branch", "master"),
        ("stack", "ble"),
        ("build_number", "b140"),
        ("target", "brd4180b"),
        ("compiler", "gcc"),
    ]

    for k, v in metadata:
        args += ["--metadata", k, v]

    @inject_context_to_env
    def call_cli_script():
        assert "TRACEPARENT" in os.environ
        process = subprocess.Popen(
            [
                sys.executable,
                os.path.join("utf_queue_client", "scripts", "ubai_search_cli.py"),
            ]
            + args,
            stdout=subprocess.PIPE,
        )
        output, _ = process.communicate()
        assert process.poll() == 0
        assert output.decode().strip() == "d89e7962-3533-4f2c-b3e9-a4b9015ea4e2"

    call_cli_script()
