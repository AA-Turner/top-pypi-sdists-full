"""AI components (contexts, instructions, chat examples, follow-up strategies, test cases…): the port every store of
the `ai_components` collection implements.

The component is polymorphic: each `type` is its own class (`AiComponentsService.instantiate_component`), and every
read builds it with that factory. CINTIA's lambdas write the same documents straight to Mongo.

Every method takes the company first; the repository does not filter by it (ADR-007 of api-chatty): the use case
checks it, and ENG-10 (reading, editing and deleting another company's component by id) is kept there.
"""
from __future__ import annotations

from typing import List, Optional, Protocol

from ...models.base_models.ai_agent_component import AiAgentComponent
from ...models.utils.types import StrObjectId


class AiComponentRepository(Protocol):
    """Raises `NotFoundError` when the component does not exist."""

    async def get(self, company_id: Optional[StrObjectId], component_id: StrObjectId) -> AiAgentComponent:
        """By id, a deleted one too. `company_id` is None for the read by bare id of any company (the AI readers)."""
        ...

    async def list_live(self, company_id: StrObjectId) -> List[AiAgentComponent]:
        """The live components of the company. One that cannot be read is skipped (logged at ERROR), not raised."""
        ...

    async def add(self, component: AiAgentComponent) -> AiAgentComponent: ...

    async def update(self, company_id: StrObjectId, component_id: StrObjectId,
                     changes: AiAgentComponent) -> AiAgentComponent:
        """Writes only the fields `changes` was built with, on what is in Mongo now; the rest stays as stored."""
        ...

    async def delete(self, company_id: StrObjectId, component_id: StrObjectId) -> AiAgentComponent:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...

    async def delete_test_cases_of_chat_example(self, company_id: StrObjectId, chat_example_id: StrObjectId) -> None:
        """Removes for good every test case of the chat example, whatever company it is of."""
        ...
