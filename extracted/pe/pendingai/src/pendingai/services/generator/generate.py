#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

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
    Molecule generator sampler output.
    """

    smiles: list[str]
    """
    Sampled SMILES structures.
    """


class GenerateInterface(ResourceInterface):
    """
    Generate resource interface; utility methods for generate resources.
    """

    def call(self, id: str | None = None, *, n: int = 100) -> Sample:
        if n < 0 or n > 1000:
            raise ValueError("'n' must be in range: [1, 1000].")
        url: str = "/generator/v1/generate" + (f"/{id}" if id else "")
        r: Response = self._requestor.request("POST", url, params={"samples": n})
        if r.status_code == 200:
            sample: Sample = cast(Sample, r.json())  # FIXME: Remove the need for filter.
            sample.smiles = list(set([x for x in sample.smiles if x.strip() != ""]))
            return sample
        elif r.status_code == 404 and id:
            raise NotFoundError(id, "Model")
        elif r.status_code == 503:
            raise ServiceUnavailableError
        raise UnexpectedResponseError("POST", "generate")
