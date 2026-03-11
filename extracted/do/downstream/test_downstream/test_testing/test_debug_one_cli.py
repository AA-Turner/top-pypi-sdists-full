import subprocess


def test_debug_one_cli_help():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.testing.debug_one",
            "--help",
        ],
        check=True,
    )


def test_debug_one_cli_version():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.testing.debug_one",
            "--version",
        ],
        check=True,
    )
