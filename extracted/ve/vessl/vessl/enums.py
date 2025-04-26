from enum import Enum


class ModelServiceType(Enum):
    PROVISIONED = 'provisioned'
    SERVERLESS = 'serverless'

class ClusterProvider(Enum):
    AWS = 'aws'
    GCP = 'gcp'
    OCI = 'oci'
    AZURE = 'azure'
    ON_PREMISE = 'on-premise'

class ClusterCustomEndpointType(Enum):
    NODE_PORT = 'nodeport'
    SUBDOMAIN = 'subdomain'