import inspect
import json
from collections import namedtuple
from pathlib import Path
from typing import Optional
from unittest.mock import Mock

from bravado.exception import HTTPNotFound

from eveuniverse import models as eveuniverse_models

_current_folder = Path(__file__).parent


"""
Helpers for stubbing ESI calls
"""


class BravadoOperationStub:
    """Stub to simulate the operation object return from bravado via django-esi"""

    class RequestConfig:
        def __init__(self, also_return_response):
            self.also_return_response = also_return_response

    class ResponseStub:
        def __init__(self, headers):
            self.headers = headers

    def __init__(
        self, data, headers: Optional[dict] = None, also_return_response: bool = False
    ):
        self._data = data
        self._headers = headers if headers else {"x-pages": 1}
        self.request_config = BravadoOperationStub.RequestConfig(also_return_response)

    def result(self, **kwargs):
        if self.request_config.also_return_response:
            return [self._data, self.ResponseStub(self._headers)]
        else:
            return self._data

    def results(self, **kwargs):
        return self.result(**kwargs)


class EsiRoute:
    def __init__(self, category, method, primary_key=None):
        self._category = category
        self._method = method
        self._primary_key = primary_key

    def call(self, **kwargs):
        pk_value = None
        try:
            if self._primary_key:
                if self._primary_key not in kwargs:
                    raise ValueError(
                        f"{self._category}.{self._method}: Missing primary key: "
                        f"{self._primary_key}"
                    )
                pk_value = str(kwargs[self._primary_key])
                result = esi_data[self._category][self._method][pk_value]

            elif self._category == "Universe" and self._method == "post_universe_names":
                result = []
                for id in kwargs["ids"]:
                    if str(id) in esi_data[self._category][self._method]:
                        result.append(esi_data[self._category][self._method][str(id)])
                    else:
                        raise HTTPNotFound(Mock(**{"status_code": 404}))

            elif self._category == "Universe" and self._method == "post_universe_ids":
                result = {
                    "agents": None,
                    "alliances": None,
                    "characters": None,
                    "constellations": None,
                    "corporations": None,
                    "factions": None,
                    "inventory_types": None,
                    "regions": None,
                    "stations": None,
                    "systems": None,
                }
                for name in kwargs["names"]:
                    if name in esi_data[self._category][self._method]:
                        result.update(esi_data[self._category][self._method][name])

            else:
                if len(kwargs) > 0:
                    raise ValueError(
                        f"{self._method} does not have parameter {kwargs.popitem()[0]}"
                    )
                result = esi_data[self._category][self._method]

        except KeyError:
            raise KeyError(
                f"{self._category}.{self._method}: No test data for "
                f"{self._primary_key} = {pk_value}"
            ) from None

        return BravadoOperationStub(result)


class EsiClientStub:
    @classmethod
    def _generate(cls):
        """Dynamically generate the client class with all attributes based on definition."""
        EsiEndpoint = namedtuple("EsiSpec", ["category", "method", "key"])
        esi_endpoints = [
            EsiEndpoint("Dogma", "get_dogma_attributes_attribute_id", "attribute_id"),
            EsiEndpoint("Dogma", "get_dogma_effects_effect_id", "effect_id"),
            EsiEndpoint(
                "Market", "get_markets_groups_market_group_id", "market_group_id"
            ),
            EsiEndpoint("Market", "get_markets_prices", None),
            EsiEndpoint("Status", "get_status", None),
            EsiEndpoint("Universe", "get_universe_ancestries", None),
            EsiEndpoint(
                "Universe",
                "get_universe_asteroid_belts_asteroid_belt_id",
                "asteroid_belt_id",
            ),
            EsiEndpoint("Universe", "get_universe_bloodlines", None),
            EsiEndpoint("Universe", "get_universe_categories", None),
            EsiEndpoint(
                "Universe", "get_universe_categories_category_id", "category_id"
            ),
            EsiEndpoint(
                "Universe",
                "get_universe_constellations_constellation_id",
                "constellation_id",
            ),
            EsiEndpoint("Universe", "get_universe_factions", None),
            EsiEndpoint("Universe", "get_universe_graphics_graphic_id", "graphic_id"),
            EsiEndpoint("Universe", "get_universe_groups", None),
            EsiEndpoint("Universe", "get_universe_groups_group_id", "group_id"),
            EsiEndpoint("Universe", "get_universe_moons_moon_id", "moon_id"),
            EsiEndpoint("Universe", "get_universe_moons_moon_id", "moon_id"),
            EsiEndpoint("Universe", "get_universe_planets_planet_id", "planet_id"),
            EsiEndpoint("Universe", "get_universe_races", None),
            EsiEndpoint("Universe", "get_universe_regions", None),
            EsiEndpoint("Universe", "get_universe_regions_region_id", "region_id"),
            EsiEndpoint(
                "Universe", "get_universe_stargates_stargate_id", "stargate_id"
            ),
            EsiEndpoint("Universe", "get_universe_stars_star_id", "star_id"),
            EsiEndpoint("Universe", "get_universe_stations_station_id", "station_id"),
            EsiEndpoint("Universe", "get_universe_systems", None),
            EsiEndpoint("Universe", "get_universe_systems_system_id", "system_id"),
            EsiEndpoint("Universe", "get_universe_types_type_id", "type_id"),
            EsiEndpoint("Universe", "get_universe_types", None),
            EsiEndpoint("Universe", "post_universe_names", None),
            EsiEndpoint("Universe", "post_universe_ids", None),
        ]
        for endpoint in esi_endpoints:
            if not hasattr(cls, endpoint.category):
                setattr(cls, endpoint.category, type(endpoint.category, (object,), {}))
            my_category = getattr(cls, endpoint.category)
            if not hasattr(my_category, endpoint.method):
                setattr(
                    my_category,
                    endpoint.method,
                    EsiRoute(endpoint.category, endpoint.method, endpoint.key).call,
                )


EsiClientStub._generate()


def _load_esi_data():
    path = _current_folder / "esi_data.json"
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    # generate list endpoints from existing test data
    entity_classes = [
        model_class
        for model_class in [
            x[1] for x in inspect.getmembers(eveuniverse_models, inspect.isclass)
        ]
        if hasattr(model_class, "_EveUniverseMeta")
        and hasattr(model_class, "_is_list_only_endpoint")
        and not model_class._is_list_only_endpoint()
        and model_class._has_esi_path_list()
    ]
    for entity_class in entity_classes:
        list_category, list_method = entity_class._esi_path_list()
        object_category, object_method = entity_class._esi_path_object()
        data[list_category][list_method] = [
            int(x) for x in data[object_category][object_method].keys()
        ]

    return data


esi_data = _load_esi_data()
