from pathlib import Path
import pytest

from fixturefilehandler.factories import DeployerFactory
from fixturefilehandler.file_paths import RelativeDeployFilePath

DEPLOYER = DeployerFactory.create(
    RelativeDeployFilePath(
        Path('test.txt'),
        Path('test.txt.bak'),
        Path('testresources/test.txt.dist'),
        Path(__file__).parent
    )
)


@pytest.fixture
def fixture_file():
    DEPLOYER.setup()
    yield DEPLOYER.FILE_PATH
    DEPLOYER.teardown()


def test_something(fixture_file):
    """test something"""
