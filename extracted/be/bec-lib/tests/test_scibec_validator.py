import os

import bec_lib
from bec_lib.scibec_validator import SciBecValidator

dir_path = os.path.abspath(os.path.join(os.path.dirname(bec_lib.__file__), "./configs/"))
SCHEMA = os.path.join(dir_path, "openapi_schema.json")


def test_scibec_validator():
    validator = SciBecValidator(SCHEMA)
    # print(validator.device_schema)
    validator.validate_device_patch({"enabled": True})
