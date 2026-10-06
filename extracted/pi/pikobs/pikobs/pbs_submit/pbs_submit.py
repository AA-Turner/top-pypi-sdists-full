"""
pikobs.pbs_submit
=================
Auto-submit helper for pikobs CLI commands.
"""
import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path


# ==============================================================================
# VERSION CHECK
# ==============================================================================
def _resolve_project_dir() -> str:
    project_dir = os.environ.get('PIKOBS_PROJECT_DIR', '')
    if not project_dir:
        try:
            import pikobs as _pk
            for _p in [Path(_pk.__file__).parent, *Path(_pk.__file__).parents]:
                if (_p / 'load_pikobs.sh').exists():
                    project_dir = str(_p)
                    break
        except Exception:
            pass
    if not project_dir:
        project_dir = os.environ.get('CONDA_PREFIX',
                      os.environ.get('VIRTUAL_ENV', ''))
    return project_dir


def _pikobs_install_location() -> str:
    try:
        import pikobs
        return str(Path(pikobs.__file__).parent)
    except Exception:
        return ''


def _read_installed_version_fresh() -> str:
    """Read pikobs version in a CLEAN subprocess to bypass the
    metadata cache of the current Python process.

    Key points:
      - DO NOT pass `-S` (it disables site-packages, so metadata is gone).
      - DO remove PYTHONPATH so an old source checkout doesn't shadow
        the freshly-installed wheel.
      - Print stderr too on failure so we can see what broke.
    """
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    # Multi-line script via real newlines — passing `;`-joined try/except
    # is a SyntaxError because `try:` needs its block on subsequent lines.
    code = (
        "import importlib.metadata as m\n"
        "import sys\n"
        "try:\n"
        "    print(m.version('pikobs'))\n"
        "except Exception as e:\n"
        "    sys.stderr.write('VERR:' + type(e).__name__ + ':' + str(e))\n"
        "    sys.exit(2)\n"
    )
    try:
        r = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True, text=True, env=env,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
        err = (r.stderr or '').strip()
        if err:
            print(f'  [verify] subprocess stderr: {err[:200]}')
        return ''
    except Exception as e:
        print(f'  [verify] subprocess crashed: {e}')
        return ''


def _check_version(project_dir: str) -> None:
    """Print the installed version, and say so when a newer one is published.

    The published versions are GitLab tags (release.sh: nothing goes to PyPI
    any more, where 3.0.476 stays): the same notice as load_pikobs, from the
    answer it keeps in <project>/.update_notice. No question to the network
    here, and never pip -- pikobs-update installs a version; pip from PyPI
    would put back an old one."""
    try:
        try:
            from importlib.metadata import version as _v
            local = _v('pikobs')
        except Exception:
            local = getattr(__import__('pikobs'), '__version__', 'installed')
    except ImportError:
        print("ERROR: cannot import pikobs.", file=sys.stderr)
        sys.exit(1)
    print(f'Pikobs : {local}')
    base = os.environ.get('PIKOBS_PROJECT_DIR') or project_dir or ''
    try:
        latest = (Path(base) / '.update_notice').read_text().split()[0]
        from packaging.version import Version
        if Version(latest) > Version(local):
            print(f'  Pikobs {latest} is published: run pikobs-update')
    except Exception:
        pass


# ==============================================================================
# PBS AUTO-SUBMIT (COMPUTE NODE CHECK)
# ==============================================================================
def maybe_submit_to_pbs(args) -> None:
    """If running on a login node (no PBS_JOBID), instruct the user to
    open an interactive session and exit. Otherwise, run locally."""

    in_compute_node = bool(os.environ.get('PBS_JOBID')
                           or os.environ.get('PBS_ENVIRONMENT'))

    if not in_compute_node:
        print("\n⚠️  WARNING: You are trying to run Pikobs on a Login Node.")
        print("   You must open an interactive session on a compute node before running this command.")
        print("   Suggested command:")
        print("   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0\n")
        print("❌ Execution cancelled. Please open the interactive session and run the command again.\n")
        sys.exit(1)

    # If we are already on a compute node (or interactive session), 
    # check the version and continue with the main script execution.
    _check_version(_resolve_project_dir())
    return
