from urllib.parse import urlparse

import boto3

from tecton_proto.common.id__client_pb2 import Id


class ModelArtifactProvider:
    def get_presigned_url(self, model_artifact_id: Id, s3_path: str) -> str:
        return


class Boto3ModelArtifactProvider(ModelArtifactProvider):
    def get_presigned_url(self, model_artifact_id: Id, s3_path: str) -> str:
        parsed_url = urlparse(s3_path)
        s3_client = boto3.client("s3")
        return s3_client.generate_presigned_url(
            "get_object", Params={"Bucket": parsed_url.netloc, "Key": parsed_url.path.lstrip("/")}
        )


DEFAULT_MODEL_PROVIDER = Boto3ModelArtifactProvider()
