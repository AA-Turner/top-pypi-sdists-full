import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.instrument_query_params import InstrumentQueryParams
from ..models.instrument_query_values import InstrumentQueryValues
from ..types import UNSET, Unset

T = TypeVar("T", bound="InstrumentQuery")


@attr.s(auto_attribs=True, repr=False)
class InstrumentQuery:
    """  """

    _command: Union[Unset, str] = UNSET
    _connection_id: Union[Unset, str] = UNSET
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _id: Union[Unset, str] = UNSET
    _info: Union[Unset, str] = UNSET
    _params: Union[Unset, InstrumentQueryParams] = UNSET
    _status: Union[Unset, str] = UNSET
    _values: Union[Unset, InstrumentQueryValues] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("command={}".format(repr(self._command)))
        fields.append("connection_id={}".format(repr(self._connection_id)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("info={}".format(repr(self._info)))
        fields.append("params={}".format(repr(self._params)))
        fields.append("status={}".format(repr(self._status)))
        fields.append("values={}".format(repr(self._values)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "InstrumentQuery({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        command = self._command
        connection_id = self._connection_id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        id = self._id
        info = self._info
        params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._params, Unset):
            params = self._params.to_dict()

        status = self._status
        values: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._values, Unset):
            values = self._values.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if command is not UNSET:
            field_dict["command"] = command
        if connection_id is not UNSET:
            field_dict["connectionId"] = connection_id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if info is not UNSET:
            field_dict["info"] = info
        if params is not UNSET:
            field_dict["params"] = params
        if status is not UNSET:
            field_dict["status"] = status
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_command() -> Union[Unset, str]:
            command = d.pop("command")
            return command

        try:
            command = get_command()
        except KeyError:
            if strict:
                raise
            command = cast(Union[Unset, str], UNSET)

        def get_connection_id() -> Union[Unset, str]:
            connection_id = d.pop("connectionId")
            return connection_id

        try:
            connection_id = get_connection_id()
        except KeyError:
            if strict:
                raise
            connection_id = cast(Union[Unset, str], UNSET)

        def get_created_at() -> Union[Unset, datetime.datetime]:
            created_at: Union[Unset, datetime.datetime] = UNSET
            _created_at = d.pop("createdAt")
            if _created_at is not None and not isinstance(_created_at, Unset):
                created_at = isoparse(cast(str, _created_at))

            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_info() -> Union[Unset, str]:
            info = d.pop("info")
            return info

        try:
            info = get_info()
        except KeyError:
            if strict:
                raise
            info = cast(Union[Unset, str], UNSET)

        def get_params() -> Union[Unset, InstrumentQueryParams]:
            params: Union[Unset, Union[Unset, InstrumentQueryParams]] = UNSET
            _params = d.pop("params")

            if not isinstance(_params, Unset):
                params = InstrumentQueryParams.from_dict(_params)

            return params

        try:
            params = get_params()
        except KeyError:
            if strict:
                raise
            params = cast(Union[Unset, InstrumentQueryParams], UNSET)

        def get_status() -> Union[Unset, str]:
            status = d.pop("status")
            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, str], UNSET)

        def get_values() -> Union[Unset, InstrumentQueryValues]:
            values: Union[Unset, Union[Unset, InstrumentQueryValues]] = UNSET
            _values = d.pop("values")

            if not isinstance(_values, Unset):
                values = InstrumentQueryValues.from_dict(_values)

            return values

        try:
            values = get_values()
        except KeyError:
            if strict:
                raise
            values = cast(Union[Unset, InstrumentQueryValues], UNSET)

        instrument_query = cls(
            command=command,
            connection_id=connection_id,
            created_at=created_at,
            id=id,
            info=info,
            params=params,
            status=status,
            values=values,
        )

        instrument_query.additional_properties = d
        return instrument_query

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def command(self) -> str:
        """ The command used in the query """
        if isinstance(self._command, Unset):
            raise NotPresentError(self, "command")
        return self._command

    @command.setter
    def command(self, value: str) -> None:
        self._command = value

    @command.deleter
    def command(self) -> None:
        self._command = UNSET

    @property
    def connection_id(self) -> str:
        """ The connection queried """
        if isinstance(self._connection_id, Unset):
            raise NotPresentError(self, "connection_id")
        return self._connection_id

    @connection_id.setter
    def connection_id(self, value: str) -> None:
        self._connection_id = value

    @connection_id.deleter
    def connection_id(self) -> None:
        self._connection_id = UNSET

    @property
    def created_at(self) -> datetime.datetime:
        """ The time the query was created """
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def id(self) -> str:
        """ The ID of the instrument query """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def info(self) -> str:
        """ Additional information about the query """
        if isinstance(self._info, Unset):
            raise NotPresentError(self, "info")
        return self._info

    @info.setter
    def info(self, value: str) -> None:
        self._info = value

    @info.deleter
    def info(self) -> None:
        self._info = UNSET

    @property
    def params(self) -> InstrumentQueryParams:
        """ Parameters used in the query """
        if isinstance(self._params, Unset):
            raise NotPresentError(self, "params")
        return self._params

    @params.setter
    def params(self, value: InstrumentQueryParams) -> None:
        self._params = value

    @params.deleter
    def params(self) -> None:
        self._params = UNSET

    @property
    def status(self) -> str:
        """ Status of the query """
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET

    @property
    def values(self) -> InstrumentQueryValues:
        """ Values returned by the query """
        if isinstance(self._values, Unset):
            raise NotPresentError(self, "values")
        return self._values

    @values.setter
    def values(self, value: InstrumentQueryValues) -> None:
        self._values = value

    @values.deleter
    def values(self) -> None:
        self._values = UNSET
