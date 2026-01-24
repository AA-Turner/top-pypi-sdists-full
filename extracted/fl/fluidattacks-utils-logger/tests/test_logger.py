import json
import logging
from io import (
    StringIO,
)

import pytest
from fa_purity import (
    Cmd,
)

from fluidattacks_utils_logger.env import (
    Envs,
)
from fluidattacks_utils_logger.handlers import (
    LoggingConf,
    logger_handler_with_env,
)
from fluidattacks_utils_logger.levels import (
    LoggingLvl,
)
from fluidattacks_utils_logger.logger import (
    set_logger,
)


def test_json_formatter_in_production() -> None:
    logger_name = "test_json_format"
    output_stream = StringIO()

    def _test() -> Cmd[None]:
        test_logger = logging.getLogger(logger_name)

        test_message = "Test message for JSON formatting"
        test_logger.info(test_message)

        output_content = output_stream.getvalue()
        try:
            formatted_output: dict[str, str] = json.loads(output_content.strip())
            assert "ddsource" in formatted_output
            assert "dd.service" in formatted_output
            assert "dd.version" in formatted_output
            assert formatted_output["ddsource"] == "python"
            assert formatted_output["message"] == test_message

        except json.JSONDecodeError as exc:
            raise RuntimeError from exc

        return Cmd.wrap_value(None)

    test_cmd = set_logger(
        name=logger_name,
        lvl=LoggingLvl.INFO,
        handlers=(
            logger_handler_with_env(
                conf=LoggingConf(
                    app_name="observes",
                    app_type="etl",
                    app_version="1.0.0",
                    release_stage=Envs.PROD,
                ),
                target=output_stream,
                env=Envs.PROD,
            ),
        ),
    ).bind(lambda _: _test())

    with pytest.raises(SystemExit):
        test_cmd.compute()


def test_colorful_formatter_in_development() -> None:
    logger_name = "test_color_format"
    output_stream = StringIO()

    def _test() -> Cmd[None]:
        test_logger = logging.getLogger(logger_name)

        test_message = "Test error message for colorful formatting"
        test_logger.error(test_message)

        output_content = output_stream.getvalue().strip()
        assert "[ERROR]" in output_content
        assert f"[{logger_name}]" in output_content
        assert test_message in output_content

        return Cmd.wrap_value(None)

    test_cmd = set_logger(
        name=logger_name,
        lvl=LoggingLvl.INFO,
        handlers=(
            logger_handler_with_env(
                conf=LoggingConf(
                    app_name="observes",
                    app_type="etl",
                    app_version="1.0.0",
                    release_stage=Envs.DEV,
                ),
                target=output_stream,
                env=Envs.DEV,
            ),
        ),
    ).bind(lambda _: _test())

    with pytest.raises(SystemExit):
        test_cmd.compute()
