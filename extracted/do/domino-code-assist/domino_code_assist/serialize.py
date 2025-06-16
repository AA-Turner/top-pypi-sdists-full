import json

import domino_code_assist.actions_store as actions_store
import domino_code_assist.viz.state

from . import action, crossfilter_widgets
from .settings import settings


class AEncoder(json.JSONEncoder):
    def default(self, obj):
        encoded = action.to_json(obj)
        if not encoded:
            encoded = actions_store.to_json(obj)
        if not encoded:
            encoded = crossfilter_widgets.to_json(obj)
        if not encoded:
            encoded = domino_code_assist.viz.state.to_json(obj)
        if not encoded:
            encoded = domino_code_assist.automl.store.to_json(obj)
        if not encoded:
            encoded = domino_code_assist.foundation_models.store.to_json(obj)
        return encoded if encoded else json.JSONEncoder.default(self, obj)


def from_json(dct):
    decoded = action.from_json(dct)
    if not decoded:
        decoded = actions_store.from_json(dct)
    if not decoded:
        decoded = domino_code_assist.viz.state.from_json(dct)
    if not decoded:
        decoded = crossfilter_widgets.from_json(dct)
    if not decoded:
        decoded = domino_code_assist.automl.store.from_json(dct)
    if not decoded:
        decoded = domino_code_assist.foundation_models.store.from_json(dct)
    return decoded if decoded else dct


def dumps(value):
    return json.dumps(value, cls=AEncoder)


def loads(str):
    try:
        data = json.loads(str, object_hook=from_json)
        # convert previously stored action list to action state
        if type(data) is list and len(data) > 0 and isinstance(data[0], action.Action):
            data = actions_store.ActionsState(preview=True, actions=data)
        return data
    except Exception as e:
        if settings.domino_code_assist_dev:
            raise e
