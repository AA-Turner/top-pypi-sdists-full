import os
from pathlib import Path
import subprocess
import sys


def test_public_import_chain_loads_from_source_tree():
    root = Path(__file__).parents[1]
    # Prepend the source tree; keep the runner's own path so the subprocess
    # resolves abstract_essentials the same way the test runner does.
    inherited = os.environ.get('PYTHONPATH')
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(p for p in (str(root / 'src'), inherited) if p))
    code = '''
import abstract_utilities
import abstract_utilities.env_utils
import abstract_utilities.file_utils
import abstract_utilities.ssh_utils
from abstract_utilities.env_utils import AbstractEnv, get_env_path, get_env_value
from abstract_utilities.type_utils import MIME_TYPES
assert MIME_TYPES and 'image' in MIME_TYPES
assert AbstractEnv is not None
assert callable(get_env_path) and callable(get_env_value)
'''
    result = subprocess.run(
        [sys.executable, '-c', code],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
