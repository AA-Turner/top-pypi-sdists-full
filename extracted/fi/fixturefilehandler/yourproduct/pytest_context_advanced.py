from pathlib import Path

import pytest

from fixturefilehandler import ResourceFileDeployer
from fixturefilehandler.file_paths import RelativeDeployFilePath


@pytest.fixture
def fixture_file_advanced(request):
    file_path = RelativeDeployFilePath(
        Path('test.txt'),
        Path('test.txt.bak'),
        Path(f'testresources/{request.node.name}.txt'),
        Path(__file__).parent
    )

    ResourceFileDeployer.setup(file_path)
    yield file_path
    ResourceFileDeployer.teardown(file_path)


def test_something(fixture_file_advanced):
    """test something"""
