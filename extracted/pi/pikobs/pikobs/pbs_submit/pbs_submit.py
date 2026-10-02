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
import time
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


def _pip_can_install(pip_cmd: list, spec: str) -> bool:
    """Dry-run check: can pip resolve this version on the configured
    index right now?  Returns True if `pip index versions` lists it,
    or if `pip install --dry-run` succeeds.

    PyPI's JSON API publishes new versions a few seconds before the
    simple index, and corporate mirrors lag even more — so we must
    confirm before offering the upgrade."""
    # Try `pip index versions pikobs` (pip ≥21.2)
    try:
        r = subprocess.run(
            pip_cmd + ['index', 'versions', 'pikobs'],
            capture_output=True, text=True, timeout=15,
        )
        if r.returncode == 0:
            # Output: "Available versions: 3.0.127, 3.0.126, ..."
            target = spec.split('==', 1)[1] if '==' in spec else ''
            if target and target in r.stdout:
                return True
            if target and target not in r.stdout:
                return False
    except Exception:
        pass
    # Fallback: dry-run install (slower but works on older pip)
    try:
        r = subprocess.run(
            pip_cmd + ['install', '--dry-run', '--no-deps', spec],
            capture_output=True, text=True, timeout=30,
        )
        return r.returncode == 0
    except Exception:
        return False


def _check_version(project_dir: str) -> None:
    """Print version banner.  If a newer PyPI version exists, is reachable
    by the local pip index, and stdin is a TTY, prompt to upgrade."""
    try:
        import pikobs                                # noqa
        try:
            from importlib.metadata import version as _v
            local = _v('pikobs')
        except Exception:
            local = getattr(__import__('pikobs'), '__version__', 'installed')
    except ImportError:
        print("ERROR: cannot import pikobs.", file=sys.stderr)
        sys.exit(1)

    latest = ''
    try:
        import urllib.request, json
        with urllib.request.urlopen(
                'https://pypi.org/pypi/pikobs/json', timeout=10) as r:
            latest = json.loads(r.read())['info']['version']
    except Exception:
        pass

    suffix = f'  (latest on PyPI: {latest})' if latest and latest != local else ''
    print(f'Pikobs : {local}{suffix}')

    if not (latest and latest != local):
        return

    try:
        from packaging.version import Version
        if Version(local) >= Version(latest):
            print(f'  ℹ️  Dev build ({local} > PyPI {latest})')
            return
    except Exception:
        return

    # Build pip command early — we need it to verify availability
    _prefix = (os.environ.get('CONDA_PREFIX')
               or os.environ.get('VIRTUAL_ENV')
               or project_dir)
    pip_path = None
    if _prefix:
        cand = Path(_prefix) / 'bin' / 'pip'
        if cand.exists():
            pip_path = str(cand)
    pip_cmd = [pip_path] if pip_path else [sys.executable, '-m', 'pip']

    # GUARD: PyPI's JSON may have published the new version a few seconds
    # before it appears on the simple index (used by pip).  Corporate
    # mirrors can lag minutes.  If pip can't see it yet, don't offer
    # the upgrade — just tell the user.
    spec = f'pikobs=={latest}'
    if not _pip_can_install(pip_cmd, spec):
        print(f'  ⏳ {latest} is on PyPI metadata but not yet on your pip '
              f'index. Try again in a minute, or run:')
        print(f'        {" ".join(pip_cmd)} install --upgrade --no-deps {spec}')
        return

    if not sys.stdin.isatty():
        print(f'  ⚠️  PyPI has {latest} — run: pip install --upgrade pikobs')
        return

    ans = input(
        f'\n  ⚠️  A newer version is available: {latest}\n'
        f'  Installed: {local}\n'
        f'  Update now? [y/N] '
    ).strip().lower()
    if ans != 'y':
        return

    cur_loc = _pikobs_install_location()
    print(f'  → currently imported pikobs lives at: {cur_loc}')

    cmd = pip_cmd + [
        'install',
        '--upgrade', '--upgrade-strategy', 'only-if-needed',
        '--no-deps',
        spec,
    ]
    print(f"  ⏳ {' '.join(cmd)}")
    t0 = time.time()
    rc = subprocess.run(cmd).returncode
    print(f'  ⏱  pip finished in {time.time()-t0:.1f}s (rc={rc})')

    if rc != 0:
        print(f'  ❌ Upgrade failed. Continuing with {local}.')
        return

    installed = _read_installed_version_fresh()
    if installed != latest:
        print(f'  ❌ Upgrade reported success but on-disk version is '
              f'{installed or "unknown"} (expected {latest}).')
        print(f'     Manual fix:')
        print(f'       {" ".join(pip_cmd)} install --upgrade --no-deps '
              f'pikobs=={latest}')
        print(f'     Continuing with {local}.\n')
        return

    print(f'  ✅ Updated to {installed} — restarting with new version...\n')

    python_exe = sys.executable
    if not Path(python_exe).is_file():
        cand = Path(_prefix) / 'bin' / 'python' if _prefix else None
        if cand and cand.is_file():
            python_exe = str(cand)
        else:
            print(f'  ⚠️  Cannot re-exec (no Python binary). '
                  f'Please re-run your command manually.')
            sys.exit(0)

    # FIX: Retrieve the exact command (including the -c code) for the restart
    try:
        with open('/proc/self/cmdline', 'r') as f:
            full_cmd = f.read().split('\0')[:-1]
        real_args = full_cmd[1:] # Ignore the 'python' executable
    except Exception:
        real_args = sys.argv

    new_argv = [python_exe] + real_args
    
    # Import shlex just to print the command legibly in the log
    import shlex
    print(f'  → exec: {" ".join(shlex.quote(a) for a in new_argv)}')
    sys.stdout.flush()
    
    # Restart the process with the real arguments
    os.execv(python_exe, new_argv)

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
