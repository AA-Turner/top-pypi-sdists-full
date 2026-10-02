from __future__ import annotations

from pathlib import Path
import os
import shlex
import sys

from . import config
from .models import (
    CardioRequest,
    FlagsRequest,
    MapobsRequest,
    ObscountdbRequest,
    ScatterRequest,
    TimeserieRequest,
    ProfileRequest,
    VerifprofileRequest,
    VdedrRequest,
    ZoneRequest,
)


def _bootstrap(module: str) -> str:
    return f'''\
import builtins


def _pikobs_web_input(prompt=""):
    text = str(prompt)
    if text:
        print(text, flush=True)
    print(
        "[pikobs-web] Interactive prompt skipped in PBS; answered 'n'. "
        "If Pikobs reported a newer version, update later on a PPP7 login "
        "with: pikobs-update",
        flush=True,
    )
    return "n"


builtins.input = _pikobs_web_input
import pikobs
pikobs.{module}.arg_call()
'''.strip()


def _control_args(req) -> list[str]:
    args: list[str] = []
    if getattr(req, 'path_control_files', ''):
        args.extend(['--path_control_files', req.path_control_files])
        args.extend(['--control_name', req.control_name])
    return args


def _base_args(req, pathwork: Path) -> list[str]:
    return [
        '--path_experience_files', *req.path_experience_files,
        '--experience_name', *req.experience_name,
        '--pathwork', str(pathwork),
        '--datestart', req.datestart,
        '--dateend', req.dateend,
        '--region', *req.region,
        '--family', *req.family,
        '--flags_criteria', *req.flags_criteria,
    ]


def _flags_base_args(req: FlagsRequest, pathwork: Path) -> list[str]:
    return [
        '--path_experience_files', *req.path_experience_files,
        '--experience_name', *req.experience_name,
        '--pathwork', str(pathwork),
        '--datestart', req.datestart,
        '--dateend', req.dateend,
        '--region', *req.region,
        '--family', *req.family,
    ]


def _varnos(args: list[str], req) -> None:
    if getattr(req, 'varnos', None):
        args.extend(['--varnos', *[str(v) for v in req.varnos]])


def _vertical_layers(args: list[str], req) -> None:
    pressure = getattr(req, 'pressure_layers', None)
    height = getattr(req, 'height_layers', None)
    if pressure:
        args.extend(['--pressure_layers', *[str(v) for v in pressure]])
    if height:
        args.extend(['--height_layers', *[str(v) for v in height]])


def vdedr_module_args(req: VdedrRequest, pathwork: Path) -> list[str]:
    args = [
        *_control_args(req),
        *_base_args(req, pathwork),
        '--land_ocean', *req.land_ocean,
        '--special_column', req.special_column,
        '--id_stn', req.id_stn,
        '--match', req.match,
        '--svg', req.svg,
        '--n_cpus', str(req.n_cpus),
        '--no_submit',
    ]
    _varnos(args, req)
    return args


def cardio_module_args(req: CardioRequest, pathwork: Path) -> list[str]:
    args = [
        *_control_args(req),
        *_base_args(req, pathwork),
        '--land_ocean', *req.land_ocean,
        '--special_column', req.special_column,
        '--id_stn', *req.id_stn,
        '--channel', *req.channel,
        # Deliberately fixed: user asked to remove PLOT_TYPE from the web UI.
        '--plot_type', 'wide',
        '--match', req.match,
        '--svg', req.svg,
        '--n_cpus', str(req.n_cpus),
        '--no_submit',
    ]
    _varnos(args, req)
    return args


def scatter_module_args(req: ScatterRequest, pathwork: Path) -> list[str]:
    args = [
        *_control_args(req),
        *_base_args(req, pathwork),
        '--land_ocean', *req.land_ocean,
        '--fonction', *req.fonction,
        '--boxsizex', str(req.boxsizex),
        '--boxsizey', str(req.boxsizey),
        '--projection', *req.projection,
        '--pressure_layers', *[str(v) for v in req.pressure_layers],
        '--height_layers', *[str(v) for v in req.height_layers],
        '--id_stn', *req.id_stn,
        '--channel', *req.channel,
        '--Points', req.points,
        '--special_column', req.special_column,
        '--match', req.match,
        '--svg', req.svg,
        '--n_cpus', str(req.n_cpus),
        '--no_submit',
    ]
    _varnos(args, req)
    return args


def zone_module_args(req: ZoneRequest, pathwork: Path) -> list[str]:
    args = [
        *_control_args(req),
        *_base_args(req, pathwork),
        '--fonction', *req.fonction,
        '--boxsizey', str(req.boxsizey),
        '--land_ocean', *req.land_ocean,
        '--min_obs', str(req.min_obs),
        '--special_column', req.special_column,
        '--white_band', str(req.white_band),
        '--id_stn', *req.id_stn,
        '--channel', *req.channel,
        '--match', req.match,
        '--svg', req.svg,
        '--n_cpus', str(req.n_cpus),
        '--no_submit',
    ]
    _varnos(args, req)
    return args


def timeserie_module_args(req: TimeserieRequest, pathwork: Path) -> list[str]:
    args = [
        *_control_args(req),
        *_base_args(req, pathwork),
        '--id_stn', *req.id_stn,
        '--channel', *req.channel,
        '--land_ocean', *req.land_ocean,
        '--special_column', req.special_column,
        '--fonction', *req.fonction,
        '--match', req.match,
        '--alert_pct', str(req.alert_pct),
        '--svg', req.svg,
        '--n_cpus', str(req.n_cpus),
        '--no_submit',
    ]
    _vertical_layers(args, req)
    _varnos(args, req)
    return args


def mapobs_module_args(req: MapobsRequest, pathwork: Path) -> list[str]:
    args = [
        *_base_args(req, pathwork),
        # Region and projection are independent in the current MAPOBS UI/API.
        '--projection', *req.projection,
        '--land_ocean', *req.land_ocean,
        '--special_column', req.special_column,
        '--interval_min', str(req.interval_min),
        '--panels', *req.panels,
        '--id_stn', *req.id_stn,
        '--channel', *req.channel,
        '--svg', req.svg,
        '--dashboard_6h', req.dashboard_6h,
        '--n_cpus', str(req.n_cpus),
        '--no_submit',
    ]
    _varnos(args, req)
    return args


def obscountdb_module_args(req: ObscountdbRequest, pathwork: Path) -> list[str]:
    args = [
        *_control_args(req),
        *_base_args(req, pathwork),
        '--svg', req.svg,
        '--n_cpus', str(req.n_cpus),
        '--no_submit',
    ]
    if req.agr:
        args.extend(['--agr', *req.agr])
    return args


def flags_module_args(req: FlagsRequest, pathwork: Path) -> list[str]:
    args = [
        *_flags_base_args(req, pathwork),
        '--land_ocean', *req.land_ocean,
        '--special_column', req.special_column,
        '--id_stn', *req.id_stn,
        '--channel', *req.channel,
        '--svg', req.svg,
        '--n_cpus', str(req.n_cpus),
        '--no_submit',
    ]
    _vertical_layers(args, req)
    _varnos(args, req)
    return args


def profile_module_args(req: ProfileRequest, pathwork: Path) -> list[str]:
    args = [
        *_control_args(req),
        *_base_args(req, pathwork),
        '--land_ocean', *req.land_ocean,
        '--special_column', req.special_column,
        '--fonction', *req.fonction,
        '--min_obs', str(req.min_obs),
        '--obs_error_model', req.obs_error_model,
        '--fit_radar', req.fit_radar,
        '--fit_radar_target', req.fit_radar_target,
        '--error_curves', *req.error_curves,
        '--id_stn', *req.id_stn,
        '--match', req.match,
        '--svg', req.svg,
        '--n_cpus', str(req.n_cpus),
        '--no_submit',
    ]
    _varnos(args, req)
    return args


def verifprofile_module_args(req: VerifprofileRequest, pathwork: Path) -> list[str]:
    args = [
        *_control_args(req),
        *_base_args(req, pathwork),
        '--fonction', *req.fonction,
        '--land_ocean', *req.land_ocean,
        '--min_obs', str(req.min_obs),
        '--ratio_figure', req.ratio_figure,
        '--special_column', req.special_column,
        '--id_stn', *req.id_stn,
        '--match', req.match,
        '--svg', req.svg,
        '--n_cpus', str(req.n_cpus),
        '--no_submit',
    ]
    _varnos(args, req)
    return args


_BUILDERS = {
    'vdedr': vdedr_module_args,
    'cardio': cardio_module_args,
    'scatter': scatter_module_args,
    'zone': zone_module_args,
    'timeserie': timeserie_module_args,
    'mapobs': mapobs_module_args,
    'obscountdb': obscountdb_module_args,
    'flags': flags_module_args,
    'profile': profile_module_args,
    'verifprofile': verifprofile_module_args,
}


def module_args(module: str, req, pathwork: Path) -> list[str]:
    try:
        return _BUILDERS[module](req, pathwork)
    except KeyError as exc:  # pragma: no cover - protected by API validation
        raise ValueError(f'unknown Pikobs module: {module}') from exc


def module_argv(module: str, req, pathwork: Path, *, pbs: bool) -> list[str]:
    code = _bootstrap(module) if pbs else f'import pikobs; pikobs.{module}.arg_call()'
    return [sys.executable, '-u', '-c', code, *module_args(module, req, pathwork)]


def display_command(module: str, req, pathwork: Path) -> str:
    return shlex.join(module_argv(module, req, pathwork, pbs=False))


def _interactive_qsub(module: str, req) -> str:
    profile = config.PBS_PROFILES.get(module, config.PBS_PROFILES['default'])
    ncpus = int(profile.get('ncpus') or req.n_cpus)
    memory = str(profile.get('memory') or config.PBS_PROFILES['default']['memory'])
    walltime = str(profile.get('walltime') or config.PBS_PROFILES['default']['walltime'])
    select = f'select=1:ncpus={ncpus}:mem={memory}'
    place = str(profile.get('place') or '').strip()
    if place:
        select += f',place={place}'
    return f'qsub -I -l{select} -lwalltime={walltime}'


def interactive_script(module: str, req) -> str:
    """Exact hand-run equivalent for the current web selection."""
    raw = os.path.expandvars(os.path.expanduser(req.pathwork))
    pathwork = Path(raw)
    if not pathwork.is_absolute():
        pathwork = config.HOME / pathwork
    command = shlex.join([
        'python', '-u', '-c', f'import pikobs; pikobs.{module}.arg_call()',
        *module_args(module, req, pathwork),
    ])
    return (
        '# 1) From a PPP7 login node, open an interactive compute node:\n'
        f'{_interactive_qsub(module, req)}\n\n'
        '# 2) On the compute node, activate Pikobs and run this exact selection:\n'
        'source "$HOME/pikobs_install/load_pikobs.sh"\n'
        f'{command}\n'
    )


def render_job_script(
    destination: Path,
    module: str,
    req,
    pathwork: Path,
    log_path: Path,
) -> str:
    argv = module_argv(module, req, pathwork, pbs=True)
    command = shlex.join(argv)
    display = display_command(module, req, pathwork)

    text = f'''#!/usr/bin/env bash
set -eo pipefail

mkdir -p {shlex.quote(str(log_path.parent))}
exec >> {shlex.quote(str(log_path))} 2>&1
export PYTHONUNBUFFERED=1

# Web/PBS jobs are non-interactive and never modify the installed environment.
export PIKOBS_NONINTERACTIVE=1
export PIKOBS_AUTO_UPDATE=0

unset PIKOBS_ENV_PATH PIKOBS_PROJECT_DIR PYTHONPATH

# Use the exact Python interpreter of the installed Pikobs environment. This
# avoids depending on ordenv/r.load.dot/conda shell functions inside PBS.
PIKOBS_PYTHON={shlex.quote(sys.executable)}
PIKOBS_ENV_ROOT="$(cd "$(dirname "$PIKOBS_PYTHON")/.." && pwd)"
export PROJ_DATA="$PIKOBS_ENV_ROOT/share/proj"
export PROJ_LIB="$PIKOBS_ENV_ROOT/share/proj"

if ! "$PIKOBS_PYTHON" -c "import pikobs" >/dev/null 2>&1; then
    echo "ERROR: pikobs cannot be imported with $PIKOBS_PYTHON" >&2
    exit 1
fi

mkdir -p {shlex.quote(str(pathwork))}

echo "[pikobs-web] module: {module.upper()}"
echo "[pikobs-web] PATHWORK: {str(pathwork)}"
echo "[pikobs-web] PBS mode: Pikobs will NOT be updated inside this job."
echo "[pikobs-web] If a newer Pikobs version is announced, the prompt is answered 'n'."
echo "[pikobs-web] Update later from a PPP7 login with: pikobs-update"

{command}
'''
    destination.write_text(text)
    destination.chmod(0o750)
    return display


# Backward-compatible helper retained for older tests/imports.
def render_vdedr_job_script(destination: Path, req: VdedrRequest, pathwork: Path, log_path: Path) -> str:
    return render_job_script(destination, 'vdedr', req, pathwork, log_path)
