import subprocess


def test_validate_one_cli_help():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.testing.validate_one",
            "--help",
        ],
        check=True,
    )


def test_validate_one_cli_version():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.testing.validate_one",
            "--version",
        ],
        check=True,
    )
