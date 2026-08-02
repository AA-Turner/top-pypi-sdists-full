from __future__ import annotations

import importlib
import types
import unittest


try:
    import torch
except Exception:  # pragma: no cover - exercised only when torch is absent.
    torch = None


scan_module = importlib.import_module("hoptorch.scan")


def _torch_version_tuple() -> tuple[int, int]:
    if torch is None:
        return (0, 0)
    base = torch.__version__.split("+", 1)[0]
    parts = base.split(".")[:2]
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


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


class ScanBackwardStateTests(PatchMixin, unittest.TestCase):
    def test_health_probe_skips_patch_when_healthy(self):
        if torch is None:
            self.skipTest("torch is not installed")
        calls = []
        self.patch_attr("has_scan", lambda: True)
        self.patch_attr("_run_scan_backward_probe", lambda device: True)
        self.patch_attr("_install_scan_backward_patch", lambda scan_module_arg: calls.append("patch") or False)

        self.assertTrue(scan_module.ensure_scan_backward("cpu"))
        self.assertEqual(calls, [])

    def test_failed_patch_returns_unavailable(self):
        if torch is None:
            self.skipTest("torch is not installed")
        self.patch_attr("has_scan", lambda: True)
        self.patch_attr("_get_torch_scan", lambda: (lambda *args, **kwargs: None, None))
        self.patch_attr("_get_torch_scan_module", lambda: (object(), None))
        self.patch_attr("_run_scan_backward_probe", lambda device: False)
        self.patch_attr("_install_scan_backward_patch", lambda scan_module_arg: False)

        self.assertFalse(scan_module.ensure_scan_backward("cpu"))
        reason = scan_module.scan_unavailable_reason("cpu")
        self.assertIsInstance(reason, str)
        self.assertIn("health check", reason)

    def test_patch_only_claims_success_after_reprobe(self):
        if torch is None:
            self.skipTest("torch is not installed")
        probe_results = iter([False, True])
        self.patch_attr("has_scan", lambda: True)
        self.patch_attr("_get_torch_scan", lambda: (lambda *args, **kwargs: None, None))
        self.patch_attr("_get_torch_scan_module", lambda: (object(), None))
        self.patch_attr("_run_scan_backward_probe", lambda device: next(probe_results))
        self.patch_attr("_install_scan_backward_patch", lambda scan_module_arg: True)

        self.assertTrue(scan_module.ensure_scan_backward("cpu"))
        self.assertIs(scan_module._SCAN_BACKWARD_HEALTH.get("cpu"), True)

    def test_compile_context_does_not_probe_without_cache(self):
        if torch is None:
            self.skipTest("torch is not installed")
        self.patch_attr("has_scan", lambda: True)
        self.patch_attr("_get_torch_scan", lambda: (lambda *args, **kwargs: None, None))
        self.patch_attr("_is_compiling", lambda: True)
        self.patch_attr("_run_scan_backward_probe", lambda device: self.fail("probe should not run during compile"))

        self.assertFalse(scan_module.ensure_scan_backward("cpu"))
        self.assertIn("torch.compile", scan_module.scan_unavailable_reason("cpu"))

    def test_compile_context_uses_warmed_cache(self):
        if torch is None:
            self.skipTest("torch is not installed")
        self.patch_attr("has_scan", lambda: True)
        self.patch_attr("_get_torch_scan", lambda: (lambda *args, **kwargs: None, None))
        scan_module._SCAN_BACKWARD_HEALTH["cpu"] = True
        self.patch_attr("_is_compiling", lambda: True)

        self.assertTrue(scan_module.ensure_scan_backward("cpu"))
        self.assertIsNone(scan_module.scan_unavailable_reason("cpu"))


class ScanPatchImplementationTests(unittest.TestCase):
    def setUp(self) -> None:
        if torch is None:
            self.skipTest("torch is not installed")

    def _fake_scan_module(self):
        import enum
        import torch.utils._pytree as pytree

        class Policy(enum.Enum):
            CLONE = enum.auto()
            REMOVE_XS = enum.auto()
            REMOVE_ADDITIONAL_INPUTS = enum.auto()
            KEEP = enum.auto()

        class ScanAutogradImpl:
            def __init__(self, *args, **kwargs):
                self._optimize_forward_intermediates()

            def _insert_clone(self, need_copy_node, output_node):
                graph = output_node.graph
                with graph.inserting_before(output_node):
                    clone_node = graph.call_function(
                        torch.ops.aten.clone.default,
                        args=(need_copy_node,),
                    )
                    clone_node.meta = need_copy_node.meta.copy()
                return clone_node

            def _optimize_forward_intermediates(self):
                raise AssertionError("patched implementation should replace this")

        def find_outputs(graph_module):
            output_node = next(iter(graph_module.graph.find_nodes(op="output")))
            return output_node.args[0]

        return types.SimpleNamespace(
            ScanAutogradImpl=ScanAutogradImpl,
            ScanForwardIntermediatesHandlingPolicy=Policy,
            _find_hop_subgraph_outputs=find_outputs,
            pytree=pytree,
        )

    def test_patch_clones_backward_outputs_that_alias_placeholders(self):
        from hoptorch._scan_patch import _patch_scan_autograd_aliasing

        fake_scan_module = self._fake_scan_module()
        self.assertTrue(_patch_scan_autograd_aliasing(fake_scan_module))

        graph = torch.fx.Graph()
        ph_tangent = graph.placeholder("tangent")
        ph_tangent.meta["val"] = torch.empty(2, 3)
        ph_zeros = graph.placeholder("zeros_like")
        ph_zeros.meta["val"] = torch.empty(6)
        computed = graph.call_function(torch.ops.aten.mul.Tensor, args=(ph_tangent, 2.0))
        computed.meta["val"] = ph_tangent.meta["val"] * 2.0
        view = graph.call_function(torch.ops.aten.view.default, args=(ph_zeros, [2, 3]))
        view.meta["val"] = ph_zeros.meta["val"].view(2, 3)
        graph.output((computed, ph_zeros, view))
        bw_gm = torch.fx.GraphModule(torch.nn.Module(), graph)

        impl = fake_scan_module.ScanAutogradImpl.__new__(
            fake_scan_module.ScanAutogradImpl
        )
        impl.hop_partitioned_graph = types.SimpleNamespace(bw_gm=bw_gm)
        impl._break_bw_input_output_aliasing()

        outputs = next(iter(bw_gm.graph.find_nodes(op="output"))).args[0]
        self.assertIs(outputs[0], computed)
        self.assertEqual(outputs[1].target, torch.ops.aten.clone.default)
        self.assertEqual(outputs[1].args, (ph_zeros,))
        self.assertEqual(outputs[2].target, torch.ops.aten.clone.default)
        self.assertEqual(outputs[2].args, (view,))

    def test_patch_clones_forward_intermediates_that_alias_placeholders(self):
        from hoptorch._scan_patch import _patch_scan_autograd_aliasing

        fake_scan_module = self._fake_scan_module()
        self.assertTrue(_patch_scan_autograd_aliasing(fake_scan_module))

        graph = torch.fx.Graph()
        ph_init = graph.placeholder("init")
        ph_init.meta["val"] = torch.empty(2, 3)
        ph_xs = graph.placeholder("xs")
        ph_xs.meta["val"] = torch.empty(6)
        ph_additional = graph.placeholder("additional")
        ph_additional.meta["val"] = torch.empty(4)

        fw_out = graph.call_function(torch.ops.aten.mul.Tensor, args=(ph_init, 2.0))
        fw_out.meta["val"] = ph_init.meta["val"] * 2.0
        computed = graph.call_function(torch.ops.aten.add.Tensor, args=(ph_init, 1.0))
        computed.meta["val"] = ph_init.meta["val"] + 1.0
        view_of_xs = graph.call_function(
            torch.ops.aten.view.default, args=(ph_xs, [2, 3])
        )
        view_of_xs.meta["val"] = ph_xs.meta["val"].view(2, 3)
        view_of_init = graph.call_function(
            torch.ops.aten.view.default, args=(ph_init, [6])
        )
        view_of_init.meta["val"] = ph_init.meta["val"].view(6)
        graph.output((fw_out, computed, view_of_xs, view_of_init))
        fw_gm = torch.fx.GraphModule(torch.nn.Module(), graph)

        impl = fake_scan_module.ScanAutogradImpl.__new__(
            fake_scan_module.ScanAutogradImpl
        )
        impl.hop_partitioned_graph = types.SimpleNamespace(
            fw_gm=fw_gm,
            n_fw_outputs=1,
        )
        impl.init = (torch.empty(2, 3),)
        impl.xs = (torch.empty(6),)
        impl.additional_inputs = (torch.empty(4),)
        impl.forward_intermediates_handling_policies = []
        impl.saved_fw_xs = []
        impl.saved_fw_additional_inputs = []
        impl.fw_spec = fake_scan_module.pytree.tree_flatten(
            (impl.init, impl.xs, impl.additional_inputs)
        )[1]

        impl._optimize_forward_intermediates()

        outputs = next(iter(fw_gm.graph.find_nodes(op="output"))).args[0]
        self.assertEqual(len(outputs), 4)
        self.assertIs(outputs[0], fw_out)
        self.assertIs(outputs[1], computed)
        self.assertEqual(outputs[2].target, torch.ops.aten.clone.default)
        self.assertEqual(outputs[2].args, (view_of_xs,))
        self.assertEqual(outputs[3].target, torch.ops.aten.clone.default)
        self.assertEqual(outputs[3].args, (view_of_init,))
        self.assertEqual(
            impl.forward_intermediates_handling_policies,
            [fake_scan_module.ScanForwardIntermediatesHandlingPolicy.KEEP] * 3,
        )
        self.assertEqual(impl.saved_fw_xs, [])
        self.assertEqual(impl.saved_fw_additional_inputs, [])


class ScanBackwardIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        scan_module._reset_scan_backward_state_for_tests()

    def tearDown(self) -> None:
        scan_module._reset_scan_backward_state_for_tests()

    def _require_scan_backward(self):
        if torch is None:
            self.skipTest("torch is not installed")
        if not scan_module.has_scan():
            self.skipTest("torch scan is not available")
        if not scan_module.ensure_scan_backward("cpu"):
            reason = scan_module.scan_unavailable_reason("cpu") or "scan backward unavailable"
            if _torch_version_tuple() < (2, 8):
                self.skipTest(reason)
            self.fail(reason)

    def test_non_grad_init_closed_over_param_grad_matches_loop(self):
        self._require_scan_backward()

        xs = torch.linspace(0.2, 0.8, 4)
        carry0 = torch.zeros(())
        weight = torch.tensor(0.7, requires_grad=True)

        def step(carry, x):
            next_carry = carry * weight + x
            return next_carry, next_carry * weight

        carry, ys = scan_module.scan(step, carry0, xs, dim=0)
        (grad,) = torch.autograd.grad(carry + ys.sum(), weight)

        ref_weight = weight.detach().clone().requires_grad_(True)
        ref_carry = carry0.detach().clone()
        ref_ys = []
        for x in xs.detach().unbind(0):
            ref_carry = ref_carry * ref_weight + x
            ref_ys.append(ref_carry * ref_weight)
        ref_loss = ref_carry + torch.stack(ref_ys).sum()
        (ref_grad,) = torch.autograd.grad(ref_loss, ref_weight)

        self.assertTrue(torch.allclose(grad, ref_grad, atol=1e-5, rtol=1e-5))

    def test_optional_compile_smoke(self):
        self._require_scan_backward()
        if not hasattr(torch, "compile"):
            self.skipTest("torch.compile is not available")

        def fn(xs):
            def step(carry, x):
                next_carry = carry + x
                return next_carry, next_carry.clone()

            _, ys = scan_module.scan(step, torch.zeros(()), xs, dim=0)
            return ys.sum()

        xs = torch.arange(4.0)
        try:
            compiled = torch.compile(fn, backend="eager")
            got = compiled(xs)
        except Exception as exc:
            self.skipTest(f"torch.compile scan smoke is not stable on this build: {exc}")
        self.assertTrue(torch.allclose(got, fn(xs)))

    def test_compile_inductor_lowers_scan_without_scalar_capture(self):
        # Regression test for the ``torch.compile`` + Inductor path. Inductor
        # lowers scan to a while_loop whose body computes ``loop_idx.item()``
        # (torch/_inductor/fx_passes/post_grad.py, decompose_scan_to_while_loop).
        # Under the default ``capture_scalar_outputs=False`` that data-dependent
        # ``.item()`` makes Inductor raise ``DataDependentOutputException`` on
        # ``aten._local_scalar_dense`` (a hard crash on torch>=2.11, a silent
        # eager-fallback graph break on some earlier builds). Verifying scan
        # backward (which TorchRL/users do in eager before compiling) enables
        # the flag so this compiles cleanly. The ``backend="eager"`` smoke test
        # above does NOT exercise this: it skips Inductor lowering entirely,
        # which is exactly why this regression shipped unnoticed.
        self._require_scan_backward()
        if not hasattr(torch, "compile"):
            self.skipTest("torch.compile is not available")

        def fn(xs):
            def step(carry, x):
                next_carry = carry + x
                return next_carry, next_carry.clone()

            _, ys = scan_module.scan(step, torch.zeros(()), xs, dim=0)
            return ys.sum()

        xs = torch.arange(4.0)
        try:
            compiled = torch.compile(fn)
            got = compiled(xs)
        except Exception as exc:
            if _torch_version_tuple() < (2, 8):
                self.skipTest(f"scan Inductor lowering unstable on this build: {exc}")
            raise
        self.assertTrue(torch.allclose(got, fn(xs)))

    def test_ensure_scan_backward_enables_scalar_capture(self):
        # The enable must happen in eager (where it persists into the later
        # compilation), not via a context manager inside the traced scan call:
        # the latter graph-breaks, which is illegal under ``fullgraph=True``.
        self._require_scan_backward()
        with torch._dynamo.config.patch(capture_scalar_outputs=False):
            self.assertFalse(torch._dynamo.config.capture_scalar_outputs)
            scan_module.ensure_scan_backward("cpu")
            self.assertTrue(torch._dynamo.config.capture_scalar_outputs)

    def test_compile_scan_fullgraph(self):
        # Guards against re-introducing an in-trace ``config.patch`` (or any
        # other graph break) inside ``scan``: such a break makes
        # ``fullgraph=True`` compilation of scan raise
        # "Attempted to call function marked as skipped", regressing code that
        # already compiled cleanly.
        self._require_scan_backward()
        if not hasattr(torch, "compile"):
            self.skipTest("torch.compile is not available")

        def fn(xs):
            def step(carry, x):
                next_carry = carry + x
                return next_carry, next_carry.clone()

            _, ys = scan_module.scan(step, torch.zeros(()), xs, dim=0)
            return ys.sum()

        xs = torch.arange(4.0)
        try:
            compiled = torch.compile(fn, fullgraph=True)
            got = compiled(xs)
        except Exception as exc:
            if _torch_version_tuple() < (2, 8):
                self.skipTest(f"scan fullgraph compile unstable on this build: {exc}")
            raise
        self.assertTrue(torch.allclose(got, fn(xs)))


if __name__ == "__main__":
    unittest.main()
