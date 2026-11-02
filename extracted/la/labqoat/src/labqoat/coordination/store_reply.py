"""The answer to one dict or queue request."""

from dataclasses import dataclass, field

from labqoat.json_document import JsonDocument


@dataclass(frozen=True)
class StoreReply:
    """A successful body, or one of the two refusals dicts and queues handle themselves: missing and full."""

    status: int
    document: JsonDocument = field(default_factory=JsonDocument)

    @property
    def missing(self) -> bool:
        """Nothing is stored under the name or key the request named."""
        return self.status == 404

    @property
    def full(self) -> bool:
        """The queue partition had no room for what the request put."""
        return self.status == 409
