"""Full GLM-5.3 text rendering through its checkpoint-owned template."""

from river_client.renderers.glm52 import Glm52Renderer


class Glm53Renderer(Glm52Renderer):
    model_label = "GLM-5.3"
    reasoning_efforts = ("low", "high", "max")

    def _render(self, messages, *, generation, tools=None):
        text = super()._render(messages, generation=generation, tools=tools)
        if generation and not self.thinking:
            # The upstream full-model template ignores enable_thinking. Prefill
            # the empty reasoning block so generation starts in the answer.
            if not text.endswith("<think>"):
                raise ValueError("GLM-5.3 generation prompt must end in <think>")
            text += "</think>"
        return text
