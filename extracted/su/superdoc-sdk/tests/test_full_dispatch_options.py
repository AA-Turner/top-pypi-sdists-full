import copy
import pytest
from superdoc import AsyncSuperDocDocument, SuperDocDocument, SuperDocError, dispatch_superdoc_tool, dispatch_superdoc_tool_async
from superdoc.client import _BoundAsyncRuntime, _BoundSyncRuntime


def recording_document(asynchronous):
    frames = []

    class SyncRuntime:
        def invoke(self, operation_id, params, *, timeout_ms=None, stdin_bytes=None):
            frames.append((operation_id, copy.deepcopy(params), timeout_ms, stdin_bytes))
            return {'result': {'success': True}}

    class AsyncRuntime:
        async def invoke(self, operation_id, params, *, timeout_ms=None, stdin_bytes=None):
            frames.append((operation_id, copy.deepcopy(params), timeout_ms, stdin_bytes))
            return {'result': {'success': True}}

    if asynchronous:
        return AsyncSuperDocDocument(_BoundAsyncRuntime(AsyncRuntime(), 'full-session'), 'full-session', {}, None), frames
    return SuperDocDocument(_BoundSyncRuntime(SyncRuntime(), 'full-session'), 'full-session', {}, None), frames


@pytest.mark.parametrize('asynchronous', [False, True])
@pytest.mark.parametrize('revision', ['not-a-revision', '01', '9007199254740992'])
@pytest.mark.asyncio
async def test_full_dispatch_real_bound_action_options_preserve_opaque_revision(asynchronous, revision):
    document, frames = recording_document(asynchronous)
    args = {'action': 'replace_text', 'edits': [{'find': 'before', 'replace': 'after'}]}
    options = {'expected_revision': revision, 'change_mode': 'tracked', 'timeout_ms': 17, 'stdin_bytes': b'synthetic'}
    before = copy.deepcopy((args, options))
    if asynchronous:
        result = await dispatch_superdoc_tool_async(document, 'superdoc_perform_action', args, options, preset='full')
    else:
        result = dispatch_superdoc_tool(document, 'superdoc_perform_action', args, options, preset='full')
    assert result == {'success': True}
    assert frames == [('doc.preset.dispatch', {'preset': 'full', 'toolName': 'superdoc_perform_action', 'args': {**args, 'expectedRevision': revision}, 'changeMode': 'tracked', 'sessionId': 'full-session'}, 17, b'synthetic')]
    assert (args, options) == before


@pytest.mark.parametrize('asynchronous', [False, True])
@pytest.mark.parametrize('key', ['dry_run', 'dryRun'])
@pytest.mark.asyncio
async def test_full_dispatch_real_bound_outer_preview_refuses_without_frame(asynchronous, key):
    document, frames = recording_document(asynchronous)
    args = {'operationId': 'doc.diff.apply', 'args': {'diff': {'synthetic': True}}}
    with pytest.raises(SuperDocError) as failure:
        if asynchronous:
            await dispatch_superdoc_tool_async(document, 'superdoc_api_call', args, {key: True}, preset='full')
        else:
            dispatch_superdoc_tool(document, 'superdoc_api_call', args, {key: True}, preset='full')
    assert failure.value.code == 'CAPABILITY_UNSUPPORTED'
    assert frames == []


@pytest.mark.parametrize('asynchronous', [False, True])
@pytest.mark.parametrize('options,explicit_revision,expected_revision,expected_outer', [
    ({'expectedRevision': 'opaque-camel', 'changeMode': 'direct', 'dryRun': False}, None, 'opaque-camel', {'changeMode': 'direct', 'dryRun': False}),
    ({'expected_revision': 7, 'dry_run': False}, None, '7', {'dryRun': False}),
    ({'expected_revision': {'unused': True}, 'expectedRevision': False}, 'explicit-live', 'explicit-live', {}),
])
@pytest.mark.asyncio
async def test_full_dispatch_real_bound_aliases_precedence_and_false_preview(asynchronous, options, explicit_revision, expected_revision, expected_outer):
    document, frames = recording_document(asynchronous)
    args = {'action': 'replace_text', 'edits': []}
    if explicit_revision is not None:
        args['expectedRevision'] = explicit_revision
    before = copy.deepcopy((args, options))
    if asynchronous:
        await dispatch_superdoc_tool_async(document, 'superdoc_perform_action', args, options, preset='full')
    else:
        dispatch_superdoc_tool(document, 'superdoc_perform_action', args, options, preset='full')
    assert frames == [('doc.preset.dispatch', {'preset': 'full', 'toolName': 'superdoc_perform_action', 'args': {**args, 'expectedRevision': expected_revision}, **expected_outer, 'sessionId': 'full-session'}, None, None)]
    assert (args, options) == before


@pytest.mark.parametrize('asynchronous', [False, True])
@pytest.mark.asyncio
async def test_full_dispatch_real_bound_extended_tool_uses_numeric_cli_revision(asynchronous):
    document, frames = recording_document(asynchronous)
    args = {'operationId': 'doc.create.paragraph', 'args': {'text': 'synthetic'}, 'dryRun': True}
    options = {'expected_revision': '7', 'change_mode': 'tracked', 'dry_run': False}
    if asynchronous:
        await dispatch_superdoc_tool_async(document, 'superdoc_api_call', args, options, preset='full')
    else:
        dispatch_superdoc_tool(document, 'superdoc_api_call', args, options, preset='full')
    assert frames == [('doc.preset.dispatch', {'preset': 'full', 'toolName': 'superdoc_api_call', 'args': args, 'expectedRevision': '7', 'changeMode': 'tracked', 'dryRun': False, 'sessionId': 'full-session'}, None, None)]


@pytest.mark.parametrize('asynchronous', [False, True])
@pytest.mark.parametrize('options', [
    {'change_mode': 'tracked', 'changeMode': 'direct'},
    {'change_mode': 'invalid'},
    {'dry_run': 'true'},
    {'expected_revision': ''},
    {'expected_revision': False},
])
@pytest.mark.asyncio
async def test_full_dispatch_real_bound_invalid_options_fail_without_frame(asynchronous, options):
    document, frames = recording_document(asynchronous)
    with pytest.raises(SuperDocError) as failure:
        if asynchronous:
            await dispatch_superdoc_tool_async(document, 'superdoc_perform_action', {'action': 'replace_text', 'edits': []}, options, preset='full')
        else:
            dispatch_superdoc_tool(document, 'superdoc_perform_action', {'action': 'replace_text', 'edits': []}, options, preset='full')
    assert failure.value.code == 'INVALID_ARGUMENT'
    assert frames == []
