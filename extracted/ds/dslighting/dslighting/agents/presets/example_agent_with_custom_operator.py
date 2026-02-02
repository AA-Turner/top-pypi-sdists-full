"""
Example: Agent with a custom Operator

This is a complete example showing how to use a custom Operator in a custom Agent.
"""
import logging
from pathlib import Path
from typing import Dict, Any

from dslighting.agents import BaseAgent
from dslighting.services import LLMService, SandboxService
from dslighting.operators.custom import TextAnalysisOperator

logger = logging.getLogger(__name__)


class ExampleAgentWithCustomOperator(BaseAgent):
    """
    Example Agent - uses a custom Operator.

    Features:
    1. Use TextAnalysisOperator to analyze the task.
    2. Use standard operators to generate and execute code.
    """

    def __init__(
        self,
        operators: Dict[str, Any],
        services: Dict[str, Any],
        agent_config: Dict[str, Any],
    ):
        """
        Initialize the agent.

        Args:
            operators: Operator registry (including custom operators).
            services: Service registry.
            agent_config: Agent configuration.
        """
        super().__init__(operators, services, agent_config)

        # ===== Standard Operators =====
        self.execute_op = operators["execute"]
        self.generate_op = operators["generate"]

        # ===== Custom Operators =====
        # Defined in custom/example_operator.py
        self.text_analysis_op = operators["text_analysis"]

        # ===== Services =====
        self.llm_service: LLMService = services["llm"]
        self.sandbox_service: SandboxService = services["sandbox"]

        # ===== Configuration =====
        self.max_iterations = agent_config.get("max_iterations", 5)

        logger.info(f"[{self.__class__.__name__}] Initialized with custom operator")

    async def solve(
        self,
        description: str,
        io_instructions: str,
        data_dir: Path,
        output_path: Path
    ) -> None:
        """
        Core solve method.

        Args:
            description: Task description.
            io_instructions: I/O instructions.
            data_dir: Data directory.
            output_path: Output path.
        """
        logger.info(f"[{self.__class__.__name__}] Starting task")
        logger.info(f"  Description: {description[:100]}...")

        # ===== Step 1: analyze task with custom operator =====
        logger.info("\n--- Step 1: Analyzing task with custom operator ---")
        analysis = await self.text_analysis_op(
            text=description,
            analysis_type="summary"
        )
        logger.info(f"Task summary: {analysis['raw_response'][:200]}...")

        # ===== Step 2: generate code with standard operator =====
        logger.info("\n--- Step 2: Generating code ---")
        prompt = f"""
Task: {description}

Instructions:
{io_instructions}

Data directory: {data_dir}

Please generate Python code to solve this task.
"""

        plan, code = await self.generate_op(system_prompt=prompt)
        logger.info(f"Generated plan: {plan[:100]}...")
        logger.info(f"Generated code: {len(code)} characters")

        # ===== Step 3: execute code with standard operator =====
        logger.info("\n--- Step 3: Executing code ---")
        exec_result = await self.execute_op(code=code, mode="script")

        if exec_result.success:
            logger.info("✓ Code executed successfully")
            logger.info(f"Output: {exec_result.stdout[:200]}...")

            # ===== Step 4: save results =====
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(exec_result.stdout)

            logger.info(f"✓ Result saved to {output_path}")

        else:
            logger.error(f"✗ Code execution failed: {exec_result.stderr}")
            raise RuntimeError(f"Execution failed: {exec_result.stderr}")

        logger.info(f"\n[{self.__class__.__name__}] Task completed successfully")


Example usage
"""
# Configuration
from dslighting.services import LLMService, SandboxService
from dslighting.operators import GenerateCodeAndPlanOperator, ExecuteAndTestOperator
from dslighting.operators.custom import TextAnalysisOperator
from dslighting.state import JournalState

# 1. Create services
services = {
    "llm": LLMService(model="gpt-4o"),
    "sandbox": SandboxService(),
    "state": JournalState(),
    "workspace": None,
}

# 2. Create operators
operators = {
    "generate": GenerateCodeAndPlanOperator(llm_service=services["llm"]),
    "execute": ExecuteAndTestOperator(sandbox_service=services["sandbox"]),
    "text_analysis": TextAnalysisOperator(llm_service=services["llm"]),  # Custom operator
}

# 3. Create agent config
agent_config = {
    "max_iterations": 5,
}

# 4. Create agent
agent = ExampleAgentWithCustomOperator(operators, services, agent_config)

# 5. Run
import asyncio

async def main():
    await agent.solve(
        description="Analyze data and generate a report",
        io_instructions="Read train.csv and generate report.txt",
        data_dir=Path("./data"),
        output_path=Path("./output/result.txt")
    )

asyncio.run(main())
"""
