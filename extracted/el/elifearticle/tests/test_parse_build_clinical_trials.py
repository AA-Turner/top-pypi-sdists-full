import unittest
from collections import OrderedDict
from elifearticle import parse


REGISTRY_NAME_TO_DOI_MAP = OrderedDict(
    [("ClinicalTrials.gov", "10.18810/clinical-trials-gov")]
)


class TestParseBuildClinicalTrials(unittest.TestCase):
    def setUp(self):
        self.clinical_trials_data = [
            OrderedDict(
                [
                    ("id", "CT1"),
                    ("content-type", "post-result"),
                    ("document-id", "NCT02836002"),
                    ("document-id-type", "clinical-trial-number"),
                    ("source-id", "ClinicalTrials.gov"),
                    ("source-id-type", "registry-name"),
                    ("source-type", "clinical-trials-registry"),
                    ("text", "NCT02836002"),
                    ("xlink_href", "https://clinicaltrials.gov/show/NCT02836002"),
                ]
            ),
            OrderedDict(
                [
                    ("id", "CT1"),
                    ("content-type", "preResult"),
                    ("document-id", "NCT04094727"),
                    ("document-id-type", "clinical-trial-number"),
                    ("source-id", "10.18810/clinical-trials-gov"),
                    ("source-id-type", "crossref-doi"),
                    ("source-type", "clinical-trials-registry"),
                    ("text", "NCT04094727"),
                    ("xlink_href", "https://clinicaltrials.gov/show/NCT04094727"),
                ]
            ),
        ]

    def test_build_clinical_trials(self):
        "test building ClinicalTrial objects from clinical trials data"
        clinical_trials = parse.build_clinical_trials(self.clinical_trials_data)
        self.assertEqual(len(clinical_trials), 2)
        # spot check a few values
        self.assertEqual(
            clinical_trials[0].xlink_href, "https://clinicaltrials.gov/show/NCT02836002"
        )
        self.assertEqual(clinical_trials[0].get_registry_doi(), None)
        self.assertEqual(clinical_trials[1].document_id, "NCT04094727")
        self.assertEqual(
            clinical_trials[1].get_registry_doi(), "10.18810/clinical-trials-gov"
        )

    def test_build_clinical_trials_registry_doi_map(self):
        "build clinicial trials data then get a registry doi using the registry name to doi map"
        clinical_trials = parse.build_clinical_trials(self.clinical_trials_data)
        # override a value for checking test coverage
        registry_doi = "injected_value"
        clinical_trials[1].registry_doi = registry_doi
        self.assertEqual(
            clinical_trials[0].get_registry_doi(REGISTRY_NAME_TO_DOI_MAP),
            "10.18810/clinical-trials-gov",
        )
        self.assertEqual(
            clinical_trials[1].get_registry_doi(REGISTRY_NAME_TO_DOI_MAP), registry_doi
        )
