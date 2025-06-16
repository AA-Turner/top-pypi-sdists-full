import pytest
from click.testing import CliRunner

from pycnpj_cpf import __main__
from pycnpj_cpf.cli import main

cli_runner = CliRunner()


@pytest.mark.unit
def test_invalid_entry_point_should_return_status_code_0():
    """Tests the pycnpj_cpf command to ensure it returns an exit code of 0 even
    in the case of invalid inputs.
    """

    out = cli_runner.invoke(main)
    assert out.exit_code == 0


@pytest.mark.unit
def test_main_entry_point_execution():
    """Tests the main entry point of the main module using the __main__.main
    command.
    """

    out = cli_runner.invoke(__main__.main)
    assert out.exit_code == 0
