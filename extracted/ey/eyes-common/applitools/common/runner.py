from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING

from .command_executor import CommandExecutor, ManagerType
from .config import DEFAULT_ALL_TEST_RESULTS_TIMEOUT
from .connection import TimeoutError
from .errors import DiffsFoundError, EyesError, NewTestError, TestFailedError
from .protocol import USDKProtocol
from .schema import demarshal_close_manager_results, demarshal_server_info
from .test_results import TestResultsSummary

if TYPE_CHECKING:
    from typing import Optional, Union

    from . import Configuration


class RunnerOptions(object):
    concurrency = 5
    _mask_log = False
    _remove_duplicate_tests = None

    def test_concurrency(self, value):
        # type: (int) -> RunnerOptions
        self.concurrency = value
        return self

    def remove_duplicate_tests(self, should_remove=True):
        # type: (bool) -> RunnerOptions
        self._remove_duplicate_tests = should_remove
        return self

    def mask_log(self, mask_log=True):
        self._mask_log = mask_log
        return self


class EyesRunner(object):
    AUTO_CLOSE_MODE_SYNC = True
    BASE_AGENT_ID = "eyes.sdk.python"
    Protocol = USDKProtocol

    def __init__(
        self,
        manager_type,  # type: ManagerType
        concurrency=None,  # type: Optional[int]
        is_legacy=None,  # type: Optional[bool]
        remove_duplicate_tests=None,  # type: Optional[bool]
        mask_log=None,  # type: Optional[bool]
    ):
        # type: (...) -> None
        self._connection_configuration = None
        self._remove_duplicate_tests = remove_duplicate_tests
        self._commands = CommandExecutor.get_instance(self.Protocol, mask_log)
        _, sdk_version = self.Protocol.SDK_INFO
        agent_id = "{}/{}".format(self.BASE_AGENT_ID, sdk_version)
        if is_legacy:
            self._ref = self._commands.core_make_manager(
                manager_type,
                legacy_concurrency=concurrency,
                agent_id=agent_id,
            )
        else:
            self._ref = self._commands.core_make_manager(
                manager_type,
                concurrency=concurrency,
                agent_id=agent_id,
            )

    def set_remove_duplicate_tests(self, should_remove):
        # type: (bool) -> None
        self._remove_duplicate_tests = should_remove

    @classmethod
    def get_server_info(cls):
        cmd = CommandExecutor.get_instance(cls.Protocol)
        result = cmd.server_get_info()
        return demarshal_server_info(result)

    def get_all_test_results(
        self, should_raise_exception=True, timeout=DEFAULT_ALL_TEST_RESULTS_TIMEOUT
    ):
        # type: (bool, Optional[int]) -> TestResultsSummary
        try:
            # Do not pass should_raise_exception because USDK raises untyped exceptions
            results = self._commands.manager_get_results(
                self._ref, should_raise_exception, self._remove_duplicate_tests, timeout
            )
        except TimeoutError:
            raise EyesError("Tests didn't finish in {} seconds".format(timeout))
        # We don't have server_url, api_key and proxy settings in runner
        # USDK should return them back as a part of TestResults
        structured_results = demarshal_close_manager_results(
            results, self._connection_configuration
        )
        for r in structured_results:
            if r.exception is not None:
                print("--- Test error. \n\tServer exception {}".format(r.exception))
            else:
                log_session_results_and_raise_exception(False, r.test_results)
        return structured_results

    def _set_connection_config(self, config):
        # type: (Configuration) -> None
        if self._connection_configuration is None:
            self._connection_configuration = config


class ClassicEyesRunner(EyesRunner):
    def __init__(self, options=RunnerOptions()):
        remove_duplicate_tests = options._remove_duplicate_tests  # noqa
        mask_log = options._mask_log  # noqa
        super(ClassicEyesRunner, self).__init__(
            ManagerType.CLASSIC,
            remove_duplicate_tests=remove_duplicate_tests,
            mask_log=mask_log,
        )


class VisualGridEyesRunner(EyesRunner):
    AUTO_CLOSE_MODE_SYNC = False

    def __init__(self, options_or_concurrency=RunnerOptions()):
        # type: (Union[RunnerOptions, int]) -> None
        if isinstance(options_or_concurrency, int):
            concurrency = options_or_concurrency * 5  # legacy factor
            remove_duplicate_tests = None
            is_legacy = True
            mask_log = None
        else:
            concurrency = options_or_concurrency.concurrency
            remove_duplicate_tests = (
                options_or_concurrency._remove_duplicate_tests  # noqa
            )
            mask_log = options_or_concurrency._mask_log  # noqa
            is_legacy = False
        super(VisualGridEyesRunner, self).__init__(
            ManagerType.UFG, concurrency, is_legacy, remove_duplicate_tests, mask_log
        )


def log_session_results_and_raise_exception(raise_ex, results):
    results_url = results.url
    scenario_id_or_name = results.name
    app_id_or_name = results.app_name
    if results.is_aborted:
        print("--- Test aborted.")
        if raise_ex:
            raise TestFailedError(results, scenario_id_or_name, app_id_or_name)
    elif results.is_unresolved:
        if results.is_new:
            print(
                "--- New test ended. \n\tPlease approve the new baseline at",
                results_url,
            )
            if raise_ex:
                raise NewTestError(results, scenario_id_or_name, app_id_or_name)
        else:
            print("--- Differences are found. \n\tSee details at", results_url)
            if raise_ex:
                raise DiffsFoundError(results, scenario_id_or_name, app_id_or_name)
    elif results.is_failed:
        print("--- Failed test ended. \n\tSee details at", results_url)
        if raise_ex:
            raise TestFailedError(results, scenario_id_or_name, app_id_or_name)
    else:
        print("--- Test passed. \n\tSee details at", results_url)
