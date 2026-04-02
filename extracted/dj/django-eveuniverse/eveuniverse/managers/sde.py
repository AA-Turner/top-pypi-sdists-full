"""Managers and Querysets for Eve universe models."""

import logging
from abc import ABC, abstractmethod
from urllib.parse import urljoin

import requests
from django.core.cache import cache
from django.db import models

from eveuniverse import __title__
from eveuniverse.app_settings import EVEUNIVERSE_API_SDE_URL
from eveuniverse.utils import LoggerAddTag

logger = LoggerAddTag(logging.getLogger(__name__), __title__)


class _ApiCacheManager(ABC):
    """A base class for adding ability to fetch objects from API with cache."""

    _sde_cache_timeout = 3600 * 24
    _sde_cache_key = ""
    _sde_api_route = ""

    def __init__(self) -> None:
        if not self._sde_cache_key:
            raise ValueError("Cache key not defined")

        if not self._sde_api_route:
            raise ValueError("API route not defined")

    @classmethod
    def _response_to_cache(cls, response: requests.Response) -> dict:
        data_all = {}
        for row in response.json():
            type_id = row["typeID"]
            if type_id not in data_all:
                data_all[type_id] = []
            data_all[type_id].append(row)
        cache.set(
            key=cls._sde_cache_key,
            value=data_all,
            timeout=cls._sde_cache_timeout,
        )
        return data_all

    @classmethod
    def _fetch_sde_data_cached(cls) -> dict:
        data = cache.get(cls._sde_cache_key)
        if not data:
            response = requests.get(
                urljoin(EVEUNIVERSE_API_SDE_URL, "latest/" + cls._sde_api_route),
                timeout=10,
            )
            response.raise_for_status()
            data = cls._response_to_cache(response)
            cache.set(
                key=cls._sde_cache_key,
                value=data,
                timeout=cls._sde_cache_timeout,
            )
        return data

    @abstractmethod
    def update_or_create_api(self, *, eve_type) -> None:
        """Update or create objects from the API for the given eve type."""


class EveTypeMaterialManager(models.Manager, _ApiCacheManager):
    """Custom manager for EveTypeMaterial."""

    _sde_cache_key = "EVEUNIVERSE_TYPE_MATERIALS_REQUEST"
    _sde_cache_timeout = 3600 * 24
    _sde_api_route = "invTypeMaterials.json"

    def update_or_create_api(self, *, eve_type) -> None:
        from eveuniverse.models import EveType

        type_material_data_all = self._fetch_sde_data_cached()
        for type_material_data in type_material_data_all.get(eve_type.id, []):
            material_eve_type, _ = EveType.objects.get_or_create_esi(  # type: ignore
                id=type_material_data.get("materialTypeID")
            )
            self.update_or_create(
                eve_type=eve_type,
                material_eve_type=material_eve_type,
                defaults={
                    "quantity": type_material_data.get("quantity"),
                },
            )


class EveIndustryActivityDurationManager(models.Manager, _ApiCacheManager):
    """Custom manager for EveIndustryActivityDuration."""

    _sde_cache_key = "EVEUNIVERSE_INDUSTRY_ACTIVITY_DURATIONS_REQUEST"
    _sde_cache_timeout = 3600 * 24
    _sde_api_route = "industryActivity.json"  # not related to EveIndustryActivity

    def update_or_create_api(self, *, eve_type) -> None:
        from eveuniverse.models import EveIndustryActivity

        industry_activity_data_all = self._fetch_sde_data_cached()
        for industry_activity_data in industry_activity_data_all.get(eve_type.id, []):
            activity = EveIndustryActivity.objects.get(
                pk=industry_activity_data.get("activityID")
            )
            self.update_or_create(
                eve_type=eve_type,
                activity=activity,
                defaults={
                    "time": industry_activity_data.get("time"),
                },
            )


class EveIndustryActivityMaterialManager(models.Manager, _ApiCacheManager):
    """Custom manager for EveIndustryActivityMaterial."""

    _sde_cache_key = "EVEUNIVERSE_INDUSTRY_ACTIVITY_MATERIALS_REQUEST"
    _sde_cache_timeout = 3600 * 24
    _sde_api_route = "industryActivityMaterials.json"

    def update_or_create_api(self, *, eve_type) -> None:
        from eveuniverse.models import EveIndustryActivity, EveType

        data_all = self._fetch_sde_data_cached()
        activity_data = data_all.get(eve_type.id, {})
        for industry_material_data in activity_data:
            material_eve_type, _ = EveType.objects.get_or_create_esi(  # type: ignore
                id=industry_material_data.get("materialTypeID")
            )
            activity = EveIndustryActivity.objects.get(
                pk=industry_material_data.get("activityID")
            )
            self.update_or_create(
                eve_type=eve_type,
                material_eve_type=material_eve_type,
                activity=activity,
                defaults={
                    "quantity": industry_material_data.get("quantity"),
                },
            )


class EveIndustryActivityProductManager(models.Manager, _ApiCacheManager):
    """Custom manager for EveIndustryActivityProduct."""

    _sde_cache_key = "EVEUNIVERSE_INDUSTRY_ACTIVITY_PRODUCTS_REQUEST"
    _sde_cache_timeout = 3600 * 24
    _sde_api_route = "industryActivityProducts.json"

    def update_or_create_api(self, *, eve_type) -> None:
        from eveuniverse.models import EveIndustryActivity, EveType

        data_all = self._fetch_sde_data_cached()
        activity_data = data_all.get(eve_type.id, {})
        for industry_products_data in activity_data:
            product_eve_type, _ = EveType.objects.get_or_create_esi(  # type: ignore
                id=industry_products_data.get("productTypeID")
            )
            activity = EveIndustryActivity.objects.get(
                pk=industry_products_data.get("activityID")
            )
            self.update_or_create(
                eve_type=eve_type,
                product_eve_type=product_eve_type,
                activity=activity,
                defaults={
                    "quantity": industry_products_data.get("quantity"),
                },
            )


class EveIndustryActivitySkillManager(models.Manager, _ApiCacheManager):
    """Custom manager for EveIndustryActivitySkill."""

    _sde_cache_key = "EVEUNIVERSE_INDUSTRY_ACTIVITY_SKILLS_REQUEST"
    _sde_cache_timeout = 3600 * 24
    _sde_api_route = "industryActivitySkills.json"

    def update_or_create_api(self, *, eve_type) -> None:
        from eveuniverse.models import EveIndustryActivity, EveType

        data_all = self._fetch_sde_data_cached()
        activity_data = data_all.get(eve_type.id, {})
        for industry_skill_data in activity_data:
            skill_eve_type, _ = EveType.objects.get_or_create_esi(  # type: ignore
                id=industry_skill_data.get("skillID")
            )
            activity = EveIndustryActivity.objects.get(
                pk=industry_skill_data.get("activityID")
            )
            self.update_or_create(
                eve_type=eve_type,
                skill_eve_type=skill_eve_type,
                activity=activity,
                defaults={
                    "level": industry_skill_data.get("level"),
                },
            )
