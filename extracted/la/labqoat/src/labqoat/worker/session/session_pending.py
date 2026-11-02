"""One retained command and its local receipt waiter survive network reconnection."""

import asyncio
from dataclasses import dataclass

from labqoat.json_document import JsonDocument
from labqoat.worker.child_result_frame import ChildResultFrame
from labqoat.worker.session.session_frames import SessionFrames
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass
class SessionPending:
    """Keep operation identity stable until the server acknowledges its committed outcome."""

    command: JsonDocument
    receipt: asyncio.Future[JsonDocument]
    updates: asyncio.Queue[JsonDocument] | None = None
    finished: bool = False

    def ready(self) -> bool:
        """Do not request another remote subset while a received frame still occupies its bounded local queue."""
        return not self.finished and (self.updates is None or self.updates.empty())

    def deliver(self, frame: JsonDocument) -> None:
        """Advance resumable identities as frames arrive, before the local consumer can disconnect."""
        if self.updates is None:
            try:
                self.receipt.set_result(SessionFrames.result(frame))
            except Exception as error:
                self.receipt.set_exception(error)
            return
        if "error" in frame:
            self.finished = True
        else:
            data = JsonDocument.expect_dict(self.command["data"])
            ids = [JsonDocument.expect_scalar(item, str) for item in JsonDocument.expect_list(data["ids"])]
            results = ChildResultFrame.capture(SessionFrames.result(frame), set(ids))
            remaining = [identity for identity in ids if identity not in results]
            if frame.get("more") is not bool(remaining):
                raise WorkerApiError("Child subscription progress is invalid", 502)
            self.command["data"] = {"ids": list(remaining)}
            self.finished = not remaining
        self.updates.put_nowait(frame)
