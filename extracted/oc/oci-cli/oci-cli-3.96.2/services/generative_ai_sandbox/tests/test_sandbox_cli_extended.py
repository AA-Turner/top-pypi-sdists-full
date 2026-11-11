# coding: utf-8
# Copyright (c) 2016, 2026, Oracle and/or its affiliates.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

import base64
import hashlib
import io
import json
from types import SimpleNamespace

import click
from click.testing import CliRunner
import pytest

from oci._vendor.requests import Request
from oci.exceptions import ServiceError
from oci.signer import inject_missing_headers

from oci_cli import cli_util
from services.generative_ai_sandbox.src.oci_cli_generative_ai_sandbox import generative_ai_sandbox_cli_extended  # noqa: F401
from services.generative_ai_sandbox.src.oci_cli_generative_ai_sandbox.generated import generativeaisandbox_cli


CLI_CTX_OBJ = {
    'config_file': None,
    'default_values_from_file': {},
    'profile': 'DEFAULT',
    'cli_rc_file': None,
    'request_id': None,
    'region': None,
    'endpoint': None,
    'realm_specific_endpoint': None,
    'connection_timeout': None,
    'enable_dual_stack': None,
    'enable_propagation': None,
    'read_timeout': None,
    'cert_bundle': None,
    'output': 'json',
    'query': None,
    'raw_output': False,
    'generate_full_command_json_input': None,
    'generate_param_json_input': None,
    'debug': False,
    'auth': None,
    'auth_purpose': None,
    'proxy': None,
    'no_retry': False,
    'max_attempts': None,
    'parameter_aliases': {},
    'command_aliases': {},
}


class FakeSSEClient(object):

    def events(self):
        yield SimpleNamespace(data='{"seq":1,"type":"STDOUT"}')
        yield SimpleNamespace(data='{"seq":2,"type":"FINISHED"}')


class FakeClient(object):

    def __init__(self):
        self.call = None

    def stream_sandbox_command_events(self, sandbox_id, command_id, **kwargs):
        self.call = {
            'sandbox_id': sandbox_id,
            'command_id': command_id,
            'kwargs': kwargs
        }
        return SimpleNamespace(
            headers={'content-type': 'text/event-stream'},
            data=FakeSSEClient()
        )


class FakeFileClient(object):

    def __init__(self, content):
        self.content = content
        self.call = None

    def write_sandbox_file(self, sandbox_id, file_path, write_sandbox_file_content_details, **kwargs):
        content = write_sandbox_file_content_details
        self.call = {
            'sandbox_id': sandbox_id,
            'file_path': file_path,
            'content': content.read() if hasattr(content, 'read') else content,
            'kwargs': kwargs
        }
        return SimpleNamespace(headers={}, data={})

    def read_sandbox_file(self, sandbox_id, file_path, **kwargs):
        self.call = {'sandbox_id': sandbox_id, 'file_path': file_path, 'kwargs': kwargs}
        return SimpleNamespace(headers={}, data=SimpleNamespace(raw=self))

    def stream(self, *args, **kwargs):
        if self.content:
            yield self.content[:3]
            yield self.content[3:]


class SigningFileClient(FakeFileClient):

    def write_sandbox_file(self, sandbox_id, file_path, write_sandbox_file_content_details, **kwargs):
        body = write_sandbox_file_content_details
        request = Request('POST', 'https://test.invalid/files/write', data=body).prepare()
        inject_missing_headers(request, sign_body=True, enforce_content_headers=True)
        self.headers = request.headers
        return super(SigningFileClient, self).write_sandbox_file(sandbox_id, file_path, body, **kwargs)


def test_sandbox_command_stream_renders_sse_event_data(monkeypatch):
    client = FakeClient()
    monkeypatch.setattr(cli_util, 'build_client', lambda *args: client)

    command = generativeaisandbox_cli.sandbox_command_group.commands['stream']
    assert not next(param for param in command.params if param.name == 'file').required
    result = CliRunner().invoke(
        command,
        [
            '--sandbox-id', 'sandbox_id',
            '--command-id', 'command_id',
            '--from-seq', '0',
            '--until-seq', '0'
        ],
        obj=dict(CLI_CTX_OBJ, request_id='stream-request-id')
    )

    assert result.exit_code == 0, result.output
    assert '"seq": 1' in result.output
    assert '"type": "STDOUT"' in result.output
    assert '"seq": 2' in result.output
    assert '"type": "FINISHED"' in result.output
    assert client.call['sandbox_id'] == 'sandbox_id'
    assert client.call['command_id'] == 'command_id'
    assert client.call['kwargs']['from_seq'] == 0
    assert client.call['kwargs']['until_seq'] == 0
    assert client.call['kwargs']['opc_request_id'] == 'stream-request-id'


def test_sandbox_command_aliases_preserve_released_paths():
    root_commands = generativeaisandbox_cli.generative_ai_sandbox_root_group.commands

    assert 'sandbox-collection' in root_commands
    assert 'sandbox-command-collection' in root_commands
    assert 'sandbox-command-event' in root_commands
    assert 'sandbox-command-output' in root_commands
    assert 'sandbox-snapshot-collection' in root_commands

    assert 'create-from-snapshot' in generativeaisandbox_cli.sandbox_group.commands
    assert 'create-sandbox-sandbox-snapshot-source' in generativeaisandbox_cli.sandbox_group.commands
    assert 'list' in generativeaisandbox_cli.sandbox_group.commands
    assert 'list' in generativeaisandbox_cli.sandbox_snapshot_group.commands
    assert 'list' in generativeaisandbox_cli.sandbox_command_group.commands
    assert 'run-and-stream' in generativeaisandbox_cli.sandbox_command_group.commands
    assert 'run-and-wait' in generativeaisandbox_cli.sandbox_command_group.commands
    assert 'stream' in generativeaisandbox_cli.sandbox_command_group.commands
    assert 'get-output' in generativeaisandbox_cli.sandbox_command_group.commands


def test_sandbox_file_manual_params_only_cover_remaining_gaps():
    read_params = {param.name: param for param in generativeaisandbox_cli.sandbox_file_group.commands['read'].params}
    write_params = {param.name: param for param in generativeaisandbox_cli.sandbox_file_group.commands['write'].params}

    assert 'sandbox_file_path' in read_params
    assert 'local_file' in read_params
    assert isinstance(read_params['file'].type, click.File)

    assert 'sandbox_file_path' in write_params
    assert isinstance(write_params['file'].type, click.types.StringParamType)
    assert isinstance(write_params['local_file'].type, click.File)


def test_sandbox_file_write_preserves_binary_content_and_request_options(monkeypatch, tmp_path):
    content = b'\x00\xff\x80binary\r\n\x00'
    local_file = tmp_path / 'upload.bin'
    local_file.write_bytes(content)
    checksum = base64.b64encode(hashlib.sha256(content).digest()).decode('ascii')
    client = FakeFileClient(content)
    monkeypatch.setattr(cli_util, 'build_client', lambda *args: client)

    result = CliRunner().invoke(
        generativeaisandbox_cli.sandbox_file_group.commands['write'],
        [
            '--sandbox-id', 'sandbox_id',
            '--sandbox-file-path', '/workspace/upload.bin',
            '--local-file', str(local_file),
            '--opc-content-sha256', checksum
        ],
        obj=dict(CLI_CTX_OBJ, request_id='upload-request-id')
    )

    assert result.exit_code == 0, result.output
    assert client.call['content'] == content
    assert client.call['sandbox_id'] == 'sandbox_id'
    assert client.call['file_path'] == '/workspace/upload.bin'
    assert client.call['kwargs']['opc_content_sha256'] == checksum
    assert client.call['kwargs']['opc_request_id'] == 'upload-request-id'


def test_sandbox_file_read_preserves_binary_content_and_request_options(monkeypatch, tmp_path):
    content = b'\x00\xff\x80binary\r\n\x00'
    local_file = tmp_path / 'download.bin'
    client = FakeFileClient(content)
    monkeypatch.setattr(cli_util, 'build_client', lambda *args: client)

    result = CliRunner().invoke(
        generativeaisandbox_cli.sandbox_file_group.commands['read'],
        [
            '--sandbox-id', 'sandbox_id',
            '--sandbox-file-path', '/workspace/download.bin',
            '--local-file', str(local_file)
        ],
        obj=dict(CLI_CTX_OBJ, request_id='download-request-id')
    )

    assert result.exit_code == 0, result.output
    assert local_file.read_bytes() == content
    assert client.call['sandbox_id'] == 'sandbox_id'
    assert client.call['file_path'] == '/workspace/download.bin'
    assert client.call['kwargs']['opc_request_id'] == 'download-request-id'


@pytest.mark.parametrize('from_json', [False, True])
@pytest.mark.parametrize('content', ['', '-', 'literal\ncontents', 'file://upload.bin', 'upload.bin', 'caf\u00e9 \u6d4b\u8bd5'])
def test_sandbox_file_write_preserves_released_literal_file_input(monkeypatch, tmp_path, content, from_json):
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'upload.bin').write_bytes(b'not-the-literal-value')
    client = SigningFileClient(b'')
    monkeypatch.setattr(cli_util, 'build_client', lambda *args: client)
    values = {'sandboxId': 'sandbox_id', 'sandboxFilePath': '/workspace/upload.bin', 'file': content}
    arguments = ['--from-json', json.dumps(values)] if from_json else [
        '--sandbox-id', values['sandboxId'], '--sandbox-file-path', values['sandboxFilePath'], '--file', content
    ]

    result = CliRunner().invoke(
        generativeaisandbox_cli.sandbox_file_group.commands['write'], arguments, obj=dict(CLI_CTX_OBJ)
    )

    assert result.exit_code == 0, result.output
    assert client.call['content'] == content.encode('utf-8')
    assert client.headers['content-length'] == str(len(content.encode('utf-8')))
    assert client.headers['content-type'] == 'application/octet-stream'
    assert 'transfer-encoding' not in client.headers


@pytest.mark.parametrize('file_key', ['file', 'localFile'])
def test_sandbox_file_read_accepts_both_json_destination_names(monkeypatch, tmp_path, file_key):
    destination = tmp_path / 'download.bin'
    content = b'\x00\xffbinary'
    client = FakeFileClient(content)
    monkeypatch.setattr(cli_util, 'build_client', lambda *args: client)
    result = CliRunner().invoke(
        generativeaisandbox_cli.sandbox_file_group.commands['read'],
        ['--from-json', json.dumps({'sandboxId': 'sandbox_id', 'sandboxFilePath': '/workspace/file.bin', file_key: str(destination)})],
        obj=dict(CLI_CTX_OBJ)
    )

    assert result.exit_code == 0, result.output
    assert destination.read_bytes() == content


@pytest.mark.parametrize('command_name', ['read', 'write'])
@pytest.mark.parametrize('both', [False, True])
@pytest.mark.parametrize('from_json', [False, True])
def test_sandbox_file_requires_one_input_or_destination(monkeypatch, tmp_path, command_name, both, from_json):
    local_file = tmp_path / 'file.bin'
    local_file.write_bytes(b'unchanged')
    client = FakeFileClient(b'')
    monkeypatch.setattr(cli_util, 'build_client', lambda *args: client)
    values = {'sandboxId': 'sandbox_id', 'sandboxFilePath': '/workspace/file.bin'}
    if both:
        values.update(file=str(local_file), localFile=str(local_file))
    if from_json:
        arguments = ['--from-json', json.dumps(values)]
    else:
        arguments = ['--sandbox-id', values['sandboxId'], '--sandbox-file-path', values['sandboxFilePath']]
        if both:
            arguments += ['--file', values['file'], '--local-file', values['localFile']]

    result = CliRunner().invoke(
        generativeaisandbox_cli.sandbox_file_group.commands[command_name], arguments, obj=dict(CLI_CTX_OBJ)
    )

    assert result.exit_code != 0
    assert 'Specify exactly one of --file or --local-file' in result.output
    assert client.call is None
    assert local_file.read_bytes() == b'unchanged'


@pytest.mark.parametrize('input_kind', ['file', 'stdin', 'json-stdin'])
@pytest.mark.parametrize('content', [b'', b'\x00\xff\x80' + b'pipe-content' * 100000])
def test_sandbox_file_write_uses_valid_signed_request_framing(monkeypatch, tmp_path, input_kind, content):
    class NonSeekableInput(io.BytesIO):
        def seekable(self):
            return False

        def seek(self, *args):
            raise io.UnsupportedOperation('pipe is not seekable')

        def tell(self):
            raise io.UnsupportedOperation('pipe has no position')

    client = SigningFileClient(content)
    monkeypatch.setattr(cli_util, 'build_client', lambda *args: client)
    values = {'sandboxId': 'sandbox_id', 'sandboxFilePath': '/workspace/pipe.bin', 'localFile': '-'}
    if input_kind == 'file':
        path = tmp_path / 'upload.bin'
        path.write_bytes(content)
        values['localFile'] = str(path)
    arguments = ['--from-json', json.dumps(values)] if input_kind == 'json-stdin' else [
        '--sandbox-id', values['sandboxId'],
        '--sandbox-file-path', values['sandboxFilePath'],
        '--local-file', values['localFile']
    ]
    result = CliRunner().invoke(
        generativeaisandbox_cli.sandbox_file_group.commands['write'],
        arguments,
        input=NonSeekableInput(content) if input_kind != 'file' else None,
        obj=dict(CLI_CTX_OBJ)
    )

    assert result.exit_code == 0, result.output
    assert client.call['content'] == content
    assert client.headers['content-length'] == str(len(content))
    assert client.headers['content-type'] == 'application/octet-stream'
    assert 'transfer-encoding' not in client.headers


@pytest.mark.parametrize('file_option', ['--file', '--local-file'])
@pytest.mark.parametrize('existing_file', [False, True])
def test_sandbox_file_empty_download_creates_or_truncates_destination(monkeypatch, tmp_path, existing_file, file_option):
    local_file = tmp_path / 'download.bin'
    if existing_file:
        local_file.write_bytes(b'old-content')
    client = FakeFileClient(b'')
    monkeypatch.setattr(cli_util, 'build_client', lambda *args: client)

    result = CliRunner().invoke(
        generativeaisandbox_cli.sandbox_file_group.commands['read'],
        ['--sandbox-id', 'sandbox_id', '--sandbox-file-path', '/workspace/empty.bin', file_option, str(local_file)],
        obj=dict(CLI_CTX_OBJ)
    )

    assert result.exit_code == 0, result.output
    assert local_file.read_bytes() == b''


@pytest.mark.parametrize('file_option', ['--file', '--local-file'])
@pytest.mark.parametrize('existing_file', [False, True])
def test_sandbox_file_failed_download_preserves_destination(monkeypatch, tmp_path, existing_file, file_option):
    def read_missing_file(*args, **kwargs):
        raise ServiceError(status=404, code='SandboxFileNotFound', headers={}, message='missing file', client_version='test-sdk')

    local_file = tmp_path / 'download.bin'
    if existing_file:
        local_file.write_bytes(b'old-content')
    client = SimpleNamespace(read_sandbox_file=read_missing_file)
    monkeypatch.setattr(cli_util, 'build_client', lambda *args: client)

    result = CliRunner().invoke(
        generativeaisandbox_cli.sandbox_file_group.commands['read'],
        ['--sandbox-id', 'sandbox_id', '--sandbox-file-path', '/workspace/missing.bin', file_option, str(local_file)],
        obj=dict(CLI_CTX_OBJ)
    )

    assert result.exit_code != 0
    assert 'SandboxFileNotFound' in result.output
    if existing_file:
        assert local_file.read_bytes() == b'old-content'
    else:
        assert not local_file.exists()
