# modifiers/config.py

from .config_loader import cargar_json_usuario  

_params = cargar_json_usuario()

if "CONFIG" not in _params or not isinstance(_params["CONFIG"], list) or len(_params["CONFIG"]) == 0:
    raise KeyError("El JSON debe contener 'CONFIG' como lista no vacía en input_params.json")

CONFIG = _params["CONFIG"]
PREDICTOR_COLUMNS = _params.get("PREDICTOR_COLUMNS", [])
