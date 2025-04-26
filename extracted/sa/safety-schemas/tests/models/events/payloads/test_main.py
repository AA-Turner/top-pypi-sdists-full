import importlib
import json
from pathlib import Path
import re
from pydantic import ValidationError
import pytest

PKG_NAME = "safety_schemas.models.events.payloads"
DATA_DIR = Path("tests/models/data/events/payloads")

PKG = importlib.import_module(PKG_NAME)

from safety_schemas.models.events import PayloadBase

EXCLUDED_MODELS = ["PackagePayloadBase", "SingleVersionPackagePayload"]

class TestModels:
    
    @pytest.mark.parametrize("model_name, model", [(name, getattr(PKG, name)) for name in PKG.__all__ if issubclass(getattr(PKG, name), PayloadBase) and name not in EXCLUDED_MODELS])
    def test_model(self, model_name, model):

        kebab_name = re.sub(r'(?<!^)(?=[A-Z])', '-', model_name).lower().replace('-payload', '')
        print(f"Testing {model_name} with {kebab_name}")
        
        test_files = list(DATA_DIR.glob(f"{kebab_name}-*.json"))
        assert test_files, f"No test files found for {model_name}"

        coerced = {"FirewallDisabledPayload": {"reason": lambda reason: len(reason) == 200}}
        
        for file_path in test_files:
            file_stem = file_path.stem
            is_valid = not file_stem.endswith('-invalid')
            is_coerced = file_stem.endswith('-coerced')
            
            with open(file_path) as f:
                test_data = json.load(f)

            if is_coerced:
                model_instance = model(**test_data, strict=False)
                assert model_instance, f"Failed to instantiate {model_name} with coerced data from {file_path}"

                if model_name in coerced:
                    for property, validate in coerced[model_name].items():
                        assert validate(getattr(model_instance, property)), f"Coercion failed for {model_name}.{property} in {file_path}"            
            elif is_valid:
                try:
                    model_instance = model(**test_data, strict=True)
                    assert model_instance, f"Failed to instantiate {model_name} with valid data from {file_path}"
                except ValidationError as e:
                    pytest.fail(f"Valid payload {file_path} failed validation: {e}")
            else:
                with pytest.raises(ValidationError):
                    model_instance = model(**test_data, strict=True)
                    print(test_data)
                    pytest.fail(f"Invalid payload {file_path} passed validation, but should have failed")
