#!/usr/bin/env python
"""One-off script to test AgentService.get_agent_spans()"""

from pycarlo.features.agent import AgentService, AgentSpanFilter

service = AgentService()

result = service.get_agent_spans(
    mcon="MCON++a5cbd8cc-8e91-4a41-aca4-4bf5bd320578++e55332d7-f832-436a-b46a-6e4f7257bde4++table++ingest:opentelemetry.traces",
    agent_span_filters=[
        AgentSpanFilter(
            agent="mc-internal-sentry-root-cause-agent",
            workflow="Sentry Root Cause Agent",
            task="analyze_and_summarize",
            span_name="ChatBedrockConverse.chat",
        )
    ],
    limit=1
)

print(f"has_error: {result.has_error}")
print(f"error: {result.error}")
print(f"row_count: {result.row_count}")
print(f"columns: {result.columns}")
print(f"rows: {result.rows}")

