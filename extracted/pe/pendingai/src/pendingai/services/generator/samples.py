#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from datetime import datetime

from requests import Response

from pendingai.api_resources.interfaces import ResourceInterface
from pendingai.api_resources.object import Object
from pendingai.api_resources.parser import cast
from pendingai.exceptions import (
    NotFoundError,
    ServiceUnavailableError,
    UnexpectedResponseError,
)


class Sample(Object):
    """
    Sample resource; represents a set of sampled molecular structures.
    """

    id: str
    """
    Sample resource ID.
    """
    object: str
    """
    Sample resource type.
    """
    model_id: str
    """
    Model resource ID.
    """
    smiles: list[str]
    """
    Sampled SMILES structures.
    """
    created_at: datetime
    """
    Sample creation timestamp.
    """


class SampleInterface(ResourceInterface):
    """
    Sample resource interface; utility methods for sample resources.
    """

    def create(self, model_id: str | None = None, size: int = 500) -> Sample:
        data: dict[str, int | str] = {"size": size}
        if model_id:
            data["model_id"] = model_id
        r: Response = self._requestor.request(
            "POST",
            "/generator/v1/samples",
            json=data,
            headers={"Accept-Encoding": "gzip"},
        )
        if r.status_code == 200:
            sample: Sample = cast(Sample, r.json())
            return sample
        elif r.status_code == 404 and model_id:
            raise NotFoundError(model_id, "Model")
        elif r.status_code == 503:
            raise ServiceUnavailableError
        raise UnexpectedResponseError("POST", "generate")
