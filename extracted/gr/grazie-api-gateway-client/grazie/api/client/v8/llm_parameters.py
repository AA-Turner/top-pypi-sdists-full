from grazie.api.client.llm_parameters import BaseParameters
from grazie.api.client.v8.parameters import Parameters


class LLMParameters(BaseParameters):
    # Speeds up and optimizes model responses when the response is supposed to be a minor modification of existing content.
    # Work only with OpenAI GPT 4.1, GPT-4o, and GPT-4o-mini series models.
    PredictedOutput = Parameters.StrKey("llm.parameters.predicted-output")

    # Lets you define how much time the models will spend thinking before they provide an answer.
    # Available for OpenAI reasoning models, such as o1, o3, and o4 series models.
    ReasoningEffort = Parameters.StrKey("llm.parameters.reasoning-effort")

    # Defines how many responses the model should generate for a single input message.
    NumberOfChoices = Parameters.IntKey("llm.parameters.number-of-choices")

    # Indicates the insertion location of cache points.
    # Available only for Anthropic models.
    CachePoints = Parameters.JsonKey("llm.parameters.cache-points")

    # JSON-format tool definition
    Tools = Parameters.JsonKey("llm.parameters.tools")

    # Run the tools in parallel. Enabled by default.
    ParallelToolCalls = Parameters.BooleanKey("llm.parameters.parallel-tool-calls")

    # The way how the model should handle tool calls.
    ToolChoiceAuto = Parameters.BooleanKey("llm.parameters.tool-choice-auto")
    ToolChoiceNone = Parameters.BooleanKey("llm.parameters.tool-choice-none")
    ToolChoiceRequired = Parameters.BooleanKey("llm.parameters.tool-choice-required")
    ToolChoiceNamed = Parameters.StrKey("llm.parameters.tool-choice-named")
    ThinkingBudget = Parameters.IntKey("llm.parameters.thinking-budget")
