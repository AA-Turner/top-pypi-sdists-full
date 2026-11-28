"""``upgrade``: replace the installed agilicus CLI with the latest release.

The package is published to the public index by the release pipeline (see
``py/.gitlab-ci.yml``), so the upgrade is a plain ``pip install --upgrade
agilicus``.  This mirrors ``devt upgrade``: a source checkout is left alone,
an already-current install is not touched, and only a run that actually
installs something reports an upgrade.
"""

import os
import re
import subprocess
import sys
import sysconfig

import click
import requests

#: Distribution name on the index.
DISTRIBUTION = "agilicus"

#: The public index's JSON API.  A user with a private mirror still gets a
#: working install: when this lookup fails the command falls through to pip,
#: which uses whatever index that environment has configured.
RELEASE_URL = f"https://pypi.org/pypi/{DISTRIBUTION}/json"

#: A release lookup that takes longer than this is not worth blocking an
#: upgrade that pip can attempt anyway.
TIMEOUT_SECONDS = 10


def installed_version():
    """Return the version pip has installed, or None if it cannot be read.

    Deliberately not ``agilicus.version``: a checkout on ``sys.path`` reports
    the version of the code being run, which is not what an upgrade replaces.
    """
    try:
        from importlib.metadata import version

        return version(DISTRIBUTION)
    except Exception:  # noqa: BLE001 - unreadable metadata must not fail
        return None


def running_from_checkout():
    """True when the package is being run from an unpacked source tree.

    Poetry's editable install points the interpreter at the working tree, so
    installing a released wheel over it would shadow the checkout.  A checkout
    is updated with git and ``poetry install`` instead.
    """
    package_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.exists(os.path.join(os.path.dirname(package_dir), "pyproject.toml"))


def release_key(version):
    """Return a comparable tuple for a plain ``X.Y.Z`` release, or None.

    Only the numeric release segment is needed to decide whether to install.
    Anything this cannot read (a pre-release, a local version) returns None so
    that the caller installs rather than risk skipping a real upgrade.
    """
    match = re.fullmatch(r"v?(\d+(?:\.\d+)*)", (version or "").strip())
    if not match:
        return None
    return tuple(int(part) for part in match.group(1).split("."))


def is_current(installed, latest):
    """True when *installed* is the same version as, or newer than, *latest*."""
    if not installed or not latest:
        return False
    if installed == latest:
        return True
    installed_key = release_key(installed)
    latest_key = release_key(latest)
    return (
        installed_key is not None
        and latest_key is not None
        and installed_key >= latest_key
    )


def latest_release(timeout=TIMEOUT_SECONDS):
    """Return the newest version published on the index."""
    response = requests.get(RELEASE_URL, timeout=timeout)
    response.raise_for_status()
    return response.json()["info"]["version"]


def in_virtualenv():
    """True when pip installs into a virtualenv rather than a system Python."""
    return sys.prefix != sys.base_prefix


def install_location_writable():
    """True when pip can write to the interpreter's default site-packages.

    Outside a virtualenv that location may be root-owned, which means the
    package was installed with ``--user``; upgrading it as the same user has
    to target the user site instead.
    """
    try:
        purelib = sysconfig.get_paths()["purelib"]
    except Exception:  # noqa: BLE001 - an unusual interpreter must not fail
        return False
    return os.access(purelib, os.W_OK)


def pip_upgrade_command():
    """Return the pip invocation that replaces the installed distribution."""
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "--disable-pip-version-check",
    ]
    if not in_virtualenv():
        # A system Python is often marked externally managed (PEP 668).  The
        # user asked for this upgrade explicitly, so opt in instead of failing
        # on the marker; inside a virtualenv the flag is unnecessary.
        command.append("--break-system-packages")
        if not install_location_writable():
            command.append("--user")
    command.append(DISTRIBUTION)
    return command


@click.command(name="upgrade")
def cli_command_upgrade():
    """Upgrade agilicus-cli to the latest release.

    Leaves a source checkout alone and does nothing when the installed
    version is already current.
    """
    if running_from_checkout():
        click.echo(
            "agilicus-cli is running from a checkout, so there is nothing to "
            "install; update it with git pull and poetry install",
            err=True,
        )
        return

    installed = installed_version()
    try:
        latest = latest_release()
    except Exception as exc:  # noqa: BLE001 - pip can still attempt the upgrade
        click.echo(
            f"warning: could not check the latest release ({exc}); "
            "asking pip to upgrade anyway",
            err=True,
        )
        latest = None

    if is_current(installed, latest):
        click.echo(f"agilicus-cli {installed} is already the latest release ({latest})")
        return

    try:
        subprocess.run(pip_upgrade_command(), check=True)
    except subprocess.CalledProcessError as exc:
        raise click.ClickException(
            f"pip could not upgrade {DISTRIBUTION} (exit code {exc.returncode})"
        )
    except OSError as exc:
        raise click.ClickException(f"could not run pip: {exc}")

    upgraded = installed_version()
    if upgraded and upgraded != installed:
        click.echo(f"Upgraded agilicus-cli {installed or 'unknown'} -> {upgraded}")
    elif upgraded:
        click.echo(
            f"agilicus-cli {upgraded} is already the newest release "
            "this Python can install"
        )
    else:
        click.echo("Upgrade finished; re-run `agilicus-cli version` to confirm.")


def add_commands(cli):
    cli.add_command(cli_command_upgrade)
