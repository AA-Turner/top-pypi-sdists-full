from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Union

from qwak.clients.feature_store.management_client import FeatureRegistryClient
from qwak.feature_store._common.packaging import upload_artifact

if TYPE_CHECKING:
    from qwak.feature_store.data_sources.streaming.kafka.deserialization import (
        Deserializer,
    )
    from qwak.feature_store.feature_sets.transformations.transformations import (
        BaseTransformation,
    )


@dataclass
class ArtifactSpec:
    """
    Dataclass for holding artifacts which will be uploaded
    """

    artifact_name: str
    root_module_path: Path
    artifact_object: Union["BaseTransformation", "Deserializer"]
    callables: List[Callable] = field(default_factory=list)
    suffix: str = ""


class ArtifactsUploader:
    @staticmethod
    def upload(artifact: ArtifactSpec) -> str:
        return upload_artifact(
            feature_store_object_name=artifact.artifact_name,
            feature_store_object_name_suffix=artifact.suffix,
            functions=artifact.callables,
            feature_module_dir=artifact.root_module_path,
            features_manager_client=FeatureRegistryClient(),
            artifact_object=artifact.artifact_object,
        )

    @staticmethod
    def get_artifact_spec(
        transformation: "BaseTransformation",
        featureset_name: str,
        __instance_module_path__: str,
    ) -> Optional[ArtifactSpec]:
        transformation_functions: Optional[List[Callable[..., Any]]] = (
            transformation.get_functions()
        )
        if not transformation_functions:
            return None

        return ArtifactSpec(
            artifact_name=featureset_name,
            root_module_path=Path(__instance_module_path__).parent,
            artifact_object=transformation,
            callables=transformation_functions,
        )
