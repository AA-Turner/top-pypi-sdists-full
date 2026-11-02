"""Parse catalog selectors and resolve authored reference annotations into immutable inputs."""

from typing import cast, get_args, get_origin

import click

from labqoat.client import Client
from labqoat.dataset import Dataset
from labqoat.references import AssetRef, CheckpointRef, Sha256


class ReferenceParameter(click.ParamType[object]):
    """Keep discovery offline and acquire typed reference values only for an actual invocation."""

    def __init__(self, annotation: object) -> None:
        """Retain the authored row or service contract and its native selector spelling."""
        self.annotation = annotation
        self.kind = cast(type[object], get_origin(annotation) or annotation)
        names: dict[type[object], str] = {Dataset: "dataset", AssetRef: "asset", CheckpointRef: "uuid"}
        self.name = names[self.kind]

    @staticmethod
    def matches(annotation: object) -> bool:
        """Require an explicit row type for datasets."""
        return annotation in (AssetRef, CheckpointRef) or get_origin(annotation) in (Dataset, CheckpointRef)

    def convert(self, value: object, param: click.Parameter | None, ctx: click.Context | None) -> object:
        """Accept names for datasets, exact IDs for checkpoints and IDs or digests for assets."""
        if isinstance(value, self.kind):
            return value
        if self.kind is Dataset:
            return click.STRING.convert(value, param, ctx)
        if self.kind is AssetRef and isinstance(value, str) and value.startswith("sha256:"):
            try:
                Sha256.parse(value.removeprefix("sha256:"))
            except ValueError as error:
                self.fail(str(error), param, ctx)
            return value
        return click.UUID.convert(str(value), param, ctx)

    def resolve(self, client: Client, value: object) -> object:
        """Use the owning SDK catalog to validate and freeze the selected reference once."""
        if value is None or isinstance(value, self.kind):
            return value
        selector = str(value)
        if self.kind is AssetRef:
            return client.assets.resolve(selector)
        if self.kind is CheckpointRef:
            return client.runs.resolve_checkpoint(selector)
        parameter = cast(type[object], get_args(self.annotation)[0])
        return client.datasets.resolve(selector, row_type=parameter)
