#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

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
    description: str | None
    """
    Optional description of the model.
    """
    version: str | None
    """
    Optional version of the model.
    """
    summary: dict
    """
    Optional summary statistics of the model.
    """
    metadata: dict
    """
    Optional metadata describing specific model features.
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
        limit: int = 25,
        next_page: str | None = None,
        prev_page: str | None = None,
    ) -> ListObject[Model]:
        if next_page and prev_page:
            raise ValueError("Cannot specify both next_page and prev_page")
        if limit < 1 or limit > 100:
            raise ValueError("List 'limit' must be in range: [1, 100].")
        params: dict[str, str | int] = {"limit": limit}
        if next_page is not None:
            params["next-page"] = next_page
        if prev_page is not None:
            params["prev-page"] = prev_page

        r: Response = self._requestor.request(
            "GET", "/generator/v1/models", params=params
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
        raise UnexpectedResponseError("GET", "retrieve_model_status")
