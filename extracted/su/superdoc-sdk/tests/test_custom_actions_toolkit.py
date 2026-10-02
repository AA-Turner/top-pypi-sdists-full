"""Custom-actions toolkit contract, runnable under plain ``unittest``.

The full pytest suites (``test_custom_actions.py``, ``test_custom_actions_async.py``)
cover the kit exhaustively but need pytest, which the SDK CI lane does not
install. This file pins the public contract — ``define_action`` +
``create_agent_toolkit`` — against a fake base preset so it runs everywhere
the other unittest suites run, with no document host.
"""

from __future__ import annotations

import unittest

from superdoc import SuperDocError, create_agent_toolkit, define_action, register_preset, unregister_preset

BUILTINS = ['insert_paragraphs', 'add_comments']


class _FakeBase:
    """Core-shaped base: perform_action with an enum, exclusions narrow it."""

    id = 'toolkit-fake-base'
    description = 'fake'
    supports_cache_control = True

    def __init__(self):
        self.calls = []

    def _active(self, exclude_actions):
        excluded = set(exclude_actions or [])
        return [name for name in BUILTINS if name not in excluded]

    def get_tools(self, provider, *, cache=False, exclude_actions=None):
        active = self._active(exclude_actions)
        tools = [{'name': 'superdoc_inspect', 'parameters': {'type': 'object', 'properties': {}}}]
        if active:
            tools.append({
                'name': 'superdoc_perform_action',
                'description': 'Built-ins: ' + ', '.join(active),
                'parameters': {'type': 'object', 'properties': {
                    'action': {'type': 'string', 'enum': active},
                    'texts': {'type': 'array'},
                }},
            })
        return {'tools': tools, 'cacheStrategy': 'disabled'}

    def get_catalog(self):
        return {'contractVersion': 'fake', 'generatedAt': None, 'toolCount': 0, 'tools': []}

    def get_system_prompt(self, *, exclude_actions=None):
        return 'BASE PROMPT\n' + '\n'.join(f'- {name} —' for name in self._active(exclude_actions))

    def get_mcp_prompt(self):
        return 'BASE MCP'

    def dispatch(self, document_handle, tool_name, args=None, invoke_options=None, *, exclude_actions=None):
        self.calls.append({'tool': tool_name, 'args': dict(args or {}), 'exclude_actions': exclude_actions})
        return {'status': 'ok', 'verificationPassed': True}

    async def dispatch_async(self, document_handle, tool_name, args=None, invoke_options=None, *, exclude_actions=None):
        return self.dispatch(document_handle, tool_name, args, invoke_options, exclude_actions=exclude_actions)


class _Doc:
    def __init__(self):
        self.revision = 0

    def info(self, args=None):
        return {'revision': str(self.revision)}

    def insert(self, args):
        self.revision += 1
        return args['value']


def _perform(tools):
    # Provider dialects differ: the fake base emits flat tools, while a
    # synthesized perform_action follows the real openai shape ({function: ...}).
    for tool in tools:
        body = tool.get('function') if isinstance(tool.get('function'), dict) else tool
        if body.get('name') == 'superdoc_perform_action':
            return body
    return None


def _enum(tools):
    tool = _perform(tools)
    return tool['parameters']['properties']['action']['enum'] if tool else []


def _stamp():
    return define_action(
        name='acme.stamp',
        description='Insert a banner and comment on it.',
        input_schema={'type': 'object', 'properties': {'label': {'type': 'string', 'default': 'CONFIDENTIAL'}}},
        steps=[
            {'action': 'insert_paragraphs', 'args': {'texts': ['{{label}}', 'Re: {{label}}\n']}},
            {'action': 'add_comments', 'args': {'commentText': 'Stamped: {{label}}'}},
        ],
    )


def _echo():
    return define_action(
        name='acme.echo',
        description='Echo a value after one write.',
        input_schema={'type': 'object', 'properties': {'value': {'type': 'string', 'default': 'default value'}}},
        run=lambda doc, args: doc.insert({'value': args['value']}),
    )


class CustomActionsToolkitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = _FakeBase()
        register_preset(self.base)

    def tearDown(self) -> None:
        unregister_preset(self.base.id)

    def kit(self, **extra):
        return create_agent_toolkit({'provider': 'openai', 'base': self.base.id, **extra})

    def test_define_action_tiers(self) -> None:
        self.assertIsInstance(_stamp()['steps'], list)
        self.assertNotIn('run', _stamp())
        self.assertTrue(callable(_echo()['run']))
        self.assertNotIn('steps', _echo())

    def test_toolkit_advertises_custom_actions_next_to_builtins(self) -> None:
        kit = self.kit(customActions=[_stamp(), _echo()])
        names = _enum(kit['tools'])
        self.assertIn('acme.stamp', names)
        self.assertIn('acme.echo', names)
        self.assertIn('insert_paragraphs', names)
        self.assertIn('- acme.stamp — Insert a banner and comment on it.', kit['system_prompt'])
        self.assertEqual(kit['meta']['preset'], 'custom_superdoc_preset')
        self.assertEqual(kit['meta']['toolCount'], len(kit['tools']))

    def test_include_actions_narrows_tools_prompt_and_dispatch_together(self) -> None:
        kit = self.kit(customActions=[_stamp()], includeActions=['insert_paragraphs'])
        names = _enum(kit['tools'])
        self.assertEqual(sorted(names), ['acme.stamp', 'insert_paragraphs'])
        self.assertNotIn('add_comments', _perform(kit['tools'])['description'])
        self.assertNotIn('- add_comments —', kit['system_prompt'])
        with self.assertRaises(SuperDocError) as ctx:
            kit['dispatch'](_Doc(), 'superdoc_perform_action', {'action': 'add_comments', 'commentText': 'x'})
        self.assertEqual(ctx.exception.details.get('excludedBy'), 'includeActions')
        self.assertEqual(self.base.calls, [])

    def test_empty_include_actions_yields_custom_only_surface(self) -> None:
        kit = self.kit(customActions=[_echo()], include_actions=[])
        self.assertEqual(_enum(kit['tools']), ['acme.echo'])  # synthesized: base dropped the tool
        self.assertNotIn('- insert_paragraphs —', kit['system_prompt'])

    def test_unknown_include_action_is_rejected(self) -> None:
        with self.assertRaises(SuperDocError) as ctx:
            self.kit(customActions=[_echo()], includeActions=['not_an_action'])
        self.assertEqual(ctx.exception.code, 'INVALID_ARGUMENT')

    def test_exclude_actions_refuses_custom_and_builtin_names(self) -> None:
        kit = self.kit(customActions=[_stamp(), _echo()], excludeActions=['acme.echo', 'add_comments'])
        names = _enum(kit['tools'])
        self.assertNotIn('acme.echo', names)
        self.assertNotIn('add_comments', names)
        self.assertIn('acme.stamp', names)
        self.assertNotIn('- acme.echo —', kit['system_prompt'])
        with self.assertRaises(SuperDocError):
            kit['dispatch'](_Doc(), 'superdoc_perform_action', {'action': 'acme.echo'})

    def test_steps_tier_templates_and_reports_per_step(self) -> None:
        kit = self.kit(customActions=[_stamp()], excludeActions=['add_comments'])
        receipt = kit['dispatch'](_Doc(), 'superdoc_perform_action', {'action': 'acme.stamp'})
        self.assertEqual(receipt['status'], 'succeeded')
        self.assertEqual(len(self.base.calls), 2)
        first, second = self.base.calls
        # Whole-string template passes the raw value; partial templates
        # interpolate and keep surrounding text, including a trailing newline.
        self.assertEqual(first['args']['texts'], ['CONFIDENTIAL', 'Re: CONFIDENTIAL\n'])
        self.assertEqual(second['args']['commentText'], 'Stamped: CONFIDENTIAL')
        # A step may use a built-in the toolkit hides from the model.
        self.assertEqual(second['args']['action'], 'add_comments')
        self.assertIsNone(second['exclude_actions'])

    def test_run_tier_applies_defaults_and_reports_revisions(self) -> None:
        kit = self.kit(customActions=[_echo()])
        doc = _Doc()
        receipt = kit['dispatch'](doc, 'superdoc_perform_action', {'action': 'acme.echo'})
        self.assertEqual(receipt['status'], 'succeeded')
        self.assertEqual(receipt['result'], 'default value')
        self.assertEqual((receipt['preRevision'], receipt['postRevision']), ('0', '1'))
        explicit = kit['dispatch'](doc, 'superdoc_perform_action', {'action': 'acme.echo', 'value': 'given'})
        self.assertEqual(explicit['result'], 'given')

    def test_run_tier_failure_reports_partial_mutation(self) -> None:
        def fail(doc, args):
            doc.insert({'value': 'applied'})
            raise RuntimeError('second write failed')

        kit = self.kit(customActions=[define_action(name='acme.fail', description='fails after a write', run=fail)])
        receipt = kit['dispatch'](_Doc(), 'superdoc_perform_action', {'action': 'acme.fail'})
        self.assertEqual(receipt['status'], 'failed')
        self.assertTrue(receipt['partialMutation'])
        self.assertEqual(receipt['errors'][0]['message'], 'second write failed')

    def test_unknown_custom_action_falls_through_to_base(self) -> None:
        kit = self.kit(customActions=[_echo()])
        kit['dispatch'](_Doc(), 'superdoc_perform_action', {'action': 'insert_paragraphs', 'texts': ['x']})
        self.assertEqual(self.base.calls[-1]['args']['action'], 'insert_paragraphs')

    def test_explicit_base_with_no_actions_does_not_fall_back_to_legacy(self) -> None:
        kit = self.kit(customActions=[])
        self.assertEqual(kit['meta']['preset'], 'custom_superdoc_preset')
        self.assertTrue(kit['system_prompt'].startswith('BASE PROMPT'))

    def test_invalid_provider_is_rejected_on_the_actions_path(self) -> None:
        with self.assertRaises(SuperDocError) as ctx:
            create_agent_toolkit({'provider': 'opneai', 'base': self.base.id, 'customActions': [_echo()]})
        self.assertEqual(ctx.exception.code, 'INVALID_ARGUMENT')


if __name__ == '__main__':
    unittest.main()
