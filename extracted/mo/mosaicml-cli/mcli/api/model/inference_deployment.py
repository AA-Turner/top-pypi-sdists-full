"""GraphQL representaion of Deployment"""
from dataclasses import dataclass, field
from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, Generator, List, Optional, Tuple, Union

from mcli.api.exceptions import MAPIException
from mcli.api.schema.generic_model import DeserializableModel, convert_datetime
from mcli.models.inference_deployment_config import FinalInferenceDeploymentConfig, InferenceDeploymentConfig


@dataclass
class InferenceDeploymentReplica(DeserializableModel):
    """A specific replica of an inference deployment
    """

    name: str
    status: str
    latest_restart_count: int
    latest_restart_time: Optional[datetime] = None

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]):
        latest_restart_time = None if response['latestRestartTime'] is None else convert_datetime(
            response['latestRestartTime'])
        return cls(name=response["name"],
                   status=response["status"],
                   latest_restart_count=response["latestRestartCount"],
                   latest_restart_time=latest_restart_time)


@dataclass
class InferenceDeployment(DeserializableModel):
    """A deployment that has been launched on the MosaicML Cloud

    Args:
        deployment_uid (`str`): Unique identifier for the deployment
        name (`str`): User-defined name of the deployment
        status (:class:`~mcli.utils.utils_deployment_status.DeploymentStatus`): Status of the deployment
        at a moment in time
        created_at (`datetime`): Date and time when the deployment was created
        updated_at (`datetime`): Date and time when the deployment was last updated
        config (:class:`~mcli.models.deployment_config.DeploymentConfig`): The
            :class:`deployment configuration <mcli.models.deployment_config.DeploymentConfig>` that was
            used to launch to the deployment
    """

    deployment_uid: str
    name: str
    status: str
    created_at: datetime
    updated_at: datetime
    config: FinalInferenceDeploymentConfig
    created_by: str
    public_dns: str = ""
    current_version: int = 0

    deleted_at: Optional[datetime] = None
    submitted_config: Optional[InferenceDeploymentConfig] = None
    replicas: List[InferenceDeploymentReplica] = field(default_factory=List)

    _required_properties: Tuple[str] = tuple(
        ['id', 'name', 'status', 'createdAt', 'updatedAt', 'inferenceDeploymentInput', 'publicDNS'])

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]):
        missing = set(cls._required_properties) - set(response)
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=f'Missing required key(s) in response to deserialize Deployment object: {", ".join(missing)}',
            )

        deleted_at = None
        if response['deletedAt'] is not None:
            deleted_at = convert_datetime(response['deletedAt'])

        submit_config = None
        if response.get('originalInferenceDeploymentInput', {}):
            submit_config = InferenceDeploymentConfig.from_mapi_response(response['originalInferenceDeploymentInput'])

        replicas = [] if 'replicas' not in response else [
            InferenceDeploymentReplica.from_mapi_response(replica) for replica in response['replicas']
        ]

        return cls(deployment_uid=response['id'],
                   name=response['name'],
                   created_at=convert_datetime(response['createdAt']),
                   updated_at=convert_datetime(response['updatedAt']),
                   deleted_at=deleted_at,
                   status=response['status'],
                   public_dns=response['publicDNS'],
                   created_by=response['createdByEmail'],
                   config=FinalInferenceDeploymentConfig.from_mapi_response(response['inferenceDeploymentInput']),
                   submitted_config=submit_config,
                   replicas=replicas,
                   current_version=response['currentVersion'] if 'currentVersion' in response else 0)

    def get_ready_replicas(self):
        if self.replicas is None:
            return self.config.replicas
        else:
            return len([r.status for r in self.replicas if r.status == "RUNNING"])

    def refresh(self) -> "InferenceDeployment":
        """
        Refreshed the data on the deployment object

        Returns:
            Refreshed :class:`~mcli.api.model.inference_deployment.InferenceDeployment` object
        """
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from mcli.api.inference_deployments import get_inference_deployment

        return get_inference_deployment(self)

    def ping(self) -> dict:
        """
        Pings the deployment

        Returns:
            Dictionary containing the status of the deployment
        """
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from mcli.api.inference_deployments import ping

        return ping(self)

    def predict(self,
                inputs: Dict[str, Any],
                stream: bool = False) -> Union[Dict[str, Any], Generator[str, None, None]]:
        """
        Sends input to the deployment and runs prediction on the input

        Args:
            inputs: Input data to run prediction on in the form of dictionary

        Returns:
            Dictionary containing the output produced by the model
        """
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from mcli.api.inference_deployments import predict

        return predict(self, inputs, stream=stream)

    def delete(self) -> "InferenceDeployment":
        """
        Deletes the deployment

        Returns:
            Deleted :class:`~mcli.api.model.inference_deployment.InferenceDeployment` object
        """
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from mcli.api.inference_deployments import delete_inference_deployment
        return delete_inference_deployment(self)
