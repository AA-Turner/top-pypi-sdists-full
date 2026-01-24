"""
fhir/parser.py
--------------
Parses FHIR JSON bundles into Pandas DataFrames for analysis.
"""

import json
import pandas as pd
 

def parse_fhir_bundle(bundle_path):
    """
    Converts a FHIR JSON bundle into a Pandas DataFrame.

    Parameters
    ----------
    bundle_path : str
        Path to the FHIR JSON file.

    Returns
    -------
    pd.DataFrame
    """
    with open(bundle_path, "r") as f:
        data = json.load(f)

    entries = data.get("entry", [])
    parsed = []
    for e in entries:
        resource = e.get("resource", {})
        resource_type = resource.get("resourceType", "Unknown")
        resource_id = resource.get("id", "")
        parsed.append({"resourceType": resource_type, "id": resource_id, **resource})

    df = pd.DataFrame(parsed)
    print(f"✅ Parsed {len(df)} FHIR resources from {bundle_path}")
    return df
