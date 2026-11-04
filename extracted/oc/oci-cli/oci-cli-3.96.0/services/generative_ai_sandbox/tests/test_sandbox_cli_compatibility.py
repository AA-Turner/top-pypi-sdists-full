# coding: utf-8
# Copyright (c) 2016, 2026, Oracle and/or its affiliates. All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

import importlib.util
import inspect
import json
from types import SimpleNamespace

import click
from click.testing import CliRunner
import pytest

from oci._vendor.sseclient import SSEClient
from oci_cli import cli_root, cli_util
from services.generative_ai_sandbox.src.oci_cli_generative_ai_sandbox import generative_ai_sandbox_cli_extended  # noqa: F401
from services.generative_ai_sandbox.src.oci_cli_generative_ai_sandbox.generated import generativeaisandbox_cli
from services.generative_ai_sandbox.tests.test_sandbox_cli_extended import CLI_CTX_OBJ as LEAF_CLI_CTX_OBJ


CLI_CTX_OBJ = dict(LEAF_CLI_CTX_OBJ, global_command_alias={}, command_sequence_alias={})


def _command_tree(command, path=()):
    yield path, command
    if isinstance(command, click.Group):
        for name, child in command.commands.items():
            yield from _command_tree(child, path + (name,))


def _required(option):
    # cli_util implements required options in its callback to support CLI defaults.
    callback_vars = inspect.getclosurevars(option.callback).nonlocals if option.callback else {}
    return option.required or callback_vars.get('required', False)


def test_extensions_preserve_generated_public_commands_and_options(monkeypatch):
    # Load the generated public interface before extensions, without registering a
    # second root in the real CLI or inheriting extension command-name overrides.
    with monkeypatch.context() as isolated:
        isolated.setattr(cli_root, 'cli', click.Group())
        isolated.setattr(cli_util, 'OVERRIDES', {
            key: value for key, value in cli_util.OVERRIDES.items()
            if not key.startswith('generative_ai_sandbox.')
        })
        spec = importlib.util.spec_from_file_location('_sandbox_public_baseline', generativeaisandbox_cli.__file__)
        baseline = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(baseline)

    public_tree = dict(_command_tree(baseline.generative_ai_sandbox_root_group))
    extended_tree = dict(_command_tree(generativeaisandbox_cli.generative_ai_sandbox_root_group))
    for path, old_command in public_tree.items():
        assert path in extended_tree, 'Removed public command: {}'.format(' '.join(path))
        new_command = extended_tree[path]
        old_options = {option.name: option for option in old_command.params}
        new_options = {option.name: option for option in new_command.params}
        for name, old_option in old_options.items():
            assert name in new_options, (path, 'Removed public option', name)
            new_option = new_options[name]
            assert set(old_option.opts) <= set(new_option.opts), (path, name)
            assert set(old_option.secondary_opts) <= set(new_option.secondary_opts), (path, name)
            assert new_option.type.__class__ is old_option.type.__class__, (path, name)
            for attribute in ('choices', 'mode', 'encoding', 'errors'):
                assert getattr(new_option.type, attribute, None) == getattr(old_option.type, attribute, None), (path, name, attribute)
            for attribute in ('nargs', 'multiple', 'is_flag', 'flag_value', 'default', 'is_eager', 'expose_value'):
                assert getattr(new_option, attribute, None) == getattr(old_option, attribute, None), (path, name, attribute)
            assert not _required(new_option) or _required(old_option), (path, 'Strengthened required option', name)
        for name in new_options.keys() - old_options.keys():
            assert not _required(new_options[name]), (path, 'New required option', name)

        if not isinstance(old_command, click.Group):
            result = CliRunner().invoke(
                new_command, ['--help'],
                obj=dict(CLI_CTX_OBJ, help=True, settings={'use_click_help': True})
            )
            assert result.exit_code == 0, (path, result.output)


ALIASES = [
    (('sandbox-collection', 'list'), ('sandbox', 'list'), 'list_sandboxes', ['--project-id', 'project_id']),
    (('sandbox-command-collection', 'list'), ('sandbox-command', 'list'), 'list_sandbox_command', ['--sandbox-id', 'sandbox_id']),
    (('sandbox-snapshot-collection', 'list'), ('sandbox-snapshot', 'list'), 'list_sandbox_snapshots', ['--project-id', 'project_id']),
    (('sandbox-command-output', 'get-output'), ('sandbox-command', 'get-output'), 'get_sandbox_command_output', ['--sandbox-id', 'sandbox_id', '--command-id', 'command_id', '--from-seq', '0']),
    (('sandbox-command-event', 'run-and-stream'), ('sandbox-command', 'run-and-stream'), 'run_sandbox_command_and_stream', ['--sandbox-id', 'sandbox_id', '--command', 'printf']),
    (('sandbox-command-event', 'stream'), ('sandbox-command', 'stream'), 'stream_sandbox_command_events', ['--sandbox-id', 'sandbox_id', '--command-id', 'command_id', '--from-seq', '0', '--until-seq', '0']),
    (('sandbox', 'create-sandbox-sandbox-snapshot-source'), ('sandbox', 'create-from-snapshot'), 'create_sandbox', ['--project-id', 'project_id', '--source-snapshot-id', 'snapshot_id']),
]


@pytest.mark.parametrize('legacy_path,alias_path,method_name,arguments', ALIASES)
def test_legacy_paths_and_aliases_forward_identical_requests(monkeypatch, tmp_path, legacy_path, alias_path, method_name, arguments):
    calls = []
    raw = SimpleNamespace(stream=lambda *args, **kwargs: iter([b'raw event\n']))

    def sdk_call(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(headers={}, data=SimpleNamespace(raw=raw, _event_source=SimpleNamespace(raw=raw)))

    client = SimpleNamespace(**{method_name: sdk_call})
    monkeypatch.setattr(cli_util, 'build_client', lambda *args: client)
    monkeypatch.setattr(cli_util, 'render_response', lambda *args: None)
    for index, path in enumerate((legacy_path, alias_path)):
        args = list(path) + arguments
        if method_name in ('stream_sandbox_command_events', 'run_sandbox_command_and_stream'):
            args += ['--file', str(tmp_path / '{}.events'.format(index))]
        result = CliRunner().invoke(
            generativeaisandbox_cli.generative_ai_sandbox_root_group,
            args, obj=dict(CLI_CTX_OBJ, request_id='compatibility-request')
        )
        assert result.exit_code == 0, (path, result.output)
        assert len(calls) == index + 1
    assert calls[0] == calls[1]
    assert calls[0]['opc_request_id'] == 'compatibility-request'


@pytest.mark.parametrize('group', ['sandbox-command-event', 'sandbox-command'])
@pytest.mark.parametrize('wrapped_sse', [False, True])
@pytest.mark.parametrize('destination_kind', ['file', 'stdout', 'from-json'])
@pytest.mark.parametrize('wire_data', [b'', b': keepalive\nid: 1\ndata: {"seq":1,"text":"caf\xc3\xa9"}\n\n'])
def test_stream_file_preserves_raw_response(monkeypatch, tmp_path, group, wrapped_sse, destination_kind, wire_data):
    calls = []
    raw = SimpleNamespace(stream=lambda *args, **kwargs: iter([wire_data[:7], wire_data[7:]]) if wire_data else iter([]))
    response = SimpleNamespace(raw=raw)

    def sdk_call(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(headers={}, data=SSEClient(response) if wrapped_sse else response)

    monkeypatch.setattr(cli_util, 'build_client', lambda *args: SimpleNamespace(stream_sandbox_command_events=sdk_call))

    def unexpected_render(*args):
        raise AssertionError('--file must retain raw response bytes')

    monkeypatch.setattr(cli_util, 'render_response', unexpected_render)
    destination = '-' if destination_kind == 'stdout' else str(tmp_path / 'events.sse')
    args = [group, 'stream']
    if destination_kind == 'from-json':
        args += ['--from-json', json.dumps({
            'sandboxId': 'sandbox_id', 'commandId': 'command_id',
            'fromSeq': 0, 'untilSeq': 0, 'file': destination
        })]
    else:
        args += ['--sandbox-id', 'sandbox_id', '--command-id', 'command_id', '--from-seq', '0', '--until-seq', '0', '--file', destination]
    result = CliRunner().invoke(
        generativeaisandbox_cli.generative_ai_sandbox_root_group,
        args, obj=dict(CLI_CTX_OBJ, request_id='raw-stream-request')
    )
    assert result.exit_code == 0, result.output
    if destination_kind == 'stdout':
        assert result.stdout_bytes == wire_data
    else:
        assert (tmp_path / 'events.sse').read_bytes() == wire_data
    assert calls == [{
        'sandbox_id': 'sandbox_id', 'command_id': 'command_id',
        'from_seq': 0, 'until_seq': 0, 'opc_request_id': 'raw-stream-request'
    }]
