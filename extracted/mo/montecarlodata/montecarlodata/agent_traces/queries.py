"""GraphQL strings for the agent-trace export flow.

Raw strings (not pycarlo typed bindings) because the schema regen that
generates pycarlo's typed mutation/query for exportAgentTrace + getAgentTraceExport
lands separately from this CLI work. Once pycarlo has the bindings, this
module can be migrated to typed Mutation()/Query() calls.
"""

EXPORT_AGENT_TRACE = """
mutation ExportAgentTrace($mcon: String!, $traceId: String!) {
    exportAgentTrace(mcon: $mcon, traceId: $traceId) {
        jobId
    }
}
"""

GET_AGENT_TRACE_EXPORT = """
query GetAgentTraceExport($jobId: UUID!) {
    getAgentTraceExport(jobId: $jobId) {
        status
        url
        error
        createdTime
        expiresAt
    }
}
"""

EXPECTED_EXPORT_AGENT_TRACE = "exportAgentTrace"
EXPECTED_GET_AGENT_TRACE_EXPORT = "getAgentTraceExport"
