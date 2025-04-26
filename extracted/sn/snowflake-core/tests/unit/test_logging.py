import copy
import logging
import pathlib
import tempfile

from unittest import mock

import pytest

from snowflake.core import simple_file_logging
from snowflake.core.stage import AwsCredentials, Stage


@pytest.fixture(scope='function', autouse=True)
def backup_reset_logging():
    logger = logging.getLogger("snowflake.core")
    original_level = logger.level
    original_handlers = copy.deepcopy(logger.handlers)
    try:
        yield
    finally:
        logger.level = original_level
        logger.handlers = original_handlers


def test_simple_file_logging_custom_path(tmp_path):
    temp_log_file = tmp_path / "asd.log"
    simple_file_logging(temp_log_file, level=logging.INFO)
    logger = logging.getLogger("snowflake.core")
    logger.info("simulated log message")
    logger.debug("shouldn't be in the file")
    logged_file = temp_log_file.read_text()
    assert "simulated log message" in logged_file
    assert "shouldn't be in the file" not in logged_file


def test_simple_file_logging():
    temp_log_file =  pathlib.Path(tempfile.gettempdir()) / "snowflake_core.log"
    simple_file_logging()
    logger = logging.getLogger("snowflake.core")
    logger.info("simulated log message")
    logger.debug("shouldn't be in the file")
    logged_file = temp_log_file.read_text()
    assert "simulated log message" in logged_file
    assert "shouldn't be in the file" in logged_file


def test_secret_logging(caplog, stages):
    """This test makes sure that secret tokens are not logged."""
    with caplog.at_level(logging.DEBUG, "snowflake.core"):
        with mock.patch("snowflake.core.stage._generated.api_client.ApiClient.request"):
            stages.create(
                Stage(
                    name="test_stage",
                    credentials=AwsCredentials(
                        aws_key_id="key_id_pwnd",
                        aws_token="token_pwnd",
                        aws_secret_key="key_pwnd"
                    ),
                ),
            )
    assert "pwnd" not in caplog.text
