import json
from collections import OrderedDict
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pook

from eveuniverse.models import EveCategory, EveGroup, EveRegion, EveType
from eveuniverse.tests.helpers import TestCaseWithClearCache
from eveuniverse.tests.testdata.factories_2 import make_esi_url
from eveuniverse.tools.testdata import (
    ModelSpec,
    create_testdata,
    load_testdata_from_file,
)

_current_dir = Path(__file__).parent

FILENAME_TESTDATA = "dummy.json"


class TestTestData(TestCaseWithClearCache):
    def setUp(self):
        EveCategory.objects.all().delete
        EveGroup.objects.all().delete
        EveType.objects.all().delete
        EveRegion.objects.all().delete

    @staticmethod
    def _get_ids(testdata: dict, model_name: str) -> set:
        objs = testdata.get(model_name, [])
        return {obj["id"] for obj in objs}

    @patch("eveuniverse.models.base.EVEUNIVERSE_LOAD_STARGATES", True)
    @patch("eveuniverse.tools.testdata.is_esi_online", lambda: True)
    @pook.on
    def test_create_testdata(self):
        # given
        category_id = 6
        group_id = 25
        group_name = "Frigate"
        type_id = 603
        type_name = "Merlin"
        pook.get(
            make_esi_url(f"universe/categories/{category_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "groups": [group_id],
                "name": "Ship",
                "published": True,
            },
        )
        pook.get(
            make_esi_url(f"universe/groups/{group_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "group_id": group_id,
                "name": group_name,
                "published": True,
                "types": [type_id],
            },
        )
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 42,
                "group_id": group_id,
                "market_group_id": 666,
                "mass": 997000,
                "name": type_name,
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id,
                "volume": 16500,
            },
        )
        spec = [
            ModelSpec("EveType", ids=[603]),
            # ModelSpec("EveType", ids=[621], enabled_sections=[EveType.Section.DOGMAS]),
            # ModelSpec("EveSolarSystem", ids=[30045339], include_children=True),
        ]
        with TemporaryDirectory() as temp_dir:
            # when
            filepath = Path(temp_dir) / FILENAME_TESTDATA
            create_testdata(spec, str(filepath))

            # then
            with filepath.open("r", encoding="utf-8") as file:
                testdata = json.load(file, object_pairs_hook=OrderedDict)

            self.assertEqual(self._get_ids(testdata, "EveType"), {603})
            self.assertEqual(self._get_ids(testdata, "EveCategory"), {6})
            self.assertEqual(self._get_ids(testdata, "EveGroup"), {25})

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
