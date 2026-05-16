from dataclasses import dataclass
from enum import auto

from mstrio.api import test_center as tc_api
from mstrio.connection import Connection
from mstrio.server.test_center.commons import (
    IntegrityTest,
    IntegrityTestResult,
    _list_object_by_class,
)
from mstrio.types import ObjectSubTypes
from mstrio.utils.enum_helper import AutoUpperName
from mstrio.utils.helper import Dictable
from mstrio.utils.object_mapping import map_objects_list
from mstrio.utils.response_processors import test_center as tc_processors
from mstrio.utils.version_helper import class_version_handler, method_version_handler


@method_version_handler("11.5.0600")
def list_baseline_tests(
    connection: Connection,
    to_dictionary: bool = False,
    to_dataframe: bool = False,
    limit: int | None = None,
    **filters,
):
    """Get all Baseline Test definitions stored on the configured storage.

    Args:
        connection(object): Strategy One connection object returned
            by 'connection.Connection()'
        to_dictionary(bool, optional): if True, return Baseline Tests as list
            of dicts.
        to_dataframe(bool, optional): if True, return Baseline Tests as
            Pandas DataFrame
        limit(int): limit the number of elements returned. If `None` (default),
            all objects are returned.
        **filters: Available filter parameters: ['name', 'id', 'description',
            'date_created', 'date_modified', 'version', 'acg', 'owner']

    Returns:
        List of Baseline Test objects in specified format
            (objects, dicts, or DataFrame)
    """
    return BaselineTest._list_all(
        connection=connection,
        to_dictionary=to_dictionary,
        to_dataframe=to_dataframe,
        limit=limit,
        **filters,
    )


@method_version_handler("11.5.0600")
def list_baseline_results(
    connection: Connection,
    to_dictionary: bool = False,
    to_dataframe: bool = False,
    limit: int | None = None,
    **filters,
):
    """Get all Baselines stored on the configured storage.

    Args:
        connection(object): Strategy One connection object returned
            by 'connection.Connection()'
        to_dictionary(bool, optional): if True, return Baselines as list
            of dicts.
        to_dataframe(bool, optional): if True, return Baselines as
            Pandas DataFrame
        limit(int): limit the number of elements returned. If `None` (default),
            all objects are returned.
        **filters: Available filter parameters: ['name', 'id', 'description',
            'date_created', 'date_modified', 'version', 'acg', 'owner']

    Returns:
        List of Baseline objects in specified format
            (objects, dicts, or DataFrame)
    """
    return Baseline._list_all(
        connection=connection,
        to_dictionary=to_dictionary,
        to_dataframe=to_dataframe,
        limit=limit,
        **filters,
    )


@class_version_handler("11.5.0600")
class Baseline(IntegrityTestResult):
    """Python representation of a Strategy One Baseline object, a result
        of a Baseline Test execution.

    Attributes:
        library_url: The Strategy Library URL of the baseline.
        status: The running status of the baseline test.
        preparation_status: The preparation status of the baseline test.
        summary: The summary of the comparison test result.
    """

    _API_GETTERS = {
        **IntegrityTestResult._API_GETTERS,
        (
            "date_created",
            "date_modified",
            "library_url",
            "status",
            "preparation_status",
        ): tc_api.get_baseline_result,
        "summary": tc_processors.get_baseline_result_summary,
    }
    _API_CANCEL = staticmethod(tc_api.cancel_baseline_run)
    _API_DELETE = staticmethod(tc_api.delete_baseline_result)
    _REST_ATTR_MAP = {
        **IntegrityTestResult._REST_ATTR_MAP,
        "baseline_id": "id",
        "integrity_test_id": "test_id",
        "test_object_baselines": "object_results",
    }

    def _init_variables(self, default_value=None, **kwargs):
        super()._init_variables(default_value, **kwargs)

        # _test_id can be set from from_dict source or from __init__ arg
        if not hasattr(self, "_test_id") or not self._test_id:
            self._test_id = kwargs.get("integrity_test_id", default_value)

        self._library_url = kwargs.get("library_url", default_value)
        self._status = kwargs.get("status", default_value)
        self._preparation_status = kwargs.get("preparation_status", default_value)

    @classmethod
    def _list_all(
        cls,
        connection: Connection,
        to_dictionary: bool = False,
        to_dataframe: bool = False,
        limit: int | None = None,
        **filters,
    ):
        filters = cls._python_to_rest(filters)
        return _list_object_by_class(
            cls=cls,
            connection=connection,
            api=tc_api.get_all_baseline_results,
            to_dictionary=to_dictionary,
            to_dataframe=to_dataframe,
            limit=limit,
            **filters,
        )

    @property
    def library_url(self) -> str:
        """Strategy Library URL of the baseline."""
        return self._library_url

    @property
    def status(self) -> str:
        """The running status of the baseline test."""
        return self._status

    @property
    def preparation_status(self) -> str:
        """The preparation status of the baseline test."""
        return self._preparation_status


class PromptAnswerSource(AutoUpperName):
    """Prompt answer source enumeration.

    Specifies the precedence for choosing prompt answers during baseline
    testing.
    """

    PERSONAL_ANSWER = auto()
    DEFAULT_ANSWER = auto()
    CUSTOM_ANSWER = auto()


@dataclass
class BaselineTestSettings(Dictable):
    """Settings for configuring a Baseline Test.

    Controls which content types are captured and how prompts are answered
    during baseline testing.

    Attributes:
        dashboard_sql_enabled: Whether to capture dashboard SQL.
        dashboard_data_enabled: Whether to capture dashboard data.
        dashboard_visualization_screenshot_enabled: Whether to capture
            dashboard visualization screenshots.
        cube_data_enabled: Whether to capture cube data.
        cube_sql_enabled: Whether to capture cube SQL.
        report_data_enabled: Whether to capture report data.
        report_sql_enabled: Whether to capture report SQL.
        prompt_answer_source_precedence: Precedence for selecting prompt
            answers.

    """

    _FROM_DICT_MAP = {
        "prompt_answer_source_precedence": [PromptAnswerSource],
    }
    dashboard_sql_enabled: bool | None = None
    dashboard_data_enabled: bool | None = None
    dashboard_visualization_screenshot_enabled: bool | None = None
    cube_data_enabled: bool | None = None
    cube_sql_enabled: bool | None = None
    report_data_enabled: bool | None = None
    report_sql_enabled: bool | None = None
    prompt_answer_source_precedence: list[PromptAnswerSource] | None = None


def _object_list_from_dict(source: list[dict], connection: Connection):
    """Wraps `map_objects_list` to be used with dict operations in `Entity`."""
    return map_objects_list(connection, source)


@class_version_handler("11.5.0600")
class BaselineTest(IntegrityTest):
    """Python representation of a Strategy One Baseline Test object.

    Attributes:
        settings: The settings of the baseline test.
    """

    _OBJECT_SUBTYPES = [ObjectSubTypes.BASELINE_TEST]

    _API_GETTERS = {
        **IntegrityTest._API_GETTERS,
        ("settings", "test_objects"): tc_processors.get_baseline_test,
    }
    _API_DELETE = staticmethod(tc_api.delete_baseline_test)
    _API_EXECUTE = staticmethod(tc_api.run_baseline_test)

    _FROM_DICT_MAP = {
        **IntegrityTest._FROM_DICT_MAP,
        "settings": BaselineTestSettings.from_dict,
        "test_objects": _object_list_from_dict,
    }
    _FN_LIST_ALL = list_baseline_tests
    _ResultClass = Baseline

    def _init_variables(self, default_value, **kwargs):
        super()._init_variables(default_value, **kwargs)
        self._settings = (
            BaselineTestSettings.from_dict(kwargs["settings"])
            if kwargs.get("settings")
            else default_value
        )

        self._test_objects = (
            map_objects_list(self._connection, kwargs["test_objects"])
            if kwargs.get("test_objects")
            else default_value
        )

    @classmethod
    def _list_all(
        cls,
        connection: Connection,
        to_dictionary: bool = False,
        to_dataframe: bool = False,
        limit: int | None = None,
        **filters,
    ):
        filters = cls._python_to_rest(filters)
        return _list_object_by_class(
            cls=cls,
            connection=connection,
            api=tc_processors.get_all_baseline_tests,
            to_dictionary=to_dictionary,
            to_dataframe=to_dataframe,
            limit=limit,
            **filters,
        )

    @property
    def settings(self) -> BaselineTestSettings:
        """The baseline test settings."""
        return self._settings
