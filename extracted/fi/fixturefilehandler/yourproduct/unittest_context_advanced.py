from pathlib import Path

import unittest

from fixturefilehandler import ResourceFileDeployer
from fixturefilehandler.file_paths import RelativeDeployFilePath


class AdvancedConfigurableTestCase(unittest.TestCase):
    @property
    def file_path(self) -> RelativeDeployFilePath:
        return RelativeDeployFilePath(
            Path('test.txt'),
            Path('test.txt.bak'),
            Path(f'testresources/{self._testMethodName}.txt'),
            Path(__file__).parent
        )

    def setUp(self):
        ResourceFileDeployer.setup(self.file_path)

    def doCleanups(self):
        ResourceFileDeployer.teardown(self.file_path)
