import logging
from abc import ABCMeta, abstractmethod
from typing import Callable

from pandas import DataFrame

from mstrio import config
from mstrio.connection import Connection
from mstrio.helpers import IServerError
from mstrio.types import ObjectTypes
from mstrio.utils.entity import DeleteMixin, Entity, EntityBase
from mstrio.utils.helper import fetch_objects, find_object_with_name
from mstrio.utils.time_helper import DatetimeFormats, map_str_to_datetime
from mstrio.utils.wip import WipLevels, wip

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

    def __init__(self, connection: Connection, id: str, test_id: str | None = None):
        if test_id is None:
            id_key = "id"
            mapping = [
                rest_key
                for rest_key, python_key in self._REST_ATTR_MAP.items()
                if python_key == "id"
            ]
            if mapping:
                id_key = mapping[0]

            candidate_objs = self._list_all(
                connection=connection, to_dictionary=True, id=id
            )
            if not candidate_objs:
                raise ValueError(
                    f"There is no {self.__class__.__name__} with the given ID: '{id}'"
                )
            obj = candidate_objs[0]
            id = obj[id_key]
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
        self._test_objects = kwargs.get("test_objects", default_value)

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
        user_input = "N"
        if not force:
            message = (
                f"Are you sure you want to delete {object_name} "
                f"with ID: {self._id}? [Y/N]: "
            )
            user_input = input(message) or "N"

        if force or user_input == "Y":
            response = self._API_DELETE(self.connection, self.test_id, self.id)

            if response.status_code == 204 and config.verbose:
                msg = f"Successfully deleted {object_name} with ID: '{self._id}'."

                logger.info(msg)

            return response.ok

        return False

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
    @wip(level=WipLevels.ERROR)
    def test_objects(self):
        return self._test_objects


class IntegrityTest(Entity, DeleteMixin, metaclass=ABCMeta):
    _OBJECT_TYPE = ObjectTypes.TEST_SUITE
    _ResultClass: type[IntegrityTestResult]
    _API_EXECUTE: Callable

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

    def execute(self) -> IntegrityTestResult:
        """Executes the test.

        Returns:
            Object containing the result execution status and results.
        """
        res = self._API_EXECUTE(self._connection, self.id).json()
        return self._ResultClass.from_dict(res, self._connection)
