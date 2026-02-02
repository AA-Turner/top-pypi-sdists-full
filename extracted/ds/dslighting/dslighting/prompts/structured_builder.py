"""
Structured Prompt Builder - dict-based prompt builder.

Recommended usage: define input/output models with Pydantic, then build prompts with StructuredPromptBuilder.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel


class StructuredPromptBuilder:
    """
    Structured prompt builder.

    Recommended format:
    ```python
    prompt_dict = {
        "Role": "You are an expert...",
        "Task Goal": "...",
        "Input Data": {...},
        "Instructions": {
            "Goal": "...",
            "Guideline": "...",
        }
    }
    ```

    Example:
        builder = StructuredPromptBuilder()
        prompt = builder.build(prompt_dict)
    """

    def __init__(self, max_length: Optional[int] = None):
        """
        Initialize the builder.

        Args:
            max_length: Maximum prompt length (characters).
        """
        self.max_length = max_length

    def build(self, prompt_dict: Dict[str, Any]) -> str:
        """
        Build the final prompt string.

        Args:
            prompt_dict: Structured prompt dict.

        Returns:
            Formatted prompt string.
        """
        prompt = self._dict_to_str(prompt_dict, indent=0)

        # Truncate to max length.
        if self.max_length and len(prompt) > self.max_length:
            prompt = prompt[:self.max_length] + "\n...[truncated]"

        return prompt

    def _dict_to_str(self, d: Dict, indent: int = 0) -> str:
        """Convert a dict to a formatted string."""
        lines = []
        prefix = "  " * indent

        for key, value in d.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(self._dict_to_str(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{prefix}{key}:")
                for item in value:
                    if isinstance(item, dict):
                        lines.append(f"{prefix}  -")
                        lines.append(self._dict_to_str(item, indent + 2))
                    else:
                        lines.append(f"{prefix}  - {item}")
            else:
                lines.append(f"{prefix}{key}: {value}")

        return "\n".join(lines)


class PromptTemplate:
    """
    Base class for prompt templates.

    Recommended to subclass this to define your prompt templates.

    Example:
        class MyOperatorPrompt(PromptTemplate):
            def get_input_schema(self):
                return MyInputModel

            def get_output_schema(self):
                return MyOutputModel

            def build(self, **kwargs):
                return {
                    "Role": "You are...",
                    "Task": kwargs["task"],
                    ...
                }
    """

    def get_input_schema(self) -> Optional[BaseModel]:
        """
        Return the input Pydantic model.

        Returns:
            Pydantic BaseModel class.
        """
        return None

    def get_output_schema(self) -> Optional[BaseModel]:
        """
        Return the output Pydantic model.

        Returns:
            Pydantic BaseModel class.
        """
        return None

    def build(self, **kwargs) -> Dict[str, Any]:
        """
        Build a prompt dict.

        Args:
            **kwargs: Input parameters.

        Returns:
            Prompt dict.
        """
        raise NotImplementedError("Subclasses must implement build()")


# ===== Helper functions =====

def truncate_output(text: str, max_length: int) -> str:
    """
    Truncate output to a specified length.

    Args:
        text: Original text.
        max_length: Maximum length.

    Returns:
        Truncated text.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "\n...[truncated]"


def format_code_block(code: str, language: str = "python") -> str:
    """
    Format a code block.

    Args:
        code: Code string.
        language: Language identifier.

    Returns:
        Formatted code block.
    """
    return f"```{language}\n{code}\n```"


def create_structured_prompt(
    role: str,
    task_goal: str,
    instructions: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
    guidelines: Optional[List[str]] = None,
    requirements: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Helper to quickly create a structured prompt.

    Args:
        role: Role.
        task_goal: Task goal.
        instructions: Instruction dict.
        context: Context information (optional).
        guidelines: Guideline list (optional).
        requirements: Requirements list (optional).

    Returns:
        Prompt dict.
    """
    prompt_dict = {
        "Role": role,
        "Task Goal": task_goal,
    }

    # Add context.
    if context:
        prompt_dict.update(context)

    # Build instructions.
    instructions_dict = dict(instructions)

    # Add guidelines.
    if guidelines:
        instructions_dict["Guidelines"] = guidelines

    # Add requirements.
    if requirements:
        instructions_dict["Requirements"] = requirements

    prompt_dict["Instructions"] = instructions_dict

    return prompt_dict
