"""
Functional workflow agents using the @rollout decorator.
"""
import agentlightning as agl
from typing import Dict
from dslighting.training.rewards.base import RewardEvaluator


@agl.rollout
def train_aide_agent(
    task: Dict[str, Any],
    llm: agl.LLM,
    rollout: agl.Rollout,
    reward_evaluator: RewardEvaluator,
    ) -> float:
        """
    Train a functional agent with the AIDE workflow.

    Parameters
    ----------
    task : Dict[str, Any]
        Task dict.
    llm : agl.LLM
        Injected LLM resource.
    rollout : agl.Rollout
        Rollout context.
    reward_evaluator : RewardEvaluator
        Reward evaluator.

    Returns
    -------
    float
        Final reward.
    """
    from dslighting import Agent

    agl.emit_message(f"[AIDE] Starting training rollout for {task['task_id']}")

    # Use DSLighting Agent API.
    agent = Agent(
        workflow="aide",
        model=llm.model,
        api_base=llm.endpoint,
        api_key=llm.api_key,
    )

    # Run agent.
    result = agent.run(task_id=task["task_id"])

    # Compute reward.
    reward = reward_evaluator.evaluate(result, task)

    # Emit trace.
    agl.emit_object({
        "workflow": "aide",
        "score": result.score,
        "reward": reward,
    })

    return reward


@agl.rollout
def train_autokaggle_agent(
    task: Dict[str, Any],
    llm: agl.LLM,
    rollout: agl.Rollout,
    reward_evaluator: RewardEvaluator,
) -> float:
    """Train a functional agent with the AutoKaggle workflow."""
    from dslighting import Agent

    agl.emit_message(f"[AutoKaggle] Starting training rollout for {task['task_id']}")

    agent = Agent(
        workflow="autokaggle",
        model=llm.model,
        api_base=llm.endpoint,
        api_key=llm.api_key,
    )

    result = agent.run(task_id=task["task_id"])
    reward = reward_evaluator.evaluate(result, task)

    agl.emit_object({
        "workflow": "autokaggle",
        "score": result.score,
        "reward": reward,
    })

    return reward


@agl.rollout
def train_data_interpreter_agent(
    task: Dict[str, Any],
    llm: agl.LLM,
    rollout: agl.Rollout,
    reward_evaluator: RewardEvaluator,
) -> float:
    """Train a functional agent with the Data Interpreter workflow."""
    from dslighting import Agent

    agl.emit_message(f"[DataInterpreter] Starting training rollout for {task['task_id']}")

    agent = Agent(
        workflow="data_interpreter",
        model=llm.model,
        api_base=llm.endpoint,
        api_key=llm.api_key,
    )

    result = agent.run(task_id=task["task_id"])
    reward = reward_evaluator.evaluate(result, task)

    agl.emit_object({
        "workflow": "data_interpreter",
        "score": result.score,
        "reward": reward,
    })

    return reward


__all__ = [
    "train_aide_agent",
    "train_autokaggle_agent",
    "train_data_interpreter_agent",
]
