"""Helper Utils for Yaml Files"""
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Union

import yaml
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

from mcli.utils.utils_logging import FAIL

logger = logging.getLogger(__name__)


class StringDumpYAML(YAML):
    """ Yaml dump to string """

    def dump(  #type: ignore
        self,
        data: Any,
        stream: Union[Path, 'StreamType'] = None,  # type: ignore
        transform: Any = None,
    ) -> Any:

        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, transform=transform)
        if inefficient:
            return stream.getvalue()  # type: ignore
        return ''


def load_yaml(path: Union[str, Path]) -> Dict[str, Any]:
    try:
        with open(path, 'r', encoding='utf8') as fh:
            config = yaml.safe_load(fh)
            if config is None:
                config = {}
    except FileNotFoundError:
        logger.error(f"{FAIL} File {path} not found")
        sys.exit(1)
    assert isinstance(config, dict), \
        f'Error expected config to be a dict but got {config}'
    return config
