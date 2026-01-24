import logging
import sys

import pytest
import simplejson as json

from fluidattacks_core.logging import init_logging
from fluidattacks_core.logging.utils import set_telemetry_metadata


def _clear_setup(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AWS_LAMBDA_FUNCTION_NAME", raising=False)
    monkeypatch.delenv("AWS_BATCH_JOB_ID", raising=False)
    monkeypatch.delenv("PRODUCT_ID", raising=False)
    monkeypatch.delenv("CONTAINER_IMAGE", raising=False)
    monkeypatch.delenv("CI_JOB_ID", raising=False)
    monkeypatch.delenv("CI_JOB_URL", raising=False)


def _production_setup(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CI_COMMIT_REF_NAME", "trunk")


def _developer_setup(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CI_COMMIT_REF_NAME", "developeratfluid")


def _lambda_setup(monkeypatch: pytest.MonkeyPatch, function_name: str | None) -> None:
    if function_name:
        monkeypatch.setenv("AWS_LAMBDA_FUNCTION_NAME", function_name)


def _batch_setup(
    monkeypatch: pytest.MonkeyPatch,
    job_name: str | None,
    job_queue: str | None,
    product_id: str | None,
) -> None:
    monkeypatch.setenv("AWS_BATCH_JOB_ID", "111")
    if job_name:
        monkeypatch.setenv("JOB_DEFINITION_NAME", job_name)
    if job_queue:
        monkeypatch.setenv("AWS_BATCH_JQ_NAME", job_queue)
    if product_id:
        monkeypatch.setenv("PRODUCT_ID", product_id)


def _gitlab_pipeline_setup(monkeypatch: pytest.MonkeyPatch, product_id: str | None) -> None:
    monkeypatch.setenv("CI_JOB_ID", "111")
    monkeypatch.setenv("CI_JOB_URL", "https://gitlab.com/fluidattacks/skims/skims/-/jobs/111")
    if product_id:
        monkeypatch.setenv("PRODUCT_ID", product_id)


def _container_setup(
    monkeypatch: pytest.MonkeyPatch, container_image: str | None, product_id: str | None
) -> None:
    if container_image:
        monkeypatch.setenv("CONTAINER_IMAGE", container_image)
    if product_id:
        monkeypatch.setenv("PRODUCT_ID", product_id)


def test_init_logging_with_custom_config(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _developer_setup(monkeypatch)
    init_logging(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "test_handler": {
                    "class": "fluidattacks_core.logging.handlers.DebuggingHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "root": {
                "handlers": ["test_handler"],
                "level": "INFO",
            },
        }
    )

    logger = logging.getLogger("test_custom_config")
    logger.warning("Test message")

    output = capsys.readouterr()
    assert output.err == ""
    assert "[WARNING] [test_custom_config] Test message" in output.out


@pytest.mark.parametrize(
    ("function_name", "expected_source", "expected_service_name"),
    [
        ("integrates_streams_hooks", "lambda", "integrates_streams_hooks"),
        (None, "python", "unknown"),
    ],
)
def test_json_formatter_for_lambdas(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    function_name: str,
    expected_source: str,
    expected_service_name: str,
) -> None:
    _clear_setup(monkeypatch)
    _lambda_setup(monkeypatch, function_name)
    _production_setup(monkeypatch)
    init_logging()

    logger = logging.getLogger("test_lambda")
    logger.info("Test message")

    output = capsys.readouterr()
    log_entry = json.loads(output.err)
    assert log_entry["ddsource"] == expected_source
    assert log_entry["dd.service"] == expected_service_name


@pytest.mark.parametrize(
    ("job_name", "job_queue", "product_id", "expected_source", "expected_service_name"),
    [
        ("skims_process", "skims_large", "skims", "batch", "skims"),
        ("skims_process", "skims_large", None, "batch", "skims_process"),
        (None, None, "skims", "batch", "skims"),
        (None, None, None, "batch", "unknown"),
        (None, "skims_large", None, "batch", "from-skims_large"),
    ],
)
def test_json_formatter_for_batch(  # noqa: PLR0913
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    job_name: str,
    job_queue: str,
    product_id: str,
    expected_source: str,
    expected_service_name: str,
) -> None:
    _clear_setup(monkeypatch)
    _batch_setup(monkeypatch, job_name, job_queue, product_id)
    _production_setup(monkeypatch)
    init_logging()

    logger = logging.getLogger("test_batch")
    logger.info("Test message")

    output = capsys.readouterr()
    log_entry = json.loads(output.err)
    assert log_entry["ddsource"] == expected_source
    assert log_entry["dd.service"] == expected_service_name
    assert log_entry["job_metadata.id"] == "111"


@pytest.mark.parametrize(
    ("container_image", "product_id", "expected_source", "expected_service_name"),
    [
        ("fluidattacks/forces", "forces", "container", "forces"),
        (None, "forces", "python", "forces"),
        (None, None, "python", "unknown"),
    ],
)
def test_json_formatter_for_container(  # noqa: PLR0913
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    container_image: str,
    product_id: str,
    expected_source: str,
    expected_service_name: str,
) -> None:
    _clear_setup(monkeypatch)
    _container_setup(monkeypatch, container_image, product_id)
    _production_setup(monkeypatch)
    init_logging()

    logger = logging.getLogger("test_container")
    logger.info("Test message")

    output = capsys.readouterr()
    log_entry = json.loads(output.err)
    assert log_entry["ddsource"] == expected_source
    assert log_entry["dd.service"] == expected_service_name


@pytest.mark.parametrize(
    ("product_id", "expected_source", "expected_service_name"),
    [
        ("skims", "ci/gitlab_ci", "skims"),
        (None, "ci/gitlab_ci", "unknown"),
    ],
)
def test_json_formatter_for_gitlab_ci(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    product_id: str,
    expected_source: str,
    expected_service_name: str,
) -> None:
    _clear_setup(monkeypatch)
    _gitlab_pipeline_setup(monkeypatch, product_id)
    _production_setup(monkeypatch)
    init_logging()

    logger = logging.getLogger("test_pipeline")
    logger.info("Test message")

    output = capsys.readouterr()
    log_entry = json.loads(output.err)
    assert log_entry["ddsource"] == expected_source
    assert log_entry["dd.service"] == expected_service_name


def test_uncaught_exception_logging(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _clear_setup(monkeypatch)
    _production_setup(monkeypatch)
    monkeypatch.setenv("PRODUCT_ID", "universe")

    init_logging()

    error = ValueError("This is an uncaught exception")

    # Simulate an uncaught exception
    sys.excepthook(error.__class__, error, error.__traceback__)

    output = capsys.readouterr()
    log_entry = json.loads(output.err)

    assert log_entry["ddsource"] == "python"
    assert log_entry["dd.service"] == "universe"

    assert log_entry["name"] == "unhandled"
    assert log_entry["level"] == "CRITICAL"
    assert log_entry["error.kind"] == "ValueError"
    assert log_entry["error.message"] == "This is an uncaught exception"


def test_json_formatter_adds_keys_for_exception(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _production_setup(monkeypatch)

    init_logging()
    logger = logging.getLogger("product")

    try:
        raise ValueError("Value error found")  # noqa: TRY301, EM101, TRY003
    except ValueError:
        logger.exception("A exception was caught")

    output = capsys.readouterr()
    log_entry = json.loads(output.err)

    assert log_entry["level"] == "ERROR"
    assert log_entry["name"] == "product"
    assert log_entry["message"] == "A exception was caught"

    assert log_entry["error.kind"] == "ValueError"
    assert log_entry["error.message"] == "Value error found"
    assert "error.stack" in log_entry


def test_json_formatter_adds_keys_with_extra_fields(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _production_setup(monkeypatch)

    init_logging()
    logger = logging.getLogger("product")

    logger.info("A info message", extra={"trace_id": "111", "span_id": "222", "other.tag": "val"})

    output = capsys.readouterr()
    log_entry = json.loads(output.err)

    assert log_entry["trace_id"] == "111"
    assert log_entry["span_id"] == "222"
    assert log_entry["other.tag"] == "val"


def test_json_formatter_adds_telemetry_metadata(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _production_setup(monkeypatch)

    init_logging()
    logger = logging.getLogger("product")
    set_telemetry_metadata({"trace_id": "111", "span_id": "222", "other.tag": "val"})

    logger.info("A info message")

    output = capsys.readouterr()
    log_entry = json.loads(output.err)

    assert log_entry["trace_id"] == "111"
    assert log_entry["span_id"] == "222"
    assert log_entry["other.tag"] == "val"


def test_colorful_formatter_uses_colors_for_warning(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _developer_setup(monkeypatch)

    init_logging()
    logger = logging.getLogger("product")

    logger.warning("A warning message")

    output = capsys.readouterr()
    log_message = output.err

    assert "\x1b[33;1m" in log_message
    assert "\x1b[0m" in log_message
    assert "[WARNING] [product]" in log_message
    assert "A warning message" in log_message
