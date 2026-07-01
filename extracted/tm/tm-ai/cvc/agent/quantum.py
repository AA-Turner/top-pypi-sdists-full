"""
cvc.agent.quantum ?" Quantum Branching & Parallel Realities.

This module provides the QuantumExecutor, which takes an agent task and explores
multiple reasoning paths simultaneously by branching the CVC context. It implements
a Tree of Thoughts (ToT) style race: the first branch to succeed is merged back to main,
and the failed branches are archived as 'failed_lessons' to prevent future hallucinations.
"""

import asyncio
from typing import Any, Callable, Coroutine
from dataclasses import dataclass

from cvc.core.models import CVCBranchRequest, CVCMergeRequest
from cvc.operations.engine import CVCEngine

@dataclass
class QuantumBranchResult:
    branch_name: str
    success: bool
    result_data: Any
    error: Exception | None = None

class QuantumExecutor:
    """
    Executes multiple agent paths in parallel isolated CVC branches.
    """
    def __init__(self, engine: CVCEngine, base_branch: str = "main"):
        self.engine = engine
        self.base_branch = base_branch

    async def race(
        self,
        task_name: str,
        strategies: list[str],
        agent_func: Callable[[str, str], Coroutine[Any, Any, QuantumBranchResult]]
    ) -> QuantumBranchResult:
        """
        Races multiple strategies in parallel.
        
        Args:
            task_name: Prefix for the ephemeral branches.
            strategies: A list of hints/strategies (e.g. ["Use API", "Use DB"]).
            agent_func: An async function that takes (branch_name, strategy) and returns a QuantumBranchResult.
        """
        branches = []
        for i, strategy in enumerate(strategies):
            branch_name = f"quantum-{task_name}-path-{i+1}"
            
            # 1. Create the parallel reality branch
            self.engine.branch(CVCBranchRequest(
                name=branch_name,
                source_commit=None,  # Branches from HEAD of current active branch
                description=f"Quantum exploration: {strategy}"
            ))
            branches.append(branch_name)

        # 2. Execute all branches concurrently
        tasks = [agent_func(branch, strategy) for branch, strategy in zip(branches, strategies)]
        results: list[QuantumBranchResult] = await asyncio.gather(*tasks, return_exceptions=True)

        # 3. Evaluate the winner
        winning_result = None
        failed_branches = []
        
        for res in results:
            if isinstance(res, Exception):
                continue
            if res.success and not winning_result:
                winning_result = res
            else:
                failed_branches.append(res.branch_name if hasattr(res, 'branch_name') else "unknown")

        if winning_result:
            # 4. Merge the winner back into the base timeline
            self.engine.merge(CVCMergeRequest(
                source_branch=winning_result.branch_name,
                target_branch=self.base_branch
            ))
            
            # 5. Archive the losers as 'failed_lessons' (implementation stub)
            self._archive_failed_lessons(failed_branches)
            
            return winning_result

        raise RuntimeError("All quantum branches failed the task.")

    def _archive_failed_lessons(self, branches: list[str]) -> None:
        """
        Extracts the reasoning traces from failed branches and commits them 
        as 'negative examples' so the agent doesn't repeat the same mistakes.
        """
        # In a full implementation, we would extract the `reasoning_trace` from the
        # branch heads and inject them into a `lessons` ChromaDB collection.
        for b in branches:
            # Stub: we would mark the branch as BranchStatus.ARCHIVED in the DB
            pass
