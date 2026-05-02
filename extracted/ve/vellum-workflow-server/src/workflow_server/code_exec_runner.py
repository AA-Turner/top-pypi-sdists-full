from datetime import datetime
import logging
import os
from threading import Event as ThreadingEvent
from uuid import uuid4
from typing import Optional

import orjson

from workflow_server.core.events import VembdaExecutionInitiatedBody, VembdaExecutionInitiatedEvent
from workflow_server.core.executor import stream_workflow
from workflow_server.core.utils import serialize_vembda_rejected_event
from workflow_server.core.workflow_executor_context import WorkflowExecutorContext
from workflow_server.utils.utils import get_version

logger = logging.getLogger(__name__)

_EVENT_LINE = "--event--"


def run_code_exec_stream() -> None:
    context: Optional[WorkflowExecutorContext] = None

    try:
        input_raw = ""
        while "--vellum-input-stop--" not in input_raw:
            # os/read they come in chunks of idk length, not as lines
            input_raw += os.read(0, 100_000_000).decode("utf-8")

        split_input = input_raw.split("\n--vellum-input-stop--\n")
        input_json = split_input[0]

        input_data = orjson.loads(input_json)
        context = WorkflowExecutorContext.model_validate(input_data)

        print("--vellum-output-start--")  # noqa: T201

        if not context.exclude_vembda_events:
            initiated_event = VembdaExecutionInitiatedEvent(
                id=uuid4(),
                timestamp=datetime.now(),
                trace_id=context.trace_id,
                span_id=context.execution_id,
                body=VembdaExecutionInitiatedBody.model_validate(get_version()),
                parent=None,
            ).model_dump_json()

            print(f"{_EVENT_LINE}{initiated_event}")  # noqa: T201

        stream_iterator, span_id = stream_workflow(
            context,
            disable_redirect=True,
            # Timeouts are handled at the code exec level right now so just passing in an unused threading event
            timeout_signal=ThreadingEvent(),
            cancel_signal=ThreadingEvent(),
        )
        for line in stream_iterator:
            print(f"{_EVENT_LINE}{orjson.dumps(line).decode('utf-8')}")  # noqa: T201
    except Exception as e:
        logger.exception(e)

        event = serialize_vembda_rejected_event(context, "Internal Server Error")
        print(f"{_EVENT_LINE}{event}")  # noqa: T201
