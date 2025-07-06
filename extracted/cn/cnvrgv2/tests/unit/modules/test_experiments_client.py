import pytest

from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.workflows import ExperimentsClient


class TestExperimentsClient:

    def test_experiment_with_csv_injection_in_title_error(self, empty_project):
        experiments_client = ExperimentsClient(empty_project)
        malicious_title = "=cmd|’ /C notepad’!‘A1’"

        with pytest.raises(CnvrgArgumentsError):
            experiments_client.create(title=malicious_title)

    def test_experiment_with_csv_injection_in_command_error(self, empty_project):
        experiments_client = ExperimentsClient(empty_project)
        malicious_command = "=cmd|’ /C notepad’!‘A1’"

        with pytest.raises(CnvrgArgumentsError):
            experiments_client.create(command=malicious_command)
