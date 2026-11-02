"""Receipts that make the ``send_message`` Workflow Update idempotent.

``MessageReceiptLedger`` keeps, per command id, the content digest and the Turn each admitted
message joined, so a retry with the same idempotency key gets that Turn back and a reuse of the
key with other content conflicts. ``message_command_id`` derives the command id from the Session
and the key. The Harness Runtime owns admission.
"""

import hashlib
import json

from mistralai.vibe_agents.sdk.app.worker.continuation import MessageReceiptRecord
from mistralai.vibe_agents.session_workflow.send_message import SendMessageInput, message_command_id

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

    def begin(self, command_id: str, *, digest: str) -> MessageReceiptRecord:
        """Store the receipt of a message about to be handed to the Runtime."""

        receipt = MessageReceiptRecord(digest=digest)
        self._receipts[command_id] = receipt
        if len(self._receipts) > _MAX_RECEIPTS:
            del self._receipts[next(iter(self._receipts))]
        return receipt

    def discard(self, command_id: str) -> None:
        self._receipts.pop(command_id, None)


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
    "message_command_id",
]
