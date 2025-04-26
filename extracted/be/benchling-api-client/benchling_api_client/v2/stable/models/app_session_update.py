from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.app_session_message_create import AppSessionMessageCreate
from ..models.app_session_update_status import AppSessionUpdateStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppSessionUpdate")


@attr.s(auto_attribs=True, repr=False)
class AppSessionUpdate:
    """ Update a session's messages or increase timeoutSeconds. """

    _messages: Union[Unset, List[AppSessionMessageCreate]] = UNSET
    _status: Union[Unset, AppSessionUpdateStatus] = UNSET
    _timeout_seconds: Union[Unset, int] = UNSET

    def __repr__(self):
        fields = []
        fields.append("messages={}".format(repr(self._messages)))
        fields.append("status={}".format(repr(self._status)))
        fields.append("timeout_seconds={}".format(repr(self._timeout_seconds)))
        return "AppSessionUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        messages: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._messages, Unset):
            messages = []
            for messages_item_data in self._messages:
                messages_item = messages_item_data.to_dict()

                messages.append(messages_item)

        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        timeout_seconds = self._timeout_seconds

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if messages is not UNSET:
            field_dict["messages"] = messages
        if status is not UNSET:
            field_dict["status"] = status
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_messages() -> Union[Unset, List[AppSessionMessageCreate]]:
            messages = []
            _messages = d.pop("messages")
            for messages_item_data in _messages or []:
                messages_item = AppSessionMessageCreate.from_dict(messages_item_data, strict=False)

                messages.append(messages_item)

            return messages

        try:
            messages = get_messages()
        except KeyError:
            if strict:
                raise
            messages = cast(Union[Unset, List[AppSessionMessageCreate]], UNSET)

        def get_status() -> Union[Unset, AppSessionUpdateStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = AppSessionUpdateStatus(_status)
                except ValueError:
                    status = AppSessionUpdateStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, AppSessionUpdateStatus], UNSET)

        def get_timeout_seconds() -> Union[Unset, int]:
            timeout_seconds = d.pop("timeoutSeconds")
            return timeout_seconds

        try:
            timeout_seconds = get_timeout_seconds()
        except KeyError:
            if strict:
                raise
            timeout_seconds = cast(Union[Unset, int], UNSET)

        app_session_update = cls(
            messages=messages,
            status=status,
            timeout_seconds=timeout_seconds,
        )

        return app_session_update

    @property
    def messages(self) -> List[AppSessionMessageCreate]:
        """An array of `SessionMessage` describing the current session state."""
        if isinstance(self._messages, Unset):
            raise NotPresentError(self, "messages")
        return self._messages

    @messages.setter
    def messages(self, value: List[AppSessionMessageCreate]) -> None:
        self._messages = value

    @messages.deleter
    def messages(self) -> None:
        self._messages = UNSET

    @property
    def status(self) -> AppSessionUpdateStatus:
        """ Values that can be specified when updating the status of a Session """
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: AppSessionUpdateStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET

    @property
    def timeout_seconds(self) -> int:
        """Timeout in seconds, a value between 1 second and 30 days. Once set, it can only be increased, not decreased."""
        if isinstance(self._timeout_seconds, Unset):
            raise NotPresentError(self, "timeout_seconds")
        return self._timeout_seconds

    @timeout_seconds.setter
    def timeout_seconds(self, value: int) -> None:
        self._timeout_seconds = value

    @timeout_seconds.deleter
    def timeout_seconds(self) -> None:
        self._timeout_seconds = UNSET
