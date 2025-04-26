import os
import pathlib
import subprocess
import sys

import pytest
from otel_extensions import inject_context_to_env, instrumented

from utf_queue_client.scripts.ubai_update_retention_cli import cli


@instrumented
@pytest.mark.parametrize(
    "set_environment_variable",
    [("DISABLE_SSL_VERIFICATION", "true"), ("DISABLE_SSL_VERIFICATION", "false")],
    indirect=True,
)
def test_ubai_update_retention_cli(set_environment_variable):
    @inject_context_to_env
    def call_cli():
        num_updated = cli("non-existent-branch", 123, 4)
        assert num_updated == 0

    call_cli()


@pytest.mark.parametrize(
    "set_environment_variable",
    [("DISABLE_SSL_VERIFICATION", "true"), ("DISABLE_SSL_VERIFICATION", "false")],
    indirect=True,
)
@instrumented
def test_ubai_search_cli_script(set_environment_variable):
    args = [
        "--branch",
        "non-existent-branch",
        "--build_number",
        "123",
        "--retention_days",
        "4",
    ]

    @inject_context_to_env
    def call_cli_script():
        assert "TRACEPARENT" in os.environ
        process = subprocess.Popen(
            [
                sys.executable,
                str(
                    pathlib.Path(__file__).parent.parent
                    / os.path.join(
                        "utf_queue_client", "scripts", "ubai_update_retention_cli.py"
                    )
                ),
            ]
            + args,
            stdout=subprocess.PIPE,
        )
        output, _ = process.communicate()
        assert process.poll() == 0
        assert output.decode().strip().splitlines()[1] == "0 records updated"

    call_cli_script()
