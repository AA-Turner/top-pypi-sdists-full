""" mcli create secret Entrypoint """
import argparse
import logging
import textwrap
from typing import Callable, Optional

from mcli.api.exceptions import cli_error_handler
from mcli.api.secrets.api_create_secret import create_secret
from mcli.models import SecretType
from mcli.objects.secrets.create.databricks import DatabricksSecretCreator
from mcli.objects.secrets.create.docker_registry import DockerSecretCreator
from mcli.objects.secrets.create.gcp import GCPSecretCreator
from mcli.objects.secrets.create.generic import EnvVarSecretCreator, FileSecretCreator
from mcli.objects.secrets.create.hugging_face import HuggingFaceSecretCreator
from mcli.objects.secrets.create.oci import OCISecretCreator
from mcli.objects.secrets.create.s3 import S3SecretCreator
from mcli.objects.secrets.create.ssh import SSHSecretCreator
from mcli.utils.utils_interactive import input_disabled
from mcli.utils.utils_logging import OK
from mcli.utils.utils_spinner import console_status

logger = logging.getLogger(__name__)

CREATORS = {
    SecretType.docker_registry: DockerSecretCreator,
    SecretType.environment: EnvVarSecretCreator,
    SecretType.mounted: FileSecretCreator,
    SecretType.ssh: SSHSecretCreator,
    SecretType.git: SSHSecretCreator,
    SecretType.sftp: SSHSecretCreator,
    SecretType.s3: S3SecretCreator,
    SecretType.gcp: GCPSecretCreator,
    SecretType.oci: OCISecretCreator,
    SecretType.databricks: DatabricksSecretCreator,
    SecretType.hugging_face: HuggingFaceSecretCreator,
}


def _create_new_secret(
    secret_type: SecretType,
    secret_name: Optional[str] = None,
    no_input: bool = False,
    **kwargs,
):

    command = secret_type.value.replace('_', '-')

    @cli_error_handler(f'mcli create secret {command}')
    def helper():
        kwargs.pop('func', None)

        with input_disabled(no_input):
            creator = CREATORS[secret_type]()
            secret = creator.create(name=secret_name, **kwargs)

            with console_status('Creating secrets..'):
                create_secret(secret=secret, timeout=None)

            logger.info(f'{OK} Created {secret.secret_type} secret: {secret.name}')
            return 0

    return helper()


def create_new_secret(
    secret_type: SecretType,
    secret_name: Optional[str] = None,
    no_input: bool = False,
    **kwargs,
) -> int:
    return _create_new_secret(secret_type, secret_name, no_input, **kwargs)


def _add_common_arguments(parser: argparse.ArgumentParser):
    parser.add_argument(
        '--name',
        dest='secret_name',
        metavar='NAME',
        help='What you would like to call the secret. Must be unique',
    )
    parser.add_argument('--no-input', action='store_true', help='Do not query for user input')


def _add_docker_registry_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    docker_registry_parser = subparser.add_parser(
        'docker',
        aliases=['docker-registry'],
        help='Create a secret to let you pull images from a private Docker registry.',
        description='Create a secret to let you pull images from a private Docker registry.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _add_common_arguments(docker_registry_parser)
    docker_registry_parser.add_argument(
        '--username',
        dest='username',
        help='Your username for the Docker registry',
    )
    docker_registry_parser.add_argument(
        '--password',
        dest='password',
        help='Your password for the Docker registry. If possible, use an API key here.',
    )
    docker_registry_parser.add_argument(
        '--email',
        dest='email',
        help='The email you use for the Docker registry',
    )
    docker_registry_parser.add_argument('--server',
                                        dest='server',
                                        help='The URL for the Docker registry. '
                                        'For DockerHub, this should be https://index.docker.io/v1/.')
    docker_registry_parser.set_defaults(func=secret_handler, secret_type=SecretType.docker_registry)
    return docker_registry_parser


def _add_ssh_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    ssh_parser = subparser.add_parser(
        'ssh',
        help='Create an SSH secret for your SSH private key',
        description='Add your SSH private key to mcli to enable SSH from within your workloads. '
        'This allows you to get data into your workloads via SSH, for example from an SFTP server.',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ssh_parser.add_argument('ssh_private_key',
                            metavar='</path/to/private-key>',
                            nargs='?',
                            help='Path the private key of an SSH key-pair')
    ssh_parser.add_argument('--mount-path',
                            metavar='</path/inside/workload>',
                            help='Location in your workload at which the SSH key should be mounted')
    _add_common_arguments(ssh_parser)
    ssh_parser.set_defaults(func=secret_handler, secret_type=SecretType.ssh, git=False)


def _add_git_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    git_parser = subparser.add_parser(
        'git-ssh',
        help='Create an SSH secret for use with Git commands',
        description='Add an SSH private key to your workloads to access private Git repos over SSH. '
        'To use this, you\'ll also need to register the associated public SSH key to your account '
        'at github.com (or your repository host of choice).',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    git_parser.add_argument('ssh_private_key',
                            metavar='</path/to/private-key>',
                            nargs='?',
                            help='Path to the private key of an SSH key-pair')
    git_parser.add_argument('--mount-path',
                            metavar='</path/inside/workload>',
                            help='Location in your workload at which the SSH key should be mounted')
    _add_common_arguments(git_parser)
    git_parser.set_defaults(func=secret_handler, secret_type=SecretType.git, git=True)


def _add_sftp_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    sftp_parser = subparser.add_parser(
        'sftp-ssh',
        help='Create an SSH secret for use with SFTP',
        description='Add an SSH private key to your workloads to access an SFTP server over SSH.',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sftp_parser.add_argument('ssh_private_key',
                             metavar='</path/to/private-key>',
                             nargs='?',
                             help='Path to the private key of an SSH key-pair')
    sftp_parser.add_argument('--mount-path',
                             metavar='</path/inside/workload>',
                             help='Location in your workload at which the SSH key should be mounted')
    sftp_parser.add_argument('--host-name', help='The hostname of the sftp server.')
    sftp_parser.add_argument('--no-host-check',
                             action='store_true',
                             default=False,
                             help='Do not verify fingerprints before adding SSH hosts to known_hosts. '
                             'WARNING: Disabling host checking is a security risk use with caution.')
    _add_common_arguments(sftp_parser)
    sftp_parser.set_defaults(func=secret_handler, secret_type=SecretType.sftp, sftp=True)


def _add_mounted_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    examples = textwrap.dedent("""

    Examples:

    # Add a file-mounted secret interactively
    mcli create secret mounted

    # Add a secret credentials file as a mounted file secret
    mcli create secret mounted /path/to/my-credentials

    # Specify a custom secret name
    mcli create secret mounted /path/to/my-credentials --name my-file
    """)
    generic_mounted_parser = subparser.add_parser(
        'mounted',
        help='Create a secret that will be mounted as a text file',
        description='Add a confidential text file to your workloads. File-mounted secrets are '
        'more secure than env secrets because they are less likely to be leaked by the processes running in your '
        'workload (e.g. some loggers can optionally record the system environment variables to aid in '
        'reproducibility).',
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    generic_mounted_parser.add_argument('secret_path',
                                        nargs='?',
                                        metavar='</path/to/secret/file>',
                                        help='A text file with secret data that you\'d like '
                                        'to have mounted within your workloads.')
    generic_mounted_parser.add_argument('--mount-path',
                                        metavar='</path/inside/workload>',
                                        help='Location in your workload at which the secret should be mounted. '
                                        'The file will be mounted at <mount-path>/secret. Must be unique')
    _add_common_arguments(generic_mounted_parser)
    generic_mounted_parser.set_defaults(func=secret_handler, secret_type=SecretType.mounted)


def _add_env_var_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    generic_env_parser = subparser.add_parser(
        'env',
        aliases=['environment'],
        help='Create a secret that will be exposed as an environment variable',
        description='Create a secret that will be exposed as an environment variable. This lets you easily use '
        'arbitrary confidential information within your workloads.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    generic_env_parser.add_argument(
        'env_pair',
        nargs='?',
        help='A KEY=VALUE pair',
    )
    _add_common_arguments(generic_env_parser)
    generic_env_parser.set_defaults(func=secret_handler, secret_type=SecretType.environment)


def _add_databricks_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    databricks_parser = subparser.add_parser(
        'databricks',
        help='Create DATABRICKS_HOST and DATBRICKS_TOKEN secrets that will be exposed as environment variables',
        description='Create DATABRICKS_HOST and DATBRICKS_TOKEN secrets that will be exposed as environment '
        'variables. This lets you easily set Databricks credentials within your workloads.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    databricks_parser.add_argument(
        '--host',
        metavar='DATABRICKS_HOST',
        help='The Databricks host, specified as the target Databricks workspace URL',
    )
    databricks_parser.add_argument(
        '--token',
        metavar='DATABRICKS_TOKEN',
        help='The Databricks Personal Access Token for the given workspace',
    )
    _add_common_arguments(databricks_parser)
    databricks_parser.set_defaults(func=secret_handler, secret_type=SecretType.databricks)


def _add_oci_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    description = """
        Add your OCI config file and key pem file to MCLI for use in your workloads. 
        
        Basically you would need a RSA key pair (API signing key) to use OCI through CLI or SDK. You would also need a config file that would contain
        the required configuration information like user credentials and tenancy OCID.

        The steps to generate these keys and config file can be found here: 
        https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm#apisigningkey_topic_How_to_Generate_an_API_Signing_Key_Console
        AND
        https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm

        A sample config file would look like:

        [DEFAULT]
        user=ocid1.user.oc1..<unique_ID>
        fingerprint=<your_fingerprint>
        key_file=~/.oci/oci_api_key.pem
        tenancy=ocid1.tenancy.oc1..<unique_ID>
        region=us-ashburn-1

        The key file is a PEM file that would look like a typical RSA private key file.

        Once you create the config and API private key pem file (note that the public key isn't needed as its fingerprint should already exist in the generated
        config file), you can create a OCI secret for MCLI. MCLI will automatically mount it to your workloads and export two environment variables:

        $OCI_CLI_CONFIG_FILE: Path to your config file.
        $OCI_CLI_KEY_FILE: Path to your API signing private key file.

        Most OCI compliant libraries will use these environment variables to discover your configs by default.
    """
    oci_configs_parser = subparser.add_parser(
        'oci',
        help='Add your OCI config and API key to MCLI',
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _add_common_arguments(oci_configs_parser)
    oci_configs_parser.add_argument('--config-file',
                                    metavar='PATH',
                                    help='Path to your OCI config file. Usually `~/.oci/config`')
    oci_configs_parser.add_argument('--key-file',
                                    metavar='PATH',
                                    help='Path to your OCI API key file. Usually `~/.oci/oci_api_key.pem`')
    oci_configs_parser.add_argument(
        '--mount-directory',
        metavar='PATH',
        help='Location in your workload at which your key and config files will be mounted.')
    oci_configs_parser.set_defaults(func=secret_handler, secret_type=SecretType.oci)


def _add_s3_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    description = """
Add your S3 config file and credentials file to MCLI for use in your workloads.

Your config and credentials files should follow the standard structure output
by `aws configure`:

~/.aws/config:

[default]
region=us-west-2
output=json


~/.aws/credentials:

[default]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY


More details on these files can be found here:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

Once you've created an S3 secret, MCLI will automatically mount it to your workloads
and export two environment variables:

$AWS_CONFIG_FILE:             Path to your config file
$AWS_SHARED_CREDENTIALS_FILE: Path to your credentials file

Most s3-compliant libraries will use these environment variables to discover your
credentials by default.
    """

    s3_cred_parser = subparser.add_parser(
        's3',
        help='Add your S3 config and credentials to MCLI',
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _add_common_arguments(s3_cred_parser)
    s3_cred_parser.add_argument('--config-file',
                                metavar='PATH',
                                help='Path to your S3 config file. Usually `~/.aws/config`')
    s3_cred_parser.add_argument('--credentials-file',
                                metavar='PATH',
                                help='Path to your S3 credentials file. Usually `~/.aws/credentials`')
    s3_cred_parser.add_argument(
        '--mount-directory',
        metavar='PATH',
        help='Location in your workload at which your credentials and config files will be mounted')
    s3_cred_parser.add_argument('--profile', metavar='PROFILE', help='The profile to use in your S3 credentials')
    s3_cred_parser.set_defaults(func=secret_handler, secret_type=SecretType.s3)


def _add_gcp_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    description = """
Add your GCP config file and credentials file to MCLI for use in your workloads.

Once you've created a GCP secret, MCLI will automatically mount it to your workloads
and export the following environment variable:

$GOOGLE_APPLICATION_CREDENTIALS: Path to your credentials file

Most gcp-compliant libraries will use this environment variable to discover your
credentials by default.
    """

    gcp_cred_parser = subparser.add_parser(
        'gcp',
        help='Add your GCP credentials to MCLI',
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _add_common_arguments(gcp_cred_parser)
    gcp_cred_parser.add_argument('--credentials-file', metavar='PATH', help='Path to your GCP credentials file.')
    gcp_cred_parser.add_argument('--mount-path',
                                 metavar='PATH',
                                 help='Location in your workload at which your credentials files will be mounted')
    gcp_cred_parser.set_defaults(func=secret_handler, secret_type=SecretType.gcp)


def _add_hugging_face_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    description = """
Add your hugging face credentials file to MCLI for use in your workloads.

Once you've created a hugging face secret, MCLI will automatically mount it 
to your workloads and export the following environment variable:

$HF_TOKEN: your hugging face token value
    """

    hf_cred_parser = subparser.add_parser(
        'hf',
        aliases=['hugging_face'],
        help='Add your hugging face credentials to MCLI',
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _add_common_arguments(hf_cred_parser)
    hf_cred_parser.add_argument('--token', metavar='TOKEN', help='Your hugging face token value.')
    hf_cred_parser.set_defaults(func=secret_handler, secret_type=SecretType.hugging_face)


def configure_secret_argparser(
    parser: argparse.ArgumentParser,
    secret_handler: Callable,
) -> None:

    subparser = parser.add_subparsers(title='MCLI Secrets',
                                      description='The table below shows the types of secrets that you can create',
                                      help='DESCRIPTION',
                                      metavar='SECRET_TYPE')

    # Environment variables
    _add_env_var_subparser(subparser, secret_handler)

    # Mounted secrets
    _add_mounted_subparser(subparser, secret_handler)

    # Docker registry
    _add_docker_registry_subparser(subparser, secret_handler)

    # SSH credentials
    _add_ssh_subparser(subparser, secret_handler)

    # Git credentials
    _add_git_subparser(subparser, secret_handler)

    # SFTP credentials
    _add_sftp_subparser(subparser, secret_handler)

    # S3 credentials
    _add_s3_subparser(subparser, secret_handler)

    # GCP credentials
    _add_gcp_subparser(subparser, secret_handler)

    # OCI credentials
    _add_oci_subparser(subparser, secret_handler)

    # Databricks credentials
    _add_databricks_subparser(subparser, secret_handler)

    # Hugging face credentials
    _add_hugging_face_subparser(subparser, secret_handler)
