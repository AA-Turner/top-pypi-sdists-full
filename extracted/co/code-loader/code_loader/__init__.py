from code_loader.leaploader import LeapLoader
from code_loader.inner_leap_binder import global_leap_binder as leap_binder
from code_loader.experiment_api.experiment import init_experiment
from code_loader.experiment_api.client import Client

try:
    from code_loader.mixpanel_tracker import track_code_loader_loaded
    track_code_loader_loaded({'event_type': 'module_import'})
except Exception:
    pass
