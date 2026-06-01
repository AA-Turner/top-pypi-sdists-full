"""Sample CDK Python stack for v0.1.129 Stage 4 testing — finisher batch.

Exercises the 18 constructs added in Stage 4. Minimal kwargs to keep
the fixture small; the parser only cares about construct identity for
type recognition (property-shape translation is Stage 5+).
"""

from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_apigatewayv2 as apigwv2
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_backup as backup
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_efs as efs
from aws_cdk import aws_eks as eks
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_events as events
from aws_cdk import aws_iam as iam
from aws_cdk import aws_kinesis as kinesis
from aws_cdk import aws_opensearchservice as opensearch
from aws_cdk import aws_secretsmanager as secrets
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sqs as sqs
from constructs import Construct


class ServicesStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        sns.Topic(self, "NotifyTopic")
        sqs.Queue(self, "WorkQueue")
        efs.FileSystem(self, "AppFs", vpc=None)
        eks.Cluster(self, "AppCluster", version=eks.KubernetesVersion.V1_28)
        ec2.Vpc(self, "AppVpc")
        secrets.Secret(self, "DbPassword")
        apigw.RestApi(self, "RestApi")
        apigwv2.HttpApi(self, "HttpApi")
        autoscaling.AutoScalingGroup(self, "AppAsg", vpc=None, instance_type=None)
        elbv2.ApplicationLoadBalancer(self, "AppAlb", vpc=None)
        cloudwatch.Alarm(self, "ErrorAlarm", metric=None, threshold=1, evaluation_periods=1)
        events.Rule(self, "DailyRule", schedule=None)
        backup.BackupVault(self, "AppBackupVault")
        backup.BackupPlan(self, "AppBackupPlan")
        iam.User(self, "ServiceUser")
        iam.Group(self, "AdminsGroup")
        kinesis.Stream(self, "EventStream")
        opensearch.Domain(self, "SearchDomain", version=opensearch.EngineVersion.OPENSEARCH_2_11)
