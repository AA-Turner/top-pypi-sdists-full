# type: ignore
"""Tools for generating fixtures from production data for Eve Universe models."""

import json
import logging
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path
from typing import Iterable, List, NamedTuple, Optional, Union

from django.core.serializers.json import DjangoJSONEncoder

from eveuniverse import __title__
from eveuniverse.core.esitools import is_esi_online
from eveuniverse.models import EveSolarSystem, EveStargate
from eveuniverse.models.base import EveUniverseBaseModel
from eveuniverse.utils import LoggerAddTag

logger = LoggerAddTag(logging.getLogger(__name__), __title__)


class ModelSpec(NamedTuple):
    """A ModelSpec class defines what objects are to be loaded as test data.

    Args:
        model_name: Name of Eve Universe model
        ids: List of Eve IDs to be loaded
        include_children: Whether to also load children of those objects
        enabled_sections: Sections to load regardless of current settings,
            e.g. `[EveType.Section.DOGMAS]` will always load dogmas for EveTypes
    """

    model_name: str
    ids: List[int]
    include_children: bool = False
    enabled_sections: Optional[Iterable[str]] = None


def create_testdata(spec: List[ModelSpec], filepath: Union[str, Path]) -> None:
    """Loads eve data from ESI as defined by spec and dumps it to file as JSON

    Args:
        spec: Specification of which Eve objects to load.
        The specification can contain the same model more than once.
        filepath: absolute path of where to store the resulting JSON file
    """

    _clear_database()
    print()

    _check_if_esi_is_available()
    _load_data_per_spec(spec)
    _dump_all_data_into_file(Path(filepath))


def _clear_database():
    for model_class in EveUniverseBaseModel.all_models():
        if model_class.__name__ != "EveUnit":
            model_class.objects.all().delete()


def _check_if_esi_is_available():
    print("Initializing ESI client ...")
    if not is_esi_online():
        raise RuntimeError("ESI not online")


def _load_data_per_spec(spec: List[ModelSpec]):
    num = 0
    for model_spec in spec:
        num += 1
        ids = set(model_spec.ids)
        print(
            f"Loading {num}/{len(spec)}: {model_spec.model_name} with "
            f"{len(ids)} objects",
            end="",
        )
        model_class = EveUniverseBaseModel.get_model_class(model_spec.model_name)
        for id in ids:
            print(".", end="")
            model_class.objects.get_or_create_esi(
                id=id,
                include_children=model_spec.include_children,
                wait_for_children=True,
                enabled_sections=model_spec.enabled_sections,
            )
        print()


def _dump_all_data_into_file(filepath: Path):
    data = OrderedDict()
    for model_class in EveUniverseBaseModel.all_models():
        if model_class.objects.count() > 0 and model_class.__name__ != "EveUnit":
            logger.info(
                "Collecting %d rows for %s",
                model_class.objects.count(),
                model_class.__name__,
            )
            my_data = list(model_class.objects.all().values())
            for row in my_data:
                try:
                    del row["last_updated"]
                except KeyError:
                    pass

            data[model_class.__name__] = my_data

    print(f"Writing testdata to: {filepath}")
    with filepath.open("w", encoding="utf-8") as file:
        json.dump(data, file, cls=DjangoJSONEncoder, indent=4, sort_keys=True)


def load_testdata_from_dict(testdata: dict) -> None:
    """Create eve objects in the database from testdata dump given as dict.

    Args:
        testdata: The dict containing the testdata as created by `create_testdata()`
    """
    for model_class in EveUniverseBaseModel.all_models():
        model_name = model_class.__name__
        if model_name in testdata:
            if model_class.__name__ == "EveStargate":
                _process_eve_stargate(testdata, model_class, model_name)
            else:
                _process_other_model(testdata, model_class, model_name)


def _process_other_model(testdata, model_class, model_name):
    entries = [model_class(**obj) for obj in testdata[model_name]]
    model_class.objects.bulk_create(entries, batch_size=500)


def _process_eve_stargate(testdata, model_class, model_name):
    for _ in range(2):
        for obj in deepcopy(testdata[model_name]):
            try:
                EveStargate.objects.get(id=obj["destination_eve_stargate_id"])
            except EveStargate.DoesNotExist:
                del obj["destination_eve_stargate_id"]
                obj["destination_eve_stargate"] = None

            try:
                EveSolarSystem.objects.get(id=obj["destination_eve_solar_system_id"])
            except EveSolarSystem.DoesNotExist:
                del obj["destination_eve_solar_system_id"]
                obj["destination_eve_solar_system"] = None

            id = obj["id"]
            del obj["id"]
            model_class.objects.update_or_create(id=id, defaults=obj)


def load_testdata_from_file(filepath: Union[str, Path]) -> None:
    """Create eve objects in the database from testdata dump given as JSON file.

    Args:
        filepath: Absolute path to the JSON file containing the testdata
        created by `create_testdata()`
    """
    my_filepath = Path(filepath)
    with my_filepath.open("r", encoding="utf-8") as file:
        testdata = json.load(file)

    load_testdata_from_dict(testdata)
