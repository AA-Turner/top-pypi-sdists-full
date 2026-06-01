"""Sample CDK Python stack for v0.1.127 Stage 2 testing.

Exercises the four new constructs added in Stage 2: KMS Key, EC2
SecurityGroup, IAM Role, CloudTrail Trail. Mix of alias and direct
import styles so both parser code paths are exercised.
"""

from aws_cdk import Stack
from aws_cdk import aws_cloudtrail as cloudtrail
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_kms as kms
from aws_cdk.aws_iam import Role
from constructs import Construct


class SecurityStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # KMS key for at-rest encryption — alias style.
        self.encryption_key = kms.Key(
            self,
            "AppEncryptionKey",
            description="App-level CMK for at-rest data",
            enable_key_rotation=True,
        )

        # Security group for the app — alias style.
        self.app_sg = ec2.SecurityGroup(
            self,
            "AppSecurityGroup",
            vpc=None,  # would normally be a vpc reference; opaque to parser
            description="Allow internal-only ingress",
            allow_all_outbound=False,
        )

        # IAM role — direct style.
        self.app_role = Role(
            self,
            "AppRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Execution role for app Lambdas",
        )

        # CloudTrail trail — alias style.
        self.audit_trail = cloudtrail.Trail(
            self,
            "AuditTrail",
            is_multi_region_trail=True,
            include_global_service_events=True,
        )
