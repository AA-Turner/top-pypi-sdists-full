"""Fast answers of a company («respuestas rápidas»): the port every fast-answer store implements.

The entity is `letschatty.models.company.assets.ChattyFastAnswer`, unchanged: CINTIA, copilot and the
ai-agent-tester import it. Unlike tags and products, a read by id is already scoped to the company: an id
alone is not an authorization. A deleted fast answer is still returned (ENG-10).
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Protocol

from ...models.company.assets.chatty_fast_answers.chatty_fast_answer import ChattyFastAnswer
from ...models.utils.custom_exceptions.custom_exceptions import NotFoundError
from ...models.utils.types import StrObjectId

logger = logging.getLogger("FastAnswers")


class FastAnswerRepository(Protocol):
    """Raises `NotFoundError` when the fast answer does not exist or is another company's."""

    async def get(self, company_id: StrObjectId, fast_answer_id: StrObjectId) -> ChattyFastAnswer:
        """Also a deleted one (ENG-10)."""
        ...

    async def get_any_company(self, fast_answer_id: StrObjectId) -> ChattyFastAnswer:
        """By id, whatever its company. Only for reading as `main` did: convert its audios first and check the company
        after (ENG-73, kept); everything else uses `get`."""
        ...

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """Live fast answers of the company, newest first, as JSON-ready preview dicts (no `messages`)."""
        ...

    async def add(self, fast_answer: ChattyFastAnswer) -> ChattyFastAnswer: ...

    async def update(self, company_id: StrObjectId, fast_answer_id: StrObjectId,
                     changes: ChattyFastAnswer) -> ChattyFastAnswer:
        """Writes only the fields `changes` was built with, merged onto what is in the store now."""
        ...

    async def save_messages(self, fast_answer: ChattyFastAnswer) -> None:
        """Writes only `messages`: the rest of the document is never rewritten from this copy."""
        ...

    async def delete(self, company_id: StrObjectId, fast_answer_id: StrObjectId) -> ChattyFastAnswer:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...


def of_company(fast_answer: ChattyFastAnswer, company_id: StrObjectId) -> ChattyFastAnswer:
    """The fast answer, only if it is `company_id`'s; else `NotFoundError`, logged as `fast_answer_foreign`."""
    if str(fast_answer.company_id) != str(company_id):
        logger.warning("fast_answer_foreign company_id=%s fast_answer_id=%s", company_id, fast_answer.id)
        raise NotFoundError(f"Fast answer {fast_answer.id} not found")
    return fast_answer
