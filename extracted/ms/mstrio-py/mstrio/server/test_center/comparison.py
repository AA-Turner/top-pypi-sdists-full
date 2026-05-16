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
from mstrio.utils.enum_helper import AutoName
from mstrio.utils.helper import Dictable
from mstrio.utils.response_processors import test_center as tc_processors
from mstrio.utils.version_helper import class_version_handler, method_version_handler


@method_version_handler("11.5.0600")
def list_comparison_tests(
    connection: Connection,
    to_dictionary: bool = False,
    to_dataframe: bool = False,
    limit: int | None = None,
    **filters,
):
    """Get all Comparison Tests stored on the configured storage.

    Optionally use `to_dictionary` or `to_dataframe` to choose output format.
    If `to_dictionary` is True, `to_dataframe` is omitted.

    Args:
        connection(object): Strategy One connection object returned
            by 'connection.Connection()'
        to_dictionary(bool, optional): if True, return Comparison Tests as
            list of dicts
        to_dataframe(bool, optional): if True, return Comparison Tests as
            Pandas DataFrame
        limit(int): limit the number of elements returned. If `None` (default),
            all objects are returned.
        **filters: Available filter parameters: ['name', 'id', 'description',
            'date_created', 'date_modified', 'version', 'acg', 'owner']

    Returns:
        List of Comparison Test objects in specified format
            (objects, dicts, or DataFrame)
    """

    return ComparisonTest._list_all(
        connection=connection,
        to_dictionary=to_dictionary,
        to_dataframe=to_dataframe,
        limit=limit,
        **filters,
    )


@method_version_handler("11.5.0600")
def list_comparison_test_results(
    connection: Connection,
    to_dictionary: bool = False,
    to_dataframe: bool = False,
    limit: int | None = None,
    **filters,
):
    """Get all Comparison Test Results stored on the configured storage.

    Optionally use `to_dictionary` or `to_dataframe` to choose output format.
    If `to_dictionary` is True, `to_dataframe` is omitted.

    Args:
        connection(object): Strategy One connection object returned
            by 'connection.Connection()'
        to_dictionary(bool, optional): if True, return Comparison Test Results
            as list of dicts
        to_dataframe(bool, optional): if True, return Comparison Test Results as
            Pandas DataFrame
        limit(int): limit the number of elements returned. If `None` (default),
            all objects are returned.
        **filters: Available filter parameters: ['name', 'id', 'description',
            'date_created', 'date_modified', 'version', 'acg', 'owner']

    Returns:
        List of Comparison Test Result objects in specified format
            (objects, dicts, or DataFrame)
    """

    return ComparisonTestResult._list_all(
        connection=connection,
        to_dictionary=to_dictionary,
        to_dataframe=to_dataframe,
        limit=limit,
        **filters,
    )


@class_version_handler("11.5.0600")
class ComparisonTestResult(IntegrityTestResult):
    """Python representation of a Strategy One Comparison Test Result object.

    Attributes:
        source: The source baseline of the comparison.
        target: The target baseline of the comparison.
        status: The running status of the comparison test.
        preparation_status: The preparation status of the comparison test.
        summary: The summary of the comparison test result.
    """

    _API_GETTERS = {
        **IntegrityTestResult._API_GETTERS,
        (
            "date_created",
            "date_modified",
            "source",
            "target",
            "status",
            "preparation_status",
        ): tc_api.get_comparison_result,
        "summary": tc_processors.get_comparison_result_summary,
    }
    _API_CANCEL = staticmethod(tc_api.cancel_comparison_run)
    _API_DELETE = staticmethod(tc_api.delete_comparison_result)
    _REST_ATTR_MAP = {
        **IntegrityTestResult._REST_ATTR_MAP,
        "comparison_id": "id",
        "integrity_comparison_id": "test_id",
        "test_object_comparisons": "object_results",
    }

    def _init_variables(self, default_value=None, **kwargs):
        super()._init_variables(default_value, **kwargs)

        # _test_id can be set from from_dict source or from __init__ arg
        if not hasattr(self, "_test_id") or not self._test_id:
            self._test_id = kwargs.get("integrity_comparison_id", default_value)

        self._source = kwargs.get("source", default_value)
        self._target = kwargs.get("target", default_value)
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
            api=tc_api.get_all_comparison_results,
            to_dictionary=to_dictionary,
            to_dataframe=to_dataframe,
            limit=limit,
            **filters,
        )

    @property
    def source(self):
        """The source baseline of the comparison."""
        return self._source

    @property
    def target(self):
        """The target baseline of the comparison."""
        return self._target

    @property
    def status(self):
        """The running status of the comparison test."""
        return self._status

    @property
    def preparation_status(self):
        """The preparation status of the comparison test."""
        return self._preparation_status


class ComparisonMethod(AutoName):
    """Comparison method enumeration.

    Specifies how objects should be matched during comparison.
    """

    BY_ID = auto()
    BY_PATH = auto()


@dataclass
class ComparisonTestSettings(Dictable):
    """Settings for configuring a Comparison Test.

    Attributes:
        compare_content: List of content types to compare: "sql" and/or "data"
        compare_method: Method used to match objects during comparison.
    """

    _FROM_DICT_MAP = {
        "compare_method": ComparisonMethod,
    }
    compare_content: list[str]
    compare_method: ComparisonMethod


@class_version_handler("11.5.0600")
class ComparisonTest(IntegrityTest):
    """Python representation of a Strategy One Comparison Test object.

    Attributes:
        settings: The comparison test settings.
        source: The source baseline in the comparison.
        target: The target baseline in the comparison.
    """

    _OBJECT_SUBTYPES = [ObjectSubTypes.COMPARISON_TEST]

    _API_GETTERS = {
        **IntegrityTest._API_GETTERS,
        ("settings", "source", "target"): tc_api.get_comparison_test,
    }
    _API_DELETE = staticmethod(tc_api.delete_comparison_test)
    _API_EXECUTE = staticmethod(tc_api.run_comparison_test)

    _FROM_DICT_MAP = {
        **IntegrityTest._FROM_DICT_MAP,
        "settings": ComparisonTestSettings.from_dict,
    }
    _ResultClass = ComparisonTestResult

    def _init_variables(self, default_value, **kwargs):
        super()._init_variables(default_value, **kwargs)
        self._settings = (
            ComparisonTestSettings.from_dict(kwargs["settings"])
            if kwargs.get("settings")
            else default_value
        )
        self._source = kwargs.get("source", default_value)
        self._target = kwargs.get("target", default_value)

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
            api=tc_api.get_all_comparison_tests,
            dict_unpack_value="integrityComparisons",
            to_dictionary=to_dictionary,
            to_dataframe=to_dataframe,
            limit=limit,
            **filters,
        )

    @property
    def settings(self) -> ComparisonTestSettings:
        """The comparison test settings."""
        return self._settings

    @property
    def source(self):
        """The source baseline in the comparison."""
        return self._source

    @property
    def target(self):
        """The target baseline in the comparison."""
        return self._target
