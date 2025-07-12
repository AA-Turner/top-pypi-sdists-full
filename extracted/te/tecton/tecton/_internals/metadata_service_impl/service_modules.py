from tecton_proto.auth import authorization_service__client_pb2 as authorization_service_pb2
from tecton_proto.data import service_account__client_pb2 as service_account_pb2
from tecton_proto.materializationjobservice import (
    materialization_job_service__client_pb2 as materialization_job_service_pb2,
)
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2
from tecton_proto.modelartifactservice import model_artifact_service__client_pb2 as model_artifact_service_pb2
from tecton_proto.principal import principal_service__client_pb2 as principal_service_pb2
from tecton_proto.remoteenvironmentservice import (
    remote_environment_service__client_pb2 as remote_environment_service_pb2,
)
from tecton_proto.secrets import secrets_service__client_pb2 as secrets_service_client_pb2
from tecton_proto.servergroupservice import server_group_service__client_pb2 as server_group_service_pb2
from tecton_proto.serviceaccounts import service_accounts_service__client_pb2 as service_accounts_service_pb2
from tecton_proto.testhelperservice import test_helper_service__client_pb2 as test_helper_service_pb2


GRPC_SERVICE_MODULES = [
    metadata_service_pb2,
    materialization_job_service_pb2,
    authorization_service_pb2,
    remote_environment_service_pb2,
    test_helper_service_pb2,
    secrets_service_client_pb2,
    server_group_service_pb2,
    model_artifact_service_pb2,
    principal_service_pb2,
    service_account_pb2,
    service_accounts_service_pb2,
]
