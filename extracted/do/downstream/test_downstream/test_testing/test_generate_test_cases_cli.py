import subprocess


def test_generate_test_cases_cli_smoke():
    result = subprocess.run(
        [
            "python3",
            "-m",
            "downstream.testing.generate_test_cases",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    lines = result.stdout.strip().split("\n")
    assert len(lines) > 0
    # verify output is pairs of integers
    S, T = lines[0].split()
    int(S)
    int(T)
