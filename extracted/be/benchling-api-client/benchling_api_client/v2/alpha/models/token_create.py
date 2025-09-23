from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.token_create_grant_type import TokenCreateGrantType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TokenCreate")


@attr.s(auto_attribs=True, repr=False)
class TokenCreate:
    """  """

    _grant_type: TokenCreateGrantType
    _client_id: Union[Unset, str] = UNSET
    _client_secret: Union[Unset, str] = UNSET
    _code: Union[Unset, str] = UNSET
    _code_verifier: Union[Unset, str] = UNSET
    _redirect_uri: Union[Unset, str] = UNSET
    _state: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("grant_type={}".format(repr(self._grant_type)))
        fields.append("client_id={}".format(repr(self._client_id)))
        fields.append("client_secret={}".format(repr(self._client_secret)))
        fields.append("code={}".format(repr(self._code)))
        fields.append("code_verifier={}".format(repr(self._code_verifier)))
        fields.append("redirect_uri={}".format(repr(self._redirect_uri)))
        fields.append("state={}".format(repr(self._state)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "TokenCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        grant_type = self._grant_type.value

        client_id = self._client_id
        client_secret = self._client_secret
        code = self._code
        code_verifier = self._code_verifier
        redirect_uri = self._redirect_uri
        state = self._state

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if grant_type is not UNSET:
            field_dict["grant_type"] = grant_type
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret
        if code is not UNSET:
            field_dict["code"] = code
        if code_verifier is not UNSET:
            field_dict["code_verifier"] = code_verifier
        if redirect_uri is not UNSET:
            field_dict["redirect_uri"] = redirect_uri
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_grant_type() -> TokenCreateGrantType:
            _grant_type = d.pop("grant_type")
            try:
                grant_type = TokenCreateGrantType(_grant_type)
            except ValueError:
                grant_type = TokenCreateGrantType.of_unknown(_grant_type)

            return grant_type

        try:
            grant_type = get_grant_type()
        except KeyError:
            if strict:
                raise
            grant_type = cast(TokenCreateGrantType, UNSET)

        def get_client_id() -> Union[Unset, str]:
            client_id = d.pop("client_id")
            return client_id

        try:
            client_id = get_client_id()
        except KeyError:
            if strict:
                raise
            client_id = cast(Union[Unset, str], UNSET)

        def get_client_secret() -> Union[Unset, str]:
            client_secret = d.pop("client_secret")
            return client_secret

        try:
            client_secret = get_client_secret()
        except KeyError:
            if strict:
                raise
            client_secret = cast(Union[Unset, str], UNSET)

        def get_code() -> Union[Unset, str]:
            code = d.pop("code")
            return code

        try:
            code = get_code()
        except KeyError:
            if strict:
                raise
            code = cast(Union[Unset, str], UNSET)

        def get_code_verifier() -> Union[Unset, str]:
            code_verifier = d.pop("code_verifier")
            return code_verifier

        try:
            code_verifier = get_code_verifier()
        except KeyError:
            if strict:
                raise
            code_verifier = cast(Union[Unset, str], UNSET)

        def get_redirect_uri() -> Union[Unset, str]:
            redirect_uri = d.pop("redirect_uri")
            return redirect_uri

        try:
            redirect_uri = get_redirect_uri()
        except KeyError:
            if strict:
                raise
            redirect_uri = cast(Union[Unset, str], UNSET)

        def get_state() -> Union[Unset, str]:
            state = d.pop("state")
            return state

        try:
            state = get_state()
        except KeyError:
            if strict:
                raise
            state = cast(Union[Unset, str], UNSET)

        token_create = cls(
            grant_type=grant_type,
            client_id=client_id,
            client_secret=client_secret,
            code=code,
            code_verifier=code_verifier,
            redirect_uri=redirect_uri,
            state=state,
        )

        token_create.additional_properties = d
        return token_create

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
    def grant_type(self) -> TokenCreateGrantType:
        if isinstance(self._grant_type, Unset):
            raise NotPresentError(self, "grant_type")
        return self._grant_type

    @grant_type.setter
    def grant_type(self, value: TokenCreateGrantType) -> None:
        self._grant_type = value

    @property
    def client_id(self) -> str:
        """ID of client to request token for. Leave off if client ID and secret are being supplied through Authorization header."""
        if isinstance(self._client_id, Unset):
            raise NotPresentError(self, "client_id")
        return self._client_id

    @client_id.setter
    def client_id(self, value: str) -> None:
        self._client_id = value

    @client_id.deleter
    def client_id(self) -> None:
        self._client_id = UNSET

    @property
    def client_secret(self) -> str:
        """Leave off if client ID and secret are being supplied through Authorization header."""
        if isinstance(self._client_secret, Unset):
            raise NotPresentError(self, "client_secret")
        return self._client_secret

    @client_secret.setter
    def client_secret(self, value: str) -> None:
        self._client_secret = value

    @client_secret.deleter
    def client_secret(self) -> None:
        self._client_secret = UNSET

    @property
    def code(self) -> str:
        """Authorization code to request token for. Required if grant_type is authorization_code."""
        if isinstance(self._code, Unset):
            raise NotPresentError(self, "code")
        return self._code

    @code.setter
    def code(self, value: str) -> None:
        self._code = value

    @code.deleter
    def code(self) -> None:
        self._code = UNSET

    @property
    def code_verifier(self) -> str:
        """Code verifier to request token for. Only required if code_verifier is provided in the authorization code request."""
        if isinstance(self._code_verifier, Unset):
            raise NotPresentError(self, "code_verifier")
        return self._code_verifier

    @code_verifier.setter
    def code_verifier(self, value: str) -> None:
        self._code_verifier = value

    @code_verifier.deleter
    def code_verifier(self) -> None:
        self._code_verifier = UNSET

    @property
    def redirect_uri(self) -> str:
        """Redirect URI to request token for. Required if grant_type is authorization_code."""
        if isinstance(self._redirect_uri, Unset):
            raise NotPresentError(self, "redirect_uri")
        return self._redirect_uri

    @redirect_uri.setter
    def redirect_uri(self, value: str) -> None:
        self._redirect_uri = value

    @redirect_uri.deleter
    def redirect_uri(self) -> None:
        self._redirect_uri = UNSET

    @property
    def state(self) -> str:
        """State to request token for. Only required if state is provided in the authorization code request."""
        if isinstance(self._state, Unset):
            raise NotPresentError(self, "state")
        return self._state

    @state.setter
    def state(self, value: str) -> None:
        self._state = value

    @state.deleter
    def state(self) -> None:
        self._state = UNSET
