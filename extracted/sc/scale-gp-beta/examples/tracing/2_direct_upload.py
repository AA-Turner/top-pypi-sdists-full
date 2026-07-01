import uuid
from datetime import datetime, timezone, timedelta

import scale_gp_beta.lib.tracing as tracing
from scale_gp_beta import SGPClient


def main() -> None:
    parent_span_id = str(uuid.uuid4())
    trace_id = str(uuid.uuid4())
    child_span_id = str(uuid.uuid4())

    now = datetime.now(timezone.utc)

    start_time = (now - timedelta(minutes=10)).isoformat()
    end_time = now.isoformat()
    parent_span = tracing.create_span(
        "my_parent_span_name",
        input={"test": "input"},
        output={"test": "output"},
        metadata={"test": "metadata"},
        span_id=parent_span_id,
        trace_id=trace_id,
    )
    parent_span.start_time = start_time
    parent_span.end_time = end_time
    parent_span.flush()

    start_time = (now - timedelta(minutes=6)).isoformat()
    end_time = (now - timedelta(minutes=2)).isoformat()
    child_span = tracing.create_span(
        "my_child_span_name",
        input={"test": "another input"},
        output={"test": "another output"},
        metadata={"test": "another metadata"},
        span_id=child_span_id,
        trace_id=trace_id,
        parent_id=parent_span_id,
    )
    child_span.start_time = start_time
    child_span.end_time = end_time
    child_span.flush()


if __name__ == "__main__":
    api_key = "xxx"
    account_id = "xxx"
    tracing.init(SGPClient(api_key=api_key, account_id=account_id), disabled=False)
    main()
