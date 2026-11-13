import hashlib
import hmac
import secrets
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from typing import Self
from uuid import UUID, uuid5

import mcp_types as types
from mcp.shared.exceptions import MCPError
from pydantic import BaseModel, ConfigDict, ValidationError

from langgraph_api.api.mcp._constants import INVALID_REQUEST_STATE
from langgraph_api.api.mcp._elicitation import Refusal, Round

BINDING_KEY = "mcp_call"
TOKEN_BYTES = 32
STORED_LABEL = b"stored"
NEXT_ROUND_LABEL = b"next-round"


class InvalidRequestState(MCPError):
    def __init__(self) -> None:
        super().__init__(types.INVALID_PARAMS, INVALID_REQUEST_STATE)


@dataclass(frozen=True, slots=True)
class RequestState:
    thread_id: UUID
    token: str = field(repr=False)

    def __post_init__(self) -> None:
        if not self.token:
            raise ValueError("A request state needs a token")

    @classmethod
    def new(cls, thread_id: str) -> Self:
        return cls(UUID(thread_id), secrets.token_urlsafe(TOKEN_BYTES))

    @classmethod
    def parse(cls, raw: str) -> Self:
        thread_id, _, token = raw.partition(".")
        try:
            return cls(UUID(thread_id), token)
        except ValueError:
            raise InvalidRequestState from None

    def __str__(self) -> str:
        return f"{self.thread_id}.{self.token}"

    @property
    def verifier(self) -> str:
        return self._derive(STORED_LABEL)

    @property
    def run_id(self) -> UUID:
        return uuid5(self.thread_id, self.verifier)

    def next(self) -> Self:
        return replace(self, token=self._derive(NEXT_ROUND_LABEL))

    def _derive(self, label: bytes) -> str:
        return hmac.new(self.token.encode(), label, hashlib.sha256).hexdigest()


class Binding(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    call: str
    state: str
    asked: str
    ended: Refusal | None = None

    @classmethod
    def of(
        cls,
        call: str,
        state: RequestState,
        asked: Round,
        ended: Refusal | None = None,
    ) -> Self:
        return cls(call=call, state=state.verifier, asked=asked.digest, ended=ended)

    @classmethod
    def stored(cls, metadata: Mapping[str, object] | None) -> Self | None:
        try:
            return cls.model_validate(metadata.get(BINDING_KEY) if metadata else None)
        except ValidationError:
            return None

    @classmethod
    def verified(
        cls, metadata: Mapping[str, object] | None, call: str, state: RequestState
    ) -> Self:
        binding = cls.stored(metadata)
        if binding is None or not (
            binding.admits(call, state) or binding.admits(call, state.next())
        ):
            raise InvalidRequestState
        return binding

    def admits(self, call: str, state: RequestState) -> bool:
        return self.call == call and hmac.compare_digest(
            self.state.encode(), state.verifier.encode()
        )

    @property
    def metadata(self) -> dict[str, dict[str, str]]:
        return {BINDING_KEY: self.model_dump(exclude_none=True)}
