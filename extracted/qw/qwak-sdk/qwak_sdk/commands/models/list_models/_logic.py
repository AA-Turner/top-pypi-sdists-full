from qwak.clients.model_management.client import ModelsManagementClient


def list_models(project_id: str):
    return ModelsManagementClient().list_models(project_id)
