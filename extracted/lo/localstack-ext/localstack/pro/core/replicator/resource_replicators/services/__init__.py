from .ec2 import Ec2SecurityGroupReplicator, Ec2SubnetReplicator, Ec2VPCReplicator
from .ecr import EcrRepositoryReplicator
from .iam import IamPolicyReplicator, IamRoleReplicator
from .kms import KmsKeyReplicator
from .lambda_ import LambdaLayerVersionReplicator
from .route53 import Route53HostedZoneReplicator
from .secrets_manager import SecretmanagerSecretReplicator
from .ssm import SsmParameterReplicator

_REPLICATOR_CLASSES = [
    Ec2SecurityGroupReplicator,
    Ec2SubnetReplicator,
    Ec2VPCReplicator,
    EcrRepositoryReplicator,
    IamPolicyReplicator,
    IamRoleReplicator,
    KmsKeyReplicator,
    LambdaLayerVersionReplicator,
    Route53HostedZoneReplicator,
    SecretmanagerSecretReplicator,
    SsmParameterReplicator,
]

# Maps CFN type -> Replicator class
RESOURCE_REPLICATORS = {replicator.type: replicator for replicator in _REPLICATOR_CLASSES}


def _build_arn_to_cfn_map() -> dict[str, str]:
    """Build mapping from ARN patterns (service.resource) to CFN types.

    For each replicator:
    - Derives default pattern from CFN type (e.g., AWS::SSM::Parameter -> ssm.parameter)
    - Adds any additional patterns from arn_resource_types (e.g., kms.alias -> AWS::KMS::Key)
    """
    mapping = {}
    for replicator in _REPLICATOR_CLASSES:
        _, service, resource = replicator.type.split("::")
        service_lower = service.lower()

        # Default: derive from CFN resource name (lowercase, no special chars)
        default_pattern = f"{service_lower}.{resource.lower()}"
        mapping[default_pattern] = replicator.type

        # Additional ARN patterns if specified
        if replicator.arn_resource_types:
            for arn_resource in replicator.arn_resource_types:
                mapping[f"{service_lower}.{arn_resource}"] = replicator.type

    return mapping


# Maps ARN pattern (service.resource) -> CFN type
ARN_TO_CFN_MAP = _build_arn_to_cfn_map()

__all__ = ["RESOURCE_REPLICATORS", "ARN_TO_CFN_MAP"]
