"""Structured preferences survive routing and distinguish resident requests."""
import asyncio
import json
from types import SimpleNamespace

import pytest
from aiohttp import ClientSession, web
from aiohttp.test_utils import TestClient, TestServer

from hugpy_core.router.core.decide import _contract_ok
from hugpy_core.router.core.types import Box, CallSpec
from hugpy_core.router.serve.proxy import execution_request, handle
from hugpy_core.router.serve.keys import CONTRACTS, REGISTRY, SESSION
from hugpy_core.router.observability import store


def request(knobs):
    return execution_request(json.dumps({'model': 'model', 'knobs': knobs}).encode(), 'application/json')


def test_key_order_is_irrelevant_but_ordered_preferences_are_not():
    a = request({'ctx_pct': 25, 'auto_preferences': {'order': ['gpu-only', 'moe']}})
    b = request({'auto_preferences': {'order': ['gpu-only', 'moe']}, 'ctx_pct': 25})
    c = request({'ctx_pct': 25, 'auto_preferences': {'order': ['moe', 'gpu-only']}})
    assert a.contract_key == b.contract_key
    assert a.contract_key != c.contract_key
    document = a.execution_request()
    document['knobs']['ctx_pct'] = 100
    assert a.execution_request()['knobs']['ctx_pct'] == 25


@pytest.mark.parametrize('knobs', [[], False, 0, 'gpu-only'])
def test_invalid_preferences_are_not_silently_defaulted(knobs):
    with pytest.raises(ValueError, match='JSON object'):
        request(knobs)


def test_resident_shortcut_requires_known_matching_preferences():
    box = Box('worker')
    first, changed = request({'ctx_pct': 25}), request({'ctx_pct': 100})
    assert not _contract_ok(box, CallSpec('model'), {})
    assert not _contract_ok(box, first, {('worker', 'model'): None})
    assert _contract_ok(box, first, {('worker', 'model'): first.contract_key})
    assert not _contract_ok(box, changed, {('worker', 'model'): first.contract_key})
    assert _contract_ok(box, CallSpec('model'), {('worker', 'model'): None})


def test_suffix_and_worker_pin_remain_compatible():
    call = execution_request(b'{"model":"model@ram-only","alloc":{"worker":" worker "}}', 'application/json')
    assert (call.model, call.options, call.pin) == ('model', 'ram-only', 'worker')
    assert call.execution_request()['knobs'] == {}


def test_http_relay_preserves_preferences_and_records_structured_receipt(monkeypatch):
    receipts = []
    monkeypatch.setattr(store, 'KEYS', SimpleNamespace(check=lambda *args: None))
    monkeypatch.setattr(store, 'open_call', lambda *args: None)
    monkeypatch.setattr(store, 'update_call', lambda *args, **kwargs: receipts.append(kwargs))

    async def scenario():
        async def echo(incoming):
            return web.json_response(await incoming.json())
        worker = web.Application()
        worker.router.add_post('/v1/chat/completions', echo)
        async with TestServer(worker) as upstream, ClientSession() as session:
            link = SimpleNamespace(url=str(upstream.make_url('')).rstrip('/'), last_picked=0,
                                   headers=lambda: {})
            box = Box('worker', models=frozenset(['model']))
            registry = SimpleNamespace(boxes=lambda: [box], link=lambda _: link)
            app = web.Application()
            app[REGISTRY], app[CONTRACTS], app[SESSION] = registry, {}, session
            app.router.add_post('/v1/chat/completions', handle)
            async with TestClient(TestServer(app)) as client:
                knobs = {'auto_preferences': {'order': ['ram-swap', 'disk_mmap-max']},
                         'swap_cap_gib': 0, 'ctx_range_enabled': False}
                response = await client.post('/v1/chat/completions', json={
                    'model': 'model', 'messages': [], 'knobs': knobs,
                    'metadata': {'intent': 'smoke-test'}})
                assert response.status == 200
                assert (await response.json())['knobs'] == knobs
                assert app[CONTRACTS][('worker', 'model')] == (*request(knobs).contract_key, None)
                decision = next(r['decision'] for r in receipts if 'decision' in r)
                assert decision['execution_request']['knobs'] == knobs
                assert decision['execution_request']['version'] == 1
    asyncio.run(scenario())


def test_expired_selected_observation_is_refused_before_forwarding(monkeypatch):
    receipts = []
    monkeypatch.setattr(store, 'KEYS', SimpleNamespace(check=lambda *args: None))
    monkeypatch.setattr(store, 'open_call', lambda *args: None)
    monkeypatch.setattr(store, 'update_call', lambda *args, **kwargs: receipts.append(kwargs))

    async def scenario():
        async def forbidden_forward(*args, **kwargs):
            raise AssertionError('stale observations must not be dispatched')
        samples = iter([[Box('worker', models=frozenset(['model']))],
                        [Box('worker', online=False, models=frozenset(['model']))]])
        link = SimpleNamespace(url='http://unused', headers=lambda: {}, last_picked=0)
        app = web.Application()
        app[REGISTRY] = SimpleNamespace(boxes=lambda: next(samples), link=lambda _: link)
        app[CONTRACTS] = {}
        app[SESSION] = SimpleNamespace(post=forbidden_forward)
        app.router.add_post('/v1/chat/completions', handle)
        async with TestClient(TestServer(app)) as client:
            response = await client.post('/v1/chat/completions', json={'model': 'model'})
            assert response.status == 503
            assert (await response.json())['error']['type'] == 'stale_observation'
        assert receipts[-1]['state'] == 'refused'
    asyncio.run(scenario())
