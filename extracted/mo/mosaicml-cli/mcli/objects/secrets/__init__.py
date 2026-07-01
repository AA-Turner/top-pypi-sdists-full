""" Reexporting All Secrets """
# pylint: disable=useless-import-alias
from typing import Dict, Type

from mcli.models import Secret, SecretType
from mcli.models.mcli_secret import MCLIGenericSecret
from mcli.objects.secrets.databricks import MCLIDatabricksSecret
from mcli.objects.secrets.docker_registry import MCLIDockerRegistrySecret
from mcli.objects.secrets.env_var import HuggingFaceSecret, MCLIEnvVarSecret
from mcli.objects.secrets.gcp import MCLIGCPSecret
from mcli.objects.secrets.mounted import MCLIMountedSecret
from mcli.objects.secrets.oci import MCLIOCISecret
from mcli.objects.secrets.s3 import MCLIS3Secret
from mcli.objects.secrets.ssh import MCLIGitSSHSecret, MCLISFTPSSHSecret, MCLISSHSecret

SECRET_CLASS_MAP: Dict[SecretType, Type[Secret]] = {
    SecretType.docker_registry: MCLIDockerRegistrySecret,
    SecretType.generic: MCLIGenericSecret,
    SecretType.environment: MCLIEnvVarSecret,
    SecretType.mounted: MCLIMountedSecret,
    SecretType.ssh: MCLISSHSecret,
    SecretType.git: MCLIGitSSHSecret,
    SecretType.sftp: MCLISFTPSSHSecret,
    SecretType.s3: MCLIS3Secret,
    SecretType.gcp: MCLIGCPSecret,
    SecretType.oci: MCLIOCISecret,
    SecretType.databricks: MCLIDatabricksSecret,
    SecretType.hugging_face: HuggingFaceSecret
}
