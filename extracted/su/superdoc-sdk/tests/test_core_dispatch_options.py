import asyncio
from types import SimpleNamespace

import pytest

from superdoc import SuperDocError, dispatch_superdoc_tool, dispatch_superdoc_tool_async
from superdoc.client import _BoundAsyncRuntime, _BoundSyncRuntime


class RecordingRuntime:
    def __init__(self):
        self.calls = []

    def invoke(self, operation_id, params=None, *, timeout_ms=None, stdin_bytes=None):
        self.calls.append((operation_id, params, timeout_ms, stdin_bytes))
        return {'result': {'success': True, 'marker': params['args']['text']}}


class RecordingAsyncRuntime(RecordingRuntime):
    async def invoke(self, operation_id, params=None, *, timeout_ms=None, stdin_bytes=None):
        return super().invoke(operation_id, params, timeout_ms=timeout_ms, stdin_bytes=stdin_bytes)


def dispatch(mode, options, args=None, **policy):
    runtime = RecordingRuntime() if mode == 'sync' else RecordingAsyncRuntime()
    bound = _BoundSyncRuntime(runtime, 'option-session') if mode == 'sync' else _BoundAsyncRuntime(
        runtime, 'option-session',
    )
    document = SimpleNamespace(_bound_runtime=bound)
    arguments = {'action': 'insert_paragraphs', 'text': 'CONTROL'} if args is None else args
    if mode == 'sync':
        result = dispatch_superdoc_tool(
            document, 'superdoc_perform_action', arguments, options, preset='core', **policy,
        )
    else:
        result = asyncio.run(dispatch_superdoc_tool_async(
            document, 'superdoc_perform_action', arguments, options, preset='core', **policy,
        ))
    return runtime, result


def stale_revision_receipt(action='insert_paragraphs', revision='0'):
    return {
        'status': 'failed',
        'intent': action,
        'preSnapshot': {'revision': revision},
        'selectedTargets': [],
        'executedOperations': [],
        'verification': [],
        'errors': [{
            'code': 'REVISION_CONFLICT',
            'message': f'{action}: expectedRevision is stale. Inspect this live document again before editing.',
            'recovery': {'kind': 'reinspect'},
        }],
    }


def record_revision_refusal(calls):
    def invoke(self, operation_id, params=None, *, timeout_ms=None, stdin_bytes=None):
        calls.append((operation_id, params, timeout_ms, stdin_bytes))
        return {'result': stale_revision_receipt()}
    return invoke


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('options', [None, {}, {'dry_run': False}, {'dryRun': False}, {'dry_run': None}])
def test_default_and_false_preview_reach_bound_runtime(mode, options):
    runtime, result = dispatch(mode, options)
    assert result == {'success': True, 'marker': 'CONTROL'}
    assert runtime.calls == [('doc.preset.dispatch', {
        'preset': 'core', 'toolName': 'superdoc_perform_action',
        'args': {'action': 'insert_paragraphs', 'text': 'CONTROL'}, 'sessionId': 'option-session',
    }, None, None)]


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('options', [{'dry_run': True}, {'dryRun': True}, {'dry_run': False, 'dryRun': True}])
def test_core_preview_refuses_before_any_runtime_call(mode, options, monkeypatch):
    calls = []
    monkeypatch.setattr(RecordingRuntime, 'invoke', lambda *args, **kwargs: calls.append(args))
    with pytest.raises(SuperDocError) as error:
        dispatch(mode, options)
    assert error.value.code == 'CAPABILITY_UNSUPPORTED'
    assert calls == []


@pytest.mark.parametrize('mode', ['sync', 'async'])
def test_false_preview_preserves_transport_options(mode):
    runtime, result = dispatch(mode, {'dry_run': False, 'timeout_ms': 4321, 'stdin_bytes': b'CONTROL'})
    assert result['success'] is True
    assert runtime.calls[0][2:] == (4321, b'CONTROL')


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('value', ['true', 1, [], {}])
def test_preview_requires_a_boolean(mode, value):
    with pytest.raises(SuperDocError) as error:
        dispatch(mode, {'dry_run': value})
    assert error.value.code == 'INVALID_ARGUMENT'


@pytest.mark.parametrize('mode', ['sync', 'async'])
def test_invalid_args_remain_invalid_argument(mode):
    with pytest.raises(SuperDocError) as error:
        dispatch(mode, {'dry_run': True}, args=['invalid'])
    assert error.value.code == 'INVALID_ARGUMENT'


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('key', ['change_mode', 'changeMode'])
@pytest.mark.parametrize('change_mode', ['direct', 'tracked'])
def test_change_mode_is_canonical_payload_not_transport_keyword(mode, key, change_mode):
    options = {key: change_mode, 'timeout_ms': 4321, 'stdin_bytes': b'CONTROL', 'dry_run': False}
    runtime, result = dispatch(mode, options)
    assert result['success'] is True
    assert runtime.calls[0][1]['changeMode'] == change_mode
    assert runtime.calls[0][2:] == (4321, b'CONTROL')
    assert options == {key: change_mode, 'timeout_ms': 4321, 'stdin_bytes': b'CONTROL', 'dry_run': False}


@pytest.mark.parametrize('mode', ['sync', 'async'])
def test_mode_forwarding_preserves_explicit_input_and_policy(mode):
    arguments = {'action': 'insert_paragraphs', 'text': 'CONTROL', 'changeMode': 'direct'}
    runtime, _ = dispatch(
        mode, {'change_mode': 'tracked'}, args=arguments,
        enforce_change_mode='tracked', allow_direct_actions=['undo_changes'], exclude_actions=['delete_text'],
    )
    assert runtime.calls[0][1] == {
        'preset': 'core', 'toolName': 'superdoc_perform_action', 'args': arguments,
        'changeMode': 'tracked', 'sessionId': 'option-session',
        'enforceChangeMode': 'tracked', 'allowDirectActions': 'undo_changes', 'excludeActions': 'delete_text',
    }
    assert arguments['changeMode'] == 'direct'


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('options', [
    {'change_mode': 'invalid'}, {'changeMode': False},
    {'change_mode': 'tracked', 'changeMode': 'direct'},
])
def test_invalid_or_conflicting_change_modes_refuse_before_transport(mode, options, monkeypatch):
    calls = []
    monkeypatch.setattr(RecordingRuntime, 'invoke', lambda *args, **kwargs: calls.append(args))
    with pytest.raises(SuperDocError) as error:
        dispatch(mode, options)
    assert error.value.code == 'INVALID_ARGUMENT'
    assert calls == []


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('key', ['expected_revision', 'expectedRevision'])
@pytest.mark.parametrize('value', [0, 0.0, '0', 42, '42', 9007199254740991])
def test_revision_options_use_the_canonical_cli_number(mode, key, value):
    options = {key: value, 'timeout_ms': 4321}
    runtime, _ = dispatch(mode, options)
    assert runtime.calls[0][1]['args']['expectedRevision'] == str(int(value))
    assert runtime.calls[0][2] == 4321
    assert 'expectedRevision' not in runtime.calls[0][1]
    assert options == {key: value, 'timeout_ms': 4321}


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('options', [
    {'expected_revision': None}, {'expectedRevision': None},
    {'expected_revision': None, 'expectedRevision': None},
])
def test_null_revision_options_are_absent(mode, options):
    runtime, _ = dispatch(mode, options)
    assert 'expectedRevision' not in runtime.calls[0][1]


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('value', ['', '01', '+1', ' 1', '1.0', 'r1', '١', True, -1, 0.5, float('nan'), float('inf'), 9007199254740992, '9' * 5000])
def test_malformed_revision_options_refuse_before_runtime(mode, value, monkeypatch):
    calls = []
    monkeypatch.setattr(RecordingRuntime, 'invoke', record_revision_refusal(calls))
    live_token = isinstance(value, str) and bool(value)
    if live_token:
        assert dispatch(mode, {'expected_revision': value})[1] == stale_revision_receipt()
    else:
        with pytest.raises(SuperDocError) as error:
            dispatch(mode, {'expected_revision': value})
        assert error.value.code == 'INVALID_ARGUMENT'
    assert calls == ([('doc.preset.dispatch', {
        'preset': 'core', 'toolName': 'superdoc_perform_action',
        'args': {'action': 'insert_paragraphs', 'text': 'CONTROL', 'expectedRevision': value},
        'sessionId': 'option-session',
    }, None, None)] if live_token else [])


@pytest.mark.parametrize('mode', ['sync', 'async'])
def test_explicit_action_revision_wins_over_unused_options_without_mutation(mode):
    arguments = {'action': 'insert_paragraphs', 'text': 'CONTROL', 'expectedRevision': '0'}
    options = {'expected_revision': 'not-a-revision', 'expectedRevision': 'also-unused', 'stdin_bytes': b'CONTROL'}
    runtime, _ = dispatch(mode, options, args=arguments)
    assert 'expectedRevision' not in runtime.calls[0][1]
    assert runtime.calls[0][1]['args'] == arguments
    assert arguments['expectedRevision'] == '0'
    assert options['expected_revision'] == 'not-a-revision'
    assert runtime.calls[0][3] == b'CONTROL'


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('value', [None, 0, False, '', '01', 'r1'])
def test_malformed_explicit_revision_cannot_fall_back_to_a_valid_option(mode, value, monkeypatch):
    calls = []
    monkeypatch.setattr(RecordingRuntime, 'invoke', record_revision_refusal(calls))
    args = {'action': 'insert_paragraphs', 'text': 'CONTROL', 'expectedRevision': value}
    live_token = isinstance(value, str) and bool(value)
    if live_token:
        assert dispatch(mode, {'expected_revision': '0'}, args=args)[1] == stale_revision_receipt()
    else:
        with pytest.raises(SuperDocError) as error:
            dispatch(mode, {'expected_revision': '0'}, args=args)
        assert error.value.code == 'INVALID_ARGUMENT'
    assert calls == ([('doc.preset.dispatch', {
        'preset': 'core', 'toolName': 'superdoc_perform_action',
        'args': {'action': 'insert_paragraphs', 'text': 'CONTROL', 'expectedRevision': value},
        'sessionId': 'option-session',
    }, None, None)] if live_token else [])


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('options', [
    {'expected_revision': '0', 'expectedRevision': '1'},
    {'expected_revision': '0', 'expectedRevision': 0},
])
def test_ambiguous_revision_aliases_do_not_select_silently(mode, options):
    with pytest.raises(SuperDocError) as error:
        dispatch(mode, options)
    assert error.value.code == 'INVALID_ARGUMENT'


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('source', ['args', 'expected_revision', 'expectedRevision'])
@pytest.mark.parametrize('revision', ['not-a-revision', '01', '9007199254740992'])
@pytest.mark.parametrize('current', [False, True])
def test_nonempty_revision_tokens_reach_the_live_comparison(mode, source, revision, current, monkeypatch):
    calls = []
    state = {'text': 'original', 'revision': revision if current else '0', 'writes': 0}

    def invoke(self, operation_id, params=None, *, timeout_ms=None, stdin_bytes=None):
        calls.append((operation_id, params, timeout_ms, stdin_bytes))
        assert operation_id == 'doc.preset.dispatch'
        requested = params['args'].get('expectedRevision', params.get('expectedRevision'))
        if requested != state['revision']:
            return {'result': stale_revision_receipt(revision=state['revision'])}
        state['writes'] += 1
        state['text'] += params['args']['text']
        return {'result': {'success': True}}

    monkeypatch.setattr(RecordingRuntime, 'invoke', invoke)
    arguments = {'action': 'insert_paragraphs', 'text': 'CONTROL'}
    options = {}
    if source == 'args':
        arguments['expectedRevision'] = revision
    else:
        options[source] = revision
    before_args, before_options = dict(arguments), dict(options)
    if current:
        _, result = dispatch(mode, options, args=arguments)
        assert result == {'success': True}
        assert state == {'text': 'originalCONTROL', 'revision': revision, 'writes': 1}
    else:
        _, result = dispatch(mode, options, args=arguments)
        assert result == stale_revision_receipt(revision='0')
        assert state == {'text': 'original', 'revision': '0', 'writes': 0}
    assert arguments == before_args
    assert options == before_options
    assert calls == [('doc.preset.dispatch', {
        'preset': 'core', 'toolName': 'superdoc_perform_action',
        'args': {'action': 'insert_paragraphs', 'text': 'CONTROL', 'expectedRevision': revision},
        'sessionId': 'option-session',
    }, None, None)]
