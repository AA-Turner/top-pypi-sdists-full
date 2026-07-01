"""
cvc.agent.telepathy_executor - Dynamic Telepathy Branching for Parallel Tools.

This module upgrades the standard ToolExecutor to support Claude Code-style
parallelism combined with CVC's Dynamic Telepathy Branching.
"""

import asyncio
from typing import Any, Dict, List
import uuid

from cvc.agent.executor import ToolExecutor
from cvc.operations.engine import CVCEngine
from cvc.core.models import CVCBranchRequest, CVCCommitRequest, CVCMergeRequest, CommitType

class TelepathicToolExecutor:
    """
    Executes multiple tools in parallel using isolated CVC branches.
    After execution, distills the context and merges it back to the main timeline.
    """
    def __init__(self, base_executor: ToolExecutor, engine: CVCEngine):
        self.base_executor = base_executor
        self.engine = engine

    async def _execute_single_tool_telepathically(self, tool_call: Dict[str, Any], base_branch: str) -> Dict[str, Any]:
        """Runs a single tool in its own isolated branch."""
        tool_name = tool_call["name"]
        arguments = tool_call["args"]
        call_id = tool_call.get("id", uuid.uuid4().hex[:6])
        
        branch_name = f"telepathy-{tool_name}-{call_id}"
        
        # 1. Spawn isolated telepathy branch
        self.engine.branch(CVCBranchRequest(name=branch_name, source_commit=None, description=f"Executing {tool_name}"))
        self.engine._active_branch = branch_name
        
        try:
            # 2. Execute the actual tool (run in executor to avoid blocking)
            loop = asyncio.get_running_loop()
            raw_output = await loop.run_in_executor(None, self.base_executor.execute, tool_name, arguments)
            success = True
        except Exception as e:
            raw_output = f"Tool execution failed: {str(e)}"
            success = False

        # 3. Commit raw output to the isolated branch
        self.engine.commit(CVCCommitRequest(
            message=f"Raw output of {tool_name}",
            commit_type=CommitType.TOOL_CALL
        ))
        
        # 4. (Future) We can distill raw_output here if it's > 5000 tokens
        distilled_output = raw_output
        
        return {
            "branch_name": branch_name,
            "tool_name": tool_name,
            "success": success,
            "output": distilled_output,
            "call_id": call_id
        }

    async def execute_parallel(self, tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Executes an array of tool calls concurrently.
        Spawns a branch for each, gathers the results, merges them, and returns.
        """
        base_branch = self.engine.active_branch
        
        # 1. Fire all tools in parallel branches
        tasks = [self._execute_single_tool_telepathically(tc, base_branch) for tc in tool_calls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 2. Switch back to base branch
        self.engine._active_branch = base_branch
        
        processed_results = []
        for res in results:
            if isinstance(res, Exception):
                processed_results.append({"error": str(res)})
                continue
                
            processed_results.append(res)
            
            # 3. Telepathically Merge the insights back
            self.engine.merge(
                CVCMergeRequest(source_branch=res["branch_name"], target_branch=base_branch),
                synthesized_summary=f"Telepathic Tool Sync: {res['tool_name']} completed. Output length: {len(res['output'])}"
            )
            
        return processed_results
