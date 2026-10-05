#!/usr/bin/env -S uv run --script

# /// script
# requires-python = '>=3.11'
# dependencies = []
# ///

"""Create this project's release tag locally.

flufl.bounce is a single package, so a release is one bare tag naming HEAD -- 5.1.0, say.  That is
what the whole tag history back to 0.90 looks like, and what the CI falls back to for a tag carrying
no distribution name, so nothing here ever writes a namespaced <distribution>@<version> tag.

The version comes from wherever hatch reads it -- a static [project] version, or the file named by
[tool.hatch.version] path -- so there is only ever one number to change:

    tools/tag.py              # tag HEAD with the current version
    tools/tag.py --dry-run    # say what would happen, and stop

Nothing is pushed.  The tag is created against HEAD and the git command to publish it is printed
for you to run, or not, yourself.
"""

import re
import sys
import tomllib
import subprocess

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path


SPACE = ' '

# A dynamic version is a __version__ assignment in the file named by [tool.hatch.version] path.
VERSION = re.compile(r"""^__version__\s*=\s*['"](?P<version>[^'"]+)['"]""", re.MULTILINE)


def git(*arguments: str) -> str:
    """Run a git command, returning its stripped stdout, or stop if git objected."""
    try:
        process = subprocess.run(['git', *arguments], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as error:
        command = SPACE.join(('git', *arguments))
        sys.exit(error.stderr.strip() or f'{command} failed')

    return process.stdout.strip()


def version(root: Path) -> str:
    """Return the version this project would release, read the way hatch reads it."""
    with open(root / 'pyproject.toml', 'rb') as pyproject_file:
        config = tomllib.load(pyproject_file)

    project = config['project']

    if (declared := project.get('version')) is not None:
        return declared

    path = root / config['tool']['hatch']['version']['path']
    found = VERSION.search(path.read_text(encoding='utf-8'))

    if found is None:
        sys.exit(f'{path}: no __version__ assignment found')

    return found['version']


def main() -> int:
    """Create the tag this project's declared version calls for."""
    parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument(
        '-n',
        '--dry-run',
        action='store_true',
        help='Show the tag that would be created, without creating it.',
    )
    options = parser.parse_args()

    # The root comes from git rather than from __file__, so the script works from any directory.
    root = Path(git('rev-parse', '--show-toplevel'))
    tag = version(root)
    head = git('rev-parse', 'HEAD')

    if git('tag', '--list', tag) == tag:
        at = git('rev-list', '-n1', tag)
        where = 'HEAD' if at == head else at[:10]
        sys.exit(f'Tag {tag} already exists at {where}.  Bump the version first.')

    # Tagging a dirty tree is legal but rarely intended; the tag names HEAD, so uncommitted work is
    # silently left out of the release.
    if git('status', '--porcelain', '--untracked-files=no') != '':
        print('WARNING: tracked files are modified; the tag will not include them.\n')

    if options.dry_run:
        print(f'Would tag HEAD ({head[:10]}) as {tag}.')
        return 0

    git('tag', tag, head)

    print(f'Tagged HEAD ({head[:10]}) as {tag}.  Nothing has been pushed.')
    print(f'To publish this release, run:\n    git push origin {tag}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
