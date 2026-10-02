from __future__ import annotations

import os
import re
import shlex
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Dict, List

from . import config


STATE_NAMES = {
    'Q': 'QUEUED',
    'H': 'HELD',
    'R': 'RUNNING',
    'E': 'EXITING',
    'B': 'ARRAY_RUNNING',
    'S': 'SUSPENDED',
    'F': 'FINISHED',
    'C': 'COMPLETED',
}


@lru_cache(maxsize=8)
def _resolve_command(name: str) -> str:
    """Resolve PBS commands even when FastAPI was started by non-interactive SSH.

    ECCC's PBS commands are normally placed on PATH by the login environment
    (ordenv). A backend started by ``ssh host command`` can miss that PATH even
    though an interactive shell finds qstat/qsub. Try the current environment
    first, then ask a login bash to resolve the executable and cache the result.
    """
    direct = shutil.which(name)
    if direct:
        return direct

    cp = subprocess.run(
        ['/bin/bash', '-lc', f'command -v {shlex.quote(name)}'],
        text=True,
        capture_output=True,
        check=False,
        cwd=str(config.HOME),
    )
    if cp.returncode == 0:
        # Site profiles may print informational lines. Select the last absolute,
        # executable path rather than trusting stdout as a single clean line.
        for line in reversed(cp.stdout.splitlines()):
            candidate = line.strip()
            if candidate.startswith('/') and os.access(candidate, os.X_OK):
                return candidate

    return ''


def _run(args: List[str]) -> subprocess.CompletedProcess:
    """Run a command without ever raising FileNotFoundError to the API layer."""
    if not args:
        return subprocess.CompletedProcess(args, 127, '', 'empty command')

    executable = _resolve_command(args[0])
    if not executable:
        return subprocess.CompletedProcess(
            args,
            127,
            '',
            f'{args[0]} not found in the backend or login-shell environment',
        )

    resolved = [executable, *args[1:]]
    return subprocess.run(
        resolved,
        text=True,
        capture_output=True,
        check=False,
        # Never inherit Uvicorn's current directory. A shared application
        # directory can be replaced during an upgrade while the backend is
        # still alive, which would otherwise make getcwd() fail inside qsub.
        cwd=str(config.HOME),
    )



def scheduler_commands() -> Dict[str, str | bool]:
    qstat = _resolve_command('qstat')
    qsub = _resolve_command('qsub')
    return {
        'qstat': qstat,
        'qsub': qsub,
        'ready': bool(qstat and qsub),
    }

def submit_job(module: str, run_script: Path, pbs_log_path: Path, n_cpus: int) -> str:
    """Submit one independent Pikobs module job under the current Unix user.

    PBS resources are module profiles, intentionally separate from Pikobs'
    own --n_cpus setting. OBSCOUNTDB, for example, reserves a large exclusive
    node but still defaults to 80 Pikobs workers.
    """
    inner = f'PBS_O_WORKDIR= bash {shlex.quote(str(run_script))}'
    profile = config.PBS_PROFILES.get(module, config.PBS_PROFILES['default'])
    pbs_ncpus = int(profile.get('ncpus') or n_cpus)
    memory = str(profile.get('memory') or config.PBS_PROFILES['default']['memory'])
    walltime = str(profile.get('walltime') or config.PBS_PROFILES['default']['walltime'])
    resources = f'select=1:ncpus={pbs_ncpus}:mem={memory}'
    place = str(profile.get('place') or '').strip()
    if place:
        resources += f',place={place}'
    job_name = re.sub(r'[^A-Za-z0-9_.-]+', '_', module)[:15] or 'pikobs'
    args = [
        'qsub',
        '-N', job_name,
        '-l' + resources,
        '-lwalltime=' + walltime,
        '-j', 'oe',
        '-o', str(pbs_log_path),
        '--', '/bin/bash', '-lc', inner,
    ]
    cp = _run(args)
    if cp.returncode != 0:
        raise RuntimeError((cp.stderr or cp.stdout or 'qsub failed').strip())
    job_id = cp.stdout.strip().splitlines()[-1].strip()
    if not job_id:
        raise RuntimeError('qsub returned no job id')
    return job_id


def submit_vdedr(run_script: Path, pbs_log_path: Path, n_cpus: int) -> str:
    return submit_job('vdedr', run_script, pbs_log_path, n_cpus)


def _fold_and_parse_qstat(text: str) -> Dict[str, str]:
    """Parse `qstat -f` / history output into a simple attribute dictionary."""
    lines: List[str] = []
    for line in text.splitlines():
        # PBS continuation lines start with whitespace and contain no new
        # attribute assignment. Fold them into the previous line.
        if line[:1].isspace() and lines and ' = ' not in line:
            lines[-1] += line.strip()
        else:
            lines.append(line.rstrip())

    attrs: Dict[str, str] = {}
    for line in lines:
        m = re.match(r'^\s*([^=]+?)\s*=\s*(.*)$', line)
        if m:
            attrs[m.group(1).strip()] = m.group(2).strip()
    return attrs


def _classify_state(attrs: Dict[str, str]) -> str:
    raw = attrs.get('job_state', '')
    base = STATE_NAMES.get(raw, raw or 'UNKNOWN')

    # Finished jobs in PBS history normally appear as F. Turn that generic
    # state into something useful for the web UI by looking at Exit_status.
    if raw == 'F':
        exit_status = attrs.get('Exit_status', '').strip()
        comment = (attrs.get('comment', '') + ' ' + attrs.get('substate', '')).lower()

        if 'delete' in comment or 'cancel' in comment:
            return 'CANCELLED'

        if exit_status:
            try:
                return 'COMPLETED' if int(exit_status) == 0 else 'FAILED'
            except ValueError:
                pass
        return 'FINISHED'

    return base


def _qstat_output(job_id: str) -> tuple[str, bool]:
    """Return qstat output and whether it came from PBS job history.

    Active jobs are queried first. Once a job leaves the live queue, PBS Pro /
    OpenPBS commonly exposes it via `qstat -x -f` (or the compact `-xf`). We
    try both history spellings so the launcher works across site variants.
    """
    attempts = [
        (['qstat', '-f', job_id], False),
        (['qstat', '-x', '-f', job_id], True),
        (['qstat', '-xf', job_id], True),
    ]
    for args, history in attempts:
        cp = _run(args)
        if cp.returncode == 0 and cp.stdout.strip():
            return cp.stdout, history
    return '', False


def qstat_full(job_id: str) -> Dict[str, str | bool]:
    output, history = _qstat_output(job_id)
    if not output:
        return {
            'job_id': job_id,
            'state': 'NOT_IN_QUEUE',
            'raw_state': '',
            'node': '',
            'walltime': '',
            'exit_status': '',
            'comment': '',
            'history': False,
        }

    attrs = _fold_and_parse_qstat(output)
    raw = attrs.get('job_state', '')
    exec_host = attrs.get('exec_host', '') or attrs.get('exec_vnode', '')
    node = exec_host.split('/')[0].lstrip('(') if exec_host else ''

    return {
        'job_id': job_id,
        'state': _classify_state(attrs),
        'raw_state': raw,
        'node': node,
        'walltime': attrs.get('resources_used.walltime', ''),
        'exit_status': attrs.get('Exit_status', ''),
        'interactive': attrs.get('interactive', ''),
        'comment': attrs.get('comment', ''),
        'history': history,
    }


def user_job_ids(user: str) -> List[str]:
    cp = _run(['qstat', '-u', user])
    if cp.returncode != 0:
        return []

    ids: List[str] = []
    for line in cp.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith('Job') or set(line) <= {'-'}:
            continue
        first = line.split()[0]
        if re.match(r'^\d+(?:\.[A-Za-z0-9_.-]+)?$', first):
            ids.append(first)
    return ids


def interactive_jobs(user: str) -> List[Dict[str, str | bool]]:
    found = []
    for job_id in user_job_ids(user):
        info = qstat_full(job_id)
        if str(info.get('interactive', '')).lower() in {'true', '1', 'yes'}:
            found.append(info)
    return found
