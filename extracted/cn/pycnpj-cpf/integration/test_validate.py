import pytest
from click.testing import CliRunner

from pycnpj_cpf.cli import main, validate

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.high
@pytest.mark.parametrize(
    "value",
    [
        "848.044.710-90",
        "998.817.900-69",
        "895.761.04050",
        "71.418.067/0001-99",
        "96971115000100",
        "99.696.7540001-95",
    ],
)
def test_positive_call_validate_command(value):
    """Test command validate."""
    result = cmd.invoke(validate, ["--value", value])
    assert result.exit_code == 0


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize(
    "wrong_command", ["val", "validaty", "verify", "check"]
)
def test_negative_call_validate_command(wrong_command):
    """Test command validate."""
    result = cmd.invoke(main, wrong_command, "--value=96971115000100")
    assert result.exit_code != 0
    assert f"No such command '{wrong_command}'." in result.output
