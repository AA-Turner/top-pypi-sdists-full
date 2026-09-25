import copy
import logging
import os
import pathlib
import stat
import tempfile

from unittest import mock

import pytest

from snowflake.core import simple_file_logging
from snowflake.core.stage import AwsCredentials, FileTransferMaterial, PresignedUrlRequest, Stage


posix_only = pytest.mark.skipif(os.name != "posix", reason="POSIX file permissions")


@pytest.fixture(scope="function", autouse=True)
def backup_reset_logging():
    logger = logging.getLogger("snowflake.core")
    original_level = logger.level
    original_handlers = copy.deepcopy(logger.handlers)
    try:
        yield
    finally:
        logger.level = original_level
        logger.handlers = original_handlers


def _mode(path: pathlib.Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


def test_simple_file_logging_custom_path(tmp_path):
    temp_log_file = tmp_path / "asd.log"
    simple_file_logging(temp_log_file, level=logging.INFO)
    logger = logging.getLogger("snowflake.core")
    logger.info("simulated log message")
    logger.debug("shouldn't be in the file")
    logged_file = temp_log_file.read_text()
    assert "simulated log message" in logged_file
    assert "shouldn't be in the file" not in logged_file
    if os.name == "posix":
        assert _mode(temp_log_file) == 0o600


def test_simple_file_logging():
    temp_log_file = pathlib.Path(tempfile.gettempdir()) / "snowflake_core.log"
    simple_file_logging()
    logger = logging.getLogger("snowflake.core")
    logger.info("simulated log message")
    logger.debug("shouldn't be in the file")
    logged_file = temp_log_file.read_text()
    assert "simulated log message" in logged_file
    assert "shouldn't be in the file" in logged_file
    if os.name == "posix":
        assert _mode(temp_log_file) == 0o600


@posix_only
def test_simple_file_logging_created_file_is_0600_despite_umask(tmp_path):
    log_file = tmp_path / "new.log"
    old_umask = os.umask(0o000)
    try:
        simple_file_logging(log_file)
    finally:
        os.umask(old_umask)
    assert _mode(log_file) == 0o600


@posix_only
def test_simple_file_logging_tightens_existing_mode(tmp_path):
    log_file = tmp_path / "wide.log"
    log_file.touch()
    log_file.chmod(0o644)
    simple_file_logging(log_file)
    assert _mode(log_file) == 0o600


@posix_only
def test_simple_file_logging_rejects_foreign_owner(tmp_path, monkeypatch):
    log_file = tmp_path / "stolen.log"
    log_file.write_text("")
    real_fstat = os.fstat

    def fake_fstat(fd: int):
        file_stat = real_fstat(fd)
        return mock.Mock(st_mode=file_stat.st_mode, st_uid=file_stat.st_uid + 1)

    monkeypatch.setattr(os, "fstat", fake_fstat)
    with pytest.raises(PermissionError, match="not owned by the current user"):
        simple_file_logging(log_file)
    assert log_file.read_text() == ""


@posix_only
def test_simple_file_logging_rejects_non_regular_file(tmp_path, monkeypatch):
    log_file = tmp_path / "not-a-file.log"
    log_file.write_text("")
    real_fstat = os.fstat

    def fake_fstat(fd: int):
        file_stat = real_fstat(fd)
        return mock.Mock(st_mode=stat.S_IFIFO, st_uid=file_stat.st_uid)

    monkeypatch.setattr(os, "fstat", fake_fstat)
    with pytest.raises(PermissionError, match="regular file"):
        simple_file_logging(log_file)


@posix_only
def test_simple_file_logging_rejects_symlink(tmp_path):
    if not hasattr(os, "O_NOFOLLOW"):
        pytest.skip("O_NOFOLLOW is not available")
    target = tmp_path / "target.log"
    target.write_text("original")
    link = tmp_path / "link.log"
    link.symlink_to(target)
    with pytest.raises(PermissionError, match="symlink"):
        simple_file_logging(link)
    assert target.read_text() == "original"


def test_secret_logging(caplog, stages):
    """This test makes sure that secret tokens are not logged."""
    with caplog.at_level(logging.DEBUG, "snowflake.core"):
        with mock.patch("snowflake.core._generated.api_client.ApiClient.request"):
            stages.create(
                Stage(
                    name="test_stage",
                    credentials=AwsCredentials(
                        aws_key_id="key_id_pwnd", aws_token="token_pwnd", aws_secret_key="key_pwnd"
                    ),
                )
            )
    assert "pwnd" not in caplog.text


def test_presigned_url_logging(caplog, stages):
    """This test makes sure that presigned URLs are not logged."""
    response = mock.MagicMock(
        status=200,
        reason="OK",
        data=FileTransferMaterial(presigned_url="https://bucket.example/pii.csv?X-Amz-Signature=pwnd").to_json(),
    )
    with caplog.at_level(logging.DEBUG, "snowflake.core"):
        with mock.patch("snowflake.core._generated.api_client.ApiClient.request", return_value=response):
            stages["test_stage"].get_presigned_url("my_file", PresignedUrlRequest())
    assert "pwnd" not in caplog.text
