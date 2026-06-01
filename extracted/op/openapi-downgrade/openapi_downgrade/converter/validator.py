import jsonschema
import requests

SCHEMA_URL = "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/3.0.3/schemas/v3.0/schema.json"

def validate_openapi_3(spec: dict) -> tuple[bool, str | None]:
    try:
        response = requests.get(SCHEMA_URL, timeout=10)
        response.raise_for_status()
        schema = response.json()

        jsonschema.validate(instance=spec, schema=schema)
        return True, None

    except jsonschema.ValidationError as ve:
        path = " → ".join(str(p) for p in ve.absolute_path)
        return False, f"Validation error at '{path}': {ve.message}"

    except Exception as e:
        return False, f"Unexpected error: {e}"
