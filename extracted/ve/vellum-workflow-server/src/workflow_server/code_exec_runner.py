from datetime import datetime
import json
import logging
import os
from uuid import uuid4
from typing import Optional

from vellum.workflows.exceptions import WorkflowInitializationException
from workflow_server.api.workflow_view import get_workflow_request_context
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

        input_data = json.loads(input_json)
        context = get_workflow_request_context(input_data)

        print("--vellum-output-start--")  # noqa: T201

        initiated_event = VembdaExecutionInitiatedEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            trace_id=context.trace_id,
            span_id=context.execution_id,
            body=VembdaExecutionInitiatedBody.model_validate(get_version()),
            parent=None,
        ).model_dump_json()

        print(f"{_EVENT_LINE}{initiated_event}")  # noqa: T201

        try:
            stream_iterator, span_id = stream_workflow(context, disable_redirect=True)
            for line in stream_iterator:
                print(f"{_EVENT_LINE}{json.dumps(line)}")  # noqa: T201
        except WorkflowInitializationException as e:
            fulfilled_event = serialize_vembda_rejected_event(context, str(e))
            print(f"{_EVENT_LINE}{fulfilled_event}")  # noqa: T201
    except Exception as e:
        logger.exception(e)

        event = serialize_vembda_rejected_event(context, "Internal Server Error")
        print(f"{_EVENT_LINE}{event}")  # noqa: T201
