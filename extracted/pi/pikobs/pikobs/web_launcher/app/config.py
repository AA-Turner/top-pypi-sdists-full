from pathlib import Path
import getpass
import os
import socket

USER = getpass.getuser()
HOME = Path.home()
HOST = socket.gethostname()
APP_VERSION = '44'
DEFAULT_PATHWORK = '/fs/site8/eccc/'

APP_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = APP_ROOT.parent
STATE_ROOT = Path(os.environ.get('PIKOBS_WEB_STATE_DIR', str(PROJECT_ROOT / '.pikobs_web')))
RUNS_ROOT = Path(os.environ.get('PIKOBS_WEB_RUNS_ROOT', str(STATE_ROOT / 'runs')))
PREFERENCES_FILE = STATE_ROOT / 'preferences.json'
HIDDEN_RUNS_FILE = STATE_ROOT / 'hidden_runs.json'

WEB_BASE = os.environ.get(
    'PIKOBS_WEB_VIEWER_BASE',
    f'https://goc-dx-u3.science.gc.ca/~{USER}/sites8',
).rstrip('/')

# The address of the documentation is kept once, in pikobs.web.notes
# (DOC_URL, moved with $PIKOBS_DOC_URL); $PIKOBS_WEB_DOC_BASE still wins here.
try:
    from pikobs.web.notes import DOC_URL as _DOC_URL
except Exception:                       # the launcher without pikobs at hand
    _DOC_URL = os.environ.get(
        'PIKOBS_DOC_URL', 'https://goc-dx-u3.science.gc.ca/~dlo001/Pikobs/docs/build/html')
DOC_BASE = os.environ.get('PIKOBS_WEB_DOC_BASE', _DOC_URL).rstrip('/')
REGIONS_DOC_URL = os.environ.get('PIKOBS_WEB_REGIONS_DOC', f'{DOC_BASE}/regions.html')
FAMILIES_DOC_URL = os.environ.get('PIKOBS_WEB_FAMILIES_DOC', f'{DOC_BASE}/families.html')
FLAGS_CRITERIA_DOC_URL = os.environ.get('PIKOBS_WEB_FLAGS_CRITERIA_DOC', f'{DOC_BASE}/flags_criteria.html')
PROJECTIONS_DOC_URL = os.environ.get('PIKOBS_WEB_PROJECTIONS_DOC', f'{DOC_BASE}/projections.html')

MODULE_DOC_URLS = {
    module: os.environ.get(f'PIKOBS_WEB_{module.upper()}_DOC', f'{DOC_BASE}/{module}.html')
    for module in ('vdedr', 'cardio', 'scatter', 'zone', 'timeserie', 'mapobs', 'obscountdb', 'flags', 'profile', 'verifprofile')
}
# Preserve the explicit variable used by older code/configurations.
VDEDR_DOC_URL = MODULE_DOC_URLS['vdedr']

PUBLIC_ROOT = Path(os.environ.get(
    'PIKOBS_WEB_PUBLIC_ROOT',
    str(HOME / 'public_html' / 'pikobs_runs'),
))
PUBLIC_URL_BASE = os.environ.get(
    'PIKOBS_WEB_PUBLIC_URL',
    f'https://goc-dx-u3.science.gc.ca/~{USER}/pikobs_runs',
).rstrip('/')

API_TOKEN = os.environ.get('PIKOBS_WEB_TOKEN', '')
PORT = os.environ.get('PIKOBS_WEB_PORT', '')

MODULES = [
    {'id': 'vdedr', 'label': 'VDEDR', 'enabled': True},
    {'id': 'cardio', 'label': 'CARDIO', 'enabled': True},
    {'id': 'scatter', 'label': 'SCATTER', 'enabled': True},
    {'id': 'zone', 'label': 'ZONE', 'enabled': True},
    {'id': 'timeserie', 'label': 'TIMESERIE', 'enabled': True},
    {'id': 'mapobs', 'label': 'MAPOBS', 'enabled': True},
    {'id': 'obscountdb', 'label': 'OBSCOUNTDB', 'enabled': True},
    {'id': 'flags', 'label': 'FLAGS', 'enabled': True},
    {'id': 'profile', 'label': 'PROFILE', 'enabled': True},
    {'id': 'verifprofile', 'label': 'VERIFPROFILE', 'enabled': True},
]

# Fallbacks only. /api/config asks the installed Pikobs for authoritative
# family / region / flag / projection lists whenever possible.
FALLBACK_FAMILIES = [
    'ai', 'sw', 'sf', 'ua', 'ro', 'radar', 'gp', 'csr', 'ch',
    'to_amsua_allsky', 'atms_allsky', 'mwhs2', 'ssmis', 'iasi', 'cris', 'atms',
]
FALLBACK_REGIONS = ['Monde', 'HemisphereNord', 'HemisphereSud', 'Tropiques', 'Canada']
FALLBACK_FLAGS_CRITERIA = [
    'all', 'assimilee', 'rejets_qc', 'bgckalt', 'bgckalt_qc', 'monitoring', 'postalt'
]
FALLBACK_PROJECTIONS = [
    'cyl', 'orthon', 'orthos', 'robinson', 'europe', 'canada',
    'ameriquenord', 'npolar', 'spolar', 'hrdps', 'reg',
]

ALLOWED_LAND_OCEAN = ['all', 'land', 'ocean']
ALLOWED_MATCH = ['on', 'off']
ALLOWED_TIMESERIE_MATCH = ['off', 'on', 'all']
ALLOWED_SVG = ['off', 'on']
ALLOWED_POINTS = ['OFF', 'ON']
ALLOWED_DASHBOARD_6H = ['auto', 'on', 'off']
ALLOWED_MAPOBS_PANELS = ['map', 'cross', 'vertical', 'stations', 'all']
ALLOWED_SCATTER_FUNCTIONS = ['omp', 'oma', 'stdomp', 'stdoma', 'obs', 'nobs', 'dens', 'bcorr']
ALLOWED_ZONE_FUNCTIONS = ['omp', 'oma', 'obs_error']
ALLOWED_TIMESERIE_FUNCTIONS = ['omp', 'oma']
ALLOWED_OBSCOUNT_AGR = ['omp', 'oma']
ALLOWED_PROFILE_FUNCTIONS = ['omp', 'oma']
ALLOWED_VERIFPROFILE_FUNCTIONS = ['omp', 'oma', 'obs_error']
ALLOWED_RATIO_FIGURE = ['off', 'on']
ALLOWED_FIT_RADAR = ['off', 'on']
ALLOWED_FIT_RADAR_TARGET = ['desroziers', 'sigma', 'sigma3']
ALLOWED_OBS_ERROR_MODEL = ['off', 'on']
ALLOWED_ERROR_CURVES = ['desroziers', 'model', 'model_fit']

# Batch resources. These are independent from the module's --n_cpus value.
# OBSCOUNTDB follows its wrapper: large exclusive node, while Pikobs itself
# still defaults to N_CPUS=80.
PBS_PROFILES = {
    'default': {
        'ncpus': None,          # use request.n_cpus
        'memory': os.environ.get('PIKOBS_WEB_QSUB_MEMORY', '185gb'),
        'walltime': os.environ.get('PIKOBS_WEB_QSUB_WALLTIME', '2:0:0'),
        'place': '',
    },
    'obscountdb': {
        'ncpus': int(os.environ.get('PIKOBS_WEB_OBSCOUNTDB_PBS_NCPUS', '256')),
        'memory': os.environ.get('PIKOBS_WEB_OBSCOUNTDB_PBS_MEMORY', '650gb'),
        'walltime': os.environ.get('PIKOBS_WEB_OBSCOUNTDB_PBS_WALLTIME', '6:0:0'),
        'place': os.environ.get('PIKOBS_WEB_OBSCOUNTDB_PBS_PLACE', 'scatter:excl'),
    },
}
