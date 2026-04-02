from unittest.mock import patch

from django.test import TestCase

from eveuniverse.models import (
    EveAncestry,
    EveAsteroidBelt,
    EveBloodline,
    EveCategory,
    EveConstellation,
    EveDogmaAttribute,
    EveDogmaEffect,
    EveDogmaEffectModifier,
    EveEntity,
    EveFaction,
    EveGraphic,
    EveGroup,
    EveIndustryActivity,
    EveIndustryActivityDuration,
    EveIndustryActivityMaterial,
    EveIndustryActivityProduct,
    EveIndustryActivitySkill,
    EveMarketGroup,
    EveMoon,
    EvePlanet,
    EveRace,
    EveRegion,
    EveSolarSystem,
    EveStar,
    EveStargate,
    EveStation,
    EveType,
    EveTypeDogmaAttribute,
    EveTypeDogmaEffect,
    EveTypeMaterial,
    EveUnit,
)
from eveuniverse.models.base import EveUniverseBaseModel


class TestEveUniverseBaseModelGetModelClass(TestCase):
    def test_should_return_class_when_it_is_valid(self):
        # when
        result = EveUniverseBaseModel.get_model_class("EveSolarSystem")
        # then
        self.assertIs(result, EveSolarSystem)

    def test_should_raise_error_when_requesting_non_existing_class(self):
        # when/then
        with self.assertRaises(LookupError):
            EveUniverseBaseModel.get_model_class("Unknown Class")

    @patch("eveuniverse.models.base.apps.get_model")
    def test_should_raise_error_when_requesting_invalid_class(self, mock_get_model):
        # given
        mock_get_model.return_value = TestCase
        # when/then
        with self.assertRaises(TypeError):
            EveUniverseBaseModel.get_model_class("EveUniverseBaseModel")


class TestEveUniverseBaseModel(TestCase):
    def test_all_models(self):
        models = EveUniverseBaseModel.all_models()
        self.maxDiff = None
        self.assertListEqual(
            models,
            [
                EveUnit,  # load_order = 100
                EveIndustryActivity,  # load_order=101
                EveEntity,  # load_order = 110
                EveGraphic,  # load_order = 120
                EveCategory,  # load_order = 130
                EveGroup,  # load_order = 132
                EveType,  # load_order = 134
                EveTypeMaterial,  # load_order = 135
                EveIndustryActivityDuration,  # load_order = 136
                EveIndustryActivityMaterial,  # load_order = 137
                EveIndustryActivityProduct,  # load_order = 138
                EveIndustryActivitySkill,  # load_order = 139
                EveDogmaAttribute,  # load_order = 140
                EveDogmaEffect,  # load_order = 142
                EveDogmaEffectModifier,  # load_order = 144
                EveTypeDogmaEffect,  # load_order = 146
                EveTypeDogmaAttribute,  # load_order = 148
                EveRace,  # load_order = 150
                EveBloodline,  # load_order = 170
                EveAncestry,  # load_order = 180
                EveRegion,  # load_order = 190
                EveConstellation,  # load_order = 192
                EveSolarSystem,  # load_order = 194
                EveAsteroidBelt,  # load_order = 200
                EvePlanet,  # load_order = 205
                EveStation,  # load_order = 207
                EveFaction,  # load_order = 210
                EveMoon,  # load_order = 220
                EveStar,  # load_order = 222
                EveStargate,  # load_order = 224
                EveMarketGroup,  # load_order = 230
            ],
        )

    def test_eve_universe_meta_attr_1(self):
        """When defined, return value"""
        self.assertEqual(EveType._eve_universe_meta_attr("esi_pk"), "type_id")

    def test_eve_universe_meta_attr_2(self):
        """When not defined, then return None"""
        self.assertIsNone(EveType._eve_universe_meta_attr("undefined_param"))

    def test_eve_universe_meta_attr_3(self):
        """When not defined and is_mandatory, then raise exception"""
        with self.assertRaises(ValueError):
            EveType._eve_universe_meta_attr_strict("undefined_param")

    def test_eve_universe_meta_attr_4(self):
        """When EveUniverseMeta class not defined, then return None"""
        self.assertIsNone(
            EveUniverseBaseModel._eve_universe_meta_attr("undefined_param")
        )
