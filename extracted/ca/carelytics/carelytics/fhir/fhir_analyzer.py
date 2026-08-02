"""
carelytics.fhir.fhir_analyzer
-----------------------------
Performs integrity checks and summary analytics on FHIR-compliant JSON resources. 
"""

import json
from collections import Counter, defaultdict

class FHIRAnalyzer:
    """Analyzes FHIR JSON bundles or individual resources for data quality and completeness."""

    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, "r") as f:
            self.bundle = json.load(f)

    def resource_count(self):
        """Count each resource type in the FHIR bundle."""
        counter = Counter(entry["resource"]["resourceType"] for entry in self.bundle.get("entry", []))
        return dict(counter)

    def check_missing_fields(self):
        """Check for missing critical fields (e.g., ID, gender, valueQuantity)."""
        missing = defaultdict(list)
        for entry in self.bundle.get("entry", []):
            r = entry["resource"]
            rtype = r["resourceType"]
            if rtype == "Patient" and not r.get("gender"):
                missing["Patient"].append(r.get("id"))
            if rtype == "Observation" and not r.get("valueQuantity", {}).get("value"):
                missing["Observation"].append(r.get("id"))
        return dict(missing)

    def summarize_observations(self):
        """Summarize observation values by code (e.g., average per LOINC code)."""
        obs_data = defaultdict(list)
        for entry in self.bundle.get("entry", []):
            r = entry["resource"]
            if r["resourceType"] == "Observation":
                code = r["code"]["coding"][0]["code"]
                value = r.get("valueQuantity", {}).get("value")
                if value is not None:
                    obs_data[code].append(float(value))

        summary = {code: sum(vals) / len(vals) for code, vals in obs_data.items() if vals}
        return summary

    def generate_report(self):
        """Generate a readable text report summarizing the bundle."""
        print("FHIR Bundle Analysis Report")
        print("=============================")
        print(f"Resource counts: {self.resource_count()}")
        print(f"Missing fields: {self.check_missing_fields()}")
        print(f"Observation summaries: {self.summarize_observations()}")

