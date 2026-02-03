# Queries related to Monitor execution

RUN_MONITOR = """
mutation runMonitor($monitorUuid: UUID!, $runtimeVariables: [RuntimeVariableValueInput!]) {
    runMonitor(monitorUuid: $monitorUuid, runtimeVariables: $runtimeVariables) {
        success
        manualMonitorExecutionUuid
    }
}
"""

GET_MANUAL_MONITOR_EXECUTION_STATUS = """
query getManualMonitorExecutionStatus($manualMonitorExecutionUuid: UUID!) {
    getManualMonitorExecutionStatus(manualMonitorExecutionUuid: $manualMonitorExecutionUuid) {
        status
        breached
        completed
    }
}
"""

GET_AGENT_MONITOR_MINIMAL = """
query getMonitor($uuids: [String]) {
    getMonitors(uuids: $uuids) {
        uuid
        name
        description
        monitorType
        entityMcons
        agentSpanFilters {
            agent { value }
            spanName { value }
            task { value }
            workflow { value }
        }
        filters {
            type
            operator
            conditions {
                ... on FilterBinary {
                    type
                    predicate { name negated }
                    left { type ... on FilterValueMapKey { key } }
                    right { type ... on FilterValueLiteral { literal } }
                }
            }
        }
    }
}
"""
