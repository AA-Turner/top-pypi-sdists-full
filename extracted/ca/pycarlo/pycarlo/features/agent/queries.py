# Queries related to Agent spans

GET_AGENT_SPAN_SAMPLE_V2 = """
query getAgentSpanSampleV2(
    $mcon: String!,
    $spanIds: [String!],
    $traceIds: [String!],
    $agentSpanFilters: [AgentSpanFilterInput!],
    $attributeFilters: [SpanAttributeFilterInput!],
    $limit: Int,
    $offset: Int,
    $ingestionStartTime: DateTime,
    $ingestionEndTime: DateTime
) {
    getAgentSpanSampleV2(
        mcon: $mcon,
        spanIds: $spanIds,
        traceIds: $traceIds,
        agentSpanFilters: $agentSpanFilters,
        attributeFilters: $attributeFilters,
        selectExpressionType: ALL,
        limit: $limit,
        offset: $offset,
        ingestionStartTime: $ingestionStartTime,
        ingestionEndTime: $ingestionEndTime
    ) {
        hasError
        error
        columns
        rows
    }
}
"""
