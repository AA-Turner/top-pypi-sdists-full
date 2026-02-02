
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from code_loader.experiment_api.client import Client
from code_loader.experiment_api.types import ApiMetrics


@dataclass
class InitExperimentRequest:
    experimentName: str
    description: str
    projectName: Optional[str] = None
    projectId: Optional[str] = None
    removeUntaggedUploadedModels: bool = True
    codeIntegrationName: Optional[str] = None
    codeIntegrationId: Optional[str] = None

@dataclass
class InitExperimentResponse:
    projectId: str
    versionId: str
    experimentId: str
    isCreatedProject: bool

@dataclass
class GetUploadModelSignedUrlRequest:
    epoch: int
    experimentId: str
    versionId: str
    projectId: str
    fileType: str
    origin: Optional[str] = None

@dataclass
class GetUploadModelSignedUrlResponse:
    url: str
    fileName: str

@dataclass
class LogExternalEpochDataRequest:
  projectId: str
  experimentId: str
  epoch: int
  metrics: ApiMetrics
  override: bool = False

@dataclass
class TagModelRequest:
  projectId: str
  experimentId: str
  epoch: int
  tags: List[str]

@dataclass
class SetExperimentPropertiesRequest:
    projectId: str
    experimentId: str
    properties: Dict[str, Any]

class Api:
    def __init__(self, client: Client):
        self.client = client
    
    def init_experiment(self, data: InitExperimentRequest) -> InitExperimentResponse:
        response = self.client.post('/versions/initExperiment', data)
        self.client.check_response(response)
        return InitExperimentResponse(**response.json())
    
    def get_uploaded_model_signed_url(self, data: GetUploadModelSignedUrlRequest)-> GetUploadModelSignedUrlResponse:
        response = self.client.post('/versions/getUploadModelSignedUrl', data)
        self.client.check_response(response)
        return GetUploadModelSignedUrlResponse(**response.json())
    
    def log_external_epoch_data(self, data: LogExternalEpochDataRequest)-> None:
        response = self.client.post('/externalepochdata/logExternalEpochData', data)
        self.client.check_response(response)
    
    def tag_model(self, data: TagModelRequest)-> None:
        response = self.client.post('/versions/tagModel', data)
        self.client.check_response(response)

    def set_experiment_properties(self, data: SetExperimentPropertiesRequest)-> None:
        response = self.client.post('/versions/setExperimentProperties', data)
        self.client.check_response(response)