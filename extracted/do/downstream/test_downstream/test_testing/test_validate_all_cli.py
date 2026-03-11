import subprocess


def test_validate_all_cli_help():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.testing.validate_all",
            "--help",
        ],
        check=True,
    )


def test_validate_all_cli_version():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.testing.validate_all",
            "--version",
        ],
        check=True,
    )
