from functools import partial
import os

from anyscale.anyscale_pydantic import BaseModel
from anyscale.client.openapi_client.api.default_api import DefaultApi
from anyscale.util import get_working_dir


class SSHKeyInfo(BaseModel):
    user: str
    key_path: str


class WorkspaceCommandContext(BaseModel):
    ssh: SSHKeyInfo
    working_dir: str
    head_ip: str
    project_id: str


def _get_ssh_key_info(
    session_id: str, api_client: DefaultApi, ssh_dir: str = "~/.ssh",
) -> SSHKeyInfo:
    # TODO (yiran): cleanup SSH keys if session no longer exists.
    def _write_ssh_key(name: str, ssh_key: str) -> str:
        key_path = os.path.join(os.path.expanduser(ssh_dir), f"{name}.pem")
        os.makedirs(os.path.dirname(key_path), exist_ok=True)

        with open(key_path, "w", opener=partial(os.open, mode=0o600)) as f:
            f.write(ssh_key)

        return key_path

    ssh_key = api_client.get_session_ssh_key_api_v2_sessions_session_id_ssh_key_get(
        session_id
    ).result

    key_path = _write_ssh_key(ssh_key.key_name, ssh_key.private_key)

    # since v2 stack the host user is ubuntu.
    return SSHKeyInfo(user="ubuntu", key_path=key_path)


def extract_workspace_parameters(
    cluster_id: str, project_id: str, api_client: DefaultApi, ssh_dir: str,
) -> WorkspaceCommandContext:
    """
    This function pulls relevant fields from the legacy cluster config
    to populate a `WorkspaceCommandContext`.

    NOTE: Any additional fields that need to go into the WorkspaceCommandContext
    should be passed via actual API calls, and not pulled from cluster configs.
    """

    head_ip = api_client.get_session_head_ip_api_v2_sessions_session_id_head_ip_get(
        cluster_id
    ).result.head_ip

    ssh_info = _get_ssh_key_info(cluster_id, api_client, ssh_dir)
    return WorkspaceCommandContext(
        ssh=ssh_info,
        project_id=project_id,
        head_ip=head_ip,
        working_dir=get_working_dir(project_id, api_client) + "/",
    )
