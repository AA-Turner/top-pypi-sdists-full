"""Plugin: no-dangerous-sink — LLM output must not flow to dangerous sinks."""

from skylos.defend.plugin import DefensePlugin
from skylos.defend.result import DefenseResult
from skylos.discover.integration import LLMIntegration
from skylos.discover.graph import AIIntegrationGraph


class NoDangerousSinkPlugin(DefensePlugin):
    id = "no-dangerous-sink"
    name = "No Dangerous Output Sink"
    severity = "critical"
    owasp_llm = "LLM02"
    description = (
        "LLM output must not flow to code execution, shell, or injection-prone sinks"
    )
    remediation = (
        "Remove direct flow from LLM output to eval/exec/subprocess. "
        "Add output validation and sanitization before any dangerous operation."
    )

    def check(self, integration: LLMIntegration, graph: AIIntegrationGraph) -> DefenseResult:
        if not integration.output_sinks:
            return self._pass(
                integration,
                integration.location,
                "LLM output does not flow to any dangerous sink",
            )

        sinks = ", ".join(integration.output_sinks)
        return self._fail(
            integration,
            integration.location,
            f"LLM output flows to dangerous sink(s): {sinks}",
        )
