import argparse
import os
import runpy
import sys

from hud_sdk.auto_init.utils import (
    log_to_user,
    set_config_path,
    set_key,
    set_service,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default=None,
        help="Path to the config file",
    )
    parser.add_argument(
        "--key",
        default="",
        help="Hud API key",
    )
    parser.add_argument(
        "--service",
        default="",
        help="Hud service name",
    )
    parser.add_argument(
        "script",
        nargs=argparse.REMAINDER,
        help="Python script to run and its arguments (Required)",
    )

    args = parser.parse_args()

    if not args.script:
        parser.print_help()
        sys.exit(1)

    if args.config:
        set_config_path(args.config)

    if args.key:
        set_key(args.key)

    if args.service:
        set_service(args.service)

    try:
        from hud_sdk.auto_init.start_hud import start_hud

        start_hud()
    except Exception:
        pass

    script_path = args.script[0]
    if not script_path:
        log_to_user("[ERROR] Hud: No script path provided.")
        sys.exit(1)

    if not os.path.exists(script_path):
        log_to_user(f"[ERROR] Hud: Script file not found: {script_path}")
        sys.exit(1)

    if not os.path.isfile(script_path):
        log_to_user(f"[ERROR] Hud: Path is not a file: {script_path}")
        sys.exit(1)

    full_path = os.path.abspath(script_path)

    # Modify sys.argv to pass script arguments to the executed script
    sys.argv = args.script

    runpy.run_path(full_path, run_name="__main__")


if __name__ == "__main__":
    main()
