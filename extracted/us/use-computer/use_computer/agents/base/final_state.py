"""Final-state metrics and accessibility snapshots."""

from __future__ import annotations

import io
import json
import os
from typing import Any

import httpx
from PIL import Image

from use_computer.core.sandbox import AsyncSandbox


class FinalStateMixin:
    async def _save_final_ax_tree(self: Any, sandbox: AsyncSandbox) -> None:
        """Snapshot the sandbox's AX tree to <agent>/final_ax_tree.json."""
        try:
            tree = await sandbox.display.get_windows()
            (self.logs_dir / "final_ax_tree.json").write_text(json.dumps(tree, indent=2))
        except Exception as e:  # noqa: BLE001
            self.logger.warning(f"Failed to capture final AX tree: {e}")

    async def _log_final_state_metrics(self: Any, sandbox: AsyncSandbox) -> None:
        """Compute screenshot and a11y metrics against expected_final.json."""
        if self.task_dir is None:
            return
        expected_path = self.task_dir / "expected_final.json"
        if not expected_path.exists():
            return
        try:
            expected = json.loads(expected_path.read_text())
        except Exception as e:
            self.logger.warning(f"expected_final.json parse failed: {e}")
            return

        metrics: dict[str, Any] = {}

        try:
            actual_bytes = await sandbox.screenshot.take_full_screen()
            ss_path = self.logs_dir / "final_screenshot.png"
            ss_path.write_bytes(actual_bytes)
            ref_filename = expected.get("screenshot_filename")
            ref_task_id = expected.get("task_id")
            if ref_filename and ref_task_id:
                ref_bytes = await self._fetch_reference_screenshot(ref_task_id, ref_filename)
                if ref_bytes:
                    sim = _screenshot_similarity(actual_bytes, ref_bytes)
                    metrics["screenshot_similarity"] = sim
                    self.logger.info(f"final-state metrics: screenshot_similarity={sim:.3f}")
        except Exception as e:
            self.logger.warning(f"screenshot similarity failed: {e}")

        try:
            ref_a11y = expected.get("a11y_after")
            if ref_a11y is not None:
                actual_a11y = await sandbox.display.get_windows()
                matched, total = _a11y_match(actual_a11y, ref_a11y)
                metrics["a11y_match"] = f"{matched}/{total}"
                metrics["a11y_match_ratio"] = (matched / total) if total else 0.0
                self.logger.info(f"final-state metrics: a11y_match={matched}/{total}")
        except Exception as e:
            self.logger.warning(f"a11y match failed: {e}")

        if metrics:
            (self.logs_dir / "verifier-metrics.json").write_text(json.dumps(metrics, indent=2))

    async def _fetch_reference_screenshot(self: Any, task_id: str, filename: str) -> bytes | None:
        """Fetch a gateway reference screenshot; returns None on failure."""
        gateway = os.environ.get("USE_COMPUTER_BASE_URL") or os.environ.get("GATEWAY_URL", "")
        api_key = os.environ.get("USE_COMPUTER_API_KEY", "")
        if not gateway:
            return None
        url = f"{gateway.rstrip('/')}/admin/tasks/{task_id}/images/{filename}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, headers={"Authorization": f"Bearer {api_key}"})
                if resp.status_code != 200:
                    self.logger.warning(f"reference screenshot fetch {resp.status_code}: {url}")
                    return None
                return resp.content
        except Exception as e:
            self.logger.warning(f"reference screenshot fetch failed: {e}")
            return None


def _screenshot_similarity(a: bytes, b: bytes) -> float:
    """Pixel-wise similarity in [0,1]."""
    try:
        ia = Image.open(io.BytesIO(a)).convert("RGB")
        ib = Image.open(io.BytesIO(b)).convert("RGB")
    except Exception:
        return 0.0
    if ib.size != ia.size:
        ib = ib.resize(ia.size)
    ba = ia.tobytes()
    bb = ib.tobytes()
    if not ba:
        return 0.0
    diff_sum = sum(abs(x - y) for x, y in zip(ba, bb, strict=False))
    max_diff = len(ba) * 255
    return 1.0 - (diff_sum / max_diff if max_diff else 0.0)


def _a11y_match(actual: Any, expected: Any) -> tuple[int, int]:
    """Count expected accessibility node signatures that appear in actual."""
    actual_sigs = _collect_a11y_signatures(actual)
    expected_sigs = _collect_a11y_signatures(expected)
    if not expected_sigs:
        return (0, 0)
    matched = sum(1 for sig in expected_sigs if sig in actual_sigs)
    return (matched, len(expected_sigs))


def _collect_a11y_signatures(node: Any, out: set | None = None) -> set:
    if out is None:
        out = set()
    if isinstance(node, dict):
        role = node.get("role") or node.get("AXRole") or node.get("type") or ""
        ident = (
            node.get("AXLabel")
            or node.get("AXTitle")
            or node.get("AXValue")
            or node.get("label")
            or node.get("name")
            or node.get("title")
            or node.get("text")
            or ""
        )
        if role or ident:
            out.add((str(role)[:40], str(ident)[:80]))
        for v in node.values():
            _collect_a11y_signatures(v, out)
    elif isinstance(node, list):
        for v in node:
            _collect_a11y_signatures(v, out)
    return out
