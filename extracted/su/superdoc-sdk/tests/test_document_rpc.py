from __future__ import annotations

import asyncio
import json
import math
import os
import shlex
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

from superdoc.document_rpc import (
    DOCUMENT_RPC_DEFAULT_CHANGE_MODE_FEATURE,
    DOCUMENT_RPC_FEATURES,
    DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE,
    DOCUMENT_RPC_SOURCE_SAVE_FEATURE,
    build_document_invoke_request,
    build_document_open_params,
    document_rpc_request_supports_response_timeout,
    map_document_lifecycle_result,
    map_document_open_result,
)
from superdoc.errors import SuperDocError
from superdoc.generated.contract import OPERATION_INDEX
from superdoc.protocol import map_jsonrpc_error
from superdoc.runtime import SuperDocAsyncRuntime, SuperDocSyncRuntime, _resolve_runtime_process
from superdoc.transport import AsyncHostTransport, SyncHostTransport


GET_TEXT_OPERATION = {
    'operationId': 'doc.getText',
    'documentApiOperationId': 'getText',
    'mutates': False,
    'idempotency': 'idempotent',
    'params': [
        {'name': 'doc', 'kind': 'doc', 'type': 'string'},
        {'name': 'sessionId', 'kind': 'flag', 'type': 'string'},
        {'name': 'in', 'kind': 'jsonFlag', 'type': 'json', 'documentApiInputName': 'in'},
    ],
}

INSERT_OPERATION = {
    'operationId': 'doc.insert',
    'documentApiOperationId': 'insert',
    'mutates': True,
    'idempotency': 'non-idempotent',
    'supportsDryRun': True,
    'supportsTrackedMode': True,
    'params': [
        {'name': 'sessionId', 'kind': 'flag', 'type': 'string'},
        {'name': 'value', 'kind': 'flag', 'type': 'string', 'documentApiInputName': 'value'},
        {'name': 'expectedRevision', 'kind': 'flag', 'type': 'string'},
        {'name': 'changeMode', 'kind': 'flag', 'type': 'string'},
        {'name': 'dryRun', 'kind': 'flag', 'type': 'boolean'},
        {'name': 'supportCheck', 'kind': 'jsonFlag', 'type': 'json'},
    ],
}

DOCUMENT_HOST_MAX_REQUEST_TIMEOUT_MS = 2_147_483_647


def _document_host_script(
    directory: Path,
    extra_features: tuple[str, ...] = (),
    expected_default_change_mode: str = '',
    timeout_open_session: str = '',
) -> tuple[str, Path, Path]:
    trace_path = directory / 'methods.jsonl'
    argv_path = directory / 'argv.json'
    host_path = directory / 'document-host.py'
    host_path.write_text(textwrap.dedent(
        f'''\
        #!/usr/bin/env python3
        import json
        import sys

        trace_path = {str(trace_path)!r}
        request_trace_path = {str(directory / 'requests.jsonl')!r}
        argv_path = {str(argv_path)!r}
        open(argv_path, 'w', encoding='utf-8').write(json.dumps(sys.argv[1:]))

        def send(request_id, result):
            sys.stdout.write(json.dumps({{'jsonrpc': '2.0', 'id': request_id, 'result': result}}) + '\\n')
            sys.stdout.flush()

        def send_timeout(request_id):
            sys.stdout.write(json.dumps({{
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {{
                    'code': -32011,
                    'message': 'Host request timed out after 1ms.',
                    'data': {{'timeoutMs': 1}},
                }},
            }}) + '\\n')
            sys.stdout.flush()

        def send_missing_session(request_id, session_id):
            sys.stdout.write(json.dumps({{
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {{
                    'code': -32013,
                    'message': 'Document session is not open.',
                    'data': {{
                        'domainCode': 'DOCUMENT_RUNTIME_SESSION_NOT_FOUND',
                        'details': {{'sessionId': session_id}},
                    }},
                }},
            }}) + '\\n')
            sys.stdout.flush()

        def send_unsupported_timeout(request_id, method, operation_id=None):
            sys.stdout.write(json.dumps({{
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {{
                    'code': -32602,
                    'message': 'requestTimeoutMs is not supported for unsafe requests.',
                    'data': {{
                        'field': 'requestTimeoutMs',
                        'method': method,
                        **({{}} if operation_id is None else {{'operationId': operation_id}}),
                    }},
                }},
            }}) + '\\n')
            sys.stdout.flush()

        source_paths = {{}}
        for raw in sys.stdin:
            request = json.loads(raw)
            method = request['method']
            with open(trace_path, 'a', encoding='utf-8') as trace:
                trace.write(method + '\\n')
            with open(request_trace_path, 'a', encoding='utf-8') as request_trace:
                request_trace.write(json.dumps(request) + '\\n')
            if method == 'host.capabilities':
                send(request['id'], {{'protocolVersion': '1.0', 'features': {list(DOCUMENT_RPC_FEATURES) + ['host.shutdown', *extra_features]!r}}})
            elif method == 'document.open':
                if request['params']['sessionId'] == {timeout_open_session!r}:
                    send_timeout(request['id'])
                    continue
                params = request['params']
                if {expected_default_change_mode!r} and params.get('defaultChangeMode') != {expected_default_change_mode!r}:
                    raise RuntimeError('Missing default change mode.')
                source_paths[params['sessionId']] = params['path']
                send(request['id'], {{'sessionId': params['sessionId'], 'byteLength': 42}})
            elif method == 'document.invoke':
                session_id = request['params']['sessionId']
                options = request['params'].get('options', {{}})
                if (
                    'requestTimeoutMs' in request
                    and request['params']['operationId'] == 'insert'
                    and options.get('dryRun') is not True
                ):
                    send_unsupported_timeout(request['id'], method, 'insert')
                elif session_id not in source_paths:
                    send_missing_session(request['id'], session_id)
                else:
                    send(request['id'], 'mock text')
            elif method == 'document.save':
                params = request['params']
                if 'requestTimeoutMs' in request:
                    send_unsupported_timeout(request['id'], method)
                else:
                    output_path = params.get('path', source_paths[params['sessionId']])
                    send(request['id'], {{'sessionId': params['sessionId'], 'saved': True, 'inPlace': 'path' not in params, 'mode': 'review-preserving', 'output': {{'path': output_path, 'byteLength': 42}}, 'report': {{'warnings': []}}}})
            elif method == 'document.close':
                params = request['params']
                source_paths.pop(params['sessionId'], None)
                if 'id' in request:
                    send(request['id'], {{'sessionId': params['sessionId'], 'closed': True, 'discarded': params.get('discard', False)}})
            elif method == 'host.shutdown':
                send(request['id'], {{'shutdown': True}})
                break
            else:
                sys.stdout.write(json.dumps({{'jsonrpc': '2.0', 'id': request['id'], 'error': {{'code': -32601, 'message': 'unexpected ' + method}}}}) + '\\n')
                sys.stdout.flush()
        '''), encoding='utf-8')
    host_path.chmod(0o755)
    return str(host_path), trace_path, argv_path


class DocumentRpcProjectionTests(unittest.TestCase):
    def test_classifies_document_response_timeout_safety(self) -> None:
        self.assertTrue(document_rpc_request_supports_response_timeout(
            GET_TEXT_OPERATION,
            'document.invoke',
            {'operationId': 'getText', 'input': {}},
        ))
        self.assertFalse(document_rpc_request_supports_response_timeout(
            INSERT_OPERATION,
            'document.invoke',
            {'operationId': 'insert', 'input': {}},
        ))
        self.assertTrue(document_rpc_request_supports_response_timeout(
            INSERT_OPERATION,
            'document.invoke',
            {'operationId': 'insert', 'input': {}, 'options': {'dryRun': True}},
        ))
        self.assertTrue(document_rpc_request_supports_response_timeout(
            {**INSERT_OPERATION, 'idempotency': 'idempotent'},
            'document.invoke',
            {'operationId': 'insert', 'input': {}},
        ))
        self.assertFalse(document_rpc_request_supports_response_timeout(
            {'operationId': 'doc.unknown'},
            'document.invoke',
            {'operationId': 'unknown', 'input': {}},
        ))
        self.assertFalse(document_rpc_request_supports_response_timeout(
            {'operationId': 'doc.save'}, 'document.save', {},
        ))
        self.assertTrue(document_rpc_request_supports_response_timeout(
            {'operationId': 'doc.close'}, 'document.close', {},
        ))

    def test_maps_document_host_domain_errors_without_cli_error_fields(self) -> None:
        error = map_jsonrpc_error({
            'code': -32013,
            'message': 'Document session is dirty.',
            'data': {
                'domainCode': 'DOCUMENT_RUNTIME_SESSION_DIRTY',
                'stage': 'close',
                'details': {'sessionId': 'session-1'},
            },
        })
        self.assertEqual(error.code, 'DOCUMENT_RUNTIME_SESSION_DIRTY')
        self.assertEqual(error.details, {
            'domainDetails': {'sessionId': 'session-1'},
            'stage': 'close',
        })

    def test_projects_open_invoke_save_and_close_without_cli_argv(self) -> None:
        session_id, opened = build_document_open_params(
            {'doc': '/tmp/source.docx', 'sessionId': 'session-1', 'runtime': 'v2'},
            {'name': 'Ada', 'email': 'ada@example.com'},
        )
        self.assertEqual(session_id, 'session-1')
        self.assertEqual(opened, {
            'sessionId': 'session-1',
            'path': '/tmp/source.docx',
            'author': {'name': 'Ada', 'email': 'ada@example.com'},
        })
        _, opened_with_default = build_document_open_params(
            {'doc': '/tmp/source.docx', 'sessionId': 'session-1'},
            default_change_mode='tracked',
        )
        self.assertEqual(opened_with_default['defaultChangeMode'], 'tracked')

        method, invoked = build_document_invoke_request(
            session_id,
            INSERT_OPERATION,
            {
                'sessionId': session_id,
                'value': 'hello',
                'expectedRevision': '4',
                'changeMode': 'tracked',
                'dryRun': True,
                'supportCheck': {'version': 'sd-html-markdown-check/1'},
            },
        )
        self.assertEqual(method, 'document.invoke')
        self.assertEqual(invoked, {
            'sessionId': session_id,
            'operationId': 'insert',
            'input': {'value': 'hello'},
            'options': {
                'expectedRevision': '4',
                'changeMode': 'tracked',
                'dryRun': True,
                'supportCheck': {'version': 'sd-html-markdown-check/1'},
            },
        })

        method, saved = build_document_invoke_request(
            session_id,
            {'operationId': 'doc.save', 'params': []},
            {'sessionId': session_id, 'out': '/tmp/saved.docx', 'force': True},
        )
        self.assertEqual((method, saved), ('document.save', {
            'sessionId': session_id,
            'path': '/tmp/saved.docx',
            'overwrite': True,
        }))

        method, saved = build_document_invoke_request(
            session_id,
            {'operationId': 'doc.save', 'params': []},
            {'sessionId': session_id},
            host_features={DOCUMENT_RPC_SOURCE_SAVE_FEATURE},
        )
        self.assertEqual((method, saved), ('document.save', {
            'sessionId': session_id,
        }))
        with self.assertRaisesRegex(
            SuperDocError,
            'Structured document RPC requires inPlace to be a boolean.',
        ):
            build_document_invoke_request(
                session_id,
                {'operationId': 'doc.save', 'params': []},
                {'sessionId': session_id, 'inPlace': 'yes'},
            )
        with self.assertRaisesRegex(
            SuperDocError,
            'Structured document RPC host does not support source saves.',
        ):
            build_document_invoke_request(
                session_id,
                {'operationId': 'doc.save', 'params': []},
                {'sessionId': session_id},
            )

        method, closed = build_document_invoke_request(
            session_id,
            {'operationId': 'doc.close', 'params': []},
            {'sessionId': session_id, 'discard': True},
        )
        self.assertEqual((method, closed), ('document.close', {
            'sessionId': session_id,
            'discard': True,
        }))

    def test_uses_generated_document_api_routing_metadata(self) -> None:
        method, payload = build_document_invoke_request(
            'session-1',
            OPERATION_INDEX['doc.comments.create'],
            {
                'sessionId': 'session-1',
                'text': 'Review this',
                'parentId': 'parent-1',
            },
        )
        self.assertEqual(method, 'document.invoke')
        self.assertEqual(payload, {
            'sessionId': 'session-1',
            'operationId': 'comments.create',
            'input': {
                'text': 'Review this',
                'parentCommentId': 'parent-1',
            },
        })

        method, payload = build_document_invoke_request(
            'session-1',
            OPERATION_INDEX['doc.tables.split'],
            {
                'sessionId': 'session-1',
                'nodeId': 'table-1',
                'atRowIndex': 2,
            },
        )
        self.assertEqual(method, 'document.invoke')
        self.assertEqual(payload['input']['rowIndex'], 2)

    def test_fails_closed_for_unsupported_input(self) -> None:
        with self.assertRaisesRegex(SuperDocError, 'does not support doc.find') as raised:
            build_document_invoke_request(
                'session-1',
                {'operationId': 'doc.find', 'params': []},
                {'sessionId': 'session-1'},
            )
        self.assertEqual(raised.exception.code, 'DOCUMENT_RPC_INPUT_UNSUPPORTED')

        with self.assertRaisesRegex(SuperDocError, 'does not support stdinBytes'):
            build_document_invoke_request(
                'session-1', GET_TEXT_OPERATION, {'sessionId': 'session-1'}, stdin_bytes=b'data',
            )

        for field, value, message in (
            ('out', 123, 'does not support per-operation output paths'),
            ('out', '', 'does not support per-operation output paths'),
            ('force', 'true', 'does not support per-operation force'),
            ('force', True, 'does not support per-operation force'),
        ):
            with self.subTest(field=field, value=value):
                with self.assertRaisesRegex(SuperDocError, message):
                    build_document_invoke_request(
                        'session-1',
                        GET_TEXT_OPERATION,
                        {'sessionId': 'session-1', field: value},
                    )

        method, payload = build_document_invoke_request(
            'session-1', GET_TEXT_OPERATION, {'sessionId': 'session-1', 'force': False},
        )
        self.assertEqual(method, 'document.invoke')
        self.assertNotIn('force', payload)

        with self.assertRaisesRegex(SuperDocError, 'does not yet support expectedRevision'):
            build_document_invoke_request(
                'session-1',
                OPERATION_INDEX['doc.history.undo'],
                {'sessionId': 'session-1', 'expectedRevision': '4'},
            )

        with self.assertRaisesRegex(SuperDocError, 'does not support tracked mode'):
            build_document_invoke_request(
                'session-1',
                OPERATION_INDEX['doc.clearContent'],
                {'sessionId': 'session-1', 'changeMode': 'tracked'},
            )

    def test_maps_host_lifecycle_results_to_generated_sdk_shapes(self) -> None:
        opened = map_document_open_result(
            {'sessionId': 'session-1', 'byteLength': 42},
            'session-1',
            '/tmp/source.docx',
        )
        self.assertEqual(opened['contextId'], 'session-1')
        self.assertEqual(opened['document']['byteLength'], 42)

        saved = map_document_lifecycle_result(
            'doc.save',
            {
                'sessionId': 'session-1',
                'saved': True,
                'inPlace': False,
                'mode': 'review-preserving',
                'output': {'path': '/tmp/saved.docx', 'byteLength': 42},
                'report': {'warnings': []},
            },
            'session-1',
        )
        self.assertEqual(saved['contextId'], 'session-1')
        self.assertTrue(saved['saved'])
        self.assertFalse(map_document_lifecycle_result(
            'doc.save',
            {
                'sessionId': 'session-1',
                'saved': True,
                'mode': 'review-preserving',
                'output': {'path': '/tmp/saved.docx', 'byteLength': 42},
                'report': {'warnings': []},
            },
            'session-1',
            expected_in_place=False,
        )['inPlace'])

        closed = map_document_lifecycle_result(
            'doc.close',
            {'sessionId': 'session-1', 'closed': True, 'discarded': False},
            'session-1',
        )
        self.assertEqual(closed, {
            'contextId': 'session-1',
            'runtime': 'v2',
            'closed': True,
            'saved': False,
            'discarded': False,
            'defaultSessionCleared': False,
        })


class DocumentHostTransportTests(unittest.TestCase):
    def assert_invalid_timeout_error(
        self, error: SuperDocError, expected_timeout: object,
    ) -> None:
        self.assertEqual(error.code, 'INVALID_ARGUMENT')
        actual_timeout = error.details['requestTimeoutMs']
        if isinstance(expected_timeout, float) and math.isnan(expected_timeout):
            self.assertTrue(math.isnan(actual_timeout))
        else:
            self.assertEqual(actual_timeout, expected_timeout)

    def test_resolves_explicit_embedded_host_without_changing_the_default(self) -> None:
        with patch(
            'superdoc.runtime.resolve_embedded_document_host_path',
            return_value='/embedded/superdoc-document-host',
        ) as resolve_host:
            self.assertEqual(
                _resolve_runtime_process({'SUPERDOC_SDK_DOCUMENT_HOST_BIN': 'embedded'}, None),
                ('/embedded/superdoc-document-host', 'document'),
            )
            resolve_host.assert_called_once_with()

        with patch(
            'superdoc.runtime.resolve_embedded_cli_path',
            return_value='/embedded/superdoc',
        ) as resolve_cli:
            self.assertEqual(_resolve_runtime_process({}, None), ('/embedded/superdoc', 'cli'))
            resolve_cli.assert_called_once_with()

    def test_rejects_empty_document_host_selectors(self) -> None:
        for kwargs, message in (
            ({'document_host_path': '   '}, 'document_host_path'),
            ({'env': {'SUPERDOC_SDK_DOCUMENT_HOST_BIN': ''}}, 'SUPERDOC_SDK_DOCUMENT_HOST_BIN'),
        ):
            with self.subTest(message=message):
                with self.assertRaisesRegex(SuperDocError, message) as raised:
                    SuperDocSyncRuntime(**kwargs)
                self.assertEqual(raised.exception.code, 'INVALID_ARGUMENT')

    def test_sync_runtime_uses_standalone_host_without_cli_arguments_or_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            host, trace_path, argv_path = _document_host_script(
                Path(raw_directory),
                (DOCUMENT_RPC_DEFAULT_CHANGE_MODE_FEATURE,),
                'tracked',
            )
            runtime = SuperDocSyncRuntime(
                document_host_path=host,
                env={'SUPERDOC_CLI_BIN': '/path/that/must/not/run'},
                default_change_mode='tracked',
            )
            try:
                opened = runtime.invoke('doc.open', {'doc': '/tmp/source.docx', 'sessionId': 'sync-1'})
                self.assertEqual(opened['contextId'], 'sync-1')
                self.assertEqual(runtime.invoke('doc.getText', {'sessionId': 'sync-1'}), 'mock text')
                saved = runtime.invoke('doc.save', {
                    'sessionId': 'sync-1',
                    'out': '/tmp/saved.docx',
                    'force': True,
                })
                self.assertFalse(saved['inPlace'])
                runtime.invoke('doc.close', {'sessionId': 'sync-1'})
                with self.assertRaises(SuperDocError) as raised:
                    runtime.invoke('doc.describe', {})
                self.assertEqual(raised.exception.code, 'DOCUMENT_RPC_INPUT_UNSUPPORTED')
            finally:
                runtime.dispose()

            self.assertEqual(json.loads(argv_path.read_text(encoding='utf-8')), [])
            methods = trace_path.read_text(encoding='utf-8').splitlines()
            self.assertIn('document.open', methods)
            self.assertIn('document.invoke', methods)
            self.assertNotIn('cli.invoke', methods)

    def test_async_runtime_uses_the_same_document_projector(self) -> None:
        async def exercise() -> None:
            with tempfile.TemporaryDirectory() as raw_directory:
                host, trace_path, argv_path = _document_host_script(
                    Path(raw_directory),
                    (DOCUMENT_RPC_DEFAULT_CHANGE_MODE_FEATURE,),
                    'direct',
                )
                runtime = SuperDocAsyncRuntime(
                    env={
                        'SUPERDOC_SDK_DOCUMENT_HOST_BIN': host,
                        'SUPERDOC_CLI_BIN': '/path/that/must/not/run',
                    },
                    default_change_mode='direct',
                )
                try:
                    opened = await runtime.invoke(
                        'doc.open', {'doc': '/tmp/source.docx', 'sessionId': 'async-1'},
                    )
                    self.assertEqual(opened['contextId'], 'async-1')
                    self.assertEqual(
                        await runtime.invoke('doc.getText', {'sessionId': 'async-1'}),
                        'mock text',
                    )
                    await runtime.invoke('doc.close', {'sessionId': 'async-1'})
                finally:
                    await runtime.dispose()

                self.assertEqual(json.loads(argv_path.read_text(encoding='utf-8')), [])
                self.assertNotIn(
                    'cli.invoke', trace_path.read_text(encoding='utf-8').splitlines(),
                )

        asyncio.run(exercise())

    def test_sync_transport_forwards_client_and_per_operation_timeouts(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            host, _, _ = _document_host_script(
                directory, (DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE,),
            )
            runtime = SuperDocSyncRuntime(
                document_host_path=host,
                request_timeout_ms=DOCUMENT_HOST_MAX_REQUEST_TIMEOUT_MS,
            )
            try:
                runtime.invoke('doc.open', {
                    'doc': '/tmp/source.docx',
                    'sessionId': 'sync-timeout',
                })
                self.assertEqual(
                    runtime.invoke(
                        'doc.getText',
                        {'sessionId': 'sync-timeout'},
                        timeout_ms=25,
                    ),
                    'mock text',
                )
                self.assertEqual(
                    runtime.invoke('doc.insert', {
                        'sessionId': 'sync-timeout',
                        'value': 'unsafe mutation',
                    }),
                    'mock text',
                )
                self.assertFalse(runtime.invoke('doc.save', {
                    'sessionId': 'sync-timeout',
                    'out': '/tmp/sync-timeout.docx',
                })['inPlace'])
            finally:
                runtime.dispose()

            requests = [
                json.loads(line)
                for line in (directory / 'requests.jsonl').read_text(encoding='utf-8').splitlines()
            ]
            opened = next(request for request in requests if request['method'] == 'document.open')
            read = next(
                request for request in requests
                if request['method'] == 'document.invoke'
                and request['params']['operationId'] == 'getText'
            )
            mutation = next(
                request for request in requests
                if request['method'] == 'document.invoke'
                and request['params']['operationId'] == 'insert'
            )
            saved = next(request for request in requests if request['method'] == 'document.save')
            self.assertEqual(
                opened['requestTimeoutMs'], DOCUMENT_HOST_MAX_REQUEST_TIMEOUT_MS,
            )
            self.assertEqual(read['requestTimeoutMs'], 25)
            self.assertNotIn('requestTimeoutMs', mutation)
            self.assertNotIn('requestTimeoutMs', saved)
            self.assertNotIn('cli.invoke', [request['method'] for request in requests])

    def test_async_transport_forwards_client_and_per_operation_timeouts(self) -> None:
        async def exercise() -> None:
            with tempfile.TemporaryDirectory() as raw_directory:
                directory = Path(raw_directory)
                host, _, _ = _document_host_script(
                    directory, (DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE,),
                )
                runtime = SuperDocAsyncRuntime(
                    document_host_path=host,
                    request_timeout_ms=DOCUMENT_HOST_MAX_REQUEST_TIMEOUT_MS,
                )
                try:
                    await runtime.invoke('doc.open', {
                        'doc': '/tmp/source.docx',
                        'sessionId': 'async-timeout',
                    })
                    self.assertEqual(
                        await runtime.invoke(
                            'doc.getText',
                            {'sessionId': 'async-timeout'},
                            timeout_ms=25,
                        ),
                        'mock text',
                    )
                    self.assertEqual(
                        await runtime.invoke(
                            'doc.insert',
                            {
                                'sessionId': 'async-timeout',
                                'value': 'unsafe mutation',
                            },
                            timeout_ms=15,
                        ),
                        'mock text',
                    )
                    self.assertFalse((await runtime.invoke('doc.save', {
                        'sessionId': 'async-timeout',
                        'out': '/tmp/async-timeout.docx',
                    }))['inPlace'])
                finally:
                    await runtime.dispose()

                requests = [
                    json.loads(line)
                    for line in (directory / 'requests.jsonl').read_text(encoding='utf-8').splitlines()
                ]
                opened = next(request for request in requests if request['method'] == 'document.open')
                read = next(
                    request for request in requests
                    if request['method'] == 'document.invoke'
                    and request['params']['operationId'] == 'getText'
                )
                mutation = next(
                    request for request in requests
                    if request['method'] == 'document.invoke'
                    and request['params']['operationId'] == 'insert'
                )
                saved = next(request for request in requests if request['method'] == 'document.save')
                self.assertEqual(
                    opened['requestTimeoutMs'], DOCUMENT_HOST_MAX_REQUEST_TIMEOUT_MS,
                )
                self.assertEqual(read['requestTimeoutMs'], 25)
                self.assertNotIn('requestTimeoutMs', mutation)
                self.assertNotIn('requestTimeoutMs', saved)
                self.assertNotIn('cli.invoke', [request['method'] for request in requests])

        asyncio.run(exercise())

    def test_sync_transport_preserves_unsafe_per_operation_watchdog(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            host, _, _ = _document_host_script(Path(raw_directory))
            runtime = SuperDocSyncRuntime(document_host_path=host)
            try:
                runtime.invoke('doc.open', {
                    'doc': '/tmp/source.docx',
                    'sessionId': 'sync-unsafe-watchdog',
                })
                with patch.object(
                    runtime._transport,
                    '_send_request',
                    wraps=runtime._transport._send_request,
                ) as send_request:
                    self.assertEqual(
                        runtime.invoke(
                            'doc.insert',
                            {
                                'sessionId': 'sync-unsafe-watchdog',
                                'value': 'definitive result',
                            },
                            timeout_ms=60_000,
                        ),
                        'mock text',
                    )
                self.assertEqual(send_request.call_args.args[2], 65_000)
                self.assertIsNone(send_request.call_args.kwargs['request_timeout_ms'])
            finally:
                runtime.dispose()

    def test_async_transport_preserves_unsafe_per_operation_watchdog(self) -> None:
        async def exercise() -> None:
            with tempfile.TemporaryDirectory() as raw_directory:
                host, _, _ = _document_host_script(Path(raw_directory))
                runtime = SuperDocAsyncRuntime(document_host_path=host)
                try:
                    await runtime.invoke('doc.open', {
                        'doc': '/tmp/source.docx',
                        'sessionId': 'async-unsafe-watchdog',
                    })
                    with patch.object(
                        runtime._transport,
                        '_send_request',
                        wraps=runtime._transport._send_request,
                    ) as send_request:
                        self.assertEqual(
                            await runtime.invoke(
                                'doc.insert',
                                {
                                    'sessionId': 'async-unsafe-watchdog',
                                    'value': 'definitive result',
                                },
                                timeout_ms=60_000,
                            ),
                            'mock text',
                        )
                    self.assertEqual(send_request.call_args.args[2], 65_000)
                    self.assertIsNone(
                        send_request.call_args.kwargs['request_timeout_ms'],
                    )
                finally:
                    await runtime.dispose()

        asyncio.run(exercise())

    def test_sync_transport_rejects_invalid_timeouts_before_sending_requests(self) -> None:
        invalid_timeouts = (
            True,
            'abc',
            0,
            -5,
            float('nan'),
            float('inf'),
            DOCUMENT_HOST_MAX_REQUEST_TIMEOUT_MS + 1,
            10**1000,
        )

        for invalid_timeout in invalid_timeouts:
            with self.subTest(source='client', timeout=invalid_timeout):
                with tempfile.TemporaryDirectory() as raw_directory:
                    directory = Path(raw_directory)
                    host, _, _ = _document_host_script(
                        directory, (DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE,),
                    )
                    runtime = SuperDocSyncRuntime(
                        document_host_path=host,
                        request_timeout_ms=invalid_timeout,
                    )
                    try:
                        with self.assertRaises(SuperDocError) as raised:
                            runtime.invoke('doc.open', {
                                'doc': '/tmp/source.docx',
                                'sessionId': 'sync-invalid-client-timeout',
                            })
                        self.assert_invalid_timeout_error(
                            raised.exception, invalid_timeout,
                        )
                        self.assertFalse((directory / 'requests.jsonl').exists())
                    finally:
                        runtime.dispose()

        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            host, _, _ = _document_host_script(
                directory, (DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE,),
            )
            runtime = SuperDocSyncRuntime(document_host_path=host)
            try:
                runtime.invoke('doc.open', {
                    'doc': '/tmp/source.docx',
                    'sessionId': 'sync-invalid-operation-timeout',
                })
                request_trace = directory / 'requests.jsonl'
                requests_before = request_trace.read_text(encoding='utf-8')
                for invalid_timeout in invalid_timeouts:
                    with self.subTest(source='operation', timeout=invalid_timeout):
                        with self.assertRaises(SuperDocError) as raised:
                            runtime.invoke(
                                'doc.getText',
                                {'sessionId': 'sync-invalid-operation-timeout'},
                                timeout_ms=invalid_timeout,
                            )
                        self.assert_invalid_timeout_error(
                            raised.exception, invalid_timeout,
                        )
                        self.assertEqual(
                            request_trace.read_text(encoding='utf-8'), requests_before,
                        )
            finally:
                runtime.dispose()

    def test_async_transport_rejects_invalid_timeouts_before_sending_requests(self) -> None:
        async def exercise() -> None:
            invalid_timeouts = (
                True,
                'abc',
                0,
                -5,
                float('nan'),
                float('inf'),
                DOCUMENT_HOST_MAX_REQUEST_TIMEOUT_MS + 1,
                10**1000,
            )

            for invalid_timeout in invalid_timeouts:
                with self.subTest(source='client', timeout=invalid_timeout):
                    with tempfile.TemporaryDirectory() as raw_directory:
                        directory = Path(raw_directory)
                        host, _, _ = _document_host_script(
                            directory, (DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE,),
                        )
                        runtime = SuperDocAsyncRuntime(
                            document_host_path=host,
                            request_timeout_ms=invalid_timeout,
                        )
                        try:
                            with self.assertRaises(SuperDocError) as raised:
                                await runtime.invoke('doc.open', {
                                    'doc': '/tmp/source.docx',
                                    'sessionId': 'async-invalid-client-timeout',
                                })
                            self.assert_invalid_timeout_error(
                                raised.exception, invalid_timeout,
                            )
                            self.assertFalse((directory / 'requests.jsonl').exists())
                        finally:
                            await runtime.dispose()

            with tempfile.TemporaryDirectory() as raw_directory:
                directory = Path(raw_directory)
                host, _, _ = _document_host_script(
                    directory, (DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE,),
                )
                runtime = SuperDocAsyncRuntime(document_host_path=host)
                try:
                    await runtime.invoke('doc.open', {
                        'doc': '/tmp/source.docx',
                        'sessionId': 'async-invalid-operation-timeout',
                    })
                    request_trace = directory / 'requests.jsonl'
                    requests_before = request_trace.read_text(encoding='utf-8')
                    for invalid_timeout in invalid_timeouts:
                        with self.subTest(source='operation', timeout=invalid_timeout):
                            with self.assertRaises(SuperDocError) as raised:
                                await runtime.invoke(
                                    'doc.getText',
                                    {'sessionId': 'async-invalid-operation-timeout'},
                                    timeout_ms=invalid_timeout,
                                )
                            self.assert_invalid_timeout_error(
                                raised.exception, invalid_timeout,
                            )
                            self.assertEqual(
                                request_trace.read_text(encoding='utf-8'), requests_before,
                            )
                finally:
                    await runtime.dispose()

        asyncio.run(exercise())

    def test_sync_transport_rejects_invalid_client_timeout_before_connect(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            host, _, argv_path = _document_host_script(
                directory, (DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE,),
            )
            runtime = SuperDocSyncRuntime(
                document_host_path=host,
                request_timeout_ms='abc',
            )
            try:
                with self.assertRaises(SuperDocError) as raised:
                    runtime.connect()
                self.assert_invalid_timeout_error(raised.exception, 'abc')
                self.assertFalse(argv_path.exists())
            finally:
                runtime.dispose()

    def test_async_transport_rejects_invalid_client_timeout_before_connect(self) -> None:
        async def exercise() -> None:
            with tempfile.TemporaryDirectory() as raw_directory:
                directory = Path(raw_directory)
                host, _, argv_path = _document_host_script(
                    directory, (DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE,),
                )
                runtime = SuperDocAsyncRuntime(
                    document_host_path=host,
                    request_timeout_ms='abc',
                )
                try:
                    with self.assertRaises(SuperDocError) as raised:
                        await runtime.connect()
                    self.assert_invalid_timeout_error(raised.exception, 'abc')
                    self.assertFalse(argv_path.exists())
                finally:
                    await runtime.dispose()

        asyncio.run(exercise())

    def test_sync_transport_relies_on_host_cleanup_after_document_open_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            host, trace_path, _ = _document_host_script(
                directory,
                (DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE,),
                timeout_open_session='sync-open-timeout',
            )
            runtime = SuperDocSyncRuntime(document_host_path=host)
            try:
                runtime.invoke('doc.open', {
                    'doc': '/tmp/source-a.docx',
                    'sessionId': 'sync-open-a',
                })
                with self.assertRaises(SuperDocError) as raised:
                    runtime.invoke('doc.open', {
                        'doc': '/tmp/source.docx',
                        'sessionId': 'sync-open-timeout',
                    }, timeout_ms=1)
                self.assertEqual(raised.exception.code, 'TIMEOUT')
                self.assertEqual(raised.exception.details, {'timeoutMs': 1})
                self.assertEqual(
                    runtime.invoke('doc.getText', {'sessionId': 'sync-open-a'}),
                    'mock text',
                )
            finally:
                runtime.dispose()

            methods = trace_path.read_text(encoding='utf-8').splitlines()
            self.assertEqual(methods.count('host.capabilities'), 1)
            self.assertEqual(methods.count('document.open'), 2)
            requests = [
                json.loads(line)
                for line in (directory / 'requests.jsonl').read_text(encoding='utf-8').splitlines()
            ]
            self.assertFalse(any(
                request['method'] == 'document.close'
                and request['params']['sessionId'] == 'sync-open-timeout'
                for request in requests
            ))

    def test_async_transport_relies_on_host_cleanup_after_document_open_timeout(self) -> None:
        async def exercise() -> None:
            with tempfile.TemporaryDirectory() as raw_directory:
                directory = Path(raw_directory)
                host, trace_path, _ = _document_host_script(
                    directory,
                    (DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE,),
                    timeout_open_session='async-open-timeout',
                )
                runtime = SuperDocAsyncRuntime(document_host_path=host)
                try:
                    await runtime.invoke('doc.open', {
                        'doc': '/tmp/source-a.docx',
                        'sessionId': 'async-open-a',
                    })
                    with self.assertRaises(SuperDocError) as raised:
                        await runtime.invoke('doc.open', {
                            'doc': '/tmp/source.docx',
                            'sessionId': 'async-open-timeout',
                        }, timeout_ms=1)
                    self.assertEqual(raised.exception.code, 'TIMEOUT')
                    self.assertEqual(raised.exception.details, {'timeoutMs': 1})
                    self.assertEqual(
                        await runtime.invoke('doc.getText', {'sessionId': 'async-open-a'}),
                        'mock text',
                    )
                finally:
                    await runtime.dispose()

                methods = trace_path.read_text(encoding='utf-8').splitlines()
                self.assertEqual(methods.count('host.capabilities'), 1)
                self.assertEqual(methods.count('document.open'), 2)
                requests = [
                    json.loads(line)
                    for line in (directory / 'requests.jsonl').read_text(encoding='utf-8').splitlines()
                ]
                self.assertFalse(any(
                    request['method'] == 'document.close'
                    and request['params']['sessionId'] == 'async-open-timeout'
                    for request in requests
                ))

        asyncio.run(exercise())

    def test_requires_timeout_capability_only_when_a_timeout_is_requested(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            host, _, _ = _document_host_script(Path(raw_directory))
            runtime = SuperDocSyncRuntime(
                document_host_path=host,
                request_timeout_ms=1_234,
            )
            with self.assertRaisesRegex(SuperDocError, DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE):
                runtime.connect()

        with tempfile.TemporaryDirectory() as raw_directory:
            host, trace_path, _ = _document_host_script(Path(raw_directory))
            runtime = SuperDocSyncRuntime(document_host_path=host)
            try:
                runtime.invoke('doc.open', {
                    'doc': '/tmp/source.docx',
                    'sessionId': 'sync-old-host',
                })
                with self.assertRaisesRegex(SuperDocError, DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE):
                    runtime.invoke(
                        'doc.getText',
                        {'sessionId': 'sync-old-host'},
                        timeout_ms=25,
                    )
                self.assertEqual(
                    runtime.invoke(
                        'doc.insert',
                        {'sessionId': 'sync-old-host', 'value': 'unsafe mutation'},
                        timeout_ms=25,
                    ),
                    'mock text',
                )
            finally:
                runtime.dispose()
            requests = [
                json.loads(line)
                for line in (
                    Path(raw_directory) / 'requests.jsonl'
                ).read_text(encoding='utf-8').splitlines()
            ]
            invoked = [request for request in requests if request['method'] == 'document.invoke']
            self.assertEqual(len(invoked), 1)
            self.assertNotIn('requestTimeoutMs', invoked[0])

        async def reject_missing_async_capability() -> None:
            with tempfile.TemporaryDirectory() as raw_directory:
                host, _, _ = _document_host_script(Path(raw_directory))
                runtime = SuperDocAsyncRuntime(
                    document_host_path=host,
                    request_timeout_ms=1_234,
                )
                with self.assertRaisesRegex(SuperDocError, DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE):
                    await runtime.connect()

        asyncio.run(reject_missing_async_capability())

        async def allow_unsafe_async_timeout_without_capability() -> None:
            with tempfile.TemporaryDirectory() as raw_directory:
                directory = Path(raw_directory)
                host, _, _ = _document_host_script(directory)
                runtime = SuperDocAsyncRuntime(document_host_path=host)
                try:
                    await runtime.invoke('doc.open', {
                        'doc': '/tmp/source.docx',
                        'sessionId': 'async-old-host',
                    })
                    self.assertEqual(
                        await runtime.invoke(
                            'doc.insert',
                            {'sessionId': 'async-old-host', 'value': 'unsafe mutation'},
                            timeout_ms=25,
                        ),
                        'mock text',
                    )
                finally:
                    await runtime.dispose()
                requests = [
                    json.loads(line)
                    for line in (
                        directory / 'requests.jsonl'
                    ).read_text(encoding='utf-8').splitlines()
                ]
                invoked = [
                    request for request in requests if request['method'] == 'document.invoke'
                ]
                self.assertEqual(len(invoked), 1)
                self.assertNotIn('requestTimeoutMs', invoked[0])

        asyncio.run(allow_unsafe_async_timeout_without_capability())

    def test_requires_default_change_mode_capability_when_configured(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            host, _, _ = _document_host_script(Path(raw_directory))
            runtime = SuperDocSyncRuntime(
                document_host_path=host,
                default_change_mode='tracked',
            )
            with self.assertRaisesRegex(
                SuperDocError, DOCUMENT_RPC_DEFAULT_CHANGE_MODE_FEATURE,
            ):
                runtime.connect()

        async def reject_missing_async_capability() -> None:
            with tempfile.TemporaryDirectory() as raw_directory:
                host, _, _ = _document_host_script(Path(raw_directory))
                runtime = SuperDocAsyncRuntime(
                    document_host_path=host,
                    default_change_mode='tracked',
                )
                with self.assertRaisesRegex(
                    SuperDocError, DOCUMENT_RPC_DEFAULT_CHANGE_MODE_FEATURE,
                ):
                    await runtime.connect()

        asyncio.run(reject_missing_async_capability())

    def test_requires_author_capability_when_user_is_configured(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            host, _, _ = _document_host_script(Path(raw_directory))
            runtime = SuperDocSyncRuntime(document_host_path=host, user={'name': 'Ada'})
            with self.assertRaisesRegex(SuperDocError, 'document.open.author'):
                runtime.connect()

        async def reject_missing_async_capability() -> None:
            with tempfile.TemporaryDirectory() as raw_directory:
                host, _, _ = _document_host_script(Path(raw_directory))
                runtime = SuperDocAsyncRuntime(document_host_path=host, user={'name': 'Ada'})
                with self.assertRaisesRegex(SuperDocError, 'document.open.author'):
                    await runtime.connect()

        asyncio.run(reject_missing_async_capability())


if __name__ == '__main__':
    unittest.main()
