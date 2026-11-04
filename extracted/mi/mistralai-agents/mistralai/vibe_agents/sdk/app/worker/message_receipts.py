"""Receipts that make the message Workflow Updates (``send_message``, ``start_turn``,
``steer_turn``) idempotent.

``MessageReceiptLedger`` keeps, per command id, the Turn each admitted message joined, so a retry
gets that Turn back. A ``send_message`` receipt also keeps the content digest, so a reuse of its
key with other content conflicts; a start or steer replays by command id alone (ADR 0038). The
Harness Runtime owns admission.
"""

import hashlib
import json

from mistralai.vibe_agents.sdk.app.worker.continuation import MessageReceiptRecord
from mistralai.vibe_agents.session_workflow.update_inputs import SendMessageInput

# ponytail: FIFO past this many message receipts, stored and carried. Retries come within
# seconds; an older retry still conflicts while the Runtime keeps its command id. Raise the
# bound if clients retry later, at about 100 bytes of continue-as-new input per receipt.
_MAX_RECEIPTS = 100


class MessageReceiptLedger:
    """Receipts of messages by command id, oldest first.

    The dictionary is the binding's carried publication state, so receipts survive
    Continue-As-New with it.
    """

    def __init__(self, receipts: dict[str, MessageReceiptRecord] | None = None) -> None:
        self._receipts = receipts if receipts is not None else {}

    def get(self, command_id: str) -> MessageReceiptRecord | None:
        return self._receipts.get(command_id)

    def begin(self, command_id: str, *, digest: str | None) -> MessageReceiptRecord:
        """Store the receipt of a message about to be handed to the Runtime."""

        receipt = MessageReceiptRecord(digest=digest)
        self._put(command_id, receipt)
        return receipt

    def keep(self, command_id: str, receipt: MessageReceiptRecord) -> None:
        """Store an admitted message's receipt again if a concurrent copy dropped it.

        Concurrent copies of one start or steer share a receipt, and a copy that is refused drops
        it, while /commands needs it to see the id of a committed steer as taken.
        """

        if command_id not in self._receipts:
            self._put(command_id, receipt)

    def _put(self, command_id: str, receipt: MessageReceiptRecord) -> None:
        self._receipts[command_id] = receipt
        if len(self._receipts) > _MAX_RECEIPTS:
            del self._receipts[next(iter(self._receipts))]

    def discard_unanswered(self, command_id: str) -> None:
        """Drop the receipt of a message refused before any answer was kept for it."""

        receipt = self._receipts.get(command_id)
        # A concurrent copy that was admitted or rejected keeps the shared receipt, so /commands
        # sees the id as taken, also after Continue-As-New.
        if (
            receipt is not None
            and receipt.turn_id is None
            and not (receipt.committed or receipt.refused or receipt.rejected)
        ):
            del self._receipts[command_id]


def build_message_digest(message: SendMessageInput) -> str:
    # Only the message, its entry id and its context messages decide a conflict, as Harness
    # ``MessageSendParams`` states. Metadata carries a per-request correlation id, and the source
    # names the sending surface, not the message. exclude_none keeps the digest stable when a
    # Harness release adds an optional block field. Not exclude_defaults: it drops the defaulted
    # block ``type``, so an image and an audio block with one URI would share a digest.
    content = message.model_dump(
        mode="json", include={"message", "message_entry_id", "context_messages"}, exclude_none=True
    )
    canonical = json.dumps(content, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


__all__ = [
    "MessageReceiptLedger",
    "build_message_digest",
]
