"""Plugin: untrusted-input-to-prompt — detect raw user input flowing to prompt construction."""

from skylos.defend.plugin import DefensePlugin
from skylos.defend.result import DefenseResult
from skylos.discover.integration import LLMIntegration
from skylos.discover.graph import AIIntegrationGraph


class UntrustedInputToPromptPlugin(DefensePlugin):
    id = "untrusted-input-to-prompt"
    name = "Untrusted Input to Prompt"
    severity = "critical"
    owasp_llm = "LLM01"
    description = (
        "User-controlled input must not flow directly into prompt construction "
        "without intermediate processing (validation, escaping, delimiters)"
    )
    remediation = (
        "Add input validation, sanitization, or prompt delimiters between "
        "user input and prompt construction. Use structured prompt templates."
    )

    def applies_to(self, integration: LLMIntegration) -> bool:
        return bool(integration.input_sources) and bool(integration.prompt_sites)

    def check(self, integration: LLMIntegration, graph: AIIntegrationGraph) -> DefenseResult:
        # Pass if an input-side defense exists between input and prompt
        # Note: output_validation is NOT an input defense — it validates LLM output,
        # not user input, so it does not prevent prompt injection
        has_defense = (
            integration.has_prompt_delimiter
            or integration.has_input_length_limit
        )

        if has_defense:
            return self._pass(
                integration,
                integration.location,
                "Input-to-prompt flow has intermediate processing",
            )

        sources = ", ".join(integration.input_sources[:3])
        return self._fail(
            integration,
            integration.location,
            f"Raw input ({sources}) flows directly to prompt construction",
        )
