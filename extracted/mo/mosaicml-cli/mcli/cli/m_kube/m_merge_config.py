"""Implements mcli kube merge-config"""
import argparse
import logging
from pathlib import Path

import yaml

from mcli.cli.m_kube.utils import merge_kubeconfigs
from mcli.utils.utils_logging import FAIL, OK

logger = logging.getLogger(__name__)


def merge_k8s(
        source: Path,
        dest: Path = Path('~/kube/config').expanduser(),
        **kwargs,
) -> int:
    del kwargs

    if not source.exists():
        logger.error(f'{FAIL} Could not find kubeconfig file {source}')
        return 1

    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists():
        with open(dest, 'r', encoding='utf-8') as f:
            dest_config = yaml.safe_load(f)
    else:
        dest_config = {
            'apiVersion': 'v1',
            'kind': 'Config',
            'clusters': [],
            'users': [],
            'contexts': [],
        }

    with open(source, 'r', encoding='utf-8') as f:
        source_config = yaml.safe_load(f)

    merged = merge_kubeconfigs(source_config, dest_config)
    with open(dest, 'w', encoding='utf-8') as f:
        yaml.safe_dump(merged, f)

    logger.info(f'{OK} Updated Kubernetes config file at: {dest_config}')

    return 0


def add_merge_config_parser(subparser: argparse._SubParsersAction):
    merge_config_parser: argparse.ArgumentParser = subparser.add_parser(
        'merge-config',
        help='Merge two kubernetes config files',
    )
    merge_config_parser.add_argument('source',
                                     metavar='SOURCE',
                                     type=Path,
                                     help='The Kubernetes config file you would like to merge')
    merge_config_parser.add_argument('dest',
                                     default=None,
                                     metavar='DEST',
                                     type=Path,
                                     help="Kubernetes config file into which the source config will be merged")
    merge_config_parser.set_defaults(func=merge_k8s)
    return merge_config_parser
