from opentelemetry import trace

from mistralai.workflows import activity, workflow

WORKFLOW_TYPE = "workflow-context-probe"
ACTIVITY_TYPE = "workflow_context_probe_activity"

# Tracer the probe activity creates its manual span with. The test binds it to the provider
# it captures spans from; the fallback only covers running the activity outside the test.
probe_tracer: trace.Tracer | None = None


@activity(name=ACTIVITY_TYPE)
async def workflow_context_probe_activity(probe_server_url: str) -> str:
    # Imports live in the body: activities run host-side, but the sandbox imports this
    # module to load the workflow class, so its top level must stay sandbox-clean.
    from mistralai.workflows._mistral_http import MISTRAL_HTTP
    from mistralai.workflows.models import EventAttributes

    producer_attributes = {EventAttributes.workflow_type: "producer-set-type"}
    tracer = probe_tracer or trace.get_tracer("workflow-context-probe")
    with tracer.start_as_current_span("manual_probe_span", attributes=producer_attributes):
        async with MISTRAL_HTTP.AsyncClient() as client:
            await client.get(probe_server_url)
    return "ok"


@workflow.define(name=WORKFLOW_TYPE)
class WorkflowContextProbeWorkflow:
    @workflow.entrypoint
    async def run(self, probe_server_url: str) -> str:
        return await workflow_context_probe_activity(probe_server_url)
