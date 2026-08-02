from __future__ import annotations

import importlib
import unittest


try:
    import torch
except Exception:  # pragma: no cover - exercised only when torch is absent.
    torch = None


scan_module = importlib.import_module("hoptorch.scan")


class PatchMixin:
    def setUp(self) -> None:
        scan_module._reset_scan_backward_state_for_tests()
        self._patches = []

    def tearDown(self) -> None:
        for name, value in reversed(self._patches):
            setattr(scan_module, name, value)
        scan_module._reset_scan_backward_state_for_tests()

    def patch_attr(self, name, value):
        self._patches.append((name, getattr(scan_module, name)))
        setattr(scan_module, name, value)


class PublicApiTests(PatchMixin, unittest.TestCase):
    def test_import_shape(self):
        import hoptorch

        self.assertTrue(callable(hoptorch.scan))
        self.assertTrue(callable(scan_module.scan))
        self.assertTrue(callable(scan_module.ensure_scan_backward))
        self.assertTrue(callable(scan_module.has_scan))
        self.assertTrue(callable(scan_module.scan_unavailable_reason))
        self.assertTrue(callable(scan_module.patch_scan_backward))

    def test_scan_exists_or_reports_reason(self):
        if torch is None:
            self.skipTest("torch is not installed")
        if scan_module.has_scan():
            self.assertIsInstance(scan_module.ensure_scan_backward("cpu"), bool)
        else:
            reason = scan_module.scan_unavailable_reason("cpu")
            self.assertIsInstance(reason, str)
            self.assertIn("scan", reason)

    def test_missing_scan_reports_stable_reason(self):
        self.patch_attr(
            "_get_torch_scan",
            lambda: (None, "torch._higher_order_ops.scan is not available"),
        )
        self.assertFalse(scan_module.has_scan())
        self.assertEqual(
            scan_module.scan_unavailable_reason("cpu"),
            "torch._higher_order_ops.scan is not available",
        )

    def test_public_scan_wrapper_raises_when_unhealthy(self):
        if torch is None:
            self.skipTest("torch is not installed")

        def fake_scan(fn, init, xs, *, dim=0, **kwargs):
            return fn(init, xs[0])

        self.patch_attr("_get_torch_scan", lambda: (fake_scan, None))
        self.patch_attr("_run_scan_backward_probe", lambda device: False)
        self.patch_attr("_install_scan_backward_patch", lambda scan_module_arg: False)

        with self.assertRaisesRegex(RuntimeError, "health check"):
            scan_module.scan(lambda carry, x: (carry + x, carry + x), torch.zeros(()), torch.ones(2))

    def test_public_scan_wrapper(self):
        if torch is None:
            self.skipTest("torch is not installed")
        if not scan_module.has_scan():
            self.skipTest("torch scan is not available")
        if not scan_module.ensure_scan_backward("cpu"):
            self.skipTest(scan_module.scan_unavailable_reason("cpu") or "scan backward unavailable")

        from hoptorch import scan

        xs = torch.arange(4.0)

        def step(carry, x):
            next_carry = carry + x
            return next_carry, next_carry * 2

        carry, ys = scan(step, torch.zeros(()), xs, dim=0)
        self.assertTrue(torch.allclose(carry, torch.tensor(6.0)))
        self.assertTrue(torch.allclose(ys, torch.tensor([0.0, 2.0, 6.0, 12.0])))


if __name__ == "__main__":
    unittest.main()
