from pipebio.pipebio_client import PipebioClient


def get_adimab_vh_id(client:PipebioClient) -> int:
    return 'ent_Y4GegZJyUWSG6wL1'

def get_project_id(client:PipebioClient) -> str:
    return 'e0d0c886-a294-44d5-89bd-02d471cfbfc2'

def get_parent_id(client:PipebioClient) -> int:
    """
    e.g. group test results together so we can easily delete them in PipeBio UI.
    """
    return 'ent_EcOkLmmXWLDIthRa' if client.is_aws else None