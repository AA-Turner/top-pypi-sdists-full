import requests
import json
from urllib3 import disable_warnings
import os
import click
import re


disable_warnings()


SCHEMA_SERVICE_URL = "https://iot-reports.silabs.net/createSchema"


@click.command()
@click.option(
    "--schema",
    required=True,
    help="Path to Typescript-formatted master schema",
)
@click.option(
    "--output",
    required=True,
    help="Path to output JSON schema as a single file",
)
@click.option(
    "--output_element_dir",
    required=True,
    help="Directory to store JSON schema as separate elements",
)
@click.option(
    "--python-generated-models-file",
    default=os.path.join(
        os.path.dirname(__file__), "..", "models", "python", "generated_models.py"
    ),
)
def main(schema, output, output_element_dir, python_generated_models_file):
    schema = os.path.abspath(schema)
    output = os.path.abspath(output)
    print(f"Loading {schema}...")
    with open(schema) as f:
        ts_schema = f.read()
    body = {
        "typeNames": "[*]",
        "requiredTypes": [],
        "settings": {"required": True, "ref": True, "topRef": True, "titles": False},
        "typeData": ts_schema,
    }
    print("Converting to JSON schema using schema converter service...")
    r = requests.post(SCHEMA_SERVICE_URL, json=body, verify=False, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(
            f"Status code {r.status_code} returned from POST to {SCHEMA_SERVICE_URL}"
        )
    schema = r.json()
    print(f"Writing {output}")
    with open(output, "w") as f:
        f.write(json.dumps(schema, indent=2))

    # Create elements directory and write each schema element to a separate file
    os.makedirs(output_element_dir, exist_ok=True)
    model_names = []
    for item in schema["definitions"]:
        model_names.append(item)
        item_schema = schema["definitions"][item]
        item_schema_json = json.dumps(item_schema)
        pattern = r'"#/definitions/([^"]*)"'
        item_schema_json = re.sub(pattern, r'"\1.json"', item_schema_json)
        item_schema = json.loads(item_schema_json)
        item_filename = os.path.join(output_element_dir, item + ".json")
        with open(item_filename, "w") as f:
            f.write(json.dumps(item_schema, indent=2))

    # Create python "generated_models.py" file to import the correct version of the models
    # for the installed version of pydantic
    with open(python_generated_models_file, "w") as f:
        f.write("from pydantic.version import VERSION as PYDANTIC_VERSION\n")
        f.write("IS_PYDANTIC_V1 = PYDANTIC_VERSION.startswith('1.')\n")
        f.write("\nif IS_PYDANTIC_V1:\n")
        for model_name in model_names:
            f.write(f"    from .generated_models_pydantic_v1 import {model_name}\n")
        f.write(f"else:\n")
        for model_name in model_names:
            f.write(f"    from .generated_models_pydantic_v2 import {model_name}\n")
        f.write("\n__all__ = [\n")
        for model_name in model_names:
            f.write(f"    '{model_name}',\n")
        f.write("]\n")

    print("Done!")


if __name__ == "__main__":
    main()
