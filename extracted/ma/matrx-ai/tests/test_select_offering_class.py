"""select_offering answers "which offering runs this call" by the CLASS rule.

Live shape (2026-10-01): Qwen3.8 27B is one model served as Matrx Fast (groq)
and Matrx Lightning (cerebras) — two products. A reader that needs the offering
a pinned run uses (its controls, its provider model id) must get the pinned
class's offering, never the model's preferred one."""

from __future__ import annotations

import pytest

from matrx_ai.catalog.errors import CatalogRoutingError
from matrx_ai.catalog.models import CatalogOffering
from matrx_ai.catalog.resolve import select_offering

FAST, LIGHTNING = "ep-fast", "ep-lightning"
OFFERINGS = [
    CatalogOffering(id="fast-1", model_id="m", endpoint_id=FAST, api_id="a", provider_model_id="qwen-fast", priority=100),
    CatalogOffering(id="light-1", model_id="m", endpoint_id=LIGHTNING, api_id="b", provider_model_id="qwen-light", priority=110),
]
PARKED_LIGHT = CatalogOffering(
    id="light-0", model_id="m", endpoint_id=LIGHTNING, api_id="b", provider_model_id="qwen-light-old", priority=90, is_available=False
)
OTHER_MODEL = CatalogOffering(id="x-1", model_id="other", endpoint_id=FAST, api_id="a", provider_model_id="x", priority=1)


class _Manager:
    def __init__(self, offerings):
        self._offerings = offerings

    def offerings_for(self, model_id):
        return [o for o in self._offerings if o.model_id == model_id]

    def offering(self, offering_id):
        return next((o for o in [*OFFERINGS, PARKED_LIGHT, OTHER_MODEL] if o.id == offering_id), None)

    def endpoint(self, endpoint_id):
        return None


def test_unpinned_runs_the_preferred_class():
    assert select_offering("m", manager=_Manager(OFFERINGS)).id == "fast-1"


def test_pinned_lightning_runs_lightning():
    assert select_offering("m", "light-1", manager=_Manager(OFFERINGS)).provider_model_id == "qwen-light"


def test_parked_pin_runs_its_own_class_never_another():
    assert select_offering("m", "light-0", manager=_Manager(OFFERINGS)).id == "light-1"


def test_pin_of_another_model_raises():
    with pytest.raises(CatalogRoutingError):
        select_offering("m", "x-1", manager=_Manager(OFFERINGS))


def test_pinned_class_with_nothing_available_raises_never_substitutes():
    with pytest.raises(CatalogRoutingError):
        select_offering("m", "light-0", manager=_Manager([OFFERINGS[0]]))
