from __future__ import annotations

import asyncio
import unittest

from superdoc.client import AsyncSuperDocClient, SuperDocClient
from superdoc.errors import SuperDocError


class LocalIntrospectionTests(unittest.TestCase):
    def test_sync_client_does_not_need_a_document_host(self) -> None:
        client = SuperDocClient(document_host_path='/missing/superdoc-document-host')

        overview = client.describe()
        detail = client.describe_command({'operationId': 'find'})

        self.assertEqual(overview['operationCount'], len(overview['operations']))
        self.assertEqual(detail['operation']['id'], 'doc.find')

    def test_async_client_does_not_need_a_document_host(self) -> None:
        async def run() -> None:
            client = AsyncSuperDocClient(document_host_path='/missing/superdoc-document-host')

            overview = await client.describe()
            detail = await client.describe_command({'operationId': 'session use'})

            self.assertEqual(overview['operationCount'], len(overview['operations']))
            self.assertEqual(detail['operation']['id'], 'doc.session.setDefault')

        asyncio.run(run())

    def test_describe_command_preserves_lookup_errors(self) -> None:
        client = SuperDocClient(document_host_path='/missing/superdoc-document-host')

        with self.assertRaises(SuperDocError) as missing:
            client.describe_command({})
        self.assertEqual(missing.exception.code, 'INVALID_ARGUMENT')
        self.assertIsNone(missing.exception.exit_code)

        with self.assertRaises(SuperDocError) as unknown:
            client.describe_command({'operationId': 'doc.missing'})
        self.assertEqual(unknown.exception.code, 'TARGET_NOT_FOUND')
        self.assertEqual(unknown.exception.details, {'query': 'doc.missing'})
        self.assertEqual(unknown.exception.exit_code, 1)

    def test_describe_returns_a_fresh_value(self) -> None:
        client = SuperDocClient(document_host_path='/missing/superdoc-document-host')
        first = client.describe()
        first['operations'][0]['id'] = 'changed'

        second = client.describe()
        self.assertNotEqual(second['operations'][0]['id'], 'changed')


if __name__ == '__main__':
    unittest.main()
