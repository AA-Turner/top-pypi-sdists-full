import unittest

import kernelguard


LAST_CALL_REPLAY_KERNEL = """
_last_inputs = None
_last_versions = None
_last_output = None


def custom_kernel(data):
    global _last_inputs, _last_versions, _last_output
    cur_inputs = (data.data_ptr(),)
    cur_versions = (data._version,)
    if _last_inputs == cur_inputs and _last_versions == cur_versions:
        return _last_output
    out = data.clone()
    _last_inputs = cur_inputs
    _last_versions = cur_versions
    _last_output = out
    return out
"""


POINTER_SIGNATURE_REPLAY_KERNEL = """
_last_key = None
_last_output = None


def custom_kernel(q, kvb):
    global _last_key, _last_output
    key = (q.data_ptr(), kvb.data_ptr())
    if _last_key == key:
        return _last_output
    out = q + kvb
    _last_key = key
    _last_output = out
    return out
"""


WORKSPACE_HELPER_KERNEL = """
_WORKSPACE = {}


def _workspace_for(shape):
    buf = _WORKSPACE.get(shape)
    if buf is not None:
        return buf
    buf = [0] * shape[0]
    _WORKSPACE[shape] = buf
    return buf


def custom_kernel(data):
    _workspace_for((128,))
    return data
"""


SPLIT_CODEC_EXEC_KERNEL = """
import codecs


def custom_kernel(payload):
    decoded = codecs.decode(payload, "rot_13")
    exec(decoded)
"""


UNSYNC_MULTISTREAM_KERNEL = """
import torch

s0 = torch.cuda.Stream()
s1 = torch.cuda.Stream()
s2 = torch.cuda.Stream()
s3 = torch.cuda.Stream()


def custom_kernel(data):
    with torch.cuda.stream(s0):
        pass
    with torch.cuda.stream(s1):
        pass
    with torch.cuda.stream(s2):
        pass
    with torch.cuda.stream(s3):
        pass
    return data
"""


class ReplayRegressionTests(unittest.TestCase):
    def analyze(self, code: str) -> dict:
        return kernelguard.analyze_code(code, compute_structural_hash=False)

    def test_last_call_replay_is_filterable(self) -> None:
        result = self.analyze(LAST_CALL_REPLAY_KERNEL)
        patterns = {pattern["pattern"] for pattern in result["matched_patterns"]}

        self.assertIn("LAST_CALL_REPLAY", patterns)
        self.assertEqual(result["classification"], "hacked")
        self.assertTrue(result["should_filter"])

    def test_pointer_signature_replay_is_filterable(self) -> None:
        result = self.analyze(POINTER_SIGNATURE_REPLAY_KERNEL)
        patterns = {pattern["pattern"] for pattern in result["matched_patterns"]}

        self.assertIn("LAST_CALL_REPLAY", patterns)
        self.assertEqual(result["classification"], "hacked")
        self.assertTrue(result["should_filter"])

    def test_workspace_helper_stays_non_filtering(self) -> None:
        result = self.analyze(WORKSPACE_HELPER_KERNEL)
        patterns = {pattern["pattern"] for pattern in result["matched_patterns"]}

        self.assertNotIn("LAST_CALL_REPLAY", patterns)
        self.assertEqual(result["classification"], "valid")
        self.assertFalse(result["should_filter"])

    def test_extract_nvidia_archive_scores_from_current_run_layout(self) -> None:
        runs = [
            {"mode": "test", "score": None},
            {"mode": "benchmark", "score": 1.0e-9},
            {"mode": "benchmark", "score": 2.0e-9},
        ]

        scores = kernelguard._extract_nvidia_archive_scores(runs)

        self.assertEqual(scores, [1.0e-9, 2.0e-9])

    def test_score_anomaly_filters_current_archive_run_layout(self) -> None:
        runs = [
            {"mode": "test", "score": None},
            {"mode": "benchmark", "score": 1.0e-9},
        ]
        metadata = {"scores": kernelguard._extract_nvidia_archive_scores(runs)}

        result = kernelguard.analyze_code(
            "def custom_kernel(data):\n    return data\n",
            metadata,
            compute_structural_hash=False,
        )
        patterns = {pattern["pattern"] for pattern in result["matched_patterns"]}

        self.assertIn("SCORE_IMPOSSIBLE", patterns)
        self.assertEqual(result["classification"], "hacked")
        self.assertTrue(result["should_filter"])

    def test_codecs_decode_scope_counts_as_obfuscation(self) -> None:
        result = self.analyze(SPLIT_CODEC_EXEC_KERNEL)
        patterns = {pattern["pattern"] for pattern in result["matched_patterns"]}

        self.assertIn("OBFUSCATED_EXEC", patterns)
        self.assertEqual(result["classification"], "hacked")
        self.assertTrue(result["should_filter"])

    def test_strict_profile_only_promotes_timing_review_families(self) -> None:
        previous = kernelguard.ACTIVE_RUNTIME_CONFIG
        try:
            kernelguard.configure_runtime(profile="strict")

            multistream_result = self.analyze(UNSYNC_MULTISTREAM_KERNEL)
            workspace_result = self.analyze(WORKSPACE_HELPER_KERNEL)
        finally:
            kernelguard.apply_runtime_config(previous)

        multistream_patterns = {pattern["pattern"] for pattern in multistream_result["matched_patterns"]}
        workspace_patterns = {pattern["pattern"] for pattern in workspace_result["matched_patterns"]}

        self.assertIn("UNSYNC_MULTISTREAM", multistream_patterns)
        self.assertEqual(multistream_result["classification"], "suspicious")
        self.assertFalse(multistream_result["should_filter"])

        self.assertNotIn("UNSYNC_MULTISTREAM", workspace_patterns)
        self.assertEqual(workspace_result["classification"], "valid")
        self.assertFalse(workspace_result["should_filter"])


if __name__ == "__main__":
    unittest.main()
