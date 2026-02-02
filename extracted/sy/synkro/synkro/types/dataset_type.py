"""Dataset type enum for steering generation pipeline."""

from enum import Enum


class DatasetType(str, Enum):
    """
    Type of dataset to generate.

    The dataset type determines:
    - Prompts used for scenario and response generation
    - Conversation turns (INSTRUCTION/EVALUATION forces 1 turn)
    - Output format and schema

    Examples:
        >>> from synkro import DatasetType
        >>> synkro.generate(policy, dataset_type=DatasetType.CONVERSATION)  # Multi-turn
        >>> synkro.generate(policy, dataset_type=DatasetType.INSTRUCTION)   # Single-turn
        >>> synkro.generate(policy, dataset_type=DatasetType.EVALUATION)    # Q&A with ground truth
        >>> synkro.generate(policy, dataset_type=DatasetType.TOOL_CALL, tools=[...])
    """

    CONVERSATION = "conversation"
    """Multi-turn conversation: {messages: [{role, content}, ...]} with multiple exchanges"""

    INSTRUCTION = "instruction"
    """Single-turn instruction-following: {messages: [{role: "user"}, {role: "assistant"}]}"""

    EVALUATION = "evaluation"
    """Q&A evaluation dataset: {question, answer, expected_answer, ground_truth_rules, difficulty}"""

    TOOL_CALL = "tool_call"
    """Tool Calling: {messages: [..., {tool_calls: [...]}, {role: tool}, ...]}"""
