# modifiers/training/utils.py

import os
import json
import pandas as pd
from pathlib import Path
def load_json_data(json_path: str) -> pd.DataFrame:
    """
    Lee un JSON del disco y devuelve un DataFrame de pandas con su contenido.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def resolve_input_params_path(json_name: str):
    input_path = Path.cwd() / json_name 
    if not input_path.exists():
        raise FileNotFoundError(f"No se encontró '{json_name}' en: {input_path.resolve()}")
    return input_path
