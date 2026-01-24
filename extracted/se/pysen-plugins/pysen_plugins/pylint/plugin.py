import pathlib
from typing import Sequence

from pysen import ComponentBase, Config, PluginBase, PluginConfig
from pysen.exceptions import InvalidConfigurationError

from .component import PylintComponent


def pylint() -> PluginBase:
    return PylintPlugin()


class PylintPlugin(PluginBase):
    def load(
        self, file_path: pathlib.Path, config: PluginConfig, root: Config
    ) -> Sequence[ComponentBase]:
        if root.lint is not None and root.lint.source is not None:
            source = root.lint.source
        else:
            raise InvalidConfigurationError("Source for pylint must be specified")
        return [PylintComponent(source)]
