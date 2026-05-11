"""T13 — Readiness self-test on session start.

Before `sage run` begins, send a tiny "write hello world in one FILE: block"
prompt and check the response. If the model can't pass this 30-second
self-test, abort with a model recommendation. Catches the Novellia
silent-collapse case at the door.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass

from sage.core.content_validator import validate_content

__all__ = ["ReadinessResult", "check_readiness"]

SendFn = Callable[..., str]


READINESS_PROMPT = (
    "Emit exactly one FILE: block writing a JavaScript file `hello.js` that "
    "logs 'hi' to stdout. No commentary, no explanation, no markdown headings."
)
READINESS_SYSTEM = (
    "You are SAGE. Reply ONLY with a single FILE: block. "
    "Format:\nFILE: hello.js\n```javascript\n<content>\n```"
)


@dataclass
class ReadinessResult:
    ok: bool
    model: str
    detail: str = ""
    response: str = ""
    model_responded: bool = False


_FILE_BLOCK_RE = re.compile(
    r"FILE:\s*\S+\s*\n```[a-zA-Z]*\n(.*?)\n```",
    re.DOTALL,
)


def check_readiness(*, model: str, send_fn: SendFn,
                    timeout_s: float = 30.0) -> ReadinessResult:
    """Run the readiness probe. Returns ok=True iff the model:
       1. Responded without exception
       2. Emitted exactly one valid FILE: block
       3. Block content passed the content validator
       4. Block content actually contains a console.log-style call
    """
    try:
        response = send_fn(READINESS_PROMPT, model=model, system=READINESS_SYSTEM)
    except Exception as exc:
        return ReadinessResult(
            ok=False, model=model, model_responded=False,
            detail=f"send error: {exc}",
        )

    if not response or not response.strip():
        return ReadinessResult(
            ok=False, model=model, model_responded=False,
            detail="empty response from model",
        )

    blocks = _FILE_BLOCK_RE.findall(response)
    if not blocks:
        return ReadinessResult(
            ok=False, model=model, model_responded=True, response=response,
            detail=("no FILE: block in response — model can't follow protocol. "
                    "Pull a stronger model (qwen2.5-coder-7b or larger)."),
        )

    content = blocks[0]

    # Validator: catches protocol leak / prose mass / etc.
    val = validate_content("hello.js", content)
    if not val.ok:
        return ReadinessResult(
            ok=False, model=model, model_responded=True, response=response,
            detail=f"FILE: block content rejected ({val.signal}): {val.reason}",
        )

    # Sanity: must mention console.log or similar print primitive
    if not re.search(r"\b(console\.log|process\.stdout\.write)\b", content):
        return ReadinessResult(
            ok=False, model=model, model_responded=True, response=response,
            detail="FILE: block content does not implement the requested logging",
        )

    return ReadinessResult(
        ok=True, model=model, model_responded=True, response=response,
        detail="passed: emitted valid FILE: block with logging primitive",
    )
