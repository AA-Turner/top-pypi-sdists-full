import logging
import logging.config

import pytest
import simplejson as json  # type: ignore[import-untyped]

from fluidattacks_core.logging import PRODUCT_LOGGING


def _production_setup(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CI_COMMIT_REF_NAME", "trunk")


def _developer_setup(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CI_COMMIT_REF_NAME", "developeratfluid")


@pytest.mark.parametrize(
    "product_id, job_id, queue_name, expected_service_name",  # noqa: PT006
    [
        # Interacts running in EC2
        ("interacts", None, None, "interacts"),
        # Labels running in a Batch Job
        ("labels", "111", "skims", "labels/skims"),
        # Integrates scheduler running in a Batch Job
        ("integrates", "111", "integrates_large", "integrates/integrates_large"),
    ],
)
def test_json_formatter_uses_envs_to_fill_keys(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    product_id: str,
    job_id: str,
    queue_name: str,
    expected_service_name: str,
) -> None:
    _production_setup(monkeypatch)
    monkeypatch.setenv("PRODUCT_ID", product_id)
    if job_id is not None:
        monkeypatch.setenv("AWS_BATCH_JOB_ID", job_id)
    if queue_name is not None:
        monkeypatch.setenv("AWS_BATCH_JQ_NAME", queue_name)

    logging.config.dictConfig(PRODUCT_LOGGING)
    logger = logging.getLogger("product")

    logger.critical("A critical message")

    output = capsys.readouterr()
    log_entry = json.loads(output.out)

    assert log_entry["service.name"] == expected_service_name
    assert log_entry["dd.service"] == expected_service_name


def test_json_formatter_adds_keys_for_exception(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _production_setup(monkeypatch)

    logging.config.dictConfig(PRODUCT_LOGGING)
    logger = logging.getLogger("product")

    try:
        raise ValueError("Value error found")  # noqa: TRY301
    except ValueError:
        logger.exception("A exception was caught")

    output = capsys.readouterr()
    log_entry = json.loads(output.out)

    assert log_entry["level"] == "ERROR"
    assert log_entry["name"] == "product"
    assert log_entry["message"] == "A exception was caught"

    assert log_entry["error.type"] == "ValueError"
    assert log_entry["error.message"] == "Value error found"
    assert "error.stack" in log_entry


def test_json_formatter_adds_keys_with_extra_fields(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _production_setup(monkeypatch)

    logging.config.dictConfig(PRODUCT_LOGGING)
    logger = logging.getLogger("product")

    logger.info("A info message", extra={"trace_id": "111", "span_id": "222", "other.tag": "val"})

    output = capsys.readouterr()
    log_entry = json.loads(output.out)

    assert log_entry["trace_id"] == "111"
    assert log_entry["span_id"] == "222"
    assert log_entry["other.tag"] == "val"


def test_colorful_formatter_uses_colors_for_warning(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _developer_setup(monkeypatch)

    logging.config.dictConfig(PRODUCT_LOGGING)
    logger = logging.getLogger("product")

    logger.warning("A warning message")

    output = capsys.readouterr()
    log_message = output.out

    assert "\x1b[33;1m" in log_message
    assert "\x1b[0m" in log_message
    assert "[WARNING] [product]" in log_message
    assert "A warning message" in log_message
