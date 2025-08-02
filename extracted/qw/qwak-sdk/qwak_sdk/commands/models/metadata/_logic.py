from qwak.clients.model_management.client import ModelsManagementClient


def list_models_metadata(project_id: str):
    return ModelsManagementClient().list_models_metadata(project_id)
