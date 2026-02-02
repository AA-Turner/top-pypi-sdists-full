"""
Custom operator base classes and helpers.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class BaseOperator(ABC):
    """
    Base class for custom operators.

    Subclasses should implement the async run() method.
    """

    def __init__(
        self,
        llm_service=None,
        sandbox_service=None,
        name: Optional[str] = None
    ):
        """
        Initialize the operator.

        Args:
            llm_service: Optional LLM service for LLM-backed operators.
            sandbox_service: Optional sandbox service for code execution.
            name: Optional operator name (defaults to class name).
        """
        self.llm_service = llm_service
        self.sandbox_service = sandbox_service
        self.name = name or self.__class__.__name__

    async def __call__(self, **kwargs) -> Any:
        """
        Invoke the operator asynchronously.

        This forwards to run(**kwargs) so operators can be called like functions.
        """
        return await self.run(**kwargs)

    @abstractmethod
    async def run(self, **kwargs) -> Any:
        """
        Execute operator logic.

        Returns:
            Operator result.
        """
        raise NotImplementedError("Subclasses must implement run()")


class SimpleOperator(BaseOperator):
    """
    Wrap a simple async function as an operator.

    Example:
        >>> from dslighting.operators.custom import SimpleOperator
        >>>
        >>> async def my_logic(data: str) -> str:
        ...     return data.upper()
        >>>
        >>> op = SimpleOperator(func=my_logic)
        >>> result = await op(data="hello")
        >>> print(result)  # "HELLO"
    """

    def __init__(self, func, name: Optional[str] = None):
        """
        Args:
            func: Async function to execute.
            name: Optional operator name.
        """
        super().__init__(name=name)
        self.func = func

    async def run(self, **kwargs) -> Any:
        """Execute the wrapped function."""
        return await self.func(**kwargs)


class LLMOperator(BaseOperator):
    """
    Operator that calls an LLM with a prompt template.

    Example:
        >>> from dslighting.operators.custom import LLMOperator
        >>>
        >>> op = LLMOperator(
        ...     llm_service=llm,
        ...     system_prompt="You are a data scientist",
        ...     user_prompt_template="Analyze: {data}"
        ... )
        >>> result = await op(data="bike dataset")
    """

    def __init__(
        self,
        llm_service,
        system_prompt: str,
        user_prompt_template: str = "{input}",
        name: Optional[str] = None
    ):
        """
        Args:
            llm_service: LLM service instance.
            system_prompt: System prompt text.
            user_prompt_template: Template for user prompt (format with kwargs).
            name: Optional operator name.
        """
        super().__init__(llm_service=llm_service, name=name)
        self.system_prompt = system_prompt
        self.user_prompt_template = user_prompt_template

    async def run(self, input: str, **kwargs) -> str:
        """
        Run the LLM operator.

        Args:
            input: Primary input string.
            **kwargs: Additional fields for template formatting.

        Returns:
            LLM response text.
        """
        # Build user prompt from template.
        user_prompt = self.user_prompt_template.format(input=input, **kwargs)

        # Compose full prompt.
        prompt = f"{self.system_prompt}\n\n{user_prompt}"
        response = await self.llm_service.call(prompt)

        return response


class CodeExecutorOperator(BaseOperator):
    """
    Operator that executes code in a sandbox.

    Example:
        >>> from dslighting.operators.custom import CodeExecutorOperator
        >>>
        >>> op = CodeExecutorOperator(
        ...     sandbox_service=sandbox,
        ...     code_template="print('Processing: {data}')"
        ... )
        >>> result = await op(data="test.csv")
    """

    def __init__(
        self,
        sandbox_service,
        code_template: str,
        name: Optional[str] = None
    ):
        """
        Args:
            sandbox_service: Sandbox service instance.
            code_template: Code template to render with kwargs.
            name: Optional operator name.
        """
        super().__init__(sandbox_service=sandbox_service, name=name)
        self.code_template = code_template

    async def run(self, **kwargs) -> Dict[str, Any]:
        """
        Execute rendered code in the sandbox.

        Returns:
            Dict: {"success": bool, "output": str, "error": str}
        """
        # Render code template.
        code = self.code_template.format(**kwargs)

        # Execute in sandbox.
        result = await self.sandbox_service.run_script(code)

        return {
            "success": result.success,
            "output": result.stdout,
            "error": result.stderr
        }


class ChainedOperator(BaseOperator):
    """
    Run operators sequentially, passing results forward.

    Example:
        >>> from dslighting.operators.custom import ChainedOperator
        >>>
        >>> op = ChainedOperator([
        ...     LLMOperator(llm, "You are an analyzer"),
        ...     CodeExecutorOperator(sandbox, "print({input})")
        ... ])
        >>> result = await op(input="data")
    """

    def __init__(self, operators: list, name: Optional[str] = None):
        """
        Args:
            operators: List of operators to run in order.
            name: Optional operator name.
        """
        super().__init__(name=name)
        self.operators = operators

    async def run(self, **kwargs) -> Any:
        """Execute all operators in sequence."""
        result = kwargs

        for i, op in enumerate(self.operators):
            logger.info(f"ChainedOperator: Step {i+1}/{len(self.operators)} - {op.name}")
            result = await op(**result)

        return result


class ConditionalOperator(BaseOperator):
    """
    Conditionally run one of two operators.

    Example:
        >>> from dslighting.operators.custom import ConditionalOperator
        >>>
        >>> def has_error(result):
        ...     return not result.get("success", True)
        >>>
        >>> op = ConditionalOperator(
        ...     condition=has_error,
        ...     if_op=RetryOperator(),
        ...     else_op=SaveOperator()
        ... )
        >>> result = await op(data="test.csv")
    """

    def __init__(
        self,
        condition: callable,
        if_op: BaseOperator,
        else_op: Optional[BaseOperator] = None,
        name: Optional[str] = None
    ):
        """
        Args:
            condition: Predicate function on current result dict.
            if_op: Operator to run when condition is True.
            else_op: Operator to run when condition is False.
            name: Optional operator name.
        """
        super().__init__(name=name)
        self.condition = condition
        self.if_op = if_op
        self.else_op = else_op

    async def run(self, **kwargs) -> Any:
        """Execute conditionally based on predicate."""
        # Start with current kwargs as result.
        result = kwargs

        # Evaluate condition and dispatch.
        if self.condition(result):
            logger.info(f"ConditionalOperator: Condition True -> {self.if_op.name}")
            return await self.if_op(**result)
        elif self.else_op:
            logger.info(f"ConditionalOperator: Condition False -> {self.else_op.name}")
            return await self.else_op(**result)
        else:
            return result


# ============================================================================
# Helper factory functions
# ============================================================================

def create_llm_operator(llm_service, system_prompt: str, **kwargs) -> LLMOperator:
    """
    Convenience helper to create an LLMOperator.

    Example:
        >>> from dslighting.operators.custom import create_llm_operator
        >>>
        >>> analyzer = create_llm_operator(
        ...     llm_service=llm,
        ...     system_prompt="You are a data analyst"
        ... )
    """
    return LLMOperator(llm_service, system_prompt, **kwargs)


def create_code_operator(sandbox_service, code_template: str, **kwargs) -> CodeExecutorOperator:
    """
    Convenience helper to create a CodeExecutorOperator.

    Example:
        >>> from dslighting.operators.custom import create_code_operator
        >>>
        >>> executor = create_code_operator(
        ...     sandbox_service=sandbox,
        ...     code_template="print('{data}')"
        ... )
    """
    return CodeExecutorOperator(sandbox_service, code_template, **kwargs)
