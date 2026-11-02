"""brain route registration (abstract_flask ``register_categories`` convention).

One blueprint for the brain evaluation surface (``brain.py``) and the
model-group store (``model_groups.py``). The handlers LIVE in those modules as
plain functions (kwargs in, JSON-able out); this module only states the URL
tree and registers it. Dict nesting is the path; the ``""`` key is the node's
own index route.
"""
from __future__ import annotations

from abstract_flask import get_bp, register_categories, spec
from hugpy_core.brain import simulation

from hugpy_core.brain.brain import brain_evaluate, brain_status
from hugpy_core.brain.model_groups import (
    model_groups_allocate,
    model_groups_create,
    model_groups_delete,
    model_groups_list,
    model_groups_resolve,
    model_groups_update,
)

brain_bp, logger = get_bp("brain_bp", __name__)

ALL_CATEGORIES = {
    "llm": {
        "simulation": {
            "catalog": spec(simulation.catalog, 'GET', response='native'),
            "run": spec(simulation.run, 'POST', response='native'),
            "templates": {
                "": spec(simulation.templates, 'GET', response='native'),
                "save": spec(simulation.save_template, 'POST', response='native'),
                "delete": spec(simulation.delete_template, 'POST', response='native'),
            },
        },
        "brain": {
            "": brain_status,                    # /llm/brain
            "evaluate": brain_evaluate,          # /llm/brain/evaluate
        },
        "model-groups": {
            "": model_groups_list,               # /llm/model-groups
            "resolve": model_groups_resolve,     # /llm/model-groups/resolve?key=
            "create": model_groups_create,       # /llm/model-groups/create
            "update": model_groups_update,       # /llm/model-groups/update {group_id, ...}
            "delete": model_groups_delete,       # /llm/model-groups/delete {group_id}
            "allocate": model_groups_allocate,   # /llm/model-groups/allocate {group_id}
        },
    },
}
register_categories(brain_bp, ALL_CATEGORIES)
