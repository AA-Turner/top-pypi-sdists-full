"""Sample CDK Python stack for v0.1.128 Stage 3 testing.

Exercises the four new constructs added in Stage 3: Lambda Function,
RDS DatabaseInstance, DynamoDB Table, CloudWatch Logs LogGroup.
"""

from aws_cdk import Stack
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_lambda as lmb
from aws_cdk import aws_logs as logs
from aws_cdk import aws_rds as rds
from constructs import Construct


class ComputeStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.api_fn = lmb.Function(
            self,
            "ApiFunction",
            runtime=lmb.Runtime.PYTHON_3_12,
            handler="app.handler",
            code=lmb.Code.from_inline("def handler(e, c): return {}"),
        )

        self.app_db = rds.DatabaseInstance(
            self,
            "AppDatabase",
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            storage_encrypted=True,
            multi_az=False,
        )

        self.session_table = dynamodb.Table(
            self,
            "SessionTable",
            partition_key={"name": "id", "type": dynamodb.AttributeType.STRING},
            point_in_time_recovery=True,
        )

        self.app_logs = logs.LogGroup(
            self,
            "AppLogs",
            retention=logs.RetentionDays.ONE_YEAR,
        )
