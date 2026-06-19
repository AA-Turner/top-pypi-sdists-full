import logging
from dataclasses import dataclass
from enum import auto

from mstrio import config
from mstrio.api import test_center as tc_api
from mstrio.connection import Connection
from mstrio.server.test_center.commons import (
    IntegrityTest,
    IntegrityTestResult,
    _list_object_by_class,
)
from mstrio.types import ExtendedType, ObjectSubTypes, ObjectTypes
from mstrio.utils.entity import Entity
from mstrio.utils.enum_helper import AutoUpperName, get_enum_val
from mstrio.utils.helper import Dictable, camel_to_snake
from mstrio.utils.object_mapping import map_objects_list
from mstrio.utils.response_processors import test_center as tc_processors
from mstrio.utils.version_helper import (
    class_version_handler,
    meets_minimal_version,
    method_version_handler,
)

logger = logging.getLogger(__name__)


def _object_list_from_dict(source: list[dict], connection: Connection):
    """Wraps `map_objects_list` to be used with dict operations
    in `EntityBase`."""
    return map_objects_list(connection, source)


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
        connection (Connection): Strategy One connection object returned
            by 'connection.Connection()'
        to_dictionary (bool, optional): if True, return Baseline Tests as list
            of dicts.
        to_dataframe (bool, optional): if True, return Baseline Tests as
            Pandas DataFrame
        limit (int, optional): limit for the number of elements returned
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
        connection (Connection): Strategy One connection object returned
            by 'connection.Connection()'
        to_dictionary (bool, optional): if True, return Baselines as list
            of dicts.
        to_dataframe (bool, optional): if True, return Baselines as
            Pandas DataFrame
        limit (int, optional): limit for the number of elements returned
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


class PromptAnswerSource(AutoUpperName):
    """Prompt answer source enumeration.

    Specifies the precedence for choosing prompt answers during baseline
    testing.
    """

    PERSONAL_ANSWER = auto()
    DEFAULT_ANSWER = auto()
    CUSTOM_ANSWER = auto()
    INTERNAL_ANSWER = auto()


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
        execute_content: List of content types to test against. Valid values
            are "DATA" and "SQL".
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
    execute_content: list[str] | None = None


def _parse_tree_structure(tree_structure: dict | None):
    if tree_structure is None:
        return [(None, None)]  # no tree, single object result entry
    return [
        (viz.get("key"), viz.get("name"))
        for chapter in tree_structure.get("chapters", [])
        for page in chapter.get("pages", [])
        for viz in page.get("visualizations", [])
    ]


# TODO: move to response_processors
def _construct_object_results(source: list[dict], *args, **kwargs) -> list[dict]:
    results = []
    for obj in source:
        tree_structure = obj.get("treeStructure")
        for viz_key, viz_name in _parse_tree_structure(tree_structure):
            obj["viz_key"] = viz_key
            obj["viz_name"] = viz_name
            results.append(camel_to_snake(obj))
    return results


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
            "object_results",
        ): tc_processors.get_baseline_result,
        "summary": tc_processors.get_baseline_result_summary,
    }
    _API_CANCEL = staticmethod(tc_api.cancel_baseline_run)
    _API_DELETE = staticmethod(tc_api.delete_baseline_result)
    _API_BULK_DELETE = staticmethod(tc_api.bulk_delete_baseline_results)
    _FROM_DICT_MAP = {
        **IntegrityTestResult._FROM_DICT_MAP,
        "object_results": _construct_object_results,
    }
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
        self._object_results = (
            _construct_object_results(kwargs["object_results"])
            if "object_results" in kwargs
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
    _API_PATCH = {
        (
            "name",
            "test_objects",
            "settings",
        ): (tc_processors.update_baseline_test, "put"),
    }
    _API_DELETE = staticmethod(tc_api.delete_baseline_test)
    _API_BULK_DELETE = staticmethod(tc_api.bulk_delete_baseline_tests)

    _FROM_DICT_MAP = {
        **IntegrityTest._FROM_DICT_MAP,
        "settings": BaselineTestSettings.from_dict,
        "test_objects": _object_list_from_dict,
    }
    _FN_LIST_ALL = list_baseline_tests

    def _init_variables(self, default_value, **kwargs):
        super()._init_variables(default_value, **kwargs)
        self.settings = (
            BaselineTestSettings.from_dict(kwargs["settings"])
            if kwargs.get("settings")
            else default_value
        )

        self.test_objects = (
            map_objects_list(self._connection, kwargs["test_objects"])
            if kwargs.get("test_objects")
            else default_value
        )

    @staticmethod
    def _entity_to_rest_request(obj, connection: Connection) -> dict:
        if isinstance(obj, Entity):
            return {
                "id": obj.id,
                "name": obj.name,
                "type": get_enum_val(obj.type, ObjectTypes),
                "subtype": get_enum_val(obj.subtype, ObjectSubTypes),
                "extType": get_enum_val(obj.ext_type, ExtendedType),
                "viewMedia": obj.view_media,
                "projectId": obj.project_id or connection.project_id,
                "ancestors": obj.ancestors,
            }
        elif isinstance(obj, dict):
            return obj
        else:
            raise ValueError(
                f"Test object must be either an Entity or a dict, got {type(obj)}"
            )

    @classmethod
    def _normalize_prompt_answer_source_precedence(
        cls, settings: dict, connection: Connection
    ) -> dict:
        """Normalize prompt answer source values in test settings to format
        expected in POST/PUT body, depending on I-Server version.
        """
        if "promptAnswerSourcePrecedence" not in settings or meets_minimal_version(
            connection.iserver_version, "11.6.0600"
        ):
            return settings

        source_to_write_value = {
            "PERSONAL_ANSWER": 0,
            "DEFAULT_ANSWER": 1,
            "CUSTOM_ANSWER": 2,
        }

        try:
            settings["promptAnswerSourcePrecedence"] = [
                source_to_write_value[source]
                for source in settings["promptAnswerSourcePrecedence"]
            ]
        except KeyError as error:
            raise ValueError(f"Unsupported prompt answer source: {error.args[0]}")

        return settings

    @classmethod
    def create(
        cls,
        connection: Connection,
        name: str,
        test_objects: list[Entity | dict],
        settings: BaselineTestSettings | None = None,
        execute_sql: bool | None = None,
        execute_data: bool | None = None,
        to_dictionary=False,
    ):
        """Create a new Baseline Test.

        Args:
            connection (Connection): Strategy One connection object returned
                by 'connection.Connection()'.
            name (str): Name of the Baseline Test.
            test_objects (list[Entity or dict]): List of test objects to include
                in the Baseline Test.
            settings (BaselineTestSettings, optional): Settings for the Baseline
                Test. Default settings will apply for any settings that are
                not specified.
            execute_sql (bool, optional): Whether to include SQL content
                in the test. Overrides the `execute_content` field in `settings`
                if specified.
            execute_data (bool, optional): Whether to include data content
                in the test. Overrides the `execute_content` field in `settings`
                if specified.
            to_dictionary (bool, optional): If True, return the new Baseline
                Test as a dictionary instead of an object. Defaults to False.

            Returns:
                BaselineTest or dict: The newly created Baseline Test.
        """
        default_settings_dict = {
            "dashboardSqlEnabled": True,
            "dashboardDataEnabled": True,
            "cubeDataEnabled": True,
            "cubeSqlEnabled": True,
            "reportDataEnabled": True,
            "reportSqlEnabled": True,
            "promptAnswerSourcePrecedence": [
                PromptAnswerSource.PERSONAL_ANSWER.value,
                PromptAnswerSource.DEFAULT_ANSWER.value,
            ],
            "executeContent": ["DATA", "SQL"],
        }
        settings = cls._normalize_execution_settings(
            content_dict_key="executeContent",
            initial_settings=default_settings_dict,
            settings_delta=settings,
            execute_sql=execute_sql,
            execute_data=execute_data,
        )
        settings = cls._normalize_prompt_answer_source_precedence(settings, connection)

        body = {
            "name": name,
            "testObjects": [
                cls._entity_to_rest_request(obj, connection) for obj in test_objects
            ],
            "settings": settings,
        }
        res_dict = tc_processors.create_baseline_test(connection, body)

        if config.verbose:
            logger.info(
                f"Successfully created Baseline Test named: '{name}' "
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
        test_objects: list[Entity] | None = None,
        settings: BaselineTestSettings | None = None,
        execute_sql: bool | None = None,
        execute_data: bool | None = None,
    ):
        """Alter the properties of the Baseline Test.

        Args:
            name (str): Name of the Baseline Test.
            test_objects (list[Entity or dict]): List of test objects to include
                in the Baseline Test.
            settings (BaselineTestSettings, optional): Settings for the Baseline
                Test. Settings that are not specified will not be updated.
            execute_sql (bool, optional): Whether to include SQL content
                in the test. Overrides the `execute_content` field in `settings`
                if specified.
            execute_data (bool, optional): Whether to include data content
                in the test. Overrides the `execute_content` field in `settings`
                if specified.
        """
        name = name or self.name
        test_objects = test_objects or self.test_objects
        test_objects = [
            self._entity_to_rest_request(obj, self._connection) for obj in test_objects
        ]

        settings = self._normalize_execution_settings(
            content_dict_key="executeContent",
            initial_settings=self.settings,
            settings_delta=settings,
            execute_sql=execute_sql,
            execute_data=execute_data,
        )
        settings = self._normalize_prompt_answer_source_precedence(
            settings, self._connection
        )

        self._alter_properties(name=name, test_objects=test_objects, settings=settings)

    def execute(self) -> Baseline:
        """Executes the test.

        Returns:
            Object containing the result execution status and results.
        """
        res = tc_api.run_baseline_test(self._connection, self.id).json()
        return Baseline.from_dict(res, self._connection)

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
