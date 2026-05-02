# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ..._models import BaseModel

__all__ = ["DeleteKnowledgeBaseDataSourceConnectionResponse"]


class DeleteKnowledgeBaseDataSourceConnectionResponse(BaseModel):
    artifacts_to_delete: Dict[str, int]

    deletion_workflow_id: Optional[str] = None
