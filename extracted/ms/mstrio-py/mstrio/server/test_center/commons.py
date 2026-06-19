import logging
from abc import ABCMeta, abstractmethod
from typing import Callable

from pandas import DataFrame
from requests import Response

from mstrio import config
from mstrio.connection import Connection
from mstrio.helpers import IServerError
from mstrio.types import ObjectTypes
from mstrio.utils.entity import DeleteMixin, Entity, EntityBase
from mstrio.utils.helper import (
    Dictable,
    delete_none_values,
    fetch_objects,
    find_object_with_name,
)
from mstrio.utils.time_helper import DatetimeFormats, map_str_to_datetime

logger = logging.getLogger(__name__)


# TODO: convert more `list_*` methods to use this pattern
def _list_object_by_class(
    cls: type["IntegrityTest | IntegrityTestResult"],
    connection: Connection,
    api: Callable,
    dict_unpack_value: str | None = None,
    to_dictionary: bool = False,
    to_dataframe: bool = False,
    limit: int | None = None,
    **filters,
):
    if to_dictionary and to_dataframe:
        raise ValueError(
            "Please select either `to_dictionary=True` or `to_dataframe=True`, "
            "but not both."
        )
    objects = fetch_objects(
        connection=connection,
        api=api,
        limit=limit,
        filters=filters,
        dict_unpack_value=dict_unpack_value,
    )

    if to_dictionary:
        return objects
    elif to_dataframe:
        return DataFrame(objects)
    else:
        return cls.bulk_from_dict(source_list=objects, connection=connection)


def _bulk_delete_helper(
    connection: Connection,
    api: Callable,
    objects: "list[str | IntegrityTest | IntegrityTestResult]",
    delete_confirm_msg: str,
    delete_success_msg: str,
    delete_failure_msg: str,
    force: bool = False,
):
    if not force:
        user_input = input(delete_confirm_msg)
        if user_input != "Y":
            return False
    try:
        body = {"ids": [t.id if isinstance(t, EntityBase) else t for t in objects]}
        res: Response = api(connection, body)

        if config.verbose and res.ok:
            logger.info(delete_success_msg)

        return res.ok
    except Exception:
        logger.warning(delete_failure_msg)
        return False


class IntegrityTestResult(EntityBase, metaclass=ABCMeta):
    _FROM_DICT_MAP = {
        **EntityBase._FROM_DICT_MAP,
        "date_created": DatetimeFormats.FULLDATETIME,
        "date_modified": DatetimeFormats.FULLDATETIME,
    }
    _REST_ATTR_MAP = {
        "creation_time": "date_created",
        "last_modified_time": "date_modified",
    }
    _API_CANCEL: Callable
    _API_DELETE: Callable
    _API_BULK_DELETE: Callable

    def __init__(self, connection: Connection, id: str, test_id: str | None = None):
        if test_id is None:
            test_id_key = "test_id"
            mapping = [
                rest_key
                for rest_key, python_key in self._REST_ATTR_MAP.items()
                if python_key == "test_id"
            ]
            if mapping:
                test_id_key = mapping[0]

            candidate_objs = self._list_all(
                connection=connection, to_dictionary=True, id=id
            )
            if not candidate_objs:
                raise ValueError(
                    f"There is no {self.__class__.__name__} with the given ID: '{id}'"
                )
            obj = candidate_objs[0]
            test_id = obj[test_id_key]
        self._test_id = test_id
        super().__init__(connection=connection, object_id=id)

    def _init_variables(self, default_value=None, **kwargs):
        super()._init_variables(default_value, **kwargs)
        self._date_created = (
            map_str_to_datetime(
                "date_created", kwargs.get("creation_time"), self._FROM_DICT_MAP
            )
            if kwargs.get("creation_time")
            else default_value
        )
        self._date_modified = (
            map_str_to_datetime(
                "date_modified", kwargs.get("last_modified_time"), self._FROM_DICT_MAP
            )
            if kwargs.get("last_modified_time")
            else default_value
        )
        self._summary = kwargs.get("summary", default_value)
        self._object_results = kwargs.get("object_results", default_value)

    def cancel_execution(self) -> bool:
        """Cancel this instance of a test execution."""
        # no DeleteMixin, because it uses `name` attribute
        try:
            response = self._API_CANCEL(self.connection, self.test_id, self.id)
        except IServerError:
            logger.error(
                f"Failed to cancel execution of test result with ID: '{self._id}'."
            )
            return False

        if response.status_code == 202 and config.verbose:
            logger.info(
                "Successfully cancelled execution of test result "
                f"with ID: '{self._id}'."
            )

        return response.ok

    def delete(self, force: bool = False) -> bool:
        """Delete this test result.

        Args:
            force: If True, no additional prompt will be shown before deleting
                the result.

        Returns:
            True when the result was successfully deleted, False otherwise.
        """
        object_name = self.__class__.__name__
        if not force:
            message = (
                f"Are you sure you want to delete {object_name} "
                f"with ID: {self._id}? [Y/N]: "
            )
            user_input = input(message)
            if user_input != "Y":
                return False

        response = self._API_DELETE(self.connection, self.test_id, self.id)

        if response.status_code == 204 and config.verbose:
            msg = f"Successfully deleted {object_name} with ID: '{self._id}'."
            logger.info(msg)

        return response.ok

    @classmethod
    def bulk_delete(
        cls,
        connection: Connection,
        objects: "list[str | IntegrityTestResult]",
        force: bool = False,
    ) -> bool:
        """Delete multiple test results by their IDs.

        Note:
            If the test results are running and not finished,
            deletion will fail.

        Args:
            connection (Connection): Strategy One connection object returned by
                `connection.Connection()`
            objects (list [str | object]): List of test result IDs or objects
                to be deleted.
            force (bool): If True, no additional prompt will be shown before
                deleting the results.

        Returns:
            True if deletion was successful, False otherwise.
        """
        object_str = "result" if len(objects) == 1 else f"{len(objects)} results"
        delete_confirm_msg = (
            f"Are you sure you want to delete the selected {object_str}? [Y/N]: "
        )
        return _bulk_delete_helper(
            connection=connection,
            objects=objects,
            api=cls._API_BULK_DELETE,
            delete_confirm_msg=delete_confirm_msg,
            delete_success_msg="Successfully deleted the batch of results.",
            delete_failure_msg="Deleting some of the results failed.",
            force=force,
        )

    @classmethod
    @abstractmethod
    def _list_all(
        cls,
        connection: Connection,
        to_dictionary: bool = False,
        to_dataframe: bool = False,
        limit: int | None = None,
        **filters,
    ):
        pass

    @property
    def test_id(self) -> str:
        return self._test_id

    @property
    def summary(self) -> dict:
        return self._summary

    @property
    def object_results(self):
        return self._object_results


class IntegrityTest(Entity, DeleteMixin, metaclass=ABCMeta):
    _OBJECT_TYPE = ObjectTypes.TEST_SUITE
    _API_BULK_DELETE: Callable

    def __init__(
        self,
        connection: Connection,
        id: str | None = None,
        name: str | None = None,
    ):
        if id is None:
            if name is None:
                raise ValueError(
                    "Please specify either 'name' or 'id' parameter in the constructor."
                )

            obj = find_object_with_name(
                connection=connection,
                cls=self.__class__,
                name=name,
                listing_function=self._list_all,
            )
            id = obj["id"]
        super().__init__(
            connection=connection,
            object_id=id,
            name=name,
        )

    @classmethod
    @abstractmethod
    def _list_all(
        cls,
        connection: Connection,
        to_dictionary: bool = False,
        to_dataframe: bool = False,
        limit: int | None = None,
        **filters,
    ):
        pass

    @staticmethod
    def _normalize_execution_settings(
        content_dict_key: str,
        initial_settings: Dictable | dict,
        settings_delta: Dictable | dict | None,
        execute_sql: bool | None = None,
        execute_data: bool | None = None,
    ) -> dict:
        """Combine initial (or default) settings with user-specified new
            settings and apply explicit changes in execution content (SQL/DATA).

        Args:
            content_dict_key (str): The key in the settings dict that contains
                the content types (e.g. "compareContent" or "executeContent").
            initial_settings (Dictable or dict): Initial or default settings.
            settings_delta (Dictable or dict, optional): User-specified settings
                that should override the initial settings. Defaults to None.
            execute_sql (bool, optional): User-specified flag. Modifies the
                `execute_content` field in `settings` if specified.
            execute_data (bool, optional): User-specified flag. Modifies the
                `execute_content` field in `settings` if specified.

        Returns:
            dict: The normalized settings dictionary to be sent in the REST API
                request body.
        """
        if isinstance(initial_settings, Dictable):
            initial_settings = initial_settings.to_dict()
        if isinstance(settings_delta, Dictable):
            settings_delta = settings_delta.to_dict()
        if settings_delta:
            settings_delta = delete_none_values(settings_delta, recursion=False)
        settings = initial_settings
        if settings_delta:
            settings |= settings_delta

        content_set = set(settings.get(content_dict_key))
        if execute_sql is True:
            content_set.add("SQL")
        if execute_sql is False:
            content_set.discard("SQL")
        if execute_data is True:
            content_set.add("DATA")
        if execute_data is False:
            content_set.discard("DATA")

        if not content_set:
            raise ValueError("At least one of SQL or DATA must be selected.")
        if set(initial_settings.get(content_dict_key)) != content_set:
            settings[content_dict_key] = list(content_set)

        return settings

    @classmethod
    def bulk_delete(
        cls,
        connection: Connection,
        objects: "list[str | IntegrityTest]",
        force: bool = False,
    ) -> bool:
        """Delete multiple tests by their IDs.

        Args:
            connection (Connection): Strategy One connection object returned by
                `connection.Connection()`
            objects (list [str | object]): List of test IDs or objects
                to be deleted.
            force (bool): If True, no additional prompt will be shown before
                deleting the tests.
        Returns:
            True if deletion was successful, False otherwise.
        """
        object_str = "test" if len(objects) == 1 else f"{len(objects)} tests"
        delete_confirm_msg = (
            f"Are you sure you want to delete the selected {object_str}? [Y/N]: "
        )
        return _bulk_delete_helper(
            connection=connection,
            objects=objects,
            api=cls._API_BULK_DELETE,
            delete_confirm_msg=delete_confirm_msg,
            delete_success_msg="Successfully deleted the batch of tests.",
            delete_failure_msg="Deleting some of the tests failed.",
            force=force,
        )
