#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from typing import Literal

from requests import Response

from pendingai.api_resources.interfaces import (
    ListResourceInterface,
    RetrieveResourceInterface,
)
from pendingai.api_resources.object import ListObject, Object
from pendingai.api_resources.parser import cast
from pendingai.exceptions import (
    NotFoundError,
    ServiceUnavailableError,
    UnexpectedResponseError,
)


class Model(Object):
    """
    Model object.
    """

    id: str
    """
    Resource id.
    """
    object: str = "model"
    """
    Resource object type.
    """
    name: str | None
    """
    Optional name of the model.
    """
    desc: str | None
    """
    Optional name of the model.
    """
    version: str | None
    """
    Optional version of the model.
    """
    summary: dict
    """
    Additional summary statistics of the model.
    """
    metadata: dict
    """
    Additional metadata describing specific model features.
    """


class ModelStatus(Object):
    """
    Model status object.
    """

    status: str


class ModelInterface(
    ListResourceInterface[Model],
    RetrieveResourceInterface[Model],
):
    """
    Model resource interface; utility methods for model resources.
    """

    def list(
        self,
        *,
        created_before: str | None = None,
        created_after: str | None = None,
        sort: Literal["asc", "desc"] = "desc",
        size: int = 25,
    ) -> ListObject[Model]:  # FIXME: Update api with additional pagination values.
        if sort not in ["asc", "desc"]:
            raise ValueError(f"'sort' must be one of: {['asc', 'desc']}")
        r: Response = self._requestor.request(
            "GET",
            "/generator/v1/models",
            params={
                "pagination-key": created_after,  # FIXME: To be removed.
                "limit": size,  # FIXME: To be removed.
                "created-before": created_before,
                "created-after": created_after,
                "sort": sort,
                "size": size,
            },
        )
        if r.status_code == 200:
            return cast(ListObject[Model], r.json())
        raise UnexpectedResponseError("GET", "list_model")

    def retrieve(self, id: str, *args, **kwargs) -> Model:
        r: Response = self._requestor.request("GET", f"/generator/v1/models/{id}")
        if r.status_code == 200:
            return cast(Model, r.json())
        elif r.status_code == 404:
            raise NotFoundError(id, "Model")
        elif r.status_code == 503:
            raise ServiceUnavailableError
        raise UnexpectedResponseError("GET", "retrieve_model")

    def status(self, id: str) -> ModelStatus:
        r: Response = self._requestor.request("GET", f"/generator/v1/models/{id}/status")
        if r.status_code == 200:
            return cast(ModelStatus, r.json())
        elif r.status_code == 404:
            raise NotFoundError(id, "Model")
        elif r.status_code == 503:
            raise ServiceUnavailableError
        raise UnexpectedResponseError("GET", "retrieve_model")
