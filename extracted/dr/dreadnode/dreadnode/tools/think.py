from loguru import logger

from dreadnode.agents.tools import tool


@tool
def think(thought: str) -> None:
    """
    Records a thought, reflection, or plan to document your reasoning process.

    This tool acts as your internal monologue, allowing you to articulate your strategy. Use it to:
    - Break down a complex problem into smaller steps.
    - Formulate a multi-step plan before you act.
    - Interpret the results of another tool's output.
    - Document a change in strategy (self-correction).

    A clear chain of thought is essential for explaining your actions.

    ## Best Practices
    - Do Not Substitute for Action**: After thinking, you must call the appropriate \
    tool to execute your plan. This tool performs no action on its own.
    - Do Not Repeat Information**: Never use this to repeat the output of other tools. \
    Use it to state your *conclusion* or *next step* based on that output.

    Args:
        thought: A clear, concise statement of your thought process or plan.
    """
    logger.info(f"Agent thought: {thought}")
