"""A typed durable Run reference bound to an explicitly configured client."""

from dataclasses import dataclass
import asyncio
from collections.abc import Mapping
from typing import TYPE_CHECKING, Generic, TypeVar

from labqoat.compute.value_codec import ValueCodec
from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonValue
from labqoat.schemas.schema_document import SchemaDocument

if TYPE_CHECKING:
    from labqoat.runs_client import RunsClient

R = TypeVar("R")


@dataclass(frozen=True)
class RunHandle(Generic[R]):
    """Reattach to accepted work and validate its result against the caller's requested type."""

    id: str
    client: "RunsClient"
    result_type: type[R]

    def result(self) -> R:
        """Wait through durable events, then check schema identity before decoding the retained result."""
        self.client.wait(self.id)
        return self.retained()

    def retained(self) -> R:
        """Decode the result of a Run the caller already observed completing, without another wait."""
        return self.decoded(self.client.result(self.id))

    def decoded(self, result: Mapping[str, JsonValue]) -> R:
        """Check schema identity before decoding a result document, however it was delivered."""
        codec = ValueCodec(self.result_type)
        expected = SchemaDocument.capture(codec.schema()).digest
        if set(result) != {"schema_digest", "data"} or result["schema_digest"] != expected:
            raise ApiError("Run result schema does not match the requested Python type")
        return codec.decode(result["data"])

    async def result_async(self) -> R:
        """Observe a durable host Run off the event loop; cancellation leaves accepted work intact."""
        return await asyncio.to_thread(self.result)
