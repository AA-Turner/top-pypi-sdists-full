import json
from collections import OrderedDict
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from eveuniverse.models import EveCategory, EveGroup, EveRegion, EveType
from eveuniverse.tools.testdata import (
    ModelSpec,
    create_testdata,
    load_testdata_from_file,
)
from eveuniverse.utils import NoSocketsTestCase

from .testdata.esi import EsiClientStub

_current_dir = Path(__file__).parent

FILENAME_TESTDATA = "dummy.json"


class TestTestData(NoSocketsTestCase):
    def setUp(self) -> None:
        EveCategory.objects.all().delete
        EveGroup.objects.all().delete
        EveType.objects.all().delete
        EveRegion.objects.all().delete

    @staticmethod
    def _get_ids(testdata: dict, model_name: str) -> set:
        return {obj["id"] for obj in testdata[model_name]}

    @patch("eveuniverse.models.base.EVEUNIVERSE_LOAD_STARGATES", True)
    @patch("eveuniverse.tools.testdata.is_esi_online", lambda: True)
    @patch("eveuniverse.managers.universe.esi")
    def test_create_testdata(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        spec = [
            ModelSpec("EveType", ids=[603]),
            ModelSpec("EveType", ids=[621], enabled_sections=[EveType.Section.DOGMAS]),
            ModelSpec("EveSolarSystem", ids=[30045339], include_children=True),
        ]
        with TemporaryDirectory() as temp_dir:
            # when
            filepath = Path(temp_dir) / FILENAME_TESTDATA
            create_testdata(spec, str(filepath))
            # then
            with filepath.open("r", encoding="utf-8") as file:
                testdata = json.load(file, object_pairs_hook=OrderedDict)

            # EveType
            # did load requested objects
            self.assertEqual(self._get_ids(testdata, "EveType"), {16, 603, 621})

            # did load their parents too
            self.assertEqual(self._get_ids(testdata, "EveCategory"), {2, 6})
            self.assertEqual(self._get_ids(testdata, "EveGroup"), {10, 25, 26})

            # did not load their children
            self.assertEqual(EveType.objects.get(id=603).dogma_attributes.count(), 0)

            # EveSolarSystem
            # did load requested objects
            self.assertEqual(self._get_ids(testdata, "EveSolarSystem"), {30045339})

            # did load their parents too
            self.assertEqual(self._get_ids(testdata, "EveConstellation"), {20000785})

            # did load children of solar systems as requested
            self.assertEqual(
                self._get_ids(testdata, "EveStargate"), {50016284, 50016286}
            )

    def test_load_testdata_from_file_with_str_format(self):
        filepath = _current_dir / "testdata_example.json"
        load_testdata_from_file(str(filepath))
        self.assertTrue(EveCategory.objects.filter(id=6).exists())
        self.assertTrue(EveGroup.objects.filter(id=25).exists())
        self.assertTrue(EveGroup.objects.filter(id=26).exists())
        self.assertTrue(EveType.objects.filter(id=603).exists())
        self.assertTrue(EveType.objects.filter(id=621).exists())
        self.assertTrue(EveRegion.objects.filter(id=10000069).exists())

    def test_load_testdata_from_file_with_path_format(self):
        filepath = _current_dir / "testdata_example.json"
        load_testdata_from_file(filepath)
        self.assertTrue(EveCategory.objects.filter(id=6).exists())
