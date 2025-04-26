from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.app_session_message_create import AppSessionMessageCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppSessionCreate")


@attr.s(auto_attribs=True, repr=False)
class AppSessionCreate:
    """  """

    _app_id: str
    _name: str
    _timeout_seconds: int
    _messages: Union[Unset, List[AppSessionMessageCreate]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("app_id={}".format(repr(self._app_id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("timeout_seconds={}".format(repr(self._timeout_seconds)))
        fields.append("messages={}".format(repr(self._messages)))
        return "AppSessionCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app_id = self._app_id
        name = self._name
        timeout_seconds = self._timeout_seconds
        messages: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._messages, Unset):
            messages = []
            for messages_item_data in self._messages:
                messages_item = messages_item_data.to_dict()

                messages.append(messages_item)

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app_id is not UNSET:
            field_dict["appId"] = app_id
        if name is not UNSET:
            field_dict["name"] = name
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds
        if messages is not UNSET:
            field_dict["messages"] = messages

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_app_id() -> str:
            app_id = d.pop("appId")
            return app_id

        try:
            app_id = get_app_id()
        except KeyError:
            if strict:
                raise
            app_id = cast(str, UNSET)

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        def get_timeout_seconds() -> int:
            timeout_seconds = d.pop("timeoutSeconds")
            return timeout_seconds

        try:
            timeout_seconds = get_timeout_seconds()
        except KeyError:
            if strict:
                raise
            timeout_seconds = cast(int, UNSET)

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

        app_session_create = cls(
            app_id=app_id,
            name=name,
            timeout_seconds=timeout_seconds,
            messages=messages,
        )

        return app_session_create

    @property
    def app_id(self) -> str:
        if isinstance(self._app_id, Unset):
            raise NotPresentError(self, "app_id")
        return self._app_id

    @app_id.setter
    def app_id(self, value: str) -> None:
        self._app_id = value

    @property
    def name(self) -> str:
        """ The name of the session. Length must be between 3-100 chars. Value is required and immutable once set. """
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def timeout_seconds(self) -> int:
        """Timeout in seconds, a value between 1 second and 30 days. Once set, it can only be increased, not decreased."""
        if isinstance(self._timeout_seconds, Unset):
            raise NotPresentError(self, "timeout_seconds")
        return self._timeout_seconds

    @timeout_seconds.setter
    def timeout_seconds(self, value: int) -> None:
        self._timeout_seconds = value

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
