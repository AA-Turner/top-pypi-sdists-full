from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import inspect
import json
import os
import re
import subprocess
import sys
import uuid
from urllib.parse import quote

from fastapi import Body, Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import config
from .command import interactive_script, render_job_script
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
from .pbs import interactive_jobs, qstat_full, scheduler_commands, submit_job
from .security import require_token

app = FastAPI(title='Pikobs Web')
app.mount('/static', StaticFiles(directory=Path(__file__).parent / 'static'), name='static')

_RUN_ID = re.compile(r'^[0-9]{8}T[0-9]{6}Z_[0-9a-f]{8}$')
_FLAG_NAME_RE = re.compile(r'(?:if|elif)\s+flags\s*==\s*[\'\"]([^\'\"]+)[\'\"]')

VIEWER_NAMES = {
    'vdedr': ['pikobs_vdedr_viewer.html'],
    'cardio': ['pikobs_cardio_viewer.html', 'pikobs_cardio_cont_exp_viewer.html', 'pikobs_cardio_exp_viewer.html'],
    'scatter': ['pikobs_scatter_viewer.html', 'pikobs_scatter_cont_exp_viewer.html', 'pikobs_scatter_exp_viewer.html'],
    'zone': ['pikobs_zone_viewer.html', 'pikobs_zone_cont_exp_viewer.html', 'pikobs_zone_exp_viewer.html'],
    'timeserie': ['pikobs_timeserie_viewer.html', 'pikobs_timeserie_cont_exp_viewer.html', 'pikobs_timeserie_exp_viewer.html'],
    'mapobs': ['pikobs_mapobs_viewer.html'],
    'obscountdb': ['pikobs_obscountdb_viewer.html'],
    'flags': ['pikobs_flags_viewer.html'],
    'profile': ['pikobs_profile_viewer.html', 'pikobs_profile_cont_exp_viewer.html', 'pikobs_profile_exp_viewer.html'],
    'verifprofile': ['pikobs_verifprofile_viewer.html', 'pikobs_verifprofile_cont_exp_viewer.html', 'pikobs_verifprofile_exp_viewer.html'],
}


FAMILY_HELP = (
    "Observation families to process. The menu is grouped by data-chain stage, from Postalt back to Dbase, "
    "and by instrument/type. Stage and instrument headings are informational only; select the family value itself. "
    "File suffixes are shown to help identify names used at each stage. The selectable values still come from the installed Pikobs."
)

FLAGS_HELP = """Select the observation population by Pikobs flag criterion. Available values are read from the installed Pikobs.

Standard
all — no flag restriction.
assimilee — BIT12 active: observation assimilated.
bgckalt — BIT9, BIT11 and BIT8 inactive.
bgckalt_qc — BIT9 and BIT11 inactive.
monitoring — BIT9 and BIT7 inactive.
postalt — BIT17, BIT9, BIT11 and BIT8 inactive.
qc — BIT9 inactive.
rejets_qc — BIT9 active.
rejets_bgck — BIT16 active.
bias_corr — BIT6 active.

Assimilated radiances / sky condition
assimilee_clear_sky — BIT12 active and BIT23 inactive.
assimilee_cloudy_sky — BIT12 and BIT23 active.
assimilee_clear_cloudy_sky — BIT12 active, clear + cloudy.
cloudy_rejected_qc — BIT9 + BIT23 active, BIT8 inactive.
cloudy_blacklisted — BIT9 + BIT23 + BIT8 active.
cloudy_thinning — BIT11 + BIT23 active, BIT8 inactive.
cloudy_thinning_blacklisted — BIT11 + BIT23 + BIT8 active.

Detailed rejection reasons
erroneous_data — BIT0, BIT2 or BIT7 active.
blacklisted — BIT8 active.
background_check_rogue — BIT9 + BIT16 active.
not_assimilated_daytime — BIT11 + BIT7 active.
land_sea_ice_sensitivity — BIT19 active.
model_top_sensitivity — BIT11 + BIT21 active.
rejected_overall_qc — BIT9 or BIT11 active.
topography_sensitivity — BIT9 + BIT18 active.
rejected_thinning — BIT11 active.
rejected_background_check — BIT9 active and BIT11 inactive."""

COMPARISON_HELP = (
    "Control vs Experience compares each experiment with a reference control. Where MATCH is supported, common observations can be compared observation by observation. "
    "Experience only processes each experiment independently; control-only comparison options are disabled and MATCH is sent as off."
)

MODULE_INTROS = {
    'vdedr': (
        'Verification of departures for a control and one or several experiments. '
        'Use the selections below to build the exact Pikobs run, then inspect the HTML viewer.'
    ),
    'cardio': (
        'Cardiogram time series for one or several experiments, optionally against a control. '
        'Regions and flag criteria are processed together and become selectors in the viewer.'
    ),
    'scatter': (
        'Spatial maps of observation statistics. A control is optional: with one, experiments are '
        'compared against it; without one, SCATTER draws the selected experiment statistics.'
    ),
    'zone': (
        'Zonal cross-sections: latitude against the vertical coordinate of each family. '
        'A control is optional and enables matched comparison and significance information.'
    ),
    'timeserie': (
        'Cycle-by-cycle availability and quality-control time series, including observation counts '
        'and available departure/error statistics. A control is optional.'
    ),
    'mapobs': (
        'Shows where observations are, with maps, profiles, cross-sections, vertical distributions '
        'and station contributions. Region and map projection are independent selections.'
    ),
    'obscountdb': (
        'Observation-volume report comparing one required control with one required experiment. '
        'Regions and flag criteria are processed in one pass and selectable in the HTML report.'
    ),
    'flags': (
        'Cycle-by-cycle view of what quality control did with each observation. '
        'There is no FLAGS_CRITERIA selection because this module shows every flag.'
    ),
    'profile': (
        'Vertical profiles of bias, sigma, assigned observation error and observation count, level by level. '
        'A control is optional and enables matched changes and significance tests.'
    ),
    'verifprofile': (
        'Vertical profiles of departures over a whole region: mean, sigma and observation count by level. '
        'A control is optional and enables matched level-by-level significance information.'
    ),
}


def _field(key: str, label: str, kind: str, help_text: str, **kwargs) -> dict:
    return {'key': key, 'label': label, 'kind': kind, 'help': help_text, **kwargs}


def _module_specs() -> dict[str, dict]:
    common_selection = [
        _field('family', 'Family', 'tokens', FAMILY_HELP, source='families', required=True),
        _field('region', 'Region', 'tokens', 'Geographic regions. Multiple regions are processed in one run and become viewer selections where supported.', source='regions', required=True),
        _field('flags_criteria', 'Flags criteria', 'tokens', FLAGS_HELP, source='flags', required=True),
    ]
    land = _field('land_ocean', 'Land / Ocean', 'tokens', 'all applies no surface filter; land and ocean use the land mask.', choices=config.ALLOWED_LAND_OCEAN, required=True)
    special = _field('special_column', 'SPECIAL_COLUMN', 'select', 'Family-specific extra dimension, for example wind method or radar elevation. off keeps values together.', choices=['off', 'on'])
    svg = _field('svg', 'SVG', 'select', 'Also write editable SVG figures next to PNG. The viewer continues to use PNG.', choices=config.ALLOWED_SVG)
    match = _field('match', 'MATCH', 'select', 'on matches observations before comparison; off keeps each run\'s observations independently.', choices=config.ALLOWED_MATCH, comparison_only=True)
    idstn = _field('id_stn', 'ID_STN', 'tokens', 'Station grouping: join merges stations, all makes one output per station; prefixes, exact =NAME and SQL-like C% patterns are accepted.', choices=['join', 'all'], allow_custom=True, required=True)
    channel = _field('channel', 'Channel / VCoord', 'tokens', 'Select the channel or vertical coordinate values used by the family. join merges them, all keeps them separate, or enter explicit values.', choices=['join', 'all'], allow_custom=True, required=True)
    varnos = _field('varnos', 'VARNOS', 'number_tokens', 'Optional varno list. Leave empty to use the family default.', required=False)

    return {
        'vdedr': {
            'control': 'required', 'experience': 'many', 'intro': MODULE_INTROS['vdedr'],
            'docs': config.MODULE_DOC_URLS['vdedr'], 'fields': [
                *common_selection, land, special,
                _field('id_stn', 'ID_STN', 'text', 'Station selection/grouping passed to VDEDR. all is the wrapper default.'),
                varnos, match, svg,
            ],
        },
        'cardio': {
            'control': 'optional_mode', 'comparison_help': COMPARISON_HELP, 'experience': 'many', 'intro': MODULE_INTROS['cardio'],
            'docs': config.MODULE_DOC_URLS['cardio'], 'fields': [
                *common_selection, land, special, idstn, channel, varnos, match, svg,
            ],
        },
        'scatter': {
            'control': 'optional_mode', 'comparison_help': COMPARISON_HELP, 'experience': 'many', 'intro': MODULE_INTROS['scatter'],
            'docs': config.MODULE_DOC_URLS['scatter'], 'fields': [
                _field('family', 'Family', 'tokens', FAMILY_HELP, source='families', required=True),
                _field('region', 'Region', 'tokens', 'Geographic regions. Multiple regions are processed in one run and become viewer selections where supported.', source='regions', required=True, group='scatter_map'),
                _field('projection', 'Projection', 'tokens', 'How the maps are drawn. This is independent from Region.', source='projections', required=True, group='scatter_map'),
                _field('flags_criteria', 'Flags criteria', 'tokens', FLAGS_HELP, source='flags', required=True),
                land,
                _field('fonction', 'FONCTION', 'tokens', 'Statistics/maps to generate. Comparison functions include O-P/O-A bias, sigma, counts, density and bias-correction changes.', choices=config.ALLOWED_SCATTER_FUNCTIONS, required=True),
                _field('boxsizex', 'BOXSIZEX', 'number', 'Longitude size of each spatial box, in degrees.', min=0.01, step='any', group='scatter_box'),
                _field('boxsizey', 'BOXSIZEY', 'number', 'Latitude size of each spatial box, in degrees.', min=0.01, step='any', group='scatter_box'),
                _field('channel', 'Channel / VCoord', 'tokens', 'Select the channel or vertical coordinate values used by the family. join merges them, all keeps them separate, or enter explicit values.', choices=['join', 'all'], allow_custom=True, required=True, group='vertical_selection'),
                _field('pressure_layers', 'PRESSURE_LAYERS', 'number_tokens', 'Optional pressure-layer boundaries in hPa for pressure-coordinate families.', group='vertical_selection'),
                _field('height_layers', 'HEIGHT_LAYERS', 'number_tokens', 'Optional height-layer boundaries in km for height-coordinate families.', group='vertical_selection'),
                idstn,
                _field('points', 'POINTS', 'select', 'ON prints the observation count in each map box; OFF keeps maps cleaner.', choices=config.ALLOWED_POINTS),
                special, varnos, match, svg,
            ],
        },
        'zone': {
            'control': 'optional_mode', 'comparison_help': COMPARISON_HELP, 'experience': 'many', 'intro': MODULE_INTROS['zone'],
            'docs': config.MODULE_DOC_URLS['zone'], 'fields': [
                *common_selection,
                _field('fonction', 'FONCTION', 'tokens', 'Departure to display: omp, oma or obs_error. One figure is produced for each selected value.', choices=config.ALLOWED_ZONE_FUNCTIONS, required=True),
                _field('boxsizey', 'BOXSIZEY', 'number', 'Latitude-band size in degrees.', min=0.01, step='any'),
                land,
                _field('min_obs', 'MIN_OBS', 'number', 'Cells with fewer observations are left empty in statistics panels; count panels still show them.', min=1, step=1),
                special,
                _field('white_band', 'WHITE_BAND', 'number', 'Comparison changes smaller than this value, in the variable units, are drawn white.', min=0, step='any', comparison_only=True),
                idstn, channel, varnos, match, svg,
            ],
        },
        'timeserie': {
            'control': 'optional_mode', 'comparison_help': COMPARISON_HELP, 'experience': 'many', 'intro': MODULE_INTROS['timeserie'],
            'docs': config.MODULE_DOC_URLS['timeserie'], 'fields': [
                *common_selection,
                _field('channel', 'Channel / VCoord', 'tokens', 'Select the channel or vertical coordinate values used by the family. join merges them, all keeps them separate, or enter explicit values.', choices=['join', 'all'], allow_custom=True, required=True, group='vertical_selection'),
                _field('pressure_layers', 'PRESSURE_LAYERS', 'number_tokens', 'Optional pressure-layer boundaries in hPa for pressure-coordinate families.', group='vertical_selection'),
                _field('height_layers', 'HEIGHT_LAYERS', 'number_tokens', 'Optional height-layer boundaries in km for height-coordinate families.', group='vertical_selection'),
                land, special,
                _field('fonction', 'FONCTION', 'tokens', 'Departure comparison to include: omp, oma, or both.', choices=config.ALLOWED_TIMESERIE_FUNCTIONS, required=True),
                _field('match', 'MATCH', 'select', 'off: each run uses all its observations; on: compare only common observations; all: viewer contains both views.', choices=config.ALLOWED_TIMESERIE_MATCH, comparison_only=True),
                _field('alert_pct', 'ALERT_PCT', 'number', '0 disables alerts. Otherwise cycles whose count falls by more than this percent below the median of the same UTC hour are flagged.', min=0, step='any'),
                idstn, varnos, svg,
            ],
        },
        'mapobs': {
            'control': 'none', 'experience': 'many', 'intro': MODULE_INTROS['mapobs'],
            'docs': config.MODULE_DOC_URLS['mapobs'], 'fields': [
                *common_selection,
                _field('projection', 'Projection', 'tokens', 'Map projection(s), independent from Region. Start typing to select from Pikobs projections.', source='projections', required=True),
                land, special, idstn, channel, varnos,
                _field('interval_min', 'INTERVAL_MIN', 'number', 'Sub-cycle length in minutes. 15 gives 24 slices per 6-hour cycle; 60 gives 6.', min=1, max=360, step=1),
                _field('panels', 'PANELS', 'tokens', 'Panels to draw: map, cross, vertical, stations, and/or all for the stacked dashboard.', choices=config.ALLOWED_MAPOBS_PANELS, required=True),
                svg,
                _field('dashboard_6h', 'DASHBOARD_6H', 'select', 'auto draws the 6-hour dashboard for four cycles or fewer; on always draws it; off disables it.', choices=config.ALLOWED_DASHBOARD_6H),
            ],
        },
        'obscountdb': {
            'control': 'required', 'experience': 'one', 'intro': MODULE_INTROS['obscountdb'],
            'docs': config.MODULE_DOC_URLS['obscountdb'], 'fields': [
                *common_selection,
                _field('agr', 'AGR', 'tokens', 'Optional departure panels in station time series: omp, oma, or both. Empty disables them and makes the run faster.', choices=config.ALLOWED_OBSCOUNT_AGR, required=False),
                svg,
            ],
        },
        'flags': {
            'control': 'none', 'experience': 'many', 'intro': MODULE_INTROS['flags'],
            'docs': config.MODULE_DOC_URLS['flags'], 'fields': [
                _field('family', 'Family', 'tokens', FAMILY_HELP, source='families', required=True),
                _field('region', 'Region', 'tokens', 'Geographic regions. Multiple regions are processed in one run and become viewer selections.', source='regions', required=True),
                land, special, idstn,
                _field('channel', 'Channel / VCoord', 'tokens', 'Select the channel or vertical coordinate values used by the family. join merges them, all keeps them separate, or enter explicit values.', choices=['join', 'all'], allow_custom=True, required=True, group='vertical_selection'),
                _field('pressure_layers', 'PRESSURE_LAYERS', 'number_tokens', 'Optional pressure-layer boundaries in hPa for pressure-coordinate families.', group='vertical_selection'),
                _field('height_layers', 'HEIGHT_LAYERS', 'number_tokens', 'Optional height-layer boundaries in km for height-coordinate families.', group='vertical_selection'),
                varnos, svg,
            ],
        },
        'profile': {
            'control': 'optional_mode', 'comparison_help': COMPARISON_HELP, 'experience': 'many', 'intro': MODULE_INTROS['profile'],
            'docs': config.MODULE_DOC_URLS['profile'], 'fields': [
                *common_selection, land, special,
                _field('fonction', 'FONCTION', 'tokens', 'Departure to profile: omp or oma. One figure is produced for each selected value.', choices=config.ALLOWED_PROFILE_FUNCTIONS, required=True),
                _field('min_obs', 'MIN_OBS', 'number', 'A level with fewer observations than this is dropped.', min=1, step=1),
                _field('obs_error_model', 'OBS_ERROR_MODEL', 'select', 'Radar only: show the current observation-error model from the calibration table.', choices=config.ALLOWED_OBS_ERROR_MODEL),
                _field('fit_radar', 'FIT_RADAR', 'select', 'Radar calibration option. Keep off for normal daily use.', choices=config.ALLOWED_FIT_RADAR),
                _field('fit_radar_target', 'FIT_RADAR_TARGET', 'select', 'Target used when FIT_RADAR is on: desroziers, sigma or sigma3.', choices=config.ALLOWED_FIT_RADAR_TARGET),
                _field('error_curves', 'ERROR_CURVES', 'tokens', 'Optional error curves beside OBS_ERROR. Suggested values: desroziers, model, model_fit.', choices=config.ALLOWED_ERROR_CURVES, allow_custom=True, required=False),
                idstn, varnos, match, svg,
            ],
        },
        'verifprofile': {
            'control': 'optional_mode', 'comparison_help': COMPARISON_HELP, 'experience': 'many', 'intro': MODULE_INTROS['verifprofile'],
            'docs': config.MODULE_DOC_URLS['verifprofile'], 'fields': [
                *common_selection,
                _field('fonction', 'FONCTION', 'tokens', 'Departure to profile: omp, oma or obs_error. One figure is produced for each selected value.', choices=config.ALLOWED_VERIFPROFILE_FUNCTIONS, required=True),
                land,
                _field('min_obs', 'MIN_OBS', 'number', 'A level with fewer observations than this is dropped because its sigma/test is not meaningful.', min=1, step=1),
                _field('ratio_figure', 'RATIO_FIGURE', 'select', 'With two or more experiences, on adds a figure with sigma_exp / sigma_ctl for all experiences.', choices=config.ALLOWED_RATIO_FIGURE, comparison_only=True),
                special, idstn, varnos, match, svg,
            ],
        },
    }


def _run_dir(run_id: str) -> Path:
    if not _RUN_ID.match(run_id):
        raise HTTPException(400, 'invalid run id')
    return config.RUNS_ROOT / run_id


def _read_meta(run_id: str) -> dict:
    path = _run_dir(run_id) / 'job.json'
    if not path.exists():
        raise HTTPException(404, 'run not found')
    return json.loads(path.read_text())


def _expand_path(value: str) -> Path:
    expanded = os.path.expandvars(os.path.expanduser(value.strip()))
    p = Path(expanded)
    if not p.is_absolute():
        p = config.HOME / p
    return p


def _default_period() -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    end_day = (now - timedelta(days=3)).date()
    start_day = (now - timedelta(days=8)).date()
    return start_day.strftime('%Y%m%d') + '00', end_day.strftime('%Y%m%d') + '18'


def _find_viewer(pathwork: Path, module: str) -> Path | None:
    for name in VIEWER_NAMES.get(module, []):
        candidate = pathwork / name
        if candidate.is_file():
            return candidate
    try:
        candidates = sorted(pathwork.glob('*viewer*.html'))
        if not candidates:
            candidates = []
            for item in pathwork.rglob('*viewer*.html'):
                candidates.append(item)
                if len(candidates) >= 30:
                    break
        module_hits = [p for p in candidates if module in p.name.lower()]
        if module_hits:
            return module_hits[0]
        if len(candidates) == 1:
            return candidates[0]
    except OSError:
        pass
    return None


def _direct_web_url(viewer_path: Path) -> str:
    bases = [config.HOME / 'sites8']
    try:
        bases.append((config.HOME / 'sites8').resolve(strict=False))
    except OSError:
        pass
    candidates = [viewer_path]
    try:
        candidates.append(viewer_path.resolve(strict=False))
    except OSError:
        pass
    for candidate in candidates:
        for base in bases:
            try:
                rel = candidate.relative_to(base)
            except ValueError:
                continue
            return f"{config.WEB_BASE}/{'/'.join(quote(part) for part in rel.parts)}"
    return ''


def _published_url(meta: dict, viewer_path: Path) -> str:
    request = meta.get('request') or {}
    if not request.get('publish'):
        return ''
    module = str(meta.get('module', 'pikobs'))
    run_id = str(meta.get('run_id', ''))
    if not _RUN_ID.match(run_id):
        return ''
    pathwork = Path(meta.get('pathwork', ''))
    try:
        rel_viewer = viewer_path.relative_to(pathwork)
    except ValueError:
        return ''
    public_dir = config.PUBLIC_ROOT / module
    public_dir.mkdir(parents=True, exist_ok=True)
    try:
        default_public_html = config.HOME / 'public_html'
        try:
            config.PUBLIC_ROOT.relative_to(default_public_html)
            default_public_html.chmod(0o755)
        except ValueError:
            pass
        config.PUBLIC_ROOT.chmod(0o755)
        public_dir.chmod(0o755)
    except OSError:
        pass
    link = public_dir / run_id
    try:
        if link.is_symlink():
            if link.resolve(strict=False) != pathwork.resolve(strict=False):
                return ''
        elif link.exists():
            return ''
        else:
            link.symlink_to(pathwork, target_is_directory=True)
    except OSError:
        return ''
    suffix = '/'.join(quote(part) for part in rel_viewer.parts)
    return f'{config.PUBLIC_URL_BASE}/{quote(module)}/{quote(run_id)}/{suffix}'


def _viewer_info(meta: dict) -> tuple[bool, str]:
    raw = meta.get('pathwork', '')
    if not raw:
        return False, ''
    module = str(meta.get('module', ''))
    viewer = _find_viewer(Path(raw), module)
    if viewer is None:
        return False, ''
    public = _published_url(meta, viewer)
    return True, public or _direct_web_url(viewer)


def _run_pbs(meta: dict) -> dict:
    if not meta.get('job_id'):
        return {'state': 'SUBMIT_FAILED'}
    pbs = qstat_full(meta['job_id'])
    viewer_ready, _ = _viewer_info(meta)
    if pbs.get('state') == 'NOT_IN_QUEUE':
        pbs = dict(pbs)
        pbs['state'] = 'COMPLETED' if viewer_ready else 'FINISHED_UNKNOWN'
    return pbs


def _official_regions() -> list[str]:
    try:
        from pikobs.configobs import regionsobs
        values = [str(x) for x in regionsobs.list_regions()]
        return sorted(dict.fromkeys(values))
    except Exception:
        return list(config.FALLBACK_REGIONS)


def _official_families() -> list[str]:
    try:
        from pikobs.configobs.families import families
        values = [str(x) for x in families()]
        return sorted(dict.fromkeys(values))
    except Exception:
        return list(config.FALLBACK_FAMILIES)


def _official_flags() -> list[str]:
    try:
        from pikobs.configobs.flags_criteria import flag_criteria
        src = inspect.getsource(flag_criteria)
        names = _FLAG_NAME_RE.findall(src)
        if names:
            return list(dict.fromkeys(names))
    except Exception:
        pass
    return list(config.FALLBACK_FLAGS_CRITERIA)


def _official_projections() -> list[str]:
    try:
        import importlib
        projection_module = importlib.import_module('pikobs.configobs.type_projection')
        rows = getattr(projection_module, '_projection_rows', None)
        if callable(rows):
            values = [str(row[0]).lower() for row in rows() if row and str(row[0]).upper() != 'PROJECTION']
            if values:
                return list(dict.fromkeys(values))
        doc = getattr(projection_module, '__doc__', '') or ''
        names = re.findall(r'\* - ``([A-Za-z0-9_]+)``', doc)
        values = [x.lower() for x in names if x.upper() != 'PROJECTION']
        if values:
            return list(dict.fromkeys(values))
    except Exception:
        pass
    return list(config.FALLBACK_PROJECTIONS)


def _live_pikobs_options() -> dict:
    """Read choices from the Pikobs installed in the current environment.

    The probe runs in a fresh interpreter so a ``pikobs-update`` is visible
    immediately, even when the FastAPI server itself has been running for a
    long time.
    """
    probe = Path(__file__).with_name('options_probe.py')
    try:
        proc = subprocess.run(
            [sys.executable, str(probe)],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        if proc.returncode == 0:
            data = json.loads(proc.stdout.strip() or '{}')
            if isinstance(data, dict):
                data['source'] = 'installed_pikobs'
                data['python'] = sys.executable
                return data
        error = (proc.stderr or proc.stdout or '').strip()[-1200:]
    except Exception as exc:
        error = str(exc)

    return {
        'families': _official_families(),
        'family_catalog': {'stage_order': [], 'stages': [], 'extras': []},
        'regions': _official_regions(),
        'flags_criteria': _official_flags(),
        'projections': _official_projections(),
        'pikobs_version': '',
        'pikobs_path': '',
        'python': sys.executable,
        'source': 'fallback',
        'warning': error,
    }


def _validate_flag(name: str) -> None:
    try:
        from pikobs.configobs.flags_criteria import flag_criteria
    except Exception:
        if name not in config.FALLBACK_FLAGS_CRITERIA:
            raise HTTPException(400, f'unsupported flags_criteria: {name}')
        return
    try:
        flag_criteria(name)
    except Exception as exc:
        raise HTTPException(400, f'unsupported flags_criteria: {name}') from exc


def _read_json(path: Path, default):
    try:
        if path.is_file():
            return json.loads(path.read_text())
    except Exception:
        pass
    return default


def _write_private_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.parent.chmod(0o700)
    except OSError:
        pass
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True))
    tmp.chmod(0o600)
    os.replace(tmp, path)


def _preferences() -> dict:
    data = _read_json(config.PREFERENCES_FILE, {})
    if not isinstance(data, dict):
        data = {}
    module_ids = [item['id'] for item in config.MODULES]
    for item in config.MODULES:
        data.setdefault(f"last_{item['id']}", {})
    hist = data.get('path_history')
    if not isinstance(hist, dict):
        hist = {}
        data['path_history'] = hist
    for key in ('control', 'experience', 'pathwork', 'project'):
        if not isinstance(hist.get(key), list):
            hist[key] = []
    data.setdefault('last_pathwork', '')

    ui = data.get('ui')
    if not isinstance(ui, dict):
        ui = {}
        data['ui'] = ui
    order = ui.get('tab_order', [])
    if not isinstance(order, list):
        order = []
    clean_order = []
    for raw in order:
        module = str(raw)
        if module in module_ids and module not in clean_order:
            clean_order.append(module)
    ui['tab_order'] = clean_order
    if ui.get('last_tab') not in module_ids:
        ui['last_tab'] = ''
    sort = ui.get('history_sort')
    allowed_sort = {'created_utc', 'module', 'project_label', 'control', 'experience', 'families', 'period', 'status'}
    if not isinstance(sort, dict) or sort.get('key') not in allowed_sort or sort.get('dir') not in {'asc', 'desc'}:
        ui['history_sort'] = {'key': 'created_utc', 'dir': 'desc'}
    widths = ui.get('history_column_widths')
    allowed_widths = {'launched', 'module', 'project', 'control', 'experience', 'families', 'period', 'status', 'actions'}
    clean_widths = {}
    if isinstance(widths, dict):
        for key, value in widths.items():
            if key not in allowed_widths:
                continue
            try:
                width = int(value)
            except (TypeError, ValueError):
                continue
            if 70 <= width <= 1200:
                clean_widths[key] = width
    ui['history_column_widths'] = clean_widths
    return data


def _remember(module: str, req) -> None:
    prefs = _preferences()
    last = req.model_dump()
    last.pop('datestart', None)
    last.pop('dateend', None)
    prefs[f'last_{module}'] = last
    # WORK PATH is remembered globally: the most recently submitted path is
    # offered in every module the next time Pikobs Web is opened.
    prefs['last_pathwork'] = str(req.pathwork).strip()
    hist = prefs.setdefault('path_history', {'control': [], 'experience': [], 'pathwork': [], 'project': []})

    def add(kind: str, values) -> None:
        current = [str(x) for x in hist.get(kind, []) if str(x).strip()]
        incoming = values if isinstance(values, list) else [values]
        for raw in reversed(incoming):
            v = str(raw).strip()
            if not v:
                continue
            current = [x for x in current if x != v]
            current.insert(0, v)
        hist[kind] = current[:30]

    add('control', getattr(req, 'path_control_files', ''))
    add('experience', req.path_experience_files)
    add('pathwork', req.pathwork)
    add('project', getattr(req, 'project_label', ''))
    _write_private_json(config.PREFERENCES_FILE, prefs)


def _merge_remembered(module: str, base: dict) -> dict:
    prefs = _preferences()
    remembered = prefs.get(f'last_{module}', {})
    if isinstance(remembered, dict):
        for key, value in remembered.items():
            if key in base and key not in {'datestart', 'dateend', 'pathwork'}:
                base[key] = value

    # PATHWORK is intentionally global rather than per-module. On a fresh
    # account the exact default is /fs/site8/eccc/. After the first submitted
    # run, every module starts from the most recently used WORK PATH.
    last_pathwork = str(prefs.get('last_pathwork', '')).strip()
    base['pathwork'] = last_pathwork or config.DEFAULT_PATHWORK
    base['datestart'], base['dateend'] = _default_period()
    return base


def _base_default(module: str, pathwork_name: str, families: list[str], regions: list[str], flags: list[str]) -> dict:
    start, end = _default_period()
    return {
        'path_experience_files': ['/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt'],
        'experience_name': ['experience'],
        'pathwork': config.DEFAULT_PATHWORK,
        'datestart': start, 'dateend': end,
        'family': families, 'region': regions, 'flags_criteria': flags,
        'n_cpus': 80, 'publish': False, 'project_label': '',
    }


def _defaults() -> dict[str, dict]:
    ctl = '/home/smco500/.suites/gdps/g0/hub/ppp7/monitoring/banco/postalt'
    common_regions = ['Monde', 'HemisphereNord', 'HemisphereSud', 'Tropiques', 'Canada']
    out: dict[str, dict] = {}

    out['vdedr'] = _base_default('vdedr', 'pikobs_vdedr_cont_exp', ['to_amsua_allsky', 'atms_allsky', 'iasi', 'cris'], common_regions, ['assimilee']) | {
        'path_control_files': ctl, 'control_name': 'control', 'land_ocean': ['all'], 'special_column': 'off',
        'id_stn': 'all', 'varnos': [], 'match': 'on', 'svg': 'off',
    }
    out['cardio'] = _base_default('cardio', 'pikobs_cardio_cont_exp', ['ai', 'sw', 'ua', 'to_amsua_allsky', 'iasi', 'cris'], common_regions, ['assimilee']) | {
        'path_control_files': ctl, 'control_name': 'control', 'land_ocean': ['all'], 'special_column': 'off',
        'id_stn': ['join', 'all'], 'channel': ['join'], 'varnos': [], 'match': 'on', 'svg': 'off',
    }
    out['scatter'] = _base_default('scatter', 'pikobs_scatter_cont_exp', ['iasi'], ['Monde'], ['all', 'assimilee']) | {
        'path_control_files': ctl, 'control_name': 'control', 'land_ocean': ['all'],
        'fonction': list(config.ALLOWED_SCATTER_FUNCTIONS), 'boxsizex': 2, 'boxsizey': 2, 'projection': ['cyl'],
        'pressure_layers': [1100, 850, 500, 250, 100, 10, 1, 0], 'height_layers': [0, 5, 10, 20, 30, 40, 60, 100],
        'id_stn': ['all'], 'channel': ['join'], 'points': 'OFF', 'special_column': 'off', 'varnos': [],
        'match': 'on', 'svg': 'off',
    }
    out['zone'] = _base_default('zone', 'pikobs_zone_cont_exp', ['sw', 'ua', 'ai', 'to_amsua_allsky', 'iasi'], common_regions, ['assimilee']) | {
        'path_control_files': ctl, 'control_name': 'control', 'fonction': ['omp'], 'boxsizey': 2, 'land_ocean': ['all'],
        'min_obs': 5, 'special_column': 'off', 'white_band': 0.1, 'id_stn': ['join', 'all'], 'channel': ['all'],
        'varnos': [], 'match': 'on', 'svg': 'off',
    }
    out['timeserie'] = _base_default('timeserie', 'pikobs_timeserie_cont_exp', ['sw', 'ua', 'ai'], common_regions, ['assimilee']) | {
        'path_control_files': ctl, 'control_name': 'control', 'channel': ['join'], 'pressure_layers': [], 'height_layers': [],
        'land_ocean': ['all'], 'special_column': 'off',
        'fonction': ['omp'], 'match': 'on', 'alert_pct': 0, 'id_stn': ['join', 'all'], 'varnos': [], 'svg': 'off',
    }
    out['mapobs'] = _base_default('mapobs', 'pikobs_mapobs', ['sw', 'ro'], ['Monde'], ['assimilee']) | {
        'projection': ['cyl', 'npolar'], 'land_ocean': ['all'], 'special_column': 'off', 'id_stn': ['join'], 'channel': ['join'],
        'varnos': [], 'interval_min': 15, 'panels': ['map', 'cross', 'vertical', 'stations', 'all'], 'svg': 'off', 'dashboard_6h': 'auto',
    }
    out['obscountdb'] = _base_default('obscountdb', 'pikobs_obscountdb_cont_exp', ['ai', 'sw', 'sf', 'ua', 'to_amsua_allsky', 'iasi', 'cris', 'atms'], common_regions, ['assimilee', 'rejets_qc']) | {
        'path_control_files': ctl, 'control_name': 'Control', 'experience_name': ['Experience'], 'agr': ['oma', 'omp'], 'svg': 'off',
    }
    out['flags'] = _base_default('flags', 'pikobs_flags', ['to_amsua_allsky', 'atms_allsky', 'mwhs2', 'ssmis', 'iasi', 'cris', 'csr'], common_regions, ['assimilee']) | {
        'land_ocean': ['all'], 'special_column': 'off', 'id_stn': ['join', 'all'], 'channel': ['join'],
        'pressure_layers': [], 'height_layers': [], 'varnos': [], 'svg': 'off',
    }
    out['flags'].pop('flags_criteria', None)
    out['profile'] = _base_default('profile', 'pikobs_profile_cont_exp', ['ua', 'ai'], common_regions, ['assimilee']) | {
        'path_control_files': ctl, 'control_name': 'control', 'land_ocean': ['all'], 'special_column': 'off',
        'fonction': ['omp'], 'min_obs': 30, 'obs_error_model': 'off', 'fit_radar': 'off', 'fit_radar_target': 'desroziers',
        'error_curves': [], 'id_stn': ['join'], 'varnos': [], 'match': 'on', 'svg': 'off',
    }
    out['verifprofile'] = _base_default('verifprofile', 'pikobs_verifprofile_cont_exp', ['sw', 'ua', 'ai', 'to_amsua_allsky', 'iasi'], common_regions, ['assimilee']) | {
        'path_control_files': ctl, 'control_name': 'control', 'fonction': ['omp'], 'land_ocean': ['all'], 'min_obs': 30,
        'ratio_figure': 'off', 'special_column': 'off', 'id_stn': ['join', 'all'], 'varnos': [], 'match': 'on', 'svg': 'off',
    }
    return {module: _merge_remembered(module, value) for module, value in out.items()}


def _hidden_runs() -> set[str]:
    data = _read_json(config.HIDDEN_RUNS_FILE, [])
    if not isinstance(data, list):
        return set()
    return {str(x) for x in data if _RUN_ID.match(str(x))}


def _save_hidden_runs(items: set[str]) -> None:
    _write_private_json(config.HIDDEN_RUNS_FILE, sorted(items))


def _is_final_state(state: str) -> bool:
    return str(state).upper() in {'COMPLETED', 'FAILED', 'CANCELLED', 'FINISHED_UNKNOWN', 'SUBMIT_FAILED'}


def _validate_common(req) -> dict:
    options = _live_pikobs_options()
    families = set(options.get('families') or config.FALLBACK_FAMILIES)
    regions = set(options.get('regions') or config.FALLBACK_REGIONS)
    flags = set(options.get('flags_criteria') or config.FALLBACK_FLAGS_CRITERIA)
    bad = [x for x in req.family if x not in families]
    if bad:
        raise HTTPException(400, f'unsupported family: {bad}')
    bad = [x for x in req.region if x not in regions]
    if bad:
        raise HTTPException(400, f'unsupported region: {bad}')
    bad = [x for x in getattr(req, 'flags_criteria', []) if x not in flags]
    if bad:
        raise HTTPException(400, f'unsupported flags_criteria: {bad}')
    return options


def _validate_land(req) -> None:
    bad = [x for x in req.land_ocean if x not in config.ALLOWED_LAND_OCEAN]
    if bad:
        raise HTTPException(400, f'unsupported land_ocean: {bad}')


def _validate_projection(req, options: dict | None = None) -> None:
    values = (options or {}).get('projections') if options else None
    known = {x.lower() for x in (values or config.FALLBACK_PROJECTIONS)}
    bad = [x for x in req.projection if x.lower() not in known]
    if bad:
        raise HTTPException(400, f'unsupported projection: {bad}')


def _validate_module(module: str, req) -> None:
    live_options = _validate_common(req)
    if hasattr(req, 'land_ocean'):
        _validate_land(req)
    if hasattr(req, 'svg') and req.svg not in config.ALLOWED_SVG:
        raise HTTPException(400, 'svg must be on/off')
    if module in {'vdedr', 'cardio', 'scatter', 'zone', 'profile', 'verifprofile'} and req.match not in config.ALLOWED_MATCH:
        raise HTTPException(400, 'match must be on/off')
    if module == 'timeserie' and req.match not in config.ALLOWED_TIMESERIE_MATCH:
        raise HTTPException(400, f'match must be one of {config.ALLOWED_TIMESERIE_MATCH}')
    if module in {'scatter', 'mapobs'}:
        _validate_projection(req, live_options)
    if module == 'scatter':
        if any(x not in config.ALLOWED_SCATTER_FUNCTIONS for x in req.fonction):
            raise HTTPException(400, 'unsupported SCATTER function')
        if req.points not in config.ALLOWED_POINTS:
            raise HTTPException(400, 'POINTS must be ON/OFF')
    if module == 'zone' and any(x not in config.ALLOWED_ZONE_FUNCTIONS for x in req.fonction):
        raise HTTPException(400, 'unsupported ZONE function')
    if module == 'timeserie' and any(x not in config.ALLOWED_TIMESERIE_FUNCTIONS for x in req.fonction):
        raise HTTPException(400, 'unsupported TIMESERIE function')
    if module == 'mapobs':
        if any(x not in config.ALLOWED_MAPOBS_PANELS for x in req.panels):
            raise HTTPException(400, 'unsupported MAPOBS panel')
        if req.dashboard_6h not in config.ALLOWED_DASHBOARD_6H:
            raise HTTPException(400, 'DASHBOARD_6H must be auto/on/off')
    if module == 'obscountdb' and any(x not in config.ALLOWED_OBSCOUNT_AGR for x in req.agr):
        raise HTTPException(400, 'AGR must contain only omp/oma')
    if module == 'profile':
        if any(x not in config.ALLOWED_PROFILE_FUNCTIONS for x in req.fonction):
            raise HTTPException(400, 'unsupported PROFILE function')
        if req.obs_error_model not in config.ALLOWED_OBS_ERROR_MODEL:
            raise HTTPException(400, 'OBS_ERROR_MODEL must be on/off')
        if req.fit_radar not in config.ALLOWED_FIT_RADAR:
            raise HTTPException(400, 'FIT_RADAR must be on/off')
        if req.fit_radar_target not in config.ALLOWED_FIT_RADAR_TARGET:
            raise HTTPException(400, 'unsupported FIT_RADAR_TARGET')
    if module == 'verifprofile':
        if any(x not in config.ALLOWED_VERIFPROFILE_FUNCTIONS for x in req.fonction):
            raise HTTPException(400, 'unsupported VERIFPROFILE function')
        if req.ratio_figure not in config.ALLOWED_RATIO_FIGURE:
            raise HTTPException(400, 'RATIO_FIGURE must be on/off')


def _active_pathwork_conflict(pathwork: Path) -> dict | None:
    """Block concurrent writes to the same exact PATHWORK, across all modules."""
    target = pathwork.resolve(strict=False)
    if not config.RUNS_ROOT.exists():
        return None
    for d in config.RUNS_ROOT.iterdir():
        meta_path = d / 'job.json'
        if not d.is_dir() or not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text())
            raw = meta.get('pathwork')
            if not raw or Path(str(raw)).resolve(strict=False) != target:
                continue
            state = str(_run_pbs(meta).get('state', '')).upper()
            if not _is_final_state(state):
                return {
                    'run_id': meta.get('run_id', d.name), 'module': meta.get('module', ''),
                    'job_id': meta.get('job_id', ''), 'state': state or 'UNKNOWN',
                }
        except Exception:
            continue
    return None


def _create_job(module: str, req):
    active_interactive = interactive_jobs(config.USER)
    if active_interactive:
        raise HTTPException(409, detail={
            'message': 'Interactive PBS compute session detected; close it before submitting a batch job.',
            'jobs': active_interactive,
        })
    _validate_module(module, req)

    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + uuid.uuid4().hex[:8]
    run_dir = config.RUNS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    try:
        run_dir.chmod(0o700)
    except OSError:
        pass

    pathwork = _expand_path(req.pathwork)
    if pathwork.exists() and not pathwork.is_dir():
        raise HTTPException(400, f'WORK PATH exists but is not a directory: {pathwork}')
    conflict = _active_pathwork_conflict(pathwork)
    if conflict:
        raise HTTPException(409, detail={
            'message': (
                f"WORK PATH is already in use by active {str(conflict['module']).upper()} run "
                f"{conflict['run_id']} ({conflict['state']}). Choose another WORK PATH or wait for it to finish."
            ),
            'conflict': conflict,
        })
    pathwork.mkdir(parents=True, exist_ok=True)

    run_script = run_dir / f'run_{module}_direct.sh'
    log_path = run_dir / f'{module}_job.log'
    pbs_log_path = run_dir / 'pbs_spool.log'
    log_path.write_text('[pikobs-web] waiting for PBS job to start...\n')
    command = render_job_script(run_script, module, req, pathwork, log_path)

    meta = {
        'run_id': run_id, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'user': config.USER, 'host': config.HOST, 'module': module,
        'run_script': str(run_script), 'command': command, 'log': str(log_path),
        'pbs_log': str(pbs_log_path), 'pathwork': str(pathwork), 'request': req.model_dump(),
    }
    try:
        job_id = submit_job(module, run_script, pbs_log_path, req.n_cpus)
    except Exception as exc:
        meta['submit_error'] = str(exc)
        (run_dir / 'job.json').write_text(json.dumps(meta, indent=2))
        raise HTTPException(500, str(exc))

    meta['job_id'] = job_id
    with log_path.open('a') as fh:
        fh.write(f'[pikobs-web] submitted PBS job: {job_id}\n')
        if req.publish:
            fh.write('[pikobs-web] public viewer requested; the link will appear when viewer HTML is ready.\n')
    (run_dir / 'job.json').write_text(json.dumps(meta, indent=2))
    _remember(module, req)
    viewer_ready, viewer_url = _viewer_info(meta)
    return {**meta, 'viewer_ready': viewer_ready, 'viewer_url': viewer_url, 'pbs': _run_pbs(meta)}


def _interactive(module: str, req):
    _validate_module(module, req)
    return {'command': interactive_script(module, req)}


@app.on_event('startup')
def startup() -> None:
    config.RUNS_ROOT.mkdir(parents=True, exist_ok=True)
    config.STATE_ROOT.mkdir(parents=True, exist_ok=True)
    for p in (config.RUNS_ROOT, config.STATE_ROOT):
        try:
            p.chmod(0o700)
        except OSError:
            pass


@app.get('/')
def index():
    return FileResponse(Path(__file__).parent / 'static/index.html', headers={'Cache-Control': 'no-store'})


@app.get('/api/health', dependencies=[Depends(require_token)])
def get_health():
    # Lightweight readiness endpoint. Do not probe the installed Pikobs here:
    # /api/config may start a fresh interpreter to discover live options.
    return {
        'ok': True,
        'families': [],
        'session': {'version': config.APP_VERSION},
    }


@app.get('/api/config', dependencies=[Depends(require_token)])
def get_config():
    options = _live_pikobs_options()
    return {
        'session': {
            'user': config.USER, 'host': config.HOST, 'version': config.APP_VERSION,
            'port': config.PORT, 'runs_root': str(config.RUNS_ROOT), 'viewer_base': config.WEB_BASE,
            'public_root': str(config.PUBLIC_ROOT), 'public_url_base': config.PUBLIC_URL_BASE,
        },
        'scheduler': scheduler_commands(), 'modules': config.MODULES,
        'families': options.get('families') or config.FALLBACK_FAMILIES,
        'family_catalog': options.get('family_catalog') or {'stage_order': [], 'stages': [], 'extras': []},
        'regions': options.get('regions') or config.FALLBACK_REGIONS,
        'flags_criteria': options.get('flags_criteria') or config.FALLBACK_FLAGS_CRITERIA,
        'projections': options.get('projections') or config.FALLBACK_PROJECTIONS,
        'options_meta': {k: options.get(k, '') for k in ('source', 'pikobs_version', 'pikobs_path', 'python', 'warning')},
        'docs': {
            'regions': config.REGIONS_DOC_URL, 'families': config.FAMILIES_DOC_URL,
            'flags_criteria': config.FLAGS_CRITERIA_DOC_URL, 'projections': config.PROJECTIONS_DOC_URL,
            **config.MODULE_DOC_URLS,
        },
        'module_specs': _module_specs(), 'defaults': _defaults(),
        'memory': _preferences().get('path_history', {}),
        'ui_preferences': _preferences().get('ui', {}),
    }


@app.get('/api/options', dependencies=[Depends(require_token)])
def get_options():
    options = _live_pikobs_options()
    return {
        'families': options.get('families') or config.FALLBACK_FAMILIES,
        'family_catalog': options.get('family_catalog') or {'stage_order': [], 'stages': [], 'extras': []},
        'regions': options.get('regions') or config.FALLBACK_REGIONS,
        'flags_criteria': options.get('flags_criteria') or config.FALLBACK_FLAGS_CRITERIA,
        'projections': options.get('projections') or config.FALLBACK_PROJECTIONS,
        'options_meta': {k: options.get(k, '') for k in ('source', 'pikobs_version', 'pikobs_path', 'python', 'warning')},
    }


@app.post('/api/preferences/reset', dependencies=[Depends(require_token)])
def reset_preferences():
    try:
        config.PREFERENCES_FILE.unlink(missing_ok=True)
    except OSError as exc:
        raise HTTPException(500, f'cannot reset preferences: {exc}')
    return {'ok': True}


@app.post('/api/preferences/reset/{module}', dependencies=[Depends(require_token)])
def reset_module_preferences(module: str):
    if module not in {x['id'] for x in config.MODULES}:
        raise HTTPException(404, 'unknown module')
    prefs = _preferences()
    prefs[f'last_{module}'] = {}
    _write_private_json(config.PREFERENCES_FILE, prefs)
    return {'ok': True}


@app.post('/api/preferences/ui', dependencies=[Depends(require_token)])
def save_ui_preferences(payload: dict = Body(...)):
    module_ids = [x['id'] for x in config.MODULES if x.get('enabled', True)]
    prefs = _preferences()
    ui = prefs.setdefault('ui', {})

    if 'tab_order' in payload:
        raw_order = payload.get('tab_order')
        if not isinstance(raw_order, list):
            raise HTTPException(400, 'tab_order must be a list')
        order = []
        for raw in raw_order:
            module = str(raw)
            if module not in module_ids:
                raise HTTPException(400, f'unknown module in tab_order: {module}')
            if module not in order:
                order.append(module)
        # Always retain newly-added modules even when an older preference file
        # does not know about them yet.
        order.extend(module for module in module_ids if module not in order)
        ui['tab_order'] = order

    if 'last_tab' in payload:
        last_tab = str(payload.get('last_tab') or '')
        if last_tab and last_tab not in module_ids:
            raise HTTPException(400, f'unknown last_tab: {last_tab}')
        ui['last_tab'] = last_tab

    if 'history_sort' in payload:
        raw_sort = payload.get('history_sort')
        allowed_sort = {'created_utc', 'module', 'project_label', 'control', 'experience', 'families', 'period', 'status'}
        if not isinstance(raw_sort, dict):
            raise HTTPException(400, 'history_sort must be an object')
        key = str(raw_sort.get('key') or '')
        direction = str(raw_sort.get('dir') or '')
        if key not in allowed_sort or direction not in {'asc', 'desc'}:
            raise HTTPException(400, 'invalid history_sort')
        ui['history_sort'] = {'key': key, 'dir': direction}

    if 'history_column_widths' in payload:
        raw_widths = payload.get('history_column_widths')
        if not isinstance(raw_widths, dict):
            raise HTTPException(400, 'history_column_widths must be an object')
        allowed_widths = {'launched', 'module', 'project', 'control', 'experience', 'families', 'period', 'status', 'actions'}
        clean_widths = {}
        for raw_key, raw_value in raw_widths.items():
            key = str(raw_key)
            if key not in allowed_widths:
                raise HTTPException(400, f'unknown History column: {key}')
            try:
                width = int(raw_value)
            except (TypeError, ValueError):
                raise HTTPException(400, f'invalid width for History column: {key}')
            if width < 70 or width > 1200:
                raise HTTPException(400, f'History column width out of range: {key}')
            clean_widths[key] = width
        ui['history_column_widths'] = clean_widths

    _write_private_json(config.PREFERENCES_FILE, prefs)
    return {'ok': True, 'ui_preferences': ui}


@app.get('/api/interactive', dependencies=[Depends(require_token)])
def get_interactive():
    return {'jobs': interactive_jobs(config.USER)}


@app.post('/api/modules/vdedr/jobs', dependencies=[Depends(require_token)])
def create_vdedr_job(req: VdedrRequest): return _create_job('vdedr', req)

@app.post('/api/modules/cardio/jobs', dependencies=[Depends(require_token)])
def create_cardio_job(req: CardioRequest): return _create_job('cardio', req)

@app.post('/api/modules/scatter/jobs', dependencies=[Depends(require_token)])
def create_scatter_job(req: ScatterRequest): return _create_job('scatter', req)

@app.post('/api/modules/zone/jobs', dependencies=[Depends(require_token)])
def create_zone_job(req: ZoneRequest): return _create_job('zone', req)

@app.post('/api/modules/timeserie/jobs', dependencies=[Depends(require_token)])
def create_timeserie_job(req: TimeserieRequest): return _create_job('timeserie', req)

@app.post('/api/modules/mapobs/jobs', dependencies=[Depends(require_token)])
def create_mapobs_job(req: MapobsRequest): return _create_job('mapobs', req)

@app.post('/api/modules/obscountdb/jobs', dependencies=[Depends(require_token)])
def create_obscountdb_job(req: ObscountdbRequest): return _create_job('obscountdb', req)

@app.post('/api/modules/flags/jobs', dependencies=[Depends(require_token)])
def create_flags_job(req: FlagsRequest): return _create_job('flags', req)

@app.post('/api/modules/profile/jobs', dependencies=[Depends(require_token)])
def create_profile_job(req: ProfileRequest): return _create_job('profile', req)

@app.post('/api/modules/verifprofile/jobs', dependencies=[Depends(require_token)])
def create_verifprofile_job(req: VerifprofileRequest): return _create_job('verifprofile', req)

# Legacy VDEDR endpoint retained for old clients.
@app.post('/api/vdedr/jobs', dependencies=[Depends(require_token)])
def create_vdedr_job_legacy(req: VdedrRequest): return _create_job('vdedr', req)


@app.post('/api/modules/vdedr/interactive-command', dependencies=[Depends(require_token)])
def vdedr_interactive(req: VdedrRequest): return _interactive('vdedr', req)

@app.post('/api/modules/cardio/interactive-command', dependencies=[Depends(require_token)])
def cardio_interactive(req: CardioRequest): return _interactive('cardio', req)

@app.post('/api/modules/scatter/interactive-command', dependencies=[Depends(require_token)])
def scatter_interactive(req: ScatterRequest): return _interactive('scatter', req)

@app.post('/api/modules/zone/interactive-command', dependencies=[Depends(require_token)])
def zone_interactive(req: ZoneRequest): return _interactive('zone', req)

@app.post('/api/modules/timeserie/interactive-command', dependencies=[Depends(require_token)])
def timeserie_interactive(req: TimeserieRequest): return _interactive('timeserie', req)

@app.post('/api/modules/mapobs/interactive-command', dependencies=[Depends(require_token)])
def mapobs_interactive(req: MapobsRequest): return _interactive('mapobs', req)

@app.post('/api/modules/obscountdb/interactive-command', dependencies=[Depends(require_token)])
def obscountdb_interactive(req: ObscountdbRequest): return _interactive('obscountdb', req)

@app.post('/api/modules/flags/interactive-command', dependencies=[Depends(require_token)])
def flags_interactive(req: FlagsRequest): return _interactive('flags', req)

@app.post('/api/modules/profile/interactive-command', dependencies=[Depends(require_token)])
def profile_interactive(req: ProfileRequest): return _interactive('profile', req)

@app.post('/api/modules/verifprofile/interactive-command', dependencies=[Depends(require_token)])
def verifprofile_interactive(req: VerifprofileRequest): return _interactive('verifprofile', req)


@app.get('/api/runs', dependencies=[Depends(require_token)])
def list_runs(include_hidden: bool = Query(False)):
    rows, hidden = [], _hidden_runs()
    if not config.RUNS_ROOT.exists():
        return {'runs': rows, 'hidden_count': len(hidden)}
    for d in sorted(config.RUNS_ROOT.iterdir(), reverse=True):
        meta_path = d / 'job.json'
        if not d.is_dir() or not meta_path.exists() or (d.name in hidden and not include_hidden):
            continue
        try:
            meta = json.loads(meta_path.read_text())
            pbs = _run_pbs(meta)
            viewer_ready, viewer_url = _viewer_info(meta)
            request = meta.get('request') or {}
            rows.append({
                'run_id': meta.get('run_id', d.name), 'module': meta.get('module', ''),
                'job_id': meta.get('job_id', ''), 'created_utc': meta.get('created_utc', ''),
                'viewer_url': viewer_url, 'viewer_ready': viewer_ready,
                'publish': bool(request.get('publish')),
                'pathwork': meta.get('pathwork', request.get('pathwork', '')),
                'request': request,
                # History colour belongs to this run only. It is deliberately
                # independent from Project / Label.
                'history_color': str(meta.get('history_color') or ''),
                'hidden': d.name in hidden, 'pbs': pbs,
            })
        except Exception:
            continue
        if len(rows) >= 100:
            break
    return {'runs': rows, 'hidden_count': len(hidden)}



@app.post('/api/projects/rename', dependencies=[Depends(require_token)])
def rename_project(payload: dict = Body(...)):
    run_id = str(payload.get('run_id') or '').strip()
    old_label = str(payload.get('old_label') or '').strip()
    new_label = str(payload.get('new_label') or '').strip()
    if '\n' in new_label or '\r' in new_label or len(new_label) > 120:
        raise HTTPException(400, 'invalid project label')
    changed = 0
    if config.RUNS_ROOT.exists():
        for d in config.RUNS_ROOT.iterdir():
            meta_path = d / 'job.json'
            if not d.is_dir() or not meta_path.exists() or not _RUN_ID.match(d.name):
                continue
            try:
                meta = json.loads(meta_path.read_text())
                req = meta.get('request') or {}
                current_label = str(req.get('project_label') or '').strip()
                if old_label:
                    if current_label != old_label:
                        continue
                else:
                    # Unassigned rows are not one shared project. Editing a blank
                    # row assigns only that run instead of renaming every blank row.
                    if d.name != run_id or current_label:
                        continue
                req['project_label'] = new_label
                meta['request'] = req
                _write_private_json(meta_path, meta)
                changed += 1
            except Exception:
                continue
    prefs = _preferences()
    hist = prefs.setdefault('path_history', {}).setdefault('project', [])
    hist = [new_label if str(x) == old_label else str(x) for x in hist]
    prefs['path_history']['project'] = [x for i,x in enumerate(hist) if x and x not in hist[:i]][:30]
    _write_private_json(config.PREFERENCES_FILE, prefs)
    return {'ok': True, 'changed': changed}


@app.post('/api/runs/{run_id}/color', dependencies=[Depends(require_token)])
def set_run_history_color(run_id: str, payload: dict = Body(...)):
    """Set the History colour for one run only.

    The colour is intentionally independent from Project / Label. A run can
    therefore be coloured before, after or without assigning any project.
    """
    color = str(payload.get('color') or '').strip().lower()
    if not re.fullmatch(r'#[0-9a-f]{6}', color):
        raise HTTPException(400, 'invalid history color')
    meta = _read_meta(run_id)
    meta['history_color'] = color
    _write_private_json(config.RUNS_ROOT / run_id / 'job.json', meta)
    return {'ok': True, 'run_id': run_id, 'history_color': color}

@app.post('/api/runs/{run_id}/hide', dependencies=[Depends(require_token)])
def hide_run(run_id: str):
    meta = _read_meta(run_id)
    if not _is_final_state(_run_pbs(meta).get('state', '')):
        raise HTTPException(409, 'only finished runs can be removed from history')
    hidden = _hidden_runs(); hidden.add(run_id); _save_hidden_runs(hidden)
    return {'ok': True}


@app.post('/api/history/clear', dependencies=[Depends(require_token)])
def clear_history():
    hidden, count = _hidden_runs(), 0
    if config.RUNS_ROOT.exists():
        for d in config.RUNS_ROOT.iterdir():
            meta_path = d / 'job.json'
            if not d.is_dir() or not meta_path.exists() or not _RUN_ID.match(d.name):
                continue
            try:
                meta = json.loads(meta_path.read_text())
                if _is_final_state(_run_pbs(meta).get('state', '')):
                    if d.name not in hidden: count += 1
                    hidden.add(d.name)
            except Exception:
                continue
    _save_hidden_runs(hidden)
    return {'ok': True, 'hidden': count}


@app.post('/api/history/restore', dependencies=[Depends(require_token)])
def restore_history():
    _save_hidden_runs(set())
    return {'ok': True}


@app.get('/api/runs/{run_id}', dependencies=[Depends(require_token)])
def get_run(run_id: str):
    meta = _read_meta(run_id)
    viewer_ready, viewer_url = _viewer_info(meta)
    return {**meta, 'viewer_ready': viewer_ready, 'viewer_url': viewer_url, 'pbs': _run_pbs(meta)}


@app.get('/api/runs/{run_id}/log', dependencies=[Depends(require_token)])
def get_log(run_id: str, lines: int = 250):
    lines = max(20, min(lines, 2000))
    meta = _read_meta(run_id)
    log_path = Path(meta['log'])
    if not log_path.exists():
        return {'text': '', 'exists': False}
    content = log_path.read_text(errors='replace').splitlines()
    return {'text': '\n'.join(content[-lines:]), 'exists': True}
