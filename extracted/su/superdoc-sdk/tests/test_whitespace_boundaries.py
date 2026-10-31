from __future__ import annotations

import asyncio
import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from superdoc.client import AsyncSuperDocClient, SuperDocClient
from superdoc.document_rpc import build_document_open_params
from superdoc.errors import SuperDocError
from superdoc.protocol import InvalidFrame, JsonRpcResponse, parse_jsonrpc_line
from superdoc.skill_api import get_skill


CHARACTERS_FILE = Path(__file__).resolve().parents[3] / 'codegen/src/node22-core-characters.json'
CHARACTERS_BYTES = CHARACTERS_FILE.read_bytes()
assert hashlib.sha256(CHARACTERS_BYTES).hexdigest() == 'ba26df167c0853b955b6e04d856a899a7c83865c7b5834d80645d1b41d66c693'
JS_TRIM_POINTS = json.loads(CHARACTERS_BYTES)['trimCodePoints']
OTHER_POINTS = [0x85, 0x1c, 0x1d, 0x1e, 0x1f, 0x200b]
POINTS = [*JS_TRIM_POINTS, *OTHER_POINTS]


class WhitespaceBoundaryTests(unittest.TestCase):
    def test_host_selectors_preserve_values_and_refuse_javascript_blanks_without_spawn(self) -> None:
        for point in POINTS:
            for asynchronous in [False, True]:
                for source in ['argument', 'environment']:
                    with self.subTest(point=hex(point), asynchronous=asynchronous, source=source):
                        value = chr(point)
                        env = {'SUPERDOC_CLI_BIN': '/unused/whitespace-cli'}
                        kwargs = {'env': env}
                        if source == 'argument':
                            kwargs['document_host_path'] = value
                        else:
                            env['SUPERDOC_SDK_DOCUMENT_HOST_BIN'] = value
                        before_env = dict(env)
                        client_type = AsyncSuperDocClient if asynchronous else SuperDocClient
                        with patch('superdoc.transport.subprocess.Popen') as sync_spawn, patch(
                            'superdoc.transport.asyncio.create_subprocess_exec',
                        ) as async_spawn:
                            if point in JS_TRIM_POINTS:
                                with self.assertRaises(SuperDocError) as error:
                                    client_type(**kwargs)
                                self.assertEqual(error.exception.code, 'INVALID_ARGUMENT')
                            else:
                                client = client_type(**kwargs)
                                self.assertEqual(client._runtime._transport._cli_bin, value)
                                self.assertEqual(client._runtime._transport._process_mode, 'document')
                                self.assertIsNone(client._runtime._transport._process)
                                cleanup = client.dispose()
                                if asynchronous:
                                    asyncio.run(cleanup)
                            sync_spawn.assert_not_called()
                            async_spawn.assert_not_called()
                        self.assertEqual(env, before_env)

    def test_skill_lookup_uses_javascript_trim_and_keeps_unknown_skill_diagnostics(self) -> None:
        expected = get_skill('editing-docx')
        for point in POINTS:
            for name in ['editing-docx', 'whitespace-missing-skill']:
                with self.subTest(point=hex(point), name=name):
                    supplied = chr(point) + name + chr(point)
                    if point in JS_TRIM_POINTS and name == 'editing-docx':
                        self.assertEqual(get_skill(supplied), expected)
                    else:
                        with self.assertRaises(SuperDocError) as error:
                            get_skill(supplied)
                        if point in JS_TRIM_POINTS:
                            self.assertEqual(error.exception.code, 'SKILL_NOT_FOUND')
                            self.assertEqual(error.exception.details['name'], name)
                            self.assertIn('editing-docx', error.exception.details['available'])
                        else:
                            self.assertEqual(error.exception.code, 'INVALID_ARGUMENT')
                            self.assertEqual(error.exception.details, {'name': supplied})

    def test_author_blankness_matches_the_authored_javascript_set(self) -> None:
        for point in POINTS:
            with self.subTest(point=hex(point)):
                name = chr(point)
                params = {'doc': 'fixture.docx', 'sessionId': 'whitespace-session'}
                if point in JS_TRIM_POINTS:
                    with self.assertRaises(SuperDocError) as error:
                        build_document_open_params(params, {'name': name})
                    self.assertEqual(error.exception.code, 'INVALID_ARGUMENT')
                    self.assertEqual(str(error.exception), 'user.name must be a non-empty string.')
                else:
                    _, opened = build_document_open_params(params, {'name': name})
                    self.assertEqual(opened['author'], {'name': name})
                _, opened = build_document_open_params(params, {'name': name + 'Ada' + name})
                self.assertEqual(opened['author'], {'name': name + 'Ada' + name})

    def test_open_path_blankness_matches_the_authored_routing_set(self) -> None:
        for point in POINTS:
            with self.subTest(point=hex(point)):
                path = chr(point)
                params = {'doc': path, 'sessionId': 'whitespace-session'}
                if point in JS_TRIM_POINTS:
                    with self.assertRaises(SuperDocError) as error:
                        build_document_open_params(params)
                    self.assertEqual(error.exception.code, 'DOCUMENT_RPC_INPUT_UNSUPPORTED')
                    self.assertEqual(error.exception.details, {'operationId': 'doc.open'})
                else:
                    session, opened = build_document_open_params(params)
                    self.assertEqual(session, 'whitespace-session')
                    self.assertEqual(opened['path'], path)

    def test_local_lookup_uses_javascript_trim_without_changing_query_metadata(self) -> None:
        for point in POINTS:
            for asynchronous in [False, True]:
                with self.subTest(point=hex(point), asynchronous=asynchronous):
                    query = chr(point) + 'doc.getText' + chr(point)
                    client_type = AsyncSuperDocClient if asynchronous else SuperDocClient
                    client = client_type(document_host_path='/missing/whitespace-document-host')
                    try:
                        def invoke():
                            result = client.describe_command({'operationId': query})
                            return asyncio.run(result) if asynchronous else result

                        if point in JS_TRIM_POINTS:
                            result = invoke()
                            self.assertEqual(result['operation']['id'], 'doc.getText')
                            self.assertEqual(result['query'], query)
                        else:
                            with self.assertRaises(SuperDocError) as error:
                                invoke()
                            self.assertEqual(error.exception.code, 'TARGET_NOT_FOUND')
                            self.assertEqual(error.exception.details, {'query': query})
                            self.assertEqual(error.exception.exit_code, 1)
                    finally:
                        cleanup = client.dispose()
                        if asynchronous:
                            asyncio.run(cleanup)

    def test_jsonl_accepts_only_json_whitespace_outside_a_frame(self) -> None:
        frame = json.dumps({'jsonrpc': '2.0', 'id': 7, 'result': {'marker': 'CONTROL'}})
        for point in POINTS:
            with self.subTest(point=hex(point)):
                line = chr(point) + frame + chr(point)
                parsed = parse_jsonrpc_line(line)
                if point in [0x20, 0x09, 0x0a, 0x0d]:
                    self.assertIsInstance(parsed, JsonRpcResponse)
                    self.assertEqual(parsed.id, 7)
                    self.assertEqual(parsed.result, {'marker': 'CONTROL'})
                else:
                    self.assertIsInstance(parsed, InvalidFrame)
                    self.assertEqual(parsed.raw, line)
