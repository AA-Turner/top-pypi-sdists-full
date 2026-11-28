"""hugpy-core: the coordinator of the wrappers of many hosts.

A wrapper (hugpy-wrapper) is the authority of its own host: what is stored there, what is loaded, what runs
next. Core connects to wrappers, keeps what they publish in one place, and suggests; it decides nothing a wrapper
decides and keeps no copy of a wrapper's rules. Each part is a folder:

    wrappers    connect to wrappers: the saved connections, one way to ask a wrapper anything (directly, or over
                the link a wrapper holds open when Core cannot reach it)
    collate     what every connected wrapper publishes, kept as it was published: its state, its call log, its
                loads, its models and drives. The tables and views of sql/ are how it is read
    serve       Core's own door: the wrappers connect here, and its command line and screens read here
    settings    the settings table of Core's database; the environment and ~/.hugpy/.env; the defaults in the code
    system      `hugpy-core system install | status | uninstall | key`: Core as a service of the host

Core is one process (`hugpy-core serve`) and one database (core.sqlite3 in its data folder).
"""
from . import settings

__all__ = ['settings']
