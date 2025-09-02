import unittest
from collections import OrderedDict
from elifearticle import parse


class TestParseBuildDatasets(unittest.TestCase):
    def setUp(self):
        pass

    def test_datasets_uri_to_doi(self):
        "test converting uri to doi value"
        # based on a dataset in elife-01201-v1
        datasets_data = {
            "generated": [
                {"uri": "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE51740"},
                {"uri": "http://dx.doi.org/10.5061/dryad.cv39v"},
            ]
        }
        datasets = parse.build_datasets(datasets_data)
        self.assertEqual(datasets[0].doi, None)
        self.assertEqual(datasets[1].doi, "10.5061/dryad.cv39v")

    def test_build_data_availability(self):
        "test extracting the data availability statement"
        statement = "Availability statement"
        expected = statement
        datasets_data = OrderedDict(
            [
                (
                    "availability",
                    [OrderedDict([("type", "paragraph"), ("text", statement)])],
                )
            ]
        )
        data_availability = parse.build_data_availability(datasets_data)
        self.assertEqual(data_availability, expected)

    def test_build_data_availability_no_value(self):
        "test extracting data availability encountering an IndexError"
        expected = None
        datasets_data = OrderedDict([("availability", "")])
        data_availability = parse.build_data_availability(datasets_data)
        self.assertEqual(data_availability, expected)
