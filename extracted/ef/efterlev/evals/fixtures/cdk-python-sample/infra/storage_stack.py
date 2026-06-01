"""Sample CDK Python stack for v0.1.126 Stage 1 testing.

Minimal: one S3 bucket per import style (alias + direct) so the
parser's both code paths are exercised by a real-shape fixture.
"""

from aws_cdk import Stack
from aws_cdk import aws_s3 as s3
from aws_cdk.aws_s3 import Bucket
from constructs import Construct


class StorageStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Style A: aliased module import.
        self.logs_bucket = s3.Bucket(
            self,
            "LogsBucket",
            bucket_name="my-org-cdk-logs",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
        )

        # Style B: direct construct import.
        self.assets_bucket = Bucket(
            self,
            "AssetsBucket",
            bucket_name="my-org-cdk-assets",
            versioned=False,
        )
