import logging
import uuid

from orchestra_sdk.check_environment import validate_environment


class TestCheckEnvironment:
    def test_null_os_environ(self, mocker, caplog):
        mocker.patch.dict("os.environ", clear=True)
        with caplog.at_level(logging.WARNING):
            validate_environment()
        assert (
            "orchestra_sdk.check_environment",
            30,
            "No environment variables loaded",
        ) in caplog.record_tuples

    def test_missing_env_vars(self, mocker, caplog):
        mocker.patch.dict("os.environ", clear=True)
        mocker.patch.dict(
            "os.environ",
            {
                "somekey": "somevalue",
            },
        )
        with caplog.at_level(logging.WARNING):
            validate_environment()
        assert (
            "orchestra_sdk.check_environment",
            logging.WARNING,
            "Missing environment variables: ORCHESTRA_TASK_RUN_ID",
        ) in caplog.record_tuples

    def test_malformed_env_vars(self, mocker, caplog):
        mocker.patch.dict("os.environ", clear=True)
        mocker.patch.dict(
            "os.environ",
            {
                "ORCHESTRA_TASK_RUN_ID": "task_run_id",
            },
        )
        with caplog.at_level(logging.ERROR):
            validate_environment()
        assert (
            "orchestra_sdk.check_environment",
            logging.ERROR,
            "Error processing environment variables: badly formed hexadecimal UUID string",
        ) in caplog.record_tuples

    def test_valid_env(self, mocker, caplog):
        mock_task_run_id = uuid.uuid4()
        mocker.patch.dict("os.environ", clear=True)
        mocker.patch.dict(
            "os.environ",
            {
                "ORCHESTRA_TASK_RUN_ID": str(mock_task_run_id),
            },
        )
        assert validate_environment() == mock_task_run_id
