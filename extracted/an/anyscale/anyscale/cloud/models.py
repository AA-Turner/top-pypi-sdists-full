from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from anyscale._private.models import ModelBase, ModelEnum


class CloudPermissionLevel(ModelEnum):
    WRITE = "WRITE"
    READONLY = "READONLY"

    __docstrings__ = {
        WRITE: "Write permission level for the cloud",
        READONLY: "Readonly permission level for the cloud",
    }  # type: ignore


@dataclass(frozen=True)
class CreateCloudCollaborator(ModelBase):
    """User to be added as a collaborator to a cloud.
    """

    __doc_py_example__ = """\
import anyscale
from anyscale.cloud.models import CloudPermissionLevel, CreateCloudCollaborator

create_cloud_collaborator = CreateCloudCollaborator(
   # Email of the user to be added as a collaborator
    email="test@anyscale.com",
    # Permission level for the user to the cloud (CloudPermissionLevel.WRITE, CloudPermissionLevel.READONLY)
    permission_level=CloudPermissionLevel.READONLY,
)
"""

    def _validate_email(self, email: str):
        if not isinstance(email, str):
            raise TypeError("Email must be a string.")

    email: str = field(
        metadata={"docstring": "Email of the user to be added as a collaborator."},
    )

    def _validate_permission_level(
        self, permission_level: CloudPermissionLevel
    ) -> CloudPermissionLevel:
        if isinstance(permission_level, str):
            return CloudPermissionLevel.validate(permission_level)  # type: ignore
        elif isinstance(permission_level, CloudPermissionLevel):
            return permission_level
        else:
            raise TypeError(
                f"'permission_level' must be a 'CloudPermissionLevel' (it is {type(permission_level)})."
            )

    permission_level: CloudPermissionLevel = field(  # type: ignore
        default=CloudPermissionLevel.READONLY,  # type: ignore
        metadata={
            "docstring": "Permission level the added user should have for the cloud"  # type: ignore
            f"(one of: {','.join([str(m.value) for m in CloudPermissionLevel])}",  # type: ignore
        },
    )


@dataclass(frozen=True)
class CreateCloudCollaborators(ModelBase):
    """List of users to be added as collaborators to a cloud.
    """

    __doc_py_example__ = """\
import anyscale
from anyscale.cloud.models import CloudPermissionLevel, CreateCloudCollaborator, CreateCloudCollaborators

create_cloud_collaborator = CreateCloudCollaborator(
   # Email of the user to be added as a collaborator
    email="test@anyscale.com",
    # Permission level for the user to the cloud (CloudPermissionLevel.WRITE, CloudPermissionLevel.READONLY)
    permission_level=CloudPermissionLevel.READONLY,
)
create_cloud_collaborators = CreateCloudCollaborators(
    collaborators=[create_cloud_collaborator]
)
"""

    collaborators: List[Dict[str, Any]] = field(
        metadata={
            "docstring": "List of users to be added as collaborators to a cloud."
        },
    )

    def _validate_collaborators(self, collaborators: List[Dict[str, Any]]):
        if not isinstance(collaborators, list):
            raise TypeError("Collaborators must be a list.")


class ComputeStack(ModelEnum):
    UNKNOWN = "UNKNOWN"
    VM = "VM"
    K8S = "K8S"

    __docstrings__ = {
        UNKNOWN: "Unknown compute stack.",
        VM: "Virtual machine-based compute stack.",
        K8S: "Kubernetes-based compute stack.",
    }  # type: ignore


class CloudProvider(ModelEnum):
    UNKNOWN = "UNKNOWN"
    AWS = "AWS"
    GCP = "GCP"
    AZURE = "AZURE"

    __docstrings__ = {
        UNKNOWN: "Unknown cloud provider.",
        AWS: "Amazon Web Services.",
        GCP: "Google Cloud Platform.",
        AZURE: "Microsoft Azure.",
    }  # type: ignore


@dataclass(frozen=True)
class Cloud(ModelBase):
    """Minimal Cloud resource model."""

    __doc_py_example__ = """\
from datetime import datetime
from anyscale.cloud.models import Cloud, CloudProvider, ComputeStack

cloud = Cloud(
    name="my-cloud",
    id="cloud-123",
    provider="AWS",  # This will be validated as CloudProvider.AWS
    region="us-west-2",
    created_at=datetime.now(),
    is_default=True,
    compute_stack="VM"  # This will be validated as ComputeStack.VM
)
"""

    name: str = field(metadata={"docstring": "Name of this Cloud."})
    id: str = field(metadata={"docstring": "Unique identifier for this Cloud."})
    provider: Union[CloudProvider, str] = field(
        metadata={
            "docstring": "Cloud provider (AWS, GCP, AZURE) or UNKNOWN if not recognized."
        },
    )
    compute_stack: Union[ComputeStack, str] = field(
        metadata={
            "docstring": "The compute stack associated with this cloud's primary cloud resource, or UNKNOWN if not recognized."
        },
    )
    region: Optional[str] = field(
        default=None, metadata={"docstring": "Region for this Cloud."}
    )
    created_at: Optional[datetime] = field(
        default=None, metadata={"docstring": "When the Cloud was created."}
    )
    is_default: Optional[bool] = field(
        default=None, metadata={"docstring": "Whether this is the default cloud."}
    )

    def _validate_name(self, name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        return name

    def _validate_id(self, id: str) -> str:  # noqa: A002
        if not isinstance(id, str) or not id.strip():
            raise ValueError("id must be a non-empty string")
        return id

    def _validate_provider(self, provider: Union[CloudProvider, str]) -> CloudProvider:
        if isinstance(provider, str):
            # This will raise a ValueError if the provider is unrecognized.
            provider = CloudProvider(provider)
        elif not isinstance(provider, CloudProvider):
            raise TypeError("'provider' must be a CloudProvider.")

        return provider

    def _validate_region(self, region: Optional[str]) -> Optional[str]:
        if region is not None and not isinstance(region, str):
            raise TypeError("region must be a string")
        return region

    def _validate_created_at(
        self, created_at: Optional[datetime]
    ) -> Optional[datetime]:
        if created_at is None:
            return None
        if not isinstance(created_at, datetime):
            raise TypeError("created_at must be a datetime object")
        return created_at

    def _validate_is_default(self, is_default: Optional[bool]) -> Optional[bool]:
        if is_default is not None and not isinstance(is_default, bool):
            raise TypeError("is_default must be a bool")
        return is_default

    def _validate_compute_stack(
        self, compute_stack: Union[ComputeStack, str]
    ) -> ComputeStack:
        if isinstance(compute_stack, str):
            # This will raise a ValueError if the compute_stack is unrecognized.
            compute_stack = ComputeStack(compute_stack)
        elif not isinstance(compute_stack, ComputeStack):
            raise TypeError("'compute_stack' must be a ComputeStack.")

        return compute_stack
