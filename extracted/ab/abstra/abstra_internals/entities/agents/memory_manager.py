from typing import List


class MemoryManager:
    def __init__(self) -> None:
        self.key_facts: List[str] = []

    def add_fact(self, fact: str) -> None:
        if fact not in self.key_facts:
            self.key_facts.append(fact)

    def get_facts_context(self) -> str:
        if not self.key_facts:
            return ""
        facts_str = "\n".join(f"- {fact}" for fact in self.key_facts)
        return f"\n## Long-term Memory (Key Facts)\n{facts_str}\n"


class MemoryReducer:
    SUMMARIZATION_THRESHOLD = 1500

    def __init__(self) -> None:
        self._summary = ""

    @property
    def summary(self) -> str:
        return self._summary

    def create_step_entry(
        self, step: int, action: str, action_input: str, observation: str
    ) -> str:
        obs_truncated = observation[:150].replace("\n", " ")
        if len(observation) > 150:
            obs_truncated += "..."
        input_display = action_input
        if len(action_input) > 100:
            input_display = action_input[:50] + "...[truncated]"
        return f"- Step {step}: {action}({input_display}) -> {obs_truncated}"

    def update(
        self, step: int, action: str, action_input: str, observation: str
    ) -> str:
        new_entry = self.create_step_entry(step, action, action_input, observation)

        if self._summary:
            self._summary = self._summary + "\n" + new_entry
        else:
            self._summary = new_entry

        if len(self._summary) > self.SUMMARIZATION_THRESHOLD:
            self._summary = self._compress(self._summary)

        return self._summary

    def _compress(self, text: str) -> str:
        lines = text.strip().split("\n")
        if len(lines) <= 5:
            return text
        kept = lines[:2] + ["- ... (earlier steps summarized)"] + lines[-3:]
        return "\n".join(kept)
