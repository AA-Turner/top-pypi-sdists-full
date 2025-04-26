from tecton._internals import metadata_service
from tecton_core.embeddings.model_artifacts import ModelArtifactProvider
from tecton_proto.common.id__client_pb2 import Id
from tecton_proto.modelartifactservice.model_artifact_service__client_pb2 import FetchModelArtifactRequest


class MDSModelArtifactProvider(ModelArtifactProvider):
    def get_presigned_url(self, model_artifact_id: Id, s3_path: str) -> str:
        try:
            mds = metadata_service.instance()
            resp = mds.FetchModelArtifact(FetchModelArtifactRequest(id=model_artifact_id))
            return resp.model_artifact_download_url
        except Exception as e:
            msg = f"Failed to fetch model artifact {model_artifact_id}: {e}"
            raise RuntimeError(msg)
