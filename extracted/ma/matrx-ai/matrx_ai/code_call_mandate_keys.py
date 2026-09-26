"""Mandate keys for code calls INSIDE matrx-ai — spelled once, import-light.

matrx-ai never imports aidream, so a package site that holds its call through
``matrx_ai.mandates.hold_code_call`` names its key here and the host declares
the mandate by importing it (aidream ``services/mandates/code_call_mandates.py``)
— the same pattern as ``workflow.step_intelligence``. This module imports
nothing, so the host can read the keys without loading the modules that use them.
"""

from __future__ import annotations

#: ai.image.concept_generate / prompt_write / qc_judge.
IMAGE_CONCEPT_MANDATE = "image_pipeline.concept"
IMAGE_PROMPT_WRITE_MANDATE = "image_pipeline.prompt_write"
IMAGE_QC_JUDGE_MANDATE = "image_pipeline.qc_judge"

#: ``AIJudge`` — bound to the existing Proof Run Judge mandate (declared in
#: aidream ``services/proof_runs/judge.py``).
AI_JUDGE_MANDATE = "proof_runs.judge"

#: The Judge harness's funnel lane, for a contract that names no mandate.
RUBRIC_JUDGE_MANDATE = "evaluators.rubric_judge"
COMPARATIVE_JUDGE_MANDATE = "evaluators.comparative_judge"

#: The conversation labeler — title, description and keywords for a chat, and for
#: a conversation an agent started (its prompt weighs the user's variables).
CONVERSATION_LABEL_CHAT_MANDATE = "conversation.label_chat"
CONVERSATION_LABEL_AGENT_RUN_MANDATE = "conversation.label_agent_run"

#: Observational Memory — the Observer turns new messages into observations, the
#: Reflector compresses them. Both used to run a code-chosen model and prompt.
MEMORY_OBSERVER_MANDATE = "memory.observer"
MEMORY_REFLECTOR_MANDATE = "memory.reflector"
