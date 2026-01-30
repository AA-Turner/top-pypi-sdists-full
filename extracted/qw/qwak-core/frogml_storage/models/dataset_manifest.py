from typing import List

from pydantic import Field

from frogml_storage.models.entity_manifest import Artifact, EntityManifest


class DatasetManifest(EntityManifest):
    """
    Represent a dataset manifest file
    """

    artifacts: List[Artifact] = Field(serialization_alias="dataset_artifacts")
