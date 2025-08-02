from dataclasses import dataclass
from code_loader.experiment_api.api import Api


@dataclass
class ExperimentContext:
    api: Api
    project_id: str
    version_id: str
    experiment_id: str