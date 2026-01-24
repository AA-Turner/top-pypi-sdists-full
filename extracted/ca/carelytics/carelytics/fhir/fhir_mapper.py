"""
carelytics.fhir.fhir_mapper
----------------------------
Maps raw healthcare data (from CSV, SQL, or API) into standardized FHIR resources.
"""
 
import json
from datetime import datetime

class FHIRMapper:
    """Utility to convert raw healthcare data into FHIR-compliant JSON structures."""

    def __init__(self, system_url="https://carelytics.io/fhir"):
        self.system_url = system_url

    def map_patient(self, row):
        """
        Convert a patient record (dictionary or DataFrame row) to a FHIR Patient resource.
        """
        patient = {
            "resourceType": "Patient",
            "id": str(row.get("patient_id", "")),
            "identifier": [
                {
                    "system": f"{self.system_url}/patient-id",
                    "value": str(row.get("patient_id", "")),
                }
            ],
            "name": [
                {
                    "family": row.get("last_name", ""),
                    "given": [row.get("first_name", "")],
                }
            ],
            "gender": row.get("gender", "unknown"),
            "birthDate": str(row.get("birth_date", "")),
        }
        return patient

    def map_observation(self, row, code="8310-5", display="Body temperature"):
        """
        Convert a vitals or lab record into a FHIR Observation resource.
        Default uses LOINC 8310-5 for body temperature.
        """
        obs = {
            "resourceType": "Observation",
            "id": f"obs-{row.get('observation_id', '')}",
            "status": "final",
            "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs"}]}],
            "code": {
                "coding": [
                    {"system": "http://loinc.org", "code": code, "display": display}
                ]
            },
            "subject": {"reference": f"Patient/{row.get('patient_id', '')}"},
            "effectiveDateTime": str(datetime.now().isoformat()),
            "valueQuantity": {
                "value": row.get("value", ""),
                "unit": row.get("unit", ""),
                "system": "http://unitsofmeasure.org",
            },
        }
        return obs

    def export_bundle(self, patients, observations, file_path="fhir_bundle.json"):
        """
        Combine multiple resources into a FHIR Bundle and export as JSON.
        """
        bundle = {
            "resourceType": "Bundle",
            "type": "collection",
            "entry": [{"resource": p} for p in patients] + [{"resource": o} for o in observations],
        }
        with open(file_path, "w") as f:
            json.dump(bundle, f, indent=2)
        print(f"FHIR Bundle exported to {file_path}")

