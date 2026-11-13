"""An arm's package joins a Core environment without replacing what Core was installed with."""
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import pytest

ADDONS = Path(__file__).resolve().parents[1] / 'src/hugpy_core/install/addons.py'
CLEAN = {'PATH': '/usr/bin:/bin'}      # no PYTHONPATH: the environments below hold only what is installed in them


def wheel(folder, name, version, requires=()):
    """A minimal installable wheel: one module and its metadata."""
    module = name.replace('-', '_')
    files = {f'{module}.py': f'VERSION = {version!r}\n',
             f'{module}-{version}.dist-info/METADATA':
                 f'Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n'
                 + ''.join(f'Requires-Dist: {item}\n' for item in requires),
             f'{module}-{version}.dist-info/WHEEL':
                 'Wheel-Version: 1.0\nGenerator: test\nRoot-Is-Purelib: true\nTag: py3-none-any\n'}
    record = ''.join(
        f"{path},sha256={base64.urlsafe_b64encode(hashlib.sha256(text.encode()).digest()).rstrip(b'=').decode()},"
        f"{len(text.encode())}\n" for path, text in files.items())
    files[f'{module}-{version}.dist-info/RECORD'] = record + f'{module}-{version}.dist-info/RECORD,,\n'
    folder.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(folder / f'{module}-{version}-py3-none-any.whl', 'w') as archive:
        for path, text in files.items():
            archive.writestr(path, text)


@pytest.fixture
def core(tmp_path):
    """A Core-shaped environment: hugpy-core and one sibling it was installed with."""
    venv = tmp_path / 'core-venv'
    subprocess.run([sys.executable, '-m', 'venv', str(venv)], check=True, env=CLEAN)
    python = venv / 'bin/python'
    base = tmp_path / 'core-wheels'
    wheel(base, 'hugpy-core', '1.0', ['hugpy-engine>=1.0', 'hugpy-media>=2.0; extra == "media"'])
    wheel(base, 'hugpy-engine', '1.0')
    subprocess.run([python, '-m', 'pip', 'install', '-q', '--no-index', '--find-links', str(base), 'hugpy-core'],
                   check=True, env=CLEAN, cwd=tmp_path)
    described = tmp_path / 'core-addons.d'
    described.mkdir()

    def addon(*args):
        return subprocess.run([python, str(ADDONS), *args, '--no-restart'], capture_output=True, text=True,
                              env={**CLEAN, 'HUGPY_CORE_ADDONS_DIR': str(described),
                                   'HUGPY_CORE_ENV_FILE': str(tmp_path / 'core.env')})

    def versions():
        out = subprocess.run([python, '-m', 'pip', 'list', '--format=json', '--disable-pip-version-check'],
                             capture_output=True, text=True, check=True, env=CLEAN, cwd=tmp_path).stdout
        return {row['name']: row['version'] for row in json.loads(out) if row['name'] != 'pip'}

    def describe(name, wheels, requirements):
        (described / f'{name}.json').write_text(json.dumps(
            {'addon': name, 'requirements': requirements, 'wheels': [str(wheels)],
             'verify': [requirements[0].replace('-', '_')]}))

    return addon, versions, describe, tmp_path


def test_an_arm_is_added_beside_core_and_removed_again(core):
    addon, versions, describe, tmp = core
    # the arm's own wheel directory carries a newer engine than Core has; Core's stays
    wheel(tmp / 'media', 'hugpy-media', '2.0', ['hugpy-engine>=1.0', 'media-helper'])
    wheel(tmp / 'media', 'media-helper', '0.5')
    wheel(tmp / 'media', 'hugpy-engine', '1.1')
    describe('media', tmp / 'media', ['hugpy-media'])

    result = addon('attach', 'media')
    assert result.returncode == 0, result.stderr
    assert versions() == {'hugpy-core': '1.0', 'hugpy-engine': '1.0', 'hugpy-media': '2.0', 'media-helper': '0.5'}

    # the arm's package is upgraded: its next attach lands the new version and the newer sibling
    # it bundles (which the old one would still have satisfied); what Core was installed with stays
    wheel(tmp / 'media', 'hugpy-media', '2.1', ['hugpy-engine>=1.0', 'media-helper'])
    wheel(tmp / 'media', 'media-helper', '0.6')
    assert addon('attach', 'media').returncode == 0
    assert versions() == {'hugpy-core': '1.0', 'hugpy-engine': '1.0', 'hugpy-media': '2.1', 'media-helper': '0.6'}

    assert addon('detach', 'media').returncode == 0
    assert versions() == {'hugpy-core': '1.0', 'hugpy-engine': '1.0'}


def test_an_arm_core_cannot_hold_is_refused_and_core_is_untouched(core):
    addon, versions, describe, tmp = core
    wheel(tmp / 'video', 'hugpy-video', '3.0', ['hugpy-engine>=2.0'])
    wheel(tmp / 'video', 'hugpy-engine', '2.0')
    describe('video', tmp / 'video', ['hugpy-video'])

    result = addon('attach', 'video')
    assert result.returncode == 3 and 'standalone' in result.stdout
    assert versions() == {'hugpy-core': '1.0', 'hugpy-engine': '1.0'}

    # and the operator's switch keeps an arm that would fit out of Core as well
    wheel(tmp / 'media', 'hugpy-media', '2.0', ['hugpy-engine>=1.0'])
    describe('media', tmp / 'media', ['hugpy-media'])
    (tmp / 'core.env').write_text('HUGPY_CORE_ADDONS=none\n')
    assert addon('sync').returncode == 0
    assert versions() == {'hugpy-core': '1.0', 'hugpy-engine': '1.0'}
