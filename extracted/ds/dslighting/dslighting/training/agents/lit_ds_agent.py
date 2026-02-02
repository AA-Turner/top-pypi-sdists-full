"""
DSLighting Training Agent - wraps DSAT workflows.

Wrap DSAT workflows as Agent-Lightning LitAgent.
"""
import agentlightning as agl
from typing import Any, Dict

try:
    from dsat.workflows.factory import get_workflow
except ImportError:
    get_workflow = None

from dslighting.training.rewards.base import RewardEvaluator


class LitDSAgent(agl.LitAgent[Dict[str, Any]]):
    """
    Wrap a DSAT workflow as an Agent-Lightning training agent.

    Parameters
    ----------
    workflow_name : str
        DSAT workflow name (e.g., "aide", "autokaggle", "data_interpreter").
    workflow_config : Dict[str, Any]
        Workflow configuration.
    reward_evaluator : RewardEvaluator
        Reward evaluator.
    max_steps : int, default=100
        Maximum execution steps.
    """

    def __init__(
        self,
        workflow_name: str,
        workflow_config: Dict[str, Any],
        reward_evaluator: RewardEvaluator,
        max_steps: int = 100,
    ):
        super().__init__()
        self.workflow_name = workflow_name
        self.workflow_config = workflow_config
        self.reward_evaluator = reward_evaluator
        self.max_steps = max_steps

    def rollout(
        self,
        task: Dict[str, Any],
        resources: agl.NamedResources,
        rollout: agl.Rollout
    ) -> float:
        """
        Execute a workflow rollout.

        Parameters
        ----------
        task : Dict[str, Any]
            Task dict containing:
            - task_id: str
            - data_dir: str
            - metadata: dict
        resources : agl.NamedResources
            Training resources containing:
            - "main_llm": agl.LLM
        rollout : agl.Rollout
            Rollout context.

        Returns
        -------
        float
            Final reward value.
        """
        # 1. Get LLM from resources.
        llm: agl.LLM = resources["main_llm"]

        # 2. Emit rollout start message.
        agl.emit_message(f"[{self.workflow_name}] Starting rollout for task {task.get('task_id')}")

        if get_workflow is None:
            agl.emit_exception(ImportError("DSAT not available"))
            return 0.0

        # 3. Update workflow config with training LLM.
        workflow_config = self.workflow_config.copy()
        workflow_config.update({
            "llm_config": {
                "model": llm.model,
                "api_base": llm.endpoint,
                "api_key": llm.api_key or "dummy-key",
                "temperature": llm.sampling_parameters.get("temperature", 0.7),
            },
            "max_steps": self.max_steps,
        })

        # 4. Create DSAT workflow.
        workflow = get_workflow(
            workflow_name=self.workflow_name,
            config=workflow_config
        )

        # 5. Run workflow.
        try:
            result = workflow.run(
                task_id=task["task_id"],
                data_dir=task["data_dir"],
            )

            # 6. Emit intermediate rewards if available.
            if hasattr(result, "intermediate_scores"):
                for step, score in enumerate(result.intermediate_scores):
                    agl.emit_reward(score)

            # 7. Compute final reward via evaluator.
            reward = self.reward_evaluator.evaluate(
                result=result,
                task=task,
            )

            # 8. Emit structured trace.
            agl.emit_object({
                "workflow": self.workflow_name,
                "task_id": task["task_id"],
                "final_score": result.score if hasattr(result, "score") else None,
                "steps_taken": len(result.history) if hasattr(result, "history") else 0,
                "reward": reward,
            })

            return reward

        except Exception as e:
            # Capture and report errors.
            agl.emit_exception(e)
            agl.emit_message(f"[{self.workflow_name}] Rollout failed: {str(e)}")
            return 0.0  # Return zero reward on failure.


__all__ = ["LitDSAgent"]
