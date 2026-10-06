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


# The ``import *`` above also brings in, from each package, the module of the
# same name (pikobs/vdedr/vdedr.py for pikobs.vdedr ...), and that module then
# hides its own package: pikobs.vdedr was the file vdedr.py, and
# ``import pikobs.vdedr.vdedr_plot`` failed. Each name is pointed back at its
# package here; every package exports what was used through the file
# (arg_call for the wrappers), so nothing calling pikobs.<module>.<name> changes.
import sys as _sys
for _name, _mod in list(_sys.modules.items()):
    if _name.startswith(__name__ + ".") and _name.count(".") == 1 and hasattr(_mod, "__path__"):
        globals()[_name.split(".", 1)[1]] = _mod
del _sys, _name, _mod


try:                                   # the version pip installed
    from importlib.metadata import version as _version
    __version__ = _version("pikobs")
except Exception:                      # pragma: no cover
    __version__ = "unknown"
