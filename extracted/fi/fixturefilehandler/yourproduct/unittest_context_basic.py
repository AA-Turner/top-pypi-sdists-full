from pathlib import Path
import unittest

from fixturefilehandler.factories import VacatorFactory
from fixturefilehandler.file_paths import RelativeVacateFilePath

VACATOR = VacatorFactory.create(
    RelativeVacateFilePath(
        Path('test.txt'),
        Path('test.txt.bak'),
        Path(__file__).parent
    )
)


class ConfigurableTestCase(unittest.TestCase):
    def setUp(self):
        VACATOR.setup()

    def doCleanups(self):
        VACATOR.teardown()
