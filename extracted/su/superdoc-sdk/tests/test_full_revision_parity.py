import copy
import json

import pytest

from superdoc import AsyncSuperDocDocument, SuperDocDocument, SuperDocError, dispatch_superdoc_tool, dispatch_superdoc_tool_async
from superdoc.client import _BoundAsyncRuntime, _BoundSyncRuntime
from superdoc.generated.contract import OPERATION_INDEX
from superdoc.protocol import build_operation_argv


def recording_document(asynchronous, reply=None):
    frames = []

    def respond(operation_id, params, timeout_ms, stdin_bytes):
        frames.append((operation_id, copy.deepcopy(params), timeout_ms, stdin_bytes))
        if reply:
            return reply(operation_id, params)
        return {'result': {'success': True}}

    class SyncRuntime:
        def invoke(self, operation_id, params, *, timeout_ms=None, stdin_bytes=None):
            return respond(operation_id, params, timeout_ms, stdin_bytes)

    class AsyncRuntime:
        async def invoke(self, operation_id, params, *, timeout_ms=None, stdin_bytes=None):
            return respond(operation_id, params, timeout_ms, stdin_bytes)

    if asynchronous:
        return AsyncSuperDocDocument(_BoundAsyncRuntime(AsyncRuntime(), 'full-session'), 'full-session', {}, None), frames
    return SuperDocDocument(_BoundSyncRuntime(SyncRuntime(), 'full-session'), 'full-session', {}, None), frames


async def dispatch(asynchronous, document, tool, args, options):
    if asynchronous:
        return await dispatch_superdoc_tool_async(document, tool, args, options, preset='full')
    return dispatch_superdoc_tool(document, tool, args, options, preset='full')


@pytest.mark.parametrize('asynchronous', [False, True])
@pytest.mark.parametrize('revision', ['', 'r:live-token', '01', '9007199254740992'])
@pytest.mark.parametrize('tool,args', [
    ('superdoc_api_call', {'operationId': 'doc.create.paragraph', 'args': {'text': 'synthetic'}}),
    ('superdoc_perform_action', {'action': 'insert_image', 'src': 'synthetic.png'}),
])
@pytest.mark.asyncio
async def test_full_outer_revision_is_preserved_for_non_action_and_helper(asynchronous, revision, tool, args):
    document, frames = recording_document(asynchronous)
    options = {'expected_revision': revision, 'change_mode': 'tracked', 'dry_run': False}
    before = copy.deepcopy((args, options))
    assert await dispatch(asynchronous, document, tool, args, options) == {'success': True}
    assert frames == [('doc.preset.dispatch', {
        'preset': 'full', 'toolName': tool, 'args': args,
        'expectedRevision': revision, 'changeMode': 'tracked', 'dryRun': False, 'sessionId': 'full-session',
    }, None, None)]
    assert (args, options) == before


@pytest.mark.parametrize('asynchronous', [False, True])
@pytest.mark.asyncio
async def test_full_unknown_tool_keeps_node_error_before_outer_preview(asynchronous):
    def unknown(_operation, params):
        assert params['dryRun'] is True
        raise SuperDocError('Unknown tool: unknown-full-tool', code='TOOL_DISPATCH_NOT_FOUND',
                            details={'toolName': 'unknown-full-tool', 'preset': 'core'})

    document, frames = recording_document(asynchronous, unknown)
    with pytest.raises(SuperDocError) as failure:
        await dispatch(asynchronous, document, 'unknown-full-tool', {}, {'dry_run': True})
    assert failure.value.code == 'TOOL_DISPATCH_NOT_FOUND'
    assert failure.value.details == {'toolName': 'unknown-full-tool', 'preset': 'core'}
    assert len(frames) == 1 and frames[0][1]['dryRun'] is True


@pytest.mark.parametrize('asynchronous', [False, True])
@pytest.mark.asyncio
async def test_full_helper_keeps_nested_and_outer_revision_distinct(asynchronous):
    args = {'action': 'insert_image', 'src': 'synthetic.png', 'expectedRevision': None}
    details = {'toolName': 'superdoc_perform_action', 'preset': 'full', 'action': 'insert_image',
               'feature': 'preset.full.helper.expectedRevision'}

    def refusal(_operation, params):
        assert params['args'] == args
        assert params['expectedRevision'] == 'r:outer'
        raise SuperDocError('Action insert_image cannot enforce args.expectedRevision. Nothing was changed.',
                            code='CAPABILITY_UNSUPPORTED', details=details)

    document, frames = recording_document(asynchronous, refusal)
    with pytest.raises(SuperDocError) as failure:
        await dispatch(asynchronous, document, 'superdoc_perform_action', args, {'expected_revision': 'r:outer'})
    assert failure.value.code == 'CAPABILITY_UNSUPPORTED'
    assert failure.value.details == details
    assert len(frames) == 1


@pytest.mark.parametrize('asynchronous', [False, True])
@pytest.mark.asyncio
async def test_full_invalid_tool_args_precede_preview(asynchronous):
    document, frames = recording_document(asynchronous)
    with pytest.raises(SuperDocError) as failure:
        await dispatch(asynchronous, document, 'superdoc_api_call', [], {'dry_run': True})
    assert failure.value.code == 'INVALID_ARGUMENT'
    assert str(failure.value) == 'Tool arguments for superdoc_api_call must be an object.'
    assert failure.value.details == {'toolName': 'superdoc_api_call'}
    assert frames == []


@pytest.mark.parametrize('asynchronous', [False, True])
@pytest.mark.asyncio
async def test_full_missing_core_action_is_rejected_before_preview(asynchronous):
    details = {'toolName': 'superdoc_perform_action', 'missingKeys': ['action']}

    def invalid(_operation, params):
        assert params['dryRun'] is True
        raise SuperDocError('Missing required argument(s) for superdoc_perform_action: action',
                            code='INVALID_ARGUMENT', details=details)

    document, frames = recording_document(asynchronous, invalid)
    with pytest.raises(SuperDocError) as failure:
        await dispatch(asynchronous, document, 'superdoc_perform_action', {}, {'dry_run': True})
    assert failure.value.code == 'INVALID_ARGUMENT'
    assert str(failure.value) == 'Missing required argument(s) for superdoc_perform_action: action'
    assert failure.value.details == details
    assert len(frames) == 1


@pytest.mark.parametrize('revision', ['01', 'r:live-token', 7.0])
def test_full_argv_preserves_revision_type_and_preview(revision):
    argv = build_operation_argv(OPERATION_INDEX['doc.preset.dispatch'], {
        'preset': 'full', 'toolName': 'superdoc_api_call', 'expectedRevision': revision, 'dryRun': False,
    })
    encoded = argv[argv.index('--expected-revision') + 1]
    assert json.loads(encoded) == revision
    assert type(json.loads(encoded)) is type(revision)
    assert argv[argv.index('--dry-run') + 1] == 'false'
