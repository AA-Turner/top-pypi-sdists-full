import logging
import re
from dataclasses import dataclass
from enum import auto

from mstrio import config
from mstrio.api import test_center as tc_api
from mstrio.connection import Connection
from mstrio.server.environment import Environment
from mstrio.server.test_center.baseline import Baseline, BaselineTest
from mstrio.server.test_center.commons import (
    IntegrityTest,
    IntegrityTestResult,
    _list_object_by_class,
)
from mstrio.types import ObjectSubTypes
from mstrio.utils.enum_helper import AutoName
from mstrio.utils.helper import Dictable, delete_none_values, snake_to_camel
from mstrio.utils.resolvers import get_conn_and_env_from_mixed_param
from mstrio.utils.response_processors import test_center as tc_processors
from mstrio.utils.version_helper import class_version_handler, method_version_handler

logger = logging.getLogger(__name__)


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
        connection (Connection): Strategy One connection object returned
            by 'connection.Connection()'
        to_dictionary (bool, optional): if True, return Comparison Tests as
            list of dicts
        to_dataframe (bool, optional): if True, return Comparison Tests as
            Pandas DataFrame
        limit (int, optional): limit for the number of elements returned
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
        connection (Connection): Strategy One connection object returned
            by 'connection.Connection()'
        to_dictionary (bool, optional): if True, return Comparison Test Results
            as list of dicts
        to_dataframe (bool, optional): if True, return Comparison Test Results
            as Pandas DataFrame
        limit (int, optional): limit for the number of elements returned
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
    _API_BULK_DELETE = staticmethod(tc_api.bulk_delete_comparison_results)
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
        self._object_results = kwargs.get("object_results", default_value)

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
    def object_results(self):
        source_baseline = Baseline(
            self._connection,
            id=self.source["baseline_id"],
            test_id=self.source["test_id"],
        )
        bl_object_results: list[dict] = source_baseline.object_results
        acc = []
        for obj_res in self._object_results:
            bl_obj_res_id = obj_res["source"]["baselineId"]
            source_object_results_by_key = {
                (bl_obj_res["baseline_id"], bl_obj_res["viz_key"]): bl_obj_res
                for bl_obj_res in bl_object_results
            }
            per_object_summary = obj_res.get("summary", {}).get("summary", {})
            for viz_key in per_object_summary:
                matching_bl_obj_res = source_object_results_by_key.get(
                    (bl_obj_res_id, viz_key if viz_key else None)
                )
                if not matching_bl_obj_res:
                    continue
                entry = {
                    "object_test_id": obj_res["comparisonId"],
                    "viz_key": viz_key if viz_key else None,
                    "tested_object": matching_bl_obj_res["tested_object"],
                    "summary": per_object_summary[viz_key],
                }
                acc.append(entry)
        return acc

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
        compare_content: List of content types to compare: "SQL" and/or "DATA"
        compare_method: Method used to match objects during comparison.
    """

    _FROM_DICT_MAP = {
        "compare_method": ComparisonMethod,
    }
    compare_content: list[str] | None = None
    compare_method: ComparisonMethod | None = None


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
    _API_PATCH = {
        (
            "name",
            "source",
            "target",
            "settings",
        ): (tc_api.update_comparison_test, "put"),
    }
    _API_DELETE = staticmethod(tc_api.delete_comparison_test)
    _API_BULK_DELETE = staticmethod(tc_api.bulk_delete_comparison_tests)

    _FROM_DICT_MAP = {
        **IntegrityTest._FROM_DICT_MAP,
        "settings": ComparisonTestSettings.from_dict,
    }

    def _init_variables(self, default_value, **kwargs):
        super()._init_variables(default_value, **kwargs)
        self.settings = (
            ComparisonTestSettings.from_dict(kwargs["settings"])
            if kwargs.get("settings")
            else default_value
        )
        self.source = kwargs.get("source", default_value)
        self.target = kwargs.get("target", default_value)

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

    @staticmethod
    def _normalize_env_url(url: str) -> str:
        return url if url.endswith("/") else url + "/"

    @staticmethod
    def _extract_env_name_from_url(url: str) -> str:
        matches = re.findall(r"[\w-]+", url)
        return matches[min(1, len(matches) - 1)] if matches else ""

    @staticmethod
    def _baseline_test_to_body_entry(b: BaselineTest):
        return {
            "type": "integrity_test",
            "testId": b.id,
            "environment": {
                "id": ComparisonTest._normalize_env_url(b._connection.base_url),
                "name": ComparisonTest._extract_env_name_from_url(
                    b._connection.base_url
                ),
            },
        }

    @staticmethod
    def _baseline_to_body_entry(b: Baseline):
        return {
            "type": "integrity_test_baseline",
            "baselineId": b.id,
            "testId": b.test_id,
            "environment": {
                "id": ComparisonTest._normalize_env_url(b.library_url),
                "name": ComparisonTest._extract_env_name_from_url(b.library_url),
            },
        }

    @staticmethod
    def _integrity_test_to_body_entry(s_t: dict | BaselineTest | Baseline):
        if isinstance(s_t, dict):
            return snake_to_camel(s_t)
        elif isinstance(s_t, BaselineTest):
            return ComparisonTest._baseline_test_to_body_entry(s_t)
        elif isinstance(s_t, Baseline):
            return ComparisonTest._baseline_to_body_entry(s_t)
        else:
            raise ValueError(
                "Integrity test must be of type `BaselineTest`, `Baseline` "
                f"or `dict`. Got {type(s_t)}"
            )

    @classmethod
    def create(
        cls,
        connection: Connection,
        name: str,
        source: dict | BaselineTest | Baseline,
        target: dict | BaselineTest | Baseline,
        settings: ComparisonTestSettings | None = None,
        execute_sql: bool | None = None,
        execute_data: bool | None = None,
        to_dictionary: bool = False,
    ):
        """Create a new Comparison Test.

        Args:
            connection (object): Strategy One connection object returned
                by 'connection.Connection()'.
            name (str): Name of the Comparison Test.
            source (dict | BaselineTest | Baseline): The source integrity test
                for the comparison. If a Baseline Test definition is provided,
                a new Baseline result will be generated for the test execution.
            target (dict | BaselineTest | Baseline): The target integrity test.
            settings (ComparisonTestSettings, optional): Settings for the
                Comparison Test. Default settings will apply for any settings
                that are not specified.
            execute_sql (bool, optional): Whether to include SQL content
                in the test. Overrides the `execute_content` field in `settings`
                if specified.
            execute_data (bool, optional): Whether to include data content
                in the test. Overrides the `execute_content` field in `settings`
                if specified.
            to_dictionary (bool, optional): If True, return the new Comparison
                Test as a dictionary instead of an object. Defaults to False.

            Returns:
                ComparisonTest or dict: The newly created Comparison Test.
        """
        default_settings_dict = {
            "compareContent": ["SQL", "DATA"],
            "compareMethod": "by_id",
        }

        settings = cls._normalize_execution_settings(
            content_dict_key="compareContent",
            initial_settings=default_settings_dict,
            settings_delta=settings,
            execute_sql=execute_sql,
            execute_data=execute_data,
        )
        body = {
            "name": name,
            "source": (ComparisonTest._integrity_test_to_body_entry(source)),
            "target": (ComparisonTest._integrity_test_to_body_entry(target)),
            "settings": settings,
        }
        body = delete_none_values(body, recursion=True)
        res_dict = tc_api.create_comparison_test(connection, body).json()

        if config.verbose:
            logger.info(
                f"Successfully created Comparison Test named: '{name}' "
                f"with ID: '{res_dict.get('id')}'"
            )
        return (
            res_dict
            if to_dictionary
            else cls.from_dict(res_dict, connection=connection)
        )

    def alter(
        self,
        name: str | None = None,
        source: dict | BaselineTest | Baseline | None = None,
        target: dict | BaselineTest | Baseline | None = None,
        settings: ComparisonTestSettings | None = None,
        execute_sql: bool | None = None,
        execute_data: bool | None = None,
    ):
        """Alter the properties of the Comparison Test.

        Args:
            name (str): Name of the Comparison Test.
            source (dict | BaselineTest | Baseline): The source integrity test
                for the comparison. If a Baseline Test definition is provided,
                a new Baseline result will be generated for the test execution.
            target (dict | BaselineTest | Baseline): The target integrity test.
            settings (ComparisonTestSettings, optional): Settings for the
                Comparison Test. Default settings will apply for any settings
                that are not specified.
            execute_sql (bool, optional): Whether to include SQL content
                in the test. Overrides the `execute_content` field in `settings`
                if specified.
            execute_data (bool, optional): Whether to include data content
                in the test. Overrides the `execute_content` field in `settings`
                if specified.
        """
        name = name or self.name
        source = self._integrity_test_to_body_entry(source or self.source)
        target = self._integrity_test_to_body_entry(target or self.target)

        settings = self._normalize_execution_settings(
            content_dict_key="compareContent",
            initial_settings=self.settings,
            settings_delta=settings,
            execute_sql=execute_sql,
            execute_data=execute_data,
        )
        self._alter_properties(
            name=name, source=source, target=target, settings=settings
        )

    def execute(
        self, target_env: Connection | Environment | None = None
    ) -> ComparisonTestResult:
        """Executes the Comparison Test.

        Args:
            target_env (Connection | Environment, optional): Connection to the
                target environment or Environment object. Required for
                cross-environment comparisons. Target must have the same
                Storage Service configuration as the source environment.

        Returns:
            ComparisonTestResult: Object containing the result execution status
                and results.
        """
        if self.is_cross_environment:
            if not target_env:
                raise ValueError(
                    "Target environment connection must be provided for "
                    "cross-environment comparison tests."
                )
            source_env = Environment(self._connection)
            target_conn, target_env = get_conn_and_env_from_mixed_param(target_env)
            if source_env.storage_service != target_env.storage_service:
                raise ValueError(
                    "Source and target environments must have the same Storage "
                    "Service configuration for cross-environment comparison tests."
                )
            match self.target["type"]:
                case "integrity_test_baseline":
                    storage_file_id = (
                        tc_api.sync_baseline_result(
                            target_conn,
                            self.target["test_id"],
                            self.target["baseline_id"],
                        )
                        .json()
                        .get("fileId")
                    )
                case "integrity_test":
                    baseline_res = tc_api.run_baseline_test(
                        target_conn, self.target["test_id"], body={"storageSync": True}
                    ).json()
                    storage_file_id = baseline_res.get("syncFileId")
                case _:
                    raise ValueError(
                        "Unknown comparison target type. "
                        "Expected 'integrity_test' or 'integrity_test_baseline'."
                    )
            body = {"storageSyncInfo": {"targetFileId": storage_file_id}}
        else:
            body = {}
        res = tc_api.run_comparison_test(self._connection, self.id, body).json()
        return ComparisonTestResult.from_dict(res, self._connection)

    @property
    def is_cross_environment(self) -> bool:
        """Whether this Comparison Test is a cross-environment comparison."""
        return bool(self.target.get("remote"))
