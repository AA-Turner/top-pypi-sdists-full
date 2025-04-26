import os
import sys
import zipfile
from pathlib import Path

from acres import Loader


def test_zipimport(tmp_path: Path) -> None:
    # Setup... no need for a fixture for a single test
    target_file = tmp_path / 'mymodule.zip'
    with zipfile.ZipFile(target_file, mode='w') as mymod:
        mymod.writestr(
            'mypkg/__init__.py',
            'from . import data\n',
        )
        mymod.writestr(
            'mypkg/data/__init__.py',
            'from acres import Loader\nload_resource = Loader(__spec__.name)\n',
        )
        mymod.writestr(
            'mypkg/data/resource.txt',
            'some text\n',
        )

    sys.path.insert(0, str(target_file))

    # Test
    import mypkg  # type: ignore[import-not-found]

    assert mypkg.__file__.endswith(os.path.join('mymodule.zip', 'mypkg', '__init__.py'))

    loader = mypkg.data.load_resource

    readable = loader.readable('resource.txt')
    assert not isinstance(readable, Path)
    assert readable.read_text() == 'some text\n'

    with loader.as_path('resource.txt') as path:
        assert isinstance(path, Path)
        assert path.exists()
        assert path.read_text() == 'some text\n'
    assert not path.exists()

    cached = loader.cached('resource.txt')
    assert isinstance(cached, Path)
    assert cached.exists()
    assert cached.read_text() == 'some text\n'

    new_loader = Loader('mypkg.data')
    assert new_loader.cached('resource.txt') == cached

    # Teardown
    sys.path.pop(0)
