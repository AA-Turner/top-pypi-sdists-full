"""
Example worker that runs multiple workflows.

This example shows how to run a worker with workflows from:
- The core SDK examples
- The mistralai plugin (requires: uv add mistralai-workflows-plugins-mistralai)
"""

import asyncio

import mistralai.workflows as workflows
from mistralai.workflows.examples.workflow_example import Workflow as WorkflowExample

try:
    from mistralai.workflows.examples.assist.workflow_insurance_claims import InsuranceClaimsWorkflow
    from mistralai.workflows.examples.assist.workflow_multi_turn_chat import MultiTurnChatWorkflow

    PLUGIN_WORKFLOWS = [InsuranceClaimsWorkflow, MultiTurnChatWorkflow]
except ImportError as e:
    import logging

    logging.warning(
        "Could not import mistralai plugin workflows: %s. Install with: uv add mistralai-workflows-plugins-mistralai",
        e,
    )
    PLUGIN_WORKFLOWS = []

if __name__ == "__main__":
    asyncio.run(workflows.run_worker([WorkflowExample, *PLUGIN_WORKFLOWS]))
