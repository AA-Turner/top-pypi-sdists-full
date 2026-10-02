from .scatter import *
from .parallel import *
from .profile import *
from .configobs import *
from .cardio import *
from .timeserie import *
from .vdedr import *
from .extension import *
from .flags import *
from .unittestpikobs import *
from .zone import *
from .histogram import *
from .obscountdb import *
from .obstimedb import *
from .mapobs import *
from .verifprofile import *
from .pikobsburp2rdb import *
from .web.viewer import generate_web 
from .spatial import *
from .pbs_submit import *
from .stations import *
from .figures import * 
from .obsdb import *
from . import stats


try:                                   # the version pip installed
    from importlib.metadata import version as _version
    __version__ = _version("pikobs")
except Exception:                      # pragma: no cover
    __version__ = "unknown"
