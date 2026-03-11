import subprocess


def test_debug_all_cli_help():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.testing.debug_all",
            "--help",
        ],
        check=True,
    )


def test_debug_all_cli_version():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.testing.debug_all",
            "--version",
        ],
        check=True,
    )
