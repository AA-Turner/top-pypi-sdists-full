"""Non-blocking AC quality review using Sonnet 4.7.

Returns None on any error (API down, invalid JSON, malformed response).
Callers MUST treat None as "no suggestion, continue".
"""

import json

from pydantic import ValidationError

from ...common.llm import get_llm_client
from .models import LLMReview

AC_REVIEW_MODEL = "claude-sonnet-4-6"
_MAX_TOKENS = 800

_SYSTEM_PROMPT = """Tu es un assistant qui évalue la qualité de critères d'acceptation \
sur un ticket GitLab. Tu réponds UNIQUEMENT en JSON valide, sans markdown, \
sans préambule. Le JSON doit suivre exactement ce schéma :

{
  "quality_score": <entier de 1 à 5>,
  "missing_aspects": [<liste de strings en français, max 4>],
  "suggestions": [<liste de strings en français actionnables, max 4>]
}

quality_score = 5 si les AC sont précis, mesurables, exhaustifs (incluent les cas \
d'erreur et limites). 1 si les AC sont vagues ou triviaux. La note est sévère \
mais juste, sans complaisance."""


def review_ac_quality(description: str, ac_section_body: str) -> LLMReview | None:
    try:
        response = get_llm_client().complete(
            model=AC_REVIEW_MODEL,
            max_tokens=_MAX_TOKENS,
            system=_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Voici la description complète du ticket :\n\n"
                        f"{description}\n\n"
                        "---\n\n"
                        "Voici la section critères d'acceptation isolée :\n\n"
                        f"{ac_section_body}"
                    ),
                }
            ],
        )
        payload = json.loads(response.text)
        return LLMReview.model_validate(payload)
    except (json.JSONDecodeError, ValidationError):
        return None
    except Exception:  # noqa: BLE001  # non-blocking on any failure (no key, API down, …)
        return None
