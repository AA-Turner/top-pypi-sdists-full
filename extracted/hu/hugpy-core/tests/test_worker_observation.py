"""Routing telemetry freshness is independent of HTTP health and restart counters."""
import asyncio
import time

import pytest
from aiohttp import ClientSession, web
from aiohttp.test_utils import TestServer

from hugpy_core.router.links.box import BoxLink
from hugpy_core.router.core.types import CallSpec
from hugpy_core.router.core.decide import _contract_ok, decide
from hugpy_core.router.imports.constants import OFFLINE_AFTER_S


def state(epoch='first', generation=3, consistent=True):
    return {'store_id': 'store', 'changes': generation,
            'models': [{'key': 'model'}], 'residents': [{'key': 'model', 'state': 'idle'}],
            'observation': {'schema': 'hugpy.worker-observation', 'version': 1,
                            'worker': 'worker', 'store_id': 'store', 'epoch': epoch,
                            'generation': generation, 'consistent': consistent, 'captured_at': 1}}


def test_health_does_not_refresh_old_resource_observations():
    link = BoxLink('worker', 'http://unused')
    assert link.accept_state(state()) and link.box().online
    link._received_at = time.monotonic() - OFFLINE_AFTER_S - 1
    link.online, link.last_ok = True, time.time()  # /health still answers
    assert not link.box().online
    assert not decide(CallSpec('model'), [link.box()]).ok
    assert not link.accept_state(state())  # unchanged full response refreshes receipt age
    assert link.box().online


def test_restart_with_identical_counter_invalidates_resident_request():
    link = BoxLink('worker', 'http://unused')
    link.accept_state(state())
    call = CallSpec('model')
    contracts = {('worker', 'model'): (*call.contract_key, link.box().observation_identity)}
    assert _contract_ok(link.box(), call, contracts)
    assert link.accept_state(state(epoch='restarted'))
    assert not _contract_ok(link.box(), call, contracts)


def test_inconsistent_snapshot_is_visible_but_not_routable():
    link = BoxLink('worker', 'http://unused')
    link.accept_state(state(consistent=False))
    assert link.state['models']
    assert not link.box().online
    assert link.accept_state(state(consistent=True))
    assert link.box().online


def test_generation_regression_rejected_but_new_epoch_can_reset():
    link = BoxLink('worker', 'http://unused')
    link.accept_state(state(generation=10))
    with pytest.raises(ValueError, match='regressed'):
        link.accept_state(state(generation=2))
    assert link.accept_state(state(epoch='restarted', generation=0))


def test_invalid_envelope_does_not_replace_last_observation():
    link = BoxLink('worker', 'http://unused')
    link.accept_state(state())
    broken = state()
    broken['observation']['store_id'] = 'different-store'
    with pytest.raises(ValueError, match='invalid'):
        link.accept_state(broken)
    assert link.state['observation']['store_id'] == 'store'


def test_legacy_worker_can_route_but_cannot_use_unscoped_completion_as_confirmation():
    link = BoxLink('worker', 'http://unused')
    link.accept_state({'changes': 1, 'models': [{'key': 'model'}]})
    call = CallSpec('model')
    assert decide(call, [link.box()]).ok
    assert not _contract_ok(link.box(), call, {('worker', 'model'): (*call.contract_key, None)})


def test_http_long_poll_carries_epoch_and_notifies_on_restart():
    async def scenario():
        incoming = []
        current = state()
        async def snapshot(request):
            incoming.append(dict(request.query))
            return web.json_response(current)
        async def health(request):
            return web.json_response({'ok': True})
        app = web.Application()
        app.router.add_get('/health', health)
        app.router.add_get('/v1/telemetry/state', snapshot)
        async with TestServer(app) as server, ClientSession() as session:
            link = BoxLink('worker', str(server.make_url('')).rstrip('/'))
            seen = []
            link.on_change.append(lambda updated: seen.append(updated.box().observation_identity))
            await link._run_remote(session)
            current['observation']['epoch'] = 'second'
            await link._run_remote(session)
            assert incoming[0]['since'] == '-1'
            assert incoming[1]['epoch'] == 'first'
            assert seen == [('store', 'first'), ('store', 'second')]
            assert link.version == 2
    asyncio.run(scenario())
