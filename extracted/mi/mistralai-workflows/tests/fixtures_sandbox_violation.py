import random

import mistralai.workflows as workflows


@workflows.workflow.define(name="sandbox-restriction-violation", enforce_determinism=True)
class SandboxRestrictionViolationWorkflow:
    # random.seed() is restricted by the sandbox (non-deterministic) even at import time
    _seed = random.seed(42)

    @workflows.workflow.entrypoint
    async def run(self) -> str:
        return ""
