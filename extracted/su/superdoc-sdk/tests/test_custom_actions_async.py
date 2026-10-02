import asyncio

import pytest

from test_custom_actions import _register_fake, _stamp_spec, cleanup_registered
from superdoc import SuperDocError, create_agent_toolkit, define_action


class AsyncDocument:
    def __init__(self):
        self.revision = 0

    async def info(self, args=None):
        await asyncio.sleep(0)
        return {'revision': str(self.revision)}

    async def insert(self, args):
        await asyncio.sleep(0)
        self.revision += 1
        return args['value']


@pytest.mark.asyncio
@pytest.mark.parametrize('async_run', [False, True])
async def test_toolkit_async_native_defaults_and_awaiting(cleanup_registered, async_run):
    _register_fake(cleanup_registered)

    async def run_async(doc, args):
        return await doc.insert({'value': args['label']})

    def run_sync(doc, args):
        return args['label']

    action = define_action(name='async.echo', description='Echo a default.',
                           input_schema={'type': 'object', 'properties': {'label': {'type': 'string', 'default': 'DEFAULT'}}},
                           run=run_async if async_run else run_sync)
    kit = create_agent_toolkit({'provider': 'anthropic', 'base': 'fake-base', 'preset': 'missing',
                                'include_actions': [], 'customActions': [action]})
    receipt = await kit['dispatch_async'](AsyncDocument(), 'superdoc_perform_action', {'action': action['name']})
    assert receipt['status'] == 'succeeded'
    assert receipt['result'] == 'DEFAULT'
    assert receipt['preRevision'] == '0'
    assert receipt['postRevision'] == ('1' if async_run else '0')


@pytest.mark.asyncio
async def test_toolkit_async_native_failure_reports_mutation(cleanup_registered):
    _register_fake(cleanup_registered)

    async def fail(doc, args):
        await doc.insert({'value': 'applied'})
        raise RuntimeError('failed after insertion')

    action = define_action(name='async.fail', description='Fail after insertion.', run=fail)
    kit = create_agent_toolkit({'provider': 'anthropic', 'base': 'fake-base', 'customActions': [action]})
    receipt = await kit['dispatch_async'](AsyncDocument(), 'superdoc_perform_action', {'action': action['name']})
    assert receipt['status'] == 'failed'
    assert receipt['partialMutation'] is True
    assert receipt['recovery']['kind'] == 'revert'
    assert receipt['errors'][0]['message'] == 'failed after insertion'


@pytest.mark.asyncio
@pytest.mark.parametrize('fail_second', [False, True])
async def test_toolkit_async_steps_await_hidden_builtins(cleanup_registered, fail_second):
    base = _register_fake(cleanup_registered)
    calls = []

    async def dispatch(handle, tool, args=None, invoke_options=None, *, exclude_actions=None):
        await asyncio.sleep(0)
        assert exclude_actions is None
        calls.append(args)
        return {'status': 'failed' if fail_second and len(calls) == 2 else 'ok'}

    base.dispatch_async = dispatch
    stamp = _stamp_spec()
    kit = create_agent_toolkit({'provider': 'anthropic', 'base': 'fake-base', 'customActions': [stamp],
                                'includeActions': [], 'exclude_actions': ['insert_paragraphs', 'add_comments']})
    with pytest.raises(SuperDocError):
        await kit['dispatch_async'](AsyncDocument(), 'superdoc_perform_action', {'action': 'insert_paragraphs'})
    receipt = await kit['dispatch_async'](AsyncDocument(), 'superdoc_perform_action',
                                         {'action': stamp['name'], 'changeMode': 'tracked'})
    assert receipt['status'] == ('partial' if fail_second else 'succeeded')
    assert calls[0]['texts'] == ['CONFIDENTIAL']
    assert calls[1]['commentText'] == 'Stamped: CONFIDENTIAL — verify.'
    assert all(call['changeMode'] == 'tracked' for call in calls)
    if fail_second:
        assert receipt['failedStep']['index'] == 1
