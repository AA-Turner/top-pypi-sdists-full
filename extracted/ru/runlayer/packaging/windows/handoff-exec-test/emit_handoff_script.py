"""Emit a production Windows update handoff as an EncodedCommand."""

from __future__ import annotations

import argparse
from pathlib import Path

from runlayer_cli.windows_update_handoff import (
    _build_handoff_action_script,
    _encoded_powershell_command,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--msiexec-path", type=Path, required=True)
    parser.add_argument("--log-path", type=Path, required=True)
    parser.add_argument("--product-directory", required=True)
    parser.add_argument("--service-name", required=True)
    parser.add_argument("--target-version", required=True)
    arguments = parser.parse_args()

    script = _build_handoff_action_script(
        msiexec_argv=[
            str(arguments.msiexec_path),
            "/i",
            str(arguments.log_path.with_suffix(".msi")),
            "/qn",
            "/norestart",
            "REBOOT=ReallySuppress",
            "/l*v",
            str(arguments.log_path),
        ],
        log_path=arguments.log_path,
        process_name="aiwatch",
        product_install_directory=arguments.product_directory,
        to_version=arguments.target_version,
        quiesce_task_names=(),
        quiesce_service_names=(arguments.service_name,),
        wait_seconds=1,
    )
    print(_encoded_powershell_command(script))


if __name__ == "__main__":
    main()
