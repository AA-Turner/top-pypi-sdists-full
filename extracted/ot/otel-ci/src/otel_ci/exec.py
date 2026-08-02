import os
import subprocess
import sys

from opentelemetry import trace
from opentelemetry.sdk.resources import PROCESS_COMMAND, PROCESS_COMMAND_ARGS
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from otel_ci import github
from otel_ci.logging import logger


def exec_command(command: list[str], span_name: str | None = None) -> None:
    """Executes a command within a trace span"""
    logger.info("Executing command: ", command)
    tracer = trace.get_tracer(__name__)
    command_str = " ".join(command)

    # Create a TraceContextTextMapPropagator instance
    propagator = TraceContextTextMapPropagator()

    # Extract the trace context from the TRACEPARENT header
    trace_parent = os.environ.get("TRACEPARENT")
    carrier = {}
    if trace_parent:
        carrier["traceparent"] = trace_parent
    else:
        if os.environ.get("GITHUB_ACTION"):
            carrier["traceparent"] = (
                f"00-{github.get_job_trace_id()}-{github.get_job_span_id}-01"
            )
    context = propagator.extract(carrier)

    shell = os.environ.get("SHELL", "/bin/sh")

    with tracer.start_as_current_span(
        span_name or " ".join(command),
        attributes={PROCESS_COMMAND: command[0], PROCESS_COMMAND_ARGS: command},
        context=context,
    ) as span:
        obj: dict[str, str] = {}
        propagator.inject(obj)
        env = os.environ.copy()
        env["TRACEPARENT"] = obj["traceparent"]
        env["OTEL_CI"] = "true"

        try:
            code = subprocess.call(command_str, shell=True, env=env, executable=shell)
        except KeyboardInterrupt:
            code = 130
        if code != 0:
            span.set_status(
                status=trace.StatusCode.ERROR,
                description=f"Command exited with code {code}",
            )
        else:
            span.set_status(status=trace.StatusCode.OK)
        sys.exit(code)
