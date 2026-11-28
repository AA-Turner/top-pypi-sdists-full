"""The constants of hugpy-core: the names its settings, its service and its wrappers' records carry."""
import os

# the settings. A saved value is a row of the settings table of Core's own database; a setting with no saved
# value takes HUGPY_CORE_<NAME> from the process environment or the one .env file, else the default below.
# Everything Core keeps is under one folder (hugpy_resources host_data_dir): the host's, /var/lib/hugpy/core, once
# `hugpy-core system install` has made it; else this account's own, ~/.local/share/hugpy/core.
PACKAGE = 'hugpy-core'                      # the distribution, and what /health says answers ("package")
PREFIX = 'HUGPY_CORE_'
ENV_FILE = os.path.join(os.path.expanduser('~'), '.hugpy', '.env')       # the one .env, for every hugpy tool
HOME_NAME = 'core'                          # the tool's folder: <hugpy data directory>/core
PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # .../hugpy_core
DEFAULTS = {
    'DATABASE': 'core.sqlite3',             # under the tool's folder unless absolute
    'HOST': '127.0.0.1',                    # where Core's door listens
    'PORT': 7002,                           # where the console's own pages say a person's Core is: http://localhost:7002
    'CONSOLE': os.path.join(PACKAGE_DIR, 'console', 'site'),   # the console's built files, served at the door
}
# an unknown path under one of these is a mistake in a request to the API and is answered so; any other path is
# the console's: one of its files, or one of its own pages (its index)
API_PREFIXES = ('/v1/', '/api/', '/fleet-link/', '/health', '/readiness')
SETTING_KEYS = ('host', 'port')             # what `hugpy-core set` saves
# Who may ask Core's door is decided by a key, never by where a call seems to come from: a proxy or a forward on
# the host (a web front, a TCP forward of the port) makes any caller look like one of the host's own programs.
API_KEY_NAME = 'api.key'                    # Core's API key, beside its database: what another host is given
LOCAL_KEY_NAME = 'local.key'                # the key of the programs of this host (Core's own command line): where
LOCAL_KEY_FILE = '/etc/hugpy/core.local.key'  # Core is a service it is this file, which every account of the host
#                                             can read and nothing outside the host can; else it is beside the database

# Core as a service of the host (system/system.py)
SERVICE_ACCOUNT = 'hugpy-core'
SERVICE_UNIT = 'hugpy-core.service'
SERVICE_BACKUPS = '/var/backups/hugpy-core'
ENDPOINT_FILE = '/etc/hugpy/core.endpoint.json'             # where the service listens, for its clients on the host
# hugpy-core before 0.5 ran these beside its server; Core is one process now. Its database server and toolserver
# (hugpy-core-postgres, hugpy-core-toolserver) are not touched: what they hold is that Core's record
EARLIER_UNITS = ('hugpy-core-intake.service', 'hugpy-core-downloader.service', 'hugpy-core-catalog.service')
WRAPPER_ENDPOINT_FILE = '/etc/hugpy/wrapper.endpoint.json'  # where this host's own wrapper listens (`connect local`)

# a wrapper, as Core knows one
WRAPPER_SERVICE = 'hugpy-wrapper'           # what a wrapper's /health says it is ("service")
WRAPPER_STATUSES = ('ok', 'degraded')       # a degraded wrapper still says who it is and is still collected
LINK_URL = 'link'                           # the saved address of a wrapper that connects out to Core
NAME_CHARS = frozenset('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-')

# the routes a wrapper is asked on (its own API; hugpy-wrapper queue/serve.py)
STATE_PATH = '/v1/telemetry/state'          # its state tables whole, its store's identity, its health stamp
LOG_PATH = '/v1/telemetry'                  # ?table=&since=&limit=: one page of a log table, by cursor
DOCUMENTS = {                               # what else is kept of a wrapper, whole: {name: its route}
    'models': '/v1/models',                 # the models it can serve, with what each would do here now
    'units': '/v1/central',                 # every model its Discovery has recorded on the host, on any drive
    'drives': '/v1/drives',                 # its drives: role, room, measured speeds
    'storage': '/storage',                  # its storage as its Discovery reports it: drives, the models on each
}
KEY_COOKIE = 'hugpy_core_key'               # the key as a browser holds it for the console (serve: /api/core/key)
# a log's rows that can still change: read again until they settle (SQL over the row as the wrapper published it)
OPEN_ROWS = {
    'call_log': "json_extract(row, '$.call_state') IS NULL OR json_extract(row, '$.call_state') IN ('pending', 'running')",
    'load_runs': "json_extract(row, '$.ended_at') IS NULL",
}

# the collector (collate/collector.py)
POLL_WAIT_S = 30                # how long a wrapper holds Core's read of its state when nothing changed
LOG_PAGE = 2000                 # rows of a log asked at once
ASK_TIMEOUT_S = 30              # one read of a wrapper
RETRY_MAX_S = 30                # the longest wait between tries of a wrapper that does not answer
REGISTRY_LOOK_S = 3             # how often the collector looks at the saved connections for a change
PASS_MIN_S = 2.0                # a wrapper that answers its long read at once is not read in a hot loop

# grading (grading/): a call made to grade a model is an ordinary call whose body carries a marker in its metadata,
# {"grading": {"query": ID, "tier": NAME, "round": ID}}. The wrapper keeps the body in its call log, so the call,
# and with it the answer, is found again by its marker: nothing else records it
GRADING_MARKER = 'grading'
TIER_NAMES = ('easy', 'medium', 'hard')     # a query's tier, 1 the easiest, as it is said
CALL_OPEN = ('pending', 'running')          # a call its wrapper has not finished (or has not said the state of)
CALL_ANSWERED = 'done'                      # a call that was answered: what a grade is read from
# a round (grading/rounds.py): a mass shot of grading calls. A wrapper's front door holds every call it was sent
# until its queue has answered it, and its queue plans among the calls it holds: so a round sends a wrapper a
# model's queries together (one load answers them all) and as many models at once as stay within this many calls
ROUND_CALLS_AT_ONCE = 256
ROUND_CALL_WAIT_S = 86400       # a call waits for its wrapper's queue as long as that takes: a day at most
ROUND_STOP_WAIT_S = 60          # how long a round that was stopped cancels what its wrappers still hold of it, and
#                                 waits for a call a wrapper is already answering: then the round is over without it
ROUND_SETTLE_S = 30             # a round is over when Core has read its last calls from the call logs: at most this long
ROUND_KINDS = ('test-fire', 'grading')      # a test fire of a wrapper; a grading of chosen models

# the link (wrappers/link.py): a wrapper Core cannot reach connects out, and Core puts its requests on that
LINK_POLL_WAIT_S = 25           # a wrapper's poll is held this long when Core has nothing for it
LINK_ALIVE_S = 75               # a link not polled for this long is down: a request on it fails at once
LINK_ANSWER_WAIT_S = 3600       # a request waits at most this long for its answer
LINK_MAX_BATCH = 16
LINK_STREAM_BLOCK = 1 << 20
LINK_STREAM_STALL_S = 600       # a streamed answer whose reader stops taking blocks this long is abandoned

__all__ = ['PACKAGE', 'PACKAGE_DIR', 'API_PREFIXES', 'PREFIX', 'ENV_FILE', 'HOME_NAME', 'DEFAULTS', 'SETTING_KEYS', 'API_KEY_NAME', 'LOCAL_KEY_NAME', 'LOCAL_KEY_FILE', 'SERVICE_ACCOUNT',
           'SERVICE_UNIT', 'SERVICE_BACKUPS', 'ENDPOINT_FILE', 'EARLIER_UNITS', 'WRAPPER_ENDPOINT_FILE', 'WRAPPER_SERVICE', 'WRAPPER_STATUSES',
           'LINK_URL', 'NAME_CHARS', 'KEY_COOKIE', 'STATE_PATH', 'LOG_PATH', 'DOCUMENTS', 'OPEN_ROWS', 'POLL_WAIT_S', 'LOG_PAGE',
           'GRADING_MARKER', 'TIER_NAMES', 'CALL_OPEN', 'CALL_ANSWERED', 'ROUND_CALLS_AT_ONCE', 'ROUND_CALL_WAIT_S',
           'ROUND_STOP_WAIT_S', 'ROUND_SETTLE_S', 'ROUND_KINDS',
           'ASK_TIMEOUT_S', 'RETRY_MAX_S', 'REGISTRY_LOOK_S', 'PASS_MIN_S', 'LINK_POLL_WAIT_S', 'LINK_ALIVE_S',
           'LINK_ANSWER_WAIT_S', 'LINK_MAX_BATCH', 'LINK_STREAM_BLOCK', 'LINK_STREAM_STALL_S']
