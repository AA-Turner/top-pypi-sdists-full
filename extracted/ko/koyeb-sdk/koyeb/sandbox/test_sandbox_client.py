import unittest
from unittest.mock import patch

from koyeb.sandbox.sandbox import AsyncSandbox, Sandbox
from koyeb.sandbox.utils import SandboxError


class TestGetClientWhenUrlUnavailable(unittest.TestCase):
    """A gone sandbox makes _get_sandbox_url() return None (the metadata/domain
    lookups swallow NotFound and return None). _get_client/_get_async_client must
    raise SandboxError in that case, as their docstring promises, rather than
    letting a raw ``TypeError: cannot unpack non-iterable NoneType object`` escape.
    """

    def test_get_client_raises_sandbox_error(self):
        sb = Sandbox.__new__(Sandbox)
        sb._client = None
        sb.sandbox_secret = None
        with patch.object(Sandbox, "_get_sandbox_url", return_value=None):
            with self.assertRaises(SandboxError):
                sb._get_client()

    def test_get_async_client_raises_sandbox_error(self):
        sb = AsyncSandbox.__new__(AsyncSandbox)
        sb._async_client = None
        sb.sandbox_secret = None
        with patch.object(AsyncSandbox, "_get_sandbox_url", return_value=None):
            with self.assertRaises(SandboxError):
                sb._get_async_client()


if __name__ == "__main__":
    unittest.main()
