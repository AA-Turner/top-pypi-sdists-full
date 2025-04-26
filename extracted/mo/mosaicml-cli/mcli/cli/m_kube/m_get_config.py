""" mcli init_kube Entrypoint """
import argparse
import logging
import webbrowser
from pathlib import Path
from typing import NamedTuple, Optional

from mcli.api.exceptions import ValidationError
from mcli.cli.m_kube.utils import generate_cluster_config, retrieve_clusters
from mcli.utils.utils_interactive import secret_prompt, simple_prompt
from mcli.utils.utils_logging import FAIL, OK
from mcli.utils.utils_spinner import console_status
from mcli.utils.utils_string_functions import validate_rfc1123_name

RANCHER_ENDPOINT_PATTERN = 'https://rancher.z[0-9]+.r[0-9]+.mosaicml.cloud'
DEEP_LINKS = {
    'DEFAULT': 'dashboard/account/create-key',
}

DEFAULT_NAMESPACE = 'mosaicml-orchestration'

logger = logging.getLogger(__name__)


def bold(text: str) -> str:
    return f'[bold green]{text}[/]'


class RancherDetails(NamedTuple):
    endpoint: str
    auth_token: str


def validate_auth_token(text: str) -> bool:
    if not text.startswith('token'):
        raise ValidationError('Bearer token should start with "token"')
    return True


def validate_number(text: str) -> bool:
    if not text.isnumeric():
        raise ValidationError(f'Zone must be a number. Got: {text}')
    return True


def fill_rancher_values(zone: Optional[int] = None,) -> RancherDetails:
    if zone is None:
        zone = int(simple_prompt(
            'Which MosaicML platform "zone" would you like to access?',
            validate=validate_number,
        ))
    rancher_endpoint = f'https://rancher.z{zone}.r0.mosaicml.cloud'

    assert rancher_endpoint is not None

    # Get required info
    path = DEEP_LINKS.get(rancher_endpoint, None) or DEEP_LINKS['DEFAULT']
    url = f'{rancher_endpoint}/{path}'
    logger.info(
        '\n\nTo communicate with this Kubernetes cluster, we\'ll need an API key '
        f'(also called the "{bold("Bearer Token")}"). '
        'Your browser should have opened to the API key creation screen. Login, if necessary, then, create a '
        f'key with "{bold("no scope")}" that expires "{bold("A day from now")}" and copy the '
        f'"{bold("Bearer Token")}" for this next step. If your browser did not open, please use this link:'
        f'\n\n[blue]{url}[/]\n\n'
        'If upon login you do not see the API key creation screen, either try the link above in Google Chrome or '
        f'select "{bold("Accounts & API Keys")}" from the top-right user menu, followed by '
        f'"{bold("Create API Key")}" and the directions above.')
    webbrowser.open_new_tab(url)

    auth_token = secret_prompt('What is your "bearer token"?', validate=validate_auth_token)

    return RancherDetails(endpoint=rancher_endpoint, auth_token=auth_token)


def initialize_k8s(
    namespace,
    kube_config,
    zone: Optional[int] = None,
    **kwargs,
) -> int:
    # pylint: disable=too-many-statements
    del kwargs

    try:
        result = validate_rfc1123_name(namespace)
        if not result:
            raise RuntimeError(result.message)

        details = fill_rancher_values(zone=zone)
        rancher_endpoint, auth_token = details

        # Retrieve all available clusters
        with console_status('Retrieving clusters...'):
            clusters = retrieve_clusters(rancher_endpoint, auth_token)
        if clusters:
            logger.info(f'{OK} Found {len(clusters)} clusters that you have access to')
        else:
            logger.error(f'{FAIL} No clusters found. Please double-check that you have access to clusters in '
                         'the MosaicML platform')
            return 1

        # Generate kubeconfig file from clusters
        with console_status('Generating custom kubeconfig file...'):
            kube_config_path = generate_cluster_config(rancher_endpoint,
                                                       auth_token,
                                                       clusters,
                                                       namespace,
                                                       kube_config_path=kube_config)
        logger.info(f'{OK} Updated Kubernetes config file at: {kube_config_path}')

        # Suggest next steps
        cluster_names = ', '.join(bold(cluster.name) for cluster in clusters)
        logger.info(f'You now have access to the following {bold(str(len(clusters)))} clusters: '
                    f'{cluster_names}')

    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1

    return 0


def add_get_config_parser(subparser: argparse._SubParsersAction):
    get_config_parser: argparse.ArgumentParser = subparser.add_parser(
        'get-config',
        help='Setup your direct access to MosaicML platform Kubernetes clusters',
    )
    get_config_parser.add_argument(
        '--zone',
        default=None,
        type=int,
        help='The "zone" in which your cluster resides. '
        'This should have been given to you by the MosaicML platform support team',
    )
    get_config_parser.add_argument(
        '--namespace',
        default=DEFAULT_NAMESPACE,
        help='The namespace you\'ll be using within the clusters. '
        'If you do not know, this will default to the MosaicML platform default namespace',
    )
    get_config_parser.add_argument(
        '--kube-config',
        default=Path('~/.kube/config').expanduser(),
        type=Path,
        help="kubeconfig file in which to place new cluster credentials (default: %(default)s)",
    )
    get_config_parser.set_defaults(func=initialize_k8s)
    return get_config_parser
