""" mcli ping entrypoint """
import argparse
import logging

from requests import HTTPError

from mcli import ping as api_ping
from mcli.api.exceptions import InferenceServerException, MAPIException
from mcli.utils import utils_completers
from mcli.utils.utils_logging import FAIL

logger = logging.getLogger(__name__)


def ping(
    deployment: str,
    **kwargs,
) -> int:
    del kwargs
    try:
        resp = api_ping(deployment)
        print(f'{deployment}\'s status: {resp.get("status", resp)}')
        return 0
    except HTTPError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except MAPIException as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except InferenceServerException as e:
        logger.error(f'{FAIL} {e}')
        return 1


def add_ping_parser(subparser: argparse._SubParsersAction):
    ping_parser: argparse.ArgumentParser = subparser.add_parser(
        'ping',
        help='Ping a inference deployment in the MosaicML platform for health metrics',
    )
    deployment_parser = ping_parser.add_argument(
        'deployment',
        metavar='DEPLOYMENT',
        help='The name or url of the inference deployment.',
    )
    deployment_parser.completer = utils_completers.DeploymentNameCompleter()  # pyright: ignore

    ping_parser.set_defaults(func=ping)
