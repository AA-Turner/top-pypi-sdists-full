"""Load platform code before assignment while retaining one fresh process per authored invocation."""

import json
import os
import sys

from labqoat.json_document import JsonDocument
from labqoat.stage_timer import StageTimer


class PreparedWorker:
    """Receive one bounded private envelope, then enter the ordinary fenced worker lifecycle."""

    @staticmethod
    def main() -> None:
        """No authored imports, credentials or effects exist until the physical worker supplies an assignment."""
        timing = StageTimer.stderr()
        from labqoat.compute.worker.compute_worker import ComputeWorker

        timing.stage("prepared.sdk_import")
        line = sys.stdin.buffer.readline(1_048_577)
        if not line:
            return
        if len(line) > 1_048_576 or not line.endswith(b"\n"):
            raise ValueError("Prepared assignment exceeds its framing limit")
        environment = JsonDocument.expect_dict(json.loads(line))
        os.environ.update({key: JsonDocument.expect_scalar(value, str) for key, value in environment.items()})
        timing.stage("prepared.assignment_wait")
        ComputeWorker.main()
