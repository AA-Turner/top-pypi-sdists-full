import json
import logging
import os
import uuid

import pytest
import responses

from orchestra_sdk.enum import TaskRunStatus
from orchestra_sdk.orchestra import OrchestraSDK

logger = logging.getLogger(__name__)

MOCK_API_KEY = "mock_api_key"
MOCK_WEBHOOK_URL = "http://orchestra-webhook-123.com/update"


class TestOrchestraSDK:
    @pytest.fixture
    def mock_task_run_id(self):
        return uuid.uuid4()

    @pytest.fixture
    def test_instance(self, mocker, mock_task_run_id) -> OrchestraSDK:
        mocker.patch.dict(
            "os.environ",
            {
                "ORCHESTRA_WEBHOOK_URL": MOCK_WEBHOOK_URL,
                "ORCHESTRA_TASK_RUN_ID": str(mock_task_run_id),
            },
        )
        return OrchestraSDK(api_key=MOCK_API_KEY)

    @responses.activate
    def test_webhook_non_200(self, caplog, test_instance: OrchestraSDK):
        @test_instance.run()
        def test_function():
            logger.info("A")

        responses.add(
            responses.POST,
            MOCK_WEBHOOK_URL,
            status=404,
            json={"error": "Could not find API"},
        )

        with caplog.at_level(logging.ERROR):
            test_function()

        assert caplog.record_tuples == [
            (
                "orchestra_sdk.http",
                40,
                "Failed request (404): {'error': 'Could not find API'}",
            ),
            (
                "orchestra_sdk.http",
                40,
                "Failed request (404): {'error': 'Could not find API'}",
            ),
        ]

    @responses.activate
    def test_works_func_succeeded(self, mock_task_run_id, test_instance: OrchestraSDK):
        @test_instance.run()
        def test_function():
            logger.info("A")
            return 1

        requests_made = responses.add(
            responses.POST,
            MOCK_WEBHOOK_URL,
            status=200,
        )

        assert test_function() == 1

        assert requests_made.call_count == 2
        assert json.loads(requests_made.calls[0].request.body or "{}") == {
            "event_type": "UPDATE_STATUS",
            "metadata": {},
            "task_run_id": str(mock_task_run_id),
            "message": "test_function started.",
            "status": "RUNNING",
        }
        assert json.loads(requests_made.calls[1].request.body or "{}") == {
            "event_type": "UPDATE_STATUS",
            "metadata": {},
            "task_run_id": str(mock_task_run_id),
            "message": "test_function succeeded.",
            "status": "SUCCEEDED",
        }

    @responses.activate
    def test_works_func_failed(self, mock_task_run_id, test_instance: OrchestraSDK):
        @test_instance.run()
        def test_function():
            raise Exception("ERROR IN YOUR FUNCTION!")

        requests_made = responses.add(
            responses.POST,
            MOCK_WEBHOOK_URL,
            status=200,
        )

        test_function()

        assert requests_made.call_count == 2
        assert json.loads(requests_made.calls[0].request.body or "{}") == {
            "event_type": "UPDATE_STATUS",
            "metadata": {},
            "task_run_id": str(mock_task_run_id),
            "message": "test_function started.",
            "status": "RUNNING",
        }
        assert json.loads(requests_made.calls[1].request.body or "{}") == {
            "event_type": "UPDATE_STATUS",
            "metadata": {},
            "task_run_id": str(mock_task_run_id),
            "message": "test_function failed. Error: ERROR IN YOUR FUNCTION!",
            "status": "FAILED",
        }

    def test_orchestra_update_task_invalid_env(self):
        o = OrchestraSDK(api_key="test")
        assert o.update_task(status=TaskRunStatus.FAILED) is False

    @responses.activate
    def test_update_task_success(self, test_instance: OrchestraSDK):
        mock_request = responses.post(test_instance.webhook_url, status=200)
        assert test_instance.update_task(status=TaskRunStatus.SUCCEEDED)
        assert json.loads(mock_request.calls[0].request.body or "{}") == {
            "event_type": "UPDATE_STATUS",
            "metadata": {},
            "status": "SUCCEEDED",
            "task_run_id": str(test_instance.task_run_id),
        }

    def test_sending_logfile_no_file_found(self, caplog, test_instance: OrchestraSDK):
        test_instance.log_file = "non_existent.log"
        test_instance.send_logs = True

        @test_instance.run()
        def test_function():
            pass

        with caplog.at_level(logging.WARNING):
            test_function()

        assert (
            "orchestra_sdk.orchestra",
            30,
            "Log file 'non_existent.log' not found.",
        ) in caplog.record_tuples

    @pytest.fixture
    def post_cleanup_logs(self, test_instance: OrchestraSDK):
        yield
        if os.path.exists(test_instance.log_file):
            os.remove(test_instance.log_file)

    @responses.activate
    def test_sending_logfile_error_on_upload(
        self, test_instance: OrchestraSDK, caplog, post_cleanup_logs
    ):
        test_instance.log_file = "test_output.log"
        test_instance.send_logs = True

        responses.post(test_instance.webhook_url, status=200)  # RUNNING update
        responses.post(test_instance.webhook_url, status=200)  # COMPLETED update

        responses.post(test_instance.webhook_url, body=Exception("Could not process server side!"))

        @test_instance.run()
        def test_function():
            # Setup logging configuration
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)

            # File handler
            file_handler = logging.FileHandler(test_instance.log_file)
            file_handler.setLevel(logging.INFO)

            # Adding handlers to the logger
            logger.addHandler(file_handler)

            logger.info("Hello, World!")

        with caplog.at_level(logging.ERROR):
            test_function()

        assert (
            "orchestra_sdk.http",
            40,
            f"Could not send POST request to {test_instance.webhook_url} - Could not process server side!",
        ) in caplog.record_tuples

    @responses.activate
    def test_sending_logfile_success(self, test_instance: OrchestraSDK, post_cleanup_logs):
        test_instance.log_file = "test_output.log"
        test_instance.send_logs = True

        requests_made = responses.post(test_instance.webhook_url, status=200)

        @test_instance.run()
        def test_function():
            # Setup logging configuration
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)

            # File handler
            file_handler = logging.FileHandler(test_instance.log_file)
            file_handler.setLevel(logging.INFO)

            # Adding handlers to the logger
            logger.addHandler(file_handler)

            logger.info("Hello, World!")
            raise Exception("This is a test exception")

        test_function()

        assert requests_made.call_count == 3
        assert json.loads(requests_made.calls[2].request.body or "{}") == {
            "event_type": "LOG",
            "metadata": {},
            "log_name": test_instance.log_file,
            "data": "Hello, World!\n",
            "task_run_id": str(test_instance.task_run_id),
        }

    def test_configure_aws_lambda_event(self):
        o = OrchestraSDK(api_key="test", log_file="test.log", send_logs=True)
        assert o.http_client is None

        mock_task_run_id = uuid.uuid4()
        o.configure_aws_lambda_event(
            {
                "orchestra_task_run_id": str(mock_task_run_id),
                "orchestra_webhook_url": MOCK_WEBHOOK_URL,
            }
        )

        assert o.task_run_id == mock_task_run_id
        assert o.log_file.startswith(f"/tmp/{mock_task_run_id}_")
        assert o.webhook_url == MOCK_WEBHOOK_URL
        assert o.http_client is not None
