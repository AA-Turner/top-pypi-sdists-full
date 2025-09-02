#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from datetime import datetime
from typing import List

from requests import Response

from pendingai.api_resources.interfaces import (
    CreateResourceInterface,
    DeleteResourceInterface,
    ListResourceInterface,
    RetrieveResourceInterface,
)
from pendingai.api_resources.object import ListObject, Object
from pendingai.api_resources.parser import cast
from pendingai.exceptions import (
    NotFoundError,
    RequestValidationError,
    UnexpectedResponseError,
)


class Job(Object):
    """
    Job object.
    """

    class Parameters(Object):
        """
        Job object parameters.
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

    class Route(Object):
        """
        Job object synthetic routes.
        """

        class Step(Object):
            """
            Job object synthetic route steps.
            """

            reaction_smiles: str
            """
            Single-step reaction SMILES.
            """
            order: int
            """
            Post-order position of the synthetic route step.
            """

        summary: str
        """
        SMILES representation of a synthetic route.
        """
        building_blocks: list[dict]
        """
        Building blocks used in the synthetic route.
        """
        steps: list[dict]  # FIXME: Requires object namespace validation.
        """
        Single-step reaction stages of the synthetic route.
        """

    id: str
    """
    Resource id.
    """
    object: str = "job"
    """
    Resource object type.
    """
    query: str
    """
    Query SMILES structure being processed.
    """
    status: str
    """
    Most recent job status.
    """
    parameters: dict  # FIXME: Requires object namespace validation.
    """
    Job parameters.
    """
    created: datetime
    """
    Timestamp for when the job was created.
    """
    updated: datetime
    """
    Timestamp for when the job was last updated.
    """
    routes: list[dict]  # FIXME: Requires object namespace validation.
    """
    Collection of found synthetic routes.
    """


class JobInterface(
    CreateResourceInterface[Job],
    ListResourceInterface[Job],
    RetrieveResourceInterface[Job],
    DeleteResourceInterface[Job],
):
    """
    Jobs resource interface; utility methods for jobs resources.
    """

    def list(
        self,
        *,
        page: int = 1,
        size: int = 10,
        status: str | None = None,
    ) -> ListObject[Job]:
        params: dict = {"page-number": page, "page-size": size}
        if status:
            params["status"] = status
        r: Response = self._requestor.request("GET", "/retro/v2/jobs", params=params)
        if r.status_code == 200:
            return cast(ListObject[Job], r.json())
        elif r.status_code == 422:
            raise RequestValidationError(r.json().get("error", {}).get("details", []))
        elif r.status_code == 404:  # FIXME: Remove in favour of empty pagination.
            return ListObject[Job](object="list", data=[], has_more=False)
        raise UnexpectedResponseError("GET", "list_job")

    def create(
        self,
        smiles: str,
        engine: str,
        libraries: List[str],
        *,
        number_of_routes: int = 25,
        processing_time: int = 300,
        reaction_limit: int = 3,
        building_block_limit: int = 3,
    ) -> Job:
        r: Response = self._requestor.request(
            "POST",
            "/retro/v2/jobs",
            json={
                "query": smiles,
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
            return cast(Job, r.json())
        raise UnexpectedResponseError("POST", "create_job")

    def retrieve(self, id: str) -> Job:
        r: Response = self._requestor.request("GET", f"/retro/v2/jobs/{id}")
        if r.status_code == 200:
            return cast(Job, r.json())
        elif r.status_code == 404:
            raise NotFoundError(id, "Job")
        raise UnexpectedResponseError("GET", "retrieve_job")

    def delete(self, id: str) -> Job:
        r: Response = self._requestor.request("DELETE", f"/retro/v2/jobs/{id}")
        if r.status_code == 200:
            return cast(Job, r.json())
        elif r.status_code == 404:
            raise NotFoundError(id, "Job")
        raise UnexpectedResponseError("DELETE", "delete_job")
