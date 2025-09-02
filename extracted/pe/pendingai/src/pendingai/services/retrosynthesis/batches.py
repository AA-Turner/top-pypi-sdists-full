#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from datetime import datetime
from typing import List, Literal

from requests import Response

from pendingai.api_resources.interfaces import (
    CreateResourceInterface,
    DeleteResourceInterface,
    ListResourceInterface,
    RetrieveResourceInterface,
    UpdateResourceInterface,
)
from pendingai.api_resources.object import ListObject, Object
from pendingai.api_resources.parser import cast
from pendingai.exceptions import (
    ContentTooLargeError,
    NotFoundError,
    UnexpectedResponseError,
)


class Batch(Object):
    """
    Batch object.
    """

    class Parameters(Object):
        """
        Batch object parameters.
        """

        retrosynthesis_engine: str
        """
        Engine resource id.
        """
        building_block_libraries: list[str]
        """
        Library resource ids.
        """
        number_of_routes: int
        """
        Maximum number of routes generated from retrosynthesis.
        """
        processing_time: int
        """
        Maximum allowable time for retrosynthesis.
        """
        reaction_limit: int
        """
        Maximum number of times a reaction can appear in a route.
        """
        building_block_limit: int
        """
        Maximum number of times a building block can appear in a route.
        """

    id: str
    """
    Resource id.
    """
    object: str = "batch"
    """
    Resource object type.
    """
    name: str | None
    """
    Optional name of the batch.
    """
    description: str | None
    """
    Optional description of the batch.
    """
    filename: str | None
    """
    Optional filename source of the batch.
    """
    created: datetime
    """
    Time the batch was created.
    """
    updated: datetime
    """
    Time the batch was last updated.
    """
    number_of_jobs: int
    """
    Number of jobs stored in the batch.
    """
    parameters: dict  # FIXME: Requires object namespace validation.
    """
    Shared batch job parameters.
    """


class BatchStatus(Object):
    """
    Batch status object.
    """

    status: str
    """
    Status identifer of the batch.
    """
    number_of_jobs: int
    """
    Number of jobs in a batch.
    """
    completed_jobs: int
    """
    Number of completed jobs in a batch.
    """


class BatchResult(Object):
    """
    Batch result object.
    """

    job_id: str
    """
    Job resource id.
    """
    smiles: str
    """
    Job SMILES structure.
    """
    completed: bool
    """
    Flag for a job being complete.
    """
    synthesizable: bool
    """
    Flag for a job having synthetic routes.
    """


class BatchInterface(
    ListResourceInterface[Batch],
    CreateResourceInterface[Batch],
    RetrieveResourceInterface[Batch],
    UpdateResourceInterface[Batch],
    DeleteResourceInterface[Batch],
):
    """
    Batch resource interface; utility methods for batch resources.
    """

    def list(
        self,
        *,
        created_before: str | None = None,
        created_after: str | None = None,
        sort: Literal["asc", "desc"] = "desc",
        size: int = 25,
    ) -> ListObject[Batch]:
        if sort not in ["asc", "desc"]:
            raise ValueError(f"'sort' must be one of: {['asc', 'desc']}")
        r: Response = self._requestor.request(
            "GET",
            "/retro/v2/batches",
            params={
                "created-before": created_before,
                "created-after": created_after,
                "sort": sort,
                "size": size,
            },
        )
        if r.status_code == 200:
            return cast(ListObject[Batch], r.json())
        raise UnexpectedResponseError("GET", "list_batch")

    def create(
        self,
        smiles: List[str],
        engine: str,
        libraries: List[str],
        *,
        name: str | None = None,
        description: str | None = None,
        filename: str | None = None,
        number_of_routes: int = 25,
        processing_time: int = 300,
        reaction_limit: int = 3,
        building_block_limit: int = 3,
    ) -> Batch:
        r: Response = self._requestor.request(
            "POST",
            "/retro/v2/batches",
            json={
                "smiles": smiles,
                "name": name,
                "description": description,
                "filename": filename,
                "parameters": {
                    "retrosynthesis_engine": engine,
                    "building_block_libraries": libraries,
                    "number_of_routes": number_of_routes,
                    "processing_time": processing_time,
                    "reaction_limit": reaction_limit,
                    "building_block_limit": building_block_limit,
                },
            },
        )
        if r.status_code == 200:
            return cast(Batch, r.json())
        raise UnexpectedResponseError("POST", "create_batch")

    def retrieve(self, id: str) -> Batch:
        r: Response = self._requestor.request("GET", f"/retro/v2/batches/{id}")
        if r.status_code == 200:
            return cast(Batch, r.json())
        elif r.status_code == 404:
            raise NotFoundError(id, "Batch")
        raise UnexpectedResponseError("GET", "retrieve_batch")

    def status(self, id: str) -> BatchStatus:
        r: Response = self._requestor.request("GET", f"/retro/v2/batches/{id}/status")
        if r.status_code == 200:
            return cast(BatchStatus, r.json())
        elif r.status_code == 404:
            raise NotFoundError(id, "Batch")
        raise UnexpectedResponseError("GET", "status_batch")

    def result(self, id: str) -> List[BatchResult]:
        r: Response = self._requestor.request(
            "GET", f"/retro/v2/batches/{id}/result", headers={"accept-encoding": "gzip"}
        )
        if r.status_code == 200:
            return cast(list[BatchResult], r.json())
        elif r.status_code == 404:
            raise NotFoundError(id, "Batch")
        raise UnexpectedResponseError("GET", "result_batch")

    def update(self, id: str, smiles: List[str]) -> Batch:
        body: dict = {"smiles": smiles}
        r: Response = self._requestor.request(
            "PUT", f"/retro/v2/batches/{id}", json=body
        )
        if r.status_code == 200:
            return cast(Batch, r.json())
        elif r.status_code == 404:
            raise NotFoundError(id, "Batch")
        elif r.status_code == 413:
            raise ContentTooLargeError(
                "Too many SMILES provided exceeding a batch limit "
                "of 100,000. Create a new batch with the additional "
                "structures."
            )
        raise UnexpectedResponseError("PUT", "update_batch")

    def delete(self, id: str) -> Batch:
        r: Response = self._requestor.request("DELETE", f"/retro/v2/batches/{id}")
        if r.status_code == 200:
            return cast(Batch, r.json())
        elif r.status_code == 404:
            raise NotFoundError(id, "Batch")
        raise UnexpectedResponseError("DELETE", "delete_batch")
