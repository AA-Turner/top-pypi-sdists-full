"""Core relays a Wrapper's own configuration to Fleet: reads pass through, and a declared attribution
or layer pin is answered only when the owning Wrapper's readback carries it."""
from urllib.parse import parse_qsl

import pytest

from hugpy_core.registry import model_browser


class FakeWrapper:
    """A Wrapper's attributions and layer-placement routes over an in-memory store."""

    def __init__(self):
        self.rows, self.pins, self.calls = [], {}, []
        self.drop_writes = False

    def request(self, worker, path, body=None):
        self.calls.append((path, body))
        route, _, query = path.partition('?')
        params = dict(parse_qsl(query))
        if route == '/v1/attributions' and body is None:
            return {'worker': 'ae', 'device': 'host:ae', 'model_uid': params.get('model_uid') or 'owner/repo',
                    'attributions': list(self.rows), 'queries': []}
        if route == '/v1/attributions':
            identity = (body['attribute'], body.get('source') or 'operator', body.get('device') or 'host:ae', body.get('unit_id') or '')
            kept = [r for r in self.rows if (r['attribute'], r['source'], r['device'], r['unit_id']) != identity]
            if body.get('retract'):
                if not self.drop_writes:
                    self.rows = kept
                return {'retracted': len(self.rows) - len(kept)}
            row = dict(zip(('attribute', 'source', 'device', 'unit_id'), identity), value=body['value'], model_uid='owner/repo')
            if not self.drop_writes:
                self.rows = kept + [row]
            return row
        if route == '/v1/attributions/derive':
            return {'derived': []}
        if route == '/v1/placements/layers':
            if body and body.get('layer_tiers') is not None and not self.drop_writes:
                for layer, components in body['layer_tiers'].items():
                    self.pins[layer] = {**self.pins.get(layer, {}), **components}
            rows = []
            for ordinal in range(2):
                for component, tier in (('non_expert', 'gpu:GPU-1'), ('expert', 'gpu:GPU-1' if ordinal == 0 else 'ram')):
                    pinned = self.pins.get(f'blk.{ordinal}', {}).get(component) or self.pins.get('*', {}).get(component)
                    rows.append({'fill_rank': len(rows) + 1, 'layer_ordinal': ordinal, 'layer_key': f'blk.{ordinal}',
                                 'component': component, 'bytes': 100, 'tier': pinned or tier,
                                 'tier_source': 'declared:layer_tiers' if pinned else 'spill:non-experts-first'})
            return {'plan_id': 'u1|stored|host:ae|None', 'unit_id': 'u1', 'tiers': [], 'bytes_by_tier': {}, 'layers': rows}
        if route == '/v1/evictions/decisions':
            return {'worker': 'ae', 'decisions': [], 'limit': params.get('limit')}
        if route == '/v1/sql/queries':
            return {'queries': [], 'receipts': []}
        if route == '/v1/sql/query':
            return {'name': body['name'], 'rows': []}
        raise AssertionError('unexpected Wrapper path ' + path)


@pytest.fixture
def wrapper(monkeypatch):
    fake = FakeWrapper()
    monkeypatch.setattr(model_browser, 'target', lambda worker_id: {'name': worker_id, 'url': 'http://worker:1', 'key': 'k'})
    monkeypatch.setattr(model_browser, 'request', fake.request)
    return fake


def test_declarations_and_pins_count_only_with_the_wrapper_readback(wrapper):
    result = model_browser.declare_attribution('ae', model_key='repo', attribute='context_window', value=4096)
    assert result['source'] == 'wrapper' and result['model_uid'] == 'owner/repo'
    assert result['readback'] == [{'attribute': 'context_window', 'source': 'operator', 'device': 'host:ae', 'unit_id': '',
                                   'value': 4096, 'model_uid': 'owner/repo'}]
    assert wrapper.calls[0] == ('/v1/attributions', {'attribute': 'context_window', 'value': 4096, 'retract': False,
                                                     'source': 'operator', 'model_key': 'repo'})
    assert model_browser.attributions('ae', model_key='repo')['attributions'][0]['value'] == 4096
    gone = model_browser.declare_attribution('ae', model_key='repo', attribute='context_window', retract=True)
    assert gone['source'] == 'wrapper' and gone['readback'] == []

    plan = model_browser.pin_layers('ae', model_key='repo', layer_tiers={'blk.0': {'expert': 'ram'}, '*': {'non_expert': 'gpu:GPU-1'}})
    assert plan['source'] == 'wrapper'
    placed = {(row['layer_key'], row['component']): row for row in plan['layers']}
    assert placed[('blk.0', 'expert')]['tier'] == 'ram' and placed[('blk.0', 'expert')]['tier_source'] == 'declared:layer_tiers'
    assert placed[('blk.1', 'non_expert')]['tier_source'] == 'declared:layer_tiers'
    assert model_browser.layer_placements('ae', model_key='repo', context='4096')['layers']
    assert wrapper.calls[-1][0] == '/v1/placements/layers?model_key=repo&context=4096'

    # Unconfirmed writes are refused with the reason, sent once, never retried.
    wrapper.drop_writes = True
    before = len(wrapper.calls)
    body, status = model_browser.declare_attribution('ae', model_key='repo', attribute='context_window', value=2048)
    assert status == 502 and 'differs' in body['error']
    assert sum(1 for path, sent in wrapper.calls[before:] if sent) == 1
    body, status = model_browser.pin_layers('ae', model_key='repo', layer_tiers={'blk.1': {'expert': 'swap'}})
    assert status == 502 and 'does not carry the pin' in body['error']
    body, status = model_browser.pin_layers('ae', model_key='repo', layer_tiers={'blk.9': {'expert': 'swap'}})
    assert status == 502 and 'no expert component for blk.9' in body['error']


def test_relay_validates_inputs_before_reaching_the_wrapper(wrapper):
    assert model_browser.attributions('ae')[1] == 400
    assert model_browser.declare_attribution('ae', model_key='repo', attribute='  ')[1] == 400
    assert model_browser.declare_attribution('ae', model_key='repo', attribute='x', source='guess')[1] == 400
    assert model_browser.pin_layers('ae', model_key='repo', layer_tiers={})[1] == 400
    assert model_browser.pin_layers('ae', model_key='repo', layer_tiers={'blk.0': 'ram'})[1] == 400
    assert model_browser.run_query('ae', name='')[1] == 400
    assert model_browser.run_query('ae', name='q', params=[1])[1] == 400
    assert wrapper.calls == []
    assert model_browser.run_query('ae', name='resource_room', params={'worker': 'ae'})['name'] == 'resource_room'
    assert model_browser.eviction_decisions('ae', limit='5')['limit'] == '5'
    assert model_browser.derive_attributions('ae') == {'derived': []}
    assert wrapper.calls[-1] == ('/v1/attributions/derive', {})


def test_fleet_reaches_the_configuration_routes_under_the_worker_model_browser():
    from flask import Flask
    from hugpy_core.registry import routes
    app = Flask('check')
    app.register_blueprint(routes.registry_bp)
    rules = {}
    for rule in app.url_map.iter_rules():
        if 'model-browser' in rule.rule:
            rules.setdefault(rule.rule, set()).update(rule.methods & {'GET', 'POST'})
    base = '/fleet/workers/<worker_id>/model-browser/'
    assert rules[base + 'attributions'] == {'GET', 'POST'}
    assert rules[base + 'attributions/derive'] == {'POST'}
    assert rules[base + 'placements'] == {'GET', 'POST'}
    assert rules[base + 'evictions'] == {'GET'}
    assert rules[base + 'queries'] == {'GET'}
    assert rules[base + 'queries/run'] == {'POST'}
