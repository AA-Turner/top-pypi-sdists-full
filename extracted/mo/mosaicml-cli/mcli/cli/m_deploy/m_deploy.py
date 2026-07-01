"""mcli deploy entrypoint"""
import argparse
import logging
import textwrap
from http import HTTPStatus
from typing import Optional

from mcli.api.exceptions import MAPIException, MCLIDeploymentConfigValidationError
from mcli.api.inference_deployments.api_create_inference_deployment import create_inference_deployment
from mcli.models.inference_deployment_config import InferenceDeploymentConfig
from mcli.utils import utils_completers
from mcli.utils.utils_logging import FAIL, OK

logger = logging.getLogger(__name__)


def print_help(**kwargs) -> int:
    del kwargs
    mock_parser = argparse.ArgumentParser()
    _configure_parser(mock_parser)
    mock_parser.print_help()
    return 1


def deploy_entrypoint(file: str,
                      override_cluster: Optional[str] = None,
                      override_gpu_type: Optional[str] = None,
                      override_gpu_num: Optional[int] = None,
                      override_image: Optional[str] = None,
                      override_replicas: Optional[int] = None,
                      **kwargs) -> int:
    del kwargs

    if file is None:
        return print_help()

    try:
        deploy_config = InferenceDeploymentConfig.from_file(path=file)

        if override_cluster is not None:
            deploy_config.cluster = override_cluster
        if override_gpu_type is not None:
            deploy_config.gpu_type = override_gpu_type

        if override_gpu_num is not None:
            deploy_config.gpu_num = override_gpu_num

        if override_image is not None:
            deploy_config.image = override_image

        if override_replicas is not None:
            deploy_config.replicas = override_replicas

        try:
            deployment = create_inference_deployment(deploy_config)
        except MAPIException as e:
            if e.status == HTTPStatus.UNAUTHORIZED:
                e.message = """MosaicML Inference is not publicly available.
                  Reach out to MosaicML support if you're interested!"""
            raise e

        message = f"""
        {OK} Deployment [cyan]{deployment.name}[/] submitted.

        To see the deployment\'s status, use:

        [bold]mcli get deployments[/]

        """
        logger.info(textwrap.dedent(message).strip())
        return 0
    except (MAPIException) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except MCLIDeploymentConfigValidationError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except FileNotFoundError as e:
        logger.error(f'{FAIL} {e}')
        return 1


def add_deploy_argparser(subparser: argparse._SubParsersAction) -> None:
    deploy_parser: argparse.ArgumentParser = subparser.add_parser(
        'deploy',
        help='Deploy a model in the MosaicML Cloud',
    )
    deploy_parser.set_defaults(func=deploy_entrypoint)
    _configure_parser(deploy_parser)


def _configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        '-f',
        '--file',
        dest='file',
        help='File from which to load arguments.',
    )

    cluster_parser = parser.add_argument(
        '--cluster',
        dest='override_cluster',
        help='Optional override for MCLI cluster',
    )
    cluster_parser.completer = utils_completers.ClusterNameCompleter()  # pyright: ignore

    gpu_type_parser = parser.add_argument(
        '--gpu-type',
        dest='override_gpu_type',
        help='Optional override for GPU type. Valid GPU type depend on'
        ' the cluster and GPU number requested',
    )
    gpu_type_parser.completer = utils_completers.GPUTypeCompleter()  # pyright: ignore

    parser.add_argument(
        '--gpus',
        type=int,
        dest='override_gpu_num',
        help='Optional override for number of GPUs. Valid GPU numbers '
        'depend on the cluster and GPU type',
    )

    parser.add_argument(
        '--image',
        dest='override_image',
        help='Optional override for docker image',
    )

    parser.add_argument(
        '--replicas',
        '--replica',
        type=int,
        dest='override_replicas',
        help='Optional override for number of replicas',
    )
