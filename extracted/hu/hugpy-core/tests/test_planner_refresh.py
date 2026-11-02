"""Regression: unchanged capacity must not freeze Wrapper live verdicts."""
import unittest
from unittest.mock import patch

from hugpy_core.brain import planner


class PlannerRefreshTests(unittest.TestCase):
    def test_unchanged_inputs_expire_and_concurrent_refresh_is_coalesced(self):
        with patch.dict(planner._last_hash, {'ae-dev': 'same'}, clear=True), \
             patch.dict(planner._last_refresh, {'ae-dev': 100}, clear=True), \
             patch.dict(planner._next_allowed, {}, clear=True), \
             patch.object(planner, '_running', set()), \
             patch.object(planner, '_timer_pending', set()):
            self.assertEqual(planner._plan_gate('ae-dev', 'same', False, 159), 'skip')
            self.assertEqual(planner._plan_gate('ae-dev', 'same', False, 160), 'run')
            self.assertEqual(planner._plan_gate('ae-dev', 'same', False, 230), 'skip')

    def test_available_memory_change_reaches_refresh_gate(self):
        worker = {'id': 'ae-dev', 'free_ram': 100, 'swap_free': 20,
                  'gpus': [{'index': 0, 'memory_total': 24, 'memory_free': 22}]}
        with patch.object(planner, '_plan_gate', return_value='skip') as gate:
            planner.maybe_refresh(worker)
            first = gate.call_args.args[1]
            planner.maybe_refresh({**worker, 'free_ram': 80})
            self.assertNotEqual(first, gate.call_args.args[1])
            planner.maybe_refresh({**worker, 'gpus': [
                {'index': 0, 'memory_total': 24, 'memory_free': 12}]})
            self.assertNotEqual(first, gate.call_args.args[1])


if __name__ == '__main__':
    unittest.main()
