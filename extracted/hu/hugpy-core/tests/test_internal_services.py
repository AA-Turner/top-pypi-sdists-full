"""Hosted requests use real Core routing; only the worker and database are faked."""
import copy
import urllib.request

import pytest
from flask import Flask

from hugpy_core.calllog import call_record
from hugpy_core.relay import internal
from hugpy_core.web import routes


@pytest.fixture
def service(monkeypatch):
    app = Flask(__name__)
    monkeypatch.setattr(internal, '_host_app', app)
    records, sent = [], []
    monkeypatch.setattr(call_record, 'write', lambda row: records.append(copy.deepcopy(row)))
    monkeypatch.setattr(routes, 'pick', lambda *a, **k: {'id': 'worker-1', 'name': 'worker', 'url': 'http://worker'})
    monkeypatch.setattr(routes, 'worker_payload', lambda kw, worker: kw)
    def worker_stream(worker, payload):
        sent.append(payload)
        yield {'type': 'token', 'text': 'direct reply'}
        yield {'type': 'done', 'usage': {}, 'finish_reason': 'stop'}
    monkeypatch.setattr(routes, 'worker_stream', worker_stream)
    def no_http(*args, **kwargs):
        pytest.fail('hosted call attempted HTTP')
    monkeypatch.setattr(urllib.request, 'urlopen', no_http)
    return records, sent


def test_chat_routes_without_request_context_and_logs_parent(service):
    records, sent = service
    with call_record.bound_call({'request_id': 'parent-123'}):
        reply, status = internal.chat({'model': 'model', 'messages': [{'role': 'user', 'content': 'hi'}],
                                      'metadata': {'intent': 'help-agent'}, 'max_tokens': 12}, caller='help')
    assert status == 200
    assert reply['choices'][0]['message']['content'] == 'direct reply'
    assert sent[0]['metadata']['intent'] == 'help-agent'
    assert records[0]['request_params']['parent_request_id'] == 'parent-123'
    assert records[-1]['call_state'] == 'done'
    assert records[-1]['caller'] == 'help'


def test_help_uses_same_router_and_preserves_model_reply(service):
    from hugpy_core.help.help_routes import _relay_chat
    text, model = _relay_chat('model', [{'role': 'user', 'content': 'help'}], 'operator')
    assert (text, model) == ('direct reply', 'model')
    assert service[0][-1]['caller'] == 'help'


def test_discord_uses_direct_router(service):
    from hugpy_core.discord.discord_routes import _relay_chat
    assert _relay_chat('model', [{'role': 'user', 'content': 'hello'}]) == 'direct reply'
    assert service[0][-1]['caller'] == 'discord'


def test_worker_failure_is_recorded_and_returned(service, monkeypatch):
    def failure(*args):
        yield {'type': 'error', 'message': 'worker offline'}
    monkeypatch.setattr(routes, 'worker_stream', failure)
    result, status = internal.chat({'model': 'model', 'messages': [{'role': 'user', 'content': 'hi'}]})
    assert status >= 400
    assert 'worker offline' in str(result['error'])
    assert service[0][-1]['call_state'] == 'failed'


def test_hosted_prompt_preserves_text_and_generation_options(service):
    result = internal.execute_prompt(task='text-generation', model_key='model', prompt='hello',
                                     max_new_tokens=17, temperature=0, caller='media')
    assert result['ok'] and result['text'] == 'direct reply'
    assert service[1][0]['messages'][0]['content'] == 'hello'
    assert service[1][0]['max_new_tokens'] == 17
    assert service[1][0]['temperature'] == 0


def test_engine_sources_do_not_fetch_http_or_disk(service, monkeypatch):
    from hugpy_engine.config.models import models_config as models
    monkeypatch.setattr(models, '_catalog_source', lambda: [{'id': 'model'}])
    monkeypatch.setattr(models, '_bindings_source', lambda: {'text-generation': 'model'})
    monkeypatch.setattr(models, '_LAST_CATALOG', [])
    monkeypatch.setattr(models, '_bindings', {})
    assert models._fetch_catalog() == [{'id': 'model'}]
    assert models.task_bindings(force=True) == {'text-generation': 'model'}
    monkeypatch.setattr(models, '_catalog_source', lambda: [])
    assert models._fetch_catalog() == []


def test_hosted_media_uses_injected_executor_and_catalog(service, monkeypatch):
    from hugpy_media import host
    monkeypatch.setattr(host, '_executor', lambda **kw: internal.execute_prompt(caller='media', **kw))
    monkeypatch.setattr(host, '_catalog', lambda: [{'id': 'model'}])
    monkeypatch.setattr(host, '_central_catalog', lambda: [])
    from hugpy_media.imports import execute_prompt
    assert execute_prompt(task='text-generation', model='model', prompt='hi')['text'] == 'direct reply'
    assert host.catalog_models() == [{'id': 'model'}]
    assert host.central_models() == []


def test_host_failure_never_falls_back_to_network(service, monkeypatch):
    from hugpy_media import host
    def failed(**kwargs):
        raise RuntimeError('host failed')
    monkeypatch.setattr(host, '_executor', failed)
    with pytest.raises(RuntimeError, match='host failed'):
        host.execute_prompt(prompt='hi')


def test_startup_wires_video_and_media_including_catalog_and_observer(service, monkeypatch):
    from hugpy_core.relay import hosted, inference_catalog, video_transport
    from hugpy_video.intel import plane
    from hugpy_media import host
    for module, names in ((plane, ('_task_executor', '_prompt_executor', '_model_task_source',
                                  '_model_catalog_source', '_text_model_source', '_task_observer')),
                          (host, ('_executor', '_catalog', '_central_catalog'))):
        for name in names:
            monkeypatch.setattr(module, name, None)
    monkeypatch.setattr(inference_catalog, 'model_tasks', lambda key: {'text-generation'})
    monkeypatch.setattr(inference_catalog, 'video_models', lambda: {'video-model': 'facts'})
    monkeypatch.setattr(inference_catalog, 'text_models', lambda: [{'model': 'model'}])
    observed = []
    monkeypatch.setattr(video_transport, 'observe_task', lambda rid, path: observed.append((rid, path)) or {'progress': 0.5})
    hosted.configure_arms(internal.application())
    from hugpy_video.imports.init_imports import execute_prompt
    assert execute_prompt(task='text-generation', model='model', prompt='hi')['text'] == 'direct reply'
    assert service[0][-1]['caller'] == 'video'
    assert plane.known_model_tasks('model') == {'text-generation'}
    assert plane.catalog_models() == {'video-model': 'facts'}
    assert plane.text_models() == [{'model': 'model'}]
    assert plane.task_observation_source('job-1')('/v1/telemetry/state') == {'progress': 0.5}
    assert observed == [('job-1', '/v1/telemetry/state')]
    assert host.execute_prompt(task='text-generation', model='model', prompt='hi')['text'] == 'direct reply'
    assert service[0][-1]['caller'] == 'media'


def test_task_dispatch_only_contacts_selected_worker(service, monkeypatch):
    import io
    import json
    from hugpy_core.relay import taskrelay
    from hugpy_core.registry import transport
    monkeypatch.setattr(taskrelay, 'pick', lambda *a, **k: {'id': 'worker-1', 'name': 'worker', 'url': 'http://selected-worker'})
    monkeypatch.setattr(transport, 'headers', lambda worker, headers: headers)
    requests = []
    class Reply(io.BytesIO):
        status = 200
        headers = {'Content-Type': 'application/json'}
    def worker_only(request, **kwargs):
        assert request.full_url == 'http://selected-worker/v1/images/generations'
        requests.append(json.loads(request.data))
        return Reply(b'{"data":[{"b64_json":"image-bytes"}]}')
    monkeypatch.setattr(urllib.request, 'urlopen', worker_only)
    result = internal.execute_prompt(task='text-to-image', model='image-model', prompt='red square',
                                     request_id='video-123', alloc={'worker': 'worker'},
                                     knobs={'ctx_pct': 0}, caller='video')
    assert result.ok
    assert requests[0]['prompt'] == 'red square'
    assert requests[0]['knobs'] == {'ctx_pct': 0}
    assert requests[0]['alloc'] == {'worker': 'worker'}
    assert service[0][0]['request_params']['parent_request_id'] == 'video-123'
    assert service[0][-1]['call_state'] == 'done'


def test_media_summary_uses_host_without_http(service, monkeypatch):
    from hugpy_media import host, toolset
    monkeypatch.setattr(host, '_executor', lambda **kw: internal.execute_prompt(caller='media', **kw))
    result = toolset.summarize('The council approved a new park on Tuesday.', model='model')
    assert 'direct reply' in str(result)
    assert service[0][-1]['caller'] == 'media'


def test_request_context_parent_is_preserved(service):
    from flask import g
    app = internal.application()
    with app.test_request_context('/api/media/summarize'):
        g.call_row = {'request_id': 'http-parent'}
        internal.chat({'model': 'model', 'messages': [{'role': 'user', 'content': 'hi'}]})
    assert service[0][0]['request_params']['parent_request_id'] == 'http-parent'


def test_openai_token_limit_is_not_replaced_by_builder_default(service):
    internal.execute_prompt(model='model', prompt='hi', task='text-generation', max_tokens=23)
    assert service[1][0]['max_new_tokens'] == 23
    assert not service[1][0].get('unbounded')


@pytest.mark.parametrize(('auth', 'scope', 'allowed'), [
    ('Bearer valid', 'use', True), ('bearer admin', 'admin', True),
    ('Bearer wrong-scope', 'install', False), ('Bearer revoked', None, False),
    ('', 'admin', False), ('Basic token', 'admin', False),
])
def test_direct_key_validation_has_same_scope_rules(service, monkeypatch, auth, scope, allowed):
    from hugpy_core.web import api_access
    monkeypatch.setattr(api_access.routing.KEYS, 'scope_of', lambda token: scope)
    assert api_access.valid_use_authorization(auth) is allowed
    with internal.application().test_request_context(headers={'Authorization': auth}):
        response = internal.application().make_response(api_access.verify_use_key())
        assert response.status_code == (204 if allowed else 401)
