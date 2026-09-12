"""THE HOLDER OF A WORKFLOW'S AI STEPS — one mandate, named here, carried everywhere.

WHY THIS EXISTS
---------------
A workflow's AI step nodes (extract, llm, chat, image, video, the agent loop,
the strict-JSON funnel) reached the provider through ``execute_ai_request``
carrying nothing but a model id read out of the node's config. No mandate key,
no agent, no Holder — so no scanner could find them, no admin could rebind
them, and one of them shipped ``"gpt-4o-mini"`` hard-coded in code as its
default. `D20 </systems/mandates/DECISIONS.md>`_: intelligence outside a Mandate
is a defect row, never an approved class.

WHAT THIS IS, AND WHAT IT IS NOT
--------------------------------
``workflow.step_intelligence`` is the Mandate that HOLDS those calls. It is
declared, with its goal and its provision, in aidream — see
``aidream/workflows/mandates.py``, which imports the constant below so the key
is spelled exactly once in the platform and the mandate scanner resolves every
call site to it.

**It is not a model override.** The workflow AUTHOR chose the model on the node,
and that choice stays exactly where it is: a run-scope setting, the top rung of
the precedence walk (agent definition → binding overrides → mandate pins, with
run-scope config winning — ``/systems/mandates/RUNTIME.md`` § THE PINS LAW,
which also forbids a mandate from ever naming a model in code). The Mandate
names WHO is accountable for the call; the node still names WHAT model runs it.

The key lives in matrx-ai (never a declaration — matrx-ai never imports aidream)
so the nodes that carry it and the host that declares it read the same string.
"""

from __future__ import annotations

from typing import Any

#: The Mandate that holds every runtime AI step of an authored workflow.
#: Declared in ``aidream/workflows/mandates.py``; spelled here once.
WORKFLOW_STEP_INTELLIGENCE_MANDATE = "workflow.step_intelligence"


def step_metadata(
    metadata: dict[str, Any] | None = None,
    *,
    spec_type: str,
) -> dict[str, Any]:
    """The node's metadata, saying WHICH KIND of step produced the call.

    The Holder travels as the ``mandate_key=`` argument to
    ``execute_ai_request`` — one carrier, named at the call, where a static
    resolver can read it. This only adds the step type, so any report (a bypass
    row, a usage row, the references board) can say "ai.extract" instead of
    naming a file. A ``spec_type`` already on the caller's metadata wins.
    """
    carried: dict[str, Any] = dict(metadata or {})
    if not str(carried.get("spec_type") or "").strip():
        carried["spec_type"] = spec_type
    return carried
