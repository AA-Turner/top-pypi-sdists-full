import importlib
import json
import logging
import os
import sys
from datetime import datetime as real_datetime
from datetime import timezone
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest
from supertokens_python import InputAppInfo, SupertokensConfig, init
from supertokens_python.constants import VERSION
from supertokens_python.logger import (
    NAMESPACE,
    enable_debug_logging,
    log_debug_message,
    streamFormatter,
)
from supertokens_python.recipe import session

from tests.utils import get_new_core_app_url, reset


class LoggerTests(TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog: pytest.LogCaptureFixture):
        # caplog is the pytest fixture to capture all logs
        self._caplog = caplog  # pylint: disable=attribute-defined-outside-init

    def setup_method(self, _):
        # Setting the log level to a higher level so debug logs are not printed
        logging.getLogger(NAMESPACE).setLevel(logging.ERROR)
        reset()

    def teardown_method(self, _):
        self._caplog.clear()
        reset()

    @patch("supertokens_python.logger.datetime", wraps=real_datetime)
    def test_1_json_msg_format(self, datetime_mock: MagicMock):
        enable_debug_logging()
        datetime_mock.now.return_value = real_datetime(2000, 1, 1, tzinfo=timezone.utc)

        with self.assertLogs(level="DEBUG") as captured:
            log_debug_message("API replied with status 200")

        record = captured.records[0]
        out = json.loads(record.msg)

        assert out == {
            "t": "2000-01-01T00:00:00+00Z",
            "sdkVer": VERSION,
            "message": "API replied with status 200",
            "file": "../tests/test_logger.py:46",
        }

    @staticmethod
    def test_2_stream_formatter_format():
        assert (
            streamFormatter._fmt  # pylint: disable=protected-access
            == "{name} {message}\n"
        )

    def test_3_logger_config_with_debug_false(self):
        init(
            supertokens_config=SupertokensConfig(get_new_core_app_url()),
            app_info=InputAppInfo(
                app_name="SuperTokens Demo",
                api_domain="api.supertokens.io",
                website_domain="supertokens.io",
                api_base_path="/",
            ),
            framework="fastapi",
            recipe_list=[session.init(anti_csrf="VIA_CUSTOM_HEADER")],
            debug=False,
        )

        logMsg = "log test - valid log"
        log_debug_message(logMsg)

        assert logMsg not in self._caplog.text

    def test_4_logger_config_with_debug_true(self):
        init(
            supertokens_config=SupertokensConfig(get_new_core_app_url()),
            app_info=InputAppInfo(
                app_name="SuperTokens Demo",
                api_domain="api.supertokens.io",
                website_domain="supertokens.io",
                api_base_path="/",
            ),
            framework="fastapi",
            recipe_list=[session.init(anti_csrf="VIA_CUSTOM_HEADER")],
            debug=True,
        )

        logMsg = "log test - valid log"
        log_debug_message(logMsg)

        assert logMsg in self._caplog.text

    def test_5_logger_config_with_debug_not_set(self):
        init(
            supertokens_config=SupertokensConfig(get_new_core_app_url()),
            app_info=InputAppInfo(
                app_name="SuperTokens Demo",
                api_domain="api.supertokens.io",
                website_domain="supertokens.io",
                api_base_path="/",
            ),
            framework="fastapi",
            recipe_list=[session.init(anti_csrf="VIA_CUSTOM_HEADER")],
        )

        logMsg = "log test - valid log"
        log_debug_message(logMsg)

        assert logMsg not in self._caplog.text

    def test_6_logger_config_with_env_var(self):
        os.environ["SUPERTOKENS_DEBUG"] = "1"

        # environment variable was already set when the logger module was imported
        # since its being changed for the test, the module needs to be reloaded.
        importlib.reload(sys.modules["supertokens_python.logger"])
        init(
            supertokens_config=SupertokensConfig(get_new_core_app_url()),
            app_info=InputAppInfo(
                app_name="SuperTokens Demo",
                api_domain="api.supertokens.io",
                website_domain="supertokens.io",
                api_base_path="/",
            ),
            framework="fastapi",
            recipe_list=[session.init(anti_csrf="VIA_CUSTOM_HEADER")],
        )

        logMsg = "log test - valid log"
        log_debug_message(logMsg)

        # Unset the environment variable
        del os.environ["SUPERTOKENS_DEBUG"]

        assert logMsg in self._caplog.text
