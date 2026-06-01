import json
from pathlib import Path
from openapi_downgrade.converter.transformer import convert_spec
from openapi_downgrade.converter.validator import validate_openapi_3

def test_petstore_3_1_conversion():
    """
    Tests the full conversion of a sample OpenAPI 3.1 PetStore spec to 3.0.
    """
    # Load the 3.1 spec
    spec_path = Path(__file__).parent / "petstore_3_1.json"
    with open(spec_path, "r") as f:
        spec_3_1 = json.load(f)

    # Convert the spec
    converted_spec = convert_spec(spec_3_1)

    # Validate the converted spec against OpenAPI 3.0 schema
    is_valid, error = validate_openapi_3(converted_spec)

    assert is_valid, f"Converted spec is not valid OpenAPI 3.0: {error}"
    assert converted_spec["openapi"] == "3.0.3"
