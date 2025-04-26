from datetime import datetime
from logging import Logger

from requests import Response

from typing import Any, Optional, Union

from typing_extensions import TypeAlias

from saml2.xmldsig import Signature

from saml2.client_base import Base

logger: Logger

LogoutResult: TypeAlias = Union[tuple[int, str, list[tuple[str, str]]], list[Any], dict[str, Any]]

class Saml2Client(Base):
    def prepare_for_authenticate(
        self,
        entityid: Optional[str] = ...,
        relay_state: str = ...,
        binding: str = ...,
        vorg: str = ...,
        nameid_format: Optional[str] = ...,
        scoping: Optional[Any] = ...,
        consent: Optional[bool] = ...,
        extensions: Optional[Any] = ...,
        sign: Optional[bool] = ...,
        sigalg: Optional[str] = ...,
        digest_alg: Optional[str] = ...,
        response_binding: str = ...,
        **kwargs: Any
    ) -> tuple[str, dict[str, Any]]: ...
    def prepare_for_negotiated_authenticate(
        self,
        entityid: Optional[str] = ...,
        relay_state: str = ...,
        binding: Optional[str] = ...,
        vorg: str = ...,
        nameid_format: Optional[str] = ...,
        scoping: Any | None = ...,
        consent: Optional[bool] = ...,
        extensions: Any | None = ...,
        sign: Optional[bool] = ...,
        response_binding: str = ...,
        sigalg: Optional[str] = ...,
        digest_alg: Optional[str] = ...,
        **kwargs
    ) -> tuple[str, str, dict[str, Any]]: ...
    def global_logout(
        self,
        name_id: str,
        reason: str = ...,
        expire: Union[datetime, str, int] = ...,
        sign: Optional[bool] = ...,
        sign_alg: Optional[str] = ...,
        digest_alg: Optional[str] = ...,
    ) -> Union[Response, dict[str, Any]]: ...
    def do_logout(
        self,
        name_id: str,
        entity_ids: list[str],
        reason: str,
        expire: Union[datetime, str, int],
        sign: Optional[bool] = ...,
        expected_binding: Optional[str] = ...,
        sign_alg: Optional[str] = ...,
        digest_alg: Optional[str] = ...,
        **kwargs
    ) -> LogoutResult: ...
    def local_logout(self, name_id: str) -> bool: ...
    def is_logged_in(self, name_id: str) -> bool: ...
    def handle_logout_response(
        self, response: Response, sign_alg: Optional[str] = ..., digest_alg: Optional[str] = ...
    ) -> LogoutResult: ...
    def do_authz_decision_query(
        self,
        entity_id: str,
        action: Any,
        subject_id: str,
        nameid_format: str,
        evidence: Optional[Any] = ...,
        resource: Optional[Any] = ...,
        sp_name_qualifier: Optional[Any] = ...,
        name_qualifier: Optional[Any] = ...,
        consent: Optional[bool] = ...,
        extensions: Optional[Any] = ...,
        sign: bool = ...,
    ) -> Optional[Response]: ...
    def do_assertion_id_request(
        self,
        assertion_ids: list[str],
        entity_id: str,
        consent: Optional[bool] = ...,
        extensions: Optional[Any] = ...,
        sign: bool = ...,
    ) -> Optional[Response]: ...
    def do_authn_query(
        self, entity_id: str, consent: Optional[bool] = ..., extensions: Optional[Any] = ..., sign: bool = ...
    ) -> Optional[Response]: ...
    def do_attribute_query(
        self,
        entityid: str,
        subject_id: str,
        attribute: Optional[Any] = ...,
        sp_name_qualifier: Optional[Any] = ...,
        name_qualifier: Optional[Any] = ...,
        nameid_format: Optional[str] = ...,
        real_id: Optional[Any] = ...,
        consent: Optional[bool] = ...,
        extensions: Optional[Any] = ...,
        sign: bool = ...,
        binding: str = ...,
        nsprefix: Optional[Any] = ...,
        sign_alg: Optional[str] = ...,
        digest_alg: Optional[str] = ...,
    ) -> Union[Response, dict[str, Any]]: ...
    def handle_logout_request(
        self,
        request: str,
        name_id: str,
        binding: str,
        sign: Optional[bool] = ...,
        sign_alg: Optional[str] = ...,
        digest_alg: Optional[str] = ...,
        relay_state: Optional[Any] = ...,
        sigalg: Optional[str] = ...,
        signature: Signature = ...,
    ) -> dict[str, Any]: ...
