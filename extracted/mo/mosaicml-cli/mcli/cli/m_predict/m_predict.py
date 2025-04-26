"""mcli predict entrypoint"""
import argparse
import logging
from pprint import pprint
from typing import Any, Dict

import yaml
from requests import HTTPError

from mcli import predict
from mcli.api.exceptions import InferenceServerException, MAPIException
from mcli.utils import utils_completers
from mcli.utils.utils_logging import FAIL

logger = logging.getLogger(__name__)


def predict_cli(
    inputs: Dict[str, Any],
    deployment: str,
    timeout: int,
    **kwargs,
) -> int:
    del kwargs
    try:
        resp = predict(deployment, inputs=inputs, timeout=timeout)
        print(f'{deployment}\'s prediction results:')
        pprint(resp)
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


def add_predict_parser(subparser: argparse._SubParsersAction):
    predict_parser: argparse.ArgumentParser = subparser.add_parser(
        'predict',
        help='Run prediction on a model in the MosaicML Cloud with given inputs. Returns forward pass result',
    )
    deployment_parser = predict_parser.add_argument(
        'deployment',
        metavar='DEPLOYMENT',
        help='The name or url of the deployment to run inference on',
    )
    deployment_parser.completer = utils_completers.DeploymentNameCompleter()  # pyright: ignore

    predict_parser.add_argument(
        '--input',
        '--inputs',
        '-i',
        dest='inputs',
        required=True,
        nargs="?",
        type=yaml.safe_load,
        metavar='INPUT',
        help='Input values to run forward pass on. Input values must be JSON-serializable and have string keys.',
    )

    predict_parser.add_argument(
        '--timeout',
        dest='timeout',
        default=60,
        required=False,
        nargs="?",
        type=yaml.safe_load,
        metavar='TIMEOUT',
        help='Timeout for the request in seconds. Defaults to 60 seconds.',
    )

    predict_parser.set_defaults(func=predict_cli)
