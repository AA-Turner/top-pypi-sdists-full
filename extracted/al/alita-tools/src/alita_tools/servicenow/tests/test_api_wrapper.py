import json
import pytest

from alita_tools.servicenow.api_wrapper import ServiceNowAPIWrapper
from pysnc.record import GlideElement
from langchain_core.tools import ToolException


class DummyElement:
    def __init__(self, value):
        self._value = value
    def get_value(self):
        return self._value


class DummyGR:
    def __init__(self, results=None, exists=True):
        # store results list of dicts
        self._GlideRecord__results = results or []
        self.queries = []
        self.fields = None
        self.limit = None
        self._exists = exists
        self.updated = False

    def add_query(self, *args):
        self.queries.append(args)

    def query(self):
        return None

    def initialize(self):
        return None

    def insert(self):
        # simulate record creation by setting results
        # return self for chaining
        return None

    def get(self, sys_id):
        return self._exists

    def update(self):
        self.updated = True
        return None

    def set_value(self, field, value):
        # simulate setting a field
        setattr(self, field, value)


class DummyClient:
    def __init__(self, gr):
        self._gr = gr
    def GlideRecord(self, table):
        return self._gr


@pytest.fixture(autouse=True)
def patch_client(monkeypatch):
    # Patch ServiceNowAPIWrapper to avoid real client init
    monkeypatch.setattr(ServiceNowAPIWrapper, 'validate_toolkit', classmethod(lambda cls, values: values))
    yield


def test_parse_glide_results_mixed():
    wrapper = ServiceNowAPIWrapper(base_url='u', password='p', username='u')
    # mix of GlideElement and primitive
    recs = [{'a': DummyElement(1), 'b': 'x'}]
    parsed = wrapper.parse_glide_results(recs)
    assert isinstance(parsed, list) and parsed == [{'a': 1, 'b': 'x'}]


def test_get_incidents_success():
    # prepare dummy results
    results = [{'id': DummyElement('id1'), 'desc': DummyElement('d')}]
    gr = DummyGR(results=results)
    client = DummyClient(gr)
    wrapper = ServiceNowAPIWrapper(base_url='u', password='p', username='u')
    wrapper.client = client
    # call get_incidents
    out = wrapper.get_incidents({'description': 'foo', 'number_of_entries': 2})
    # should return JSON string of parsed results
    data = json.loads(out)
    assert data == [{'id': 'id1', 'desc': 'd'}]
    # filter applied
    assert gr.queries and any('description' in q for q in gr.queries)


def test_create_incident_and_update_success():
    # simulate create
    gr_create = DummyGR(results=[{'x': 'y'}])
    client_create = DummyClient(gr_create)
    wrapper = ServiceNowAPIWrapper(base_url='u', password='p', username='u')
    wrapper.client = client_create
    out = wrapper.create_incident({'a': 'b'})
    assert json.loads(out) == [{'x': 'y'}]
    # simulate update found
    gr_update = DummyGR(results=[{'m': 'n'}], exists=True)
    client_update = DummyClient(gr_update)
    wrapper.client = client_update
    out2 = wrapper.update_incident('someid', json.dumps({'c': 'd'}))
    assert json.loads(out2) == [{'m': 'n'}]
    assert gr_update.updated


def test_update_incident_not_found():
    gr = DummyGR(results=[], exists=False)
    client = DummyClient(gr)
    wrapper = ServiceNowAPIWrapper(base_url='u', password='p', username='u')
    wrapper.client = client
    res = wrapper.update_incident('id', '{}')
    assert isinstance(res, ToolException)