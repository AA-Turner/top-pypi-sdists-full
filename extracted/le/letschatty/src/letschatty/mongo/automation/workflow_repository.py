"""`WorkflowRepository` on the `flows` collection: the same two reads the legacy `Flows` service of api-chatty ran. It
reuses the service's asset collection (`FlowCollection`), so the documents are built exactly as before and a missing
id raises the same `NotFoundError`. Only reads: copilot_v2 writes this collection."""
from __future__ import annotations

from typing import List, Set

from bson import ObjectId

from ...models.company.assets.flow import FlowPreview


class MongoWorkflowRepository:
    def __init__(self, collection):
        self.collection = collection

    async def by_id(self, workflow_id: str) -> FlowPreview:
        return await self.collection.get_by_id(workflow_id)

    async def live_of_companies(self, company_ids: List[str], *, not_generated_by: str) -> List[FlowPreview]:
        # `companyId` (camelCase) is what copilot writes: the generic `company_id` filter only matches the handful of
        # documents that also carry it. `deleted_at: None` is null OR missing (copilot's documents have none).
        cursor = self.collection.collection.find({
            "companyId": {"$in": list(company_ids)},
            "deleted_at": None,
            "generado_por": {"$ne": not_generated_by},
        })
        docs = await cursor.to_list(None)
        return [self.collection.create_instance(doc) for doc in docs]

    async def selectable_among(self, company_ids: List[str], ids: List[str], *, not_generated_by: str) -> Set[str]:
        cursor = self.collection.collection.find({
            "_id": {"$in": [ObjectId(i) for i in ids]},
            "companyId": {"$in": list(company_ids)},
            "deleted_at": None,
            "visible": {"$ne": False},  # a hidden workflow is offered by no picker (as in copilot)
            "generado_por": {"$ne": not_generated_by},
        }, projection={"_id": 1})
        return {str(d["_id"]) for d in await cursor.to_list(None)}
