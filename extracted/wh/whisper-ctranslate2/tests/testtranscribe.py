import unittest
from types import SimpleNamespace

from whisper_ctranslate2.transcribe import Transcribe


class TestTranscribe(unittest.TestCase):
    def test_explicit_zero_vad_parameters_are_preserved(self):
        options = SimpleNamespace(
            vad_threshold=0.0,
            vad_min_speech_duration_ms=0,
            vad_max_speech_duration_s=None,
            vad_min_silence_duration_ms=0,
        )
        transcribe = Transcribe.__new__(Transcribe)
        self.assertEqual(
            transcribe._get_vad_parameters_dictionary(options),
            {
                "threshold": 0.0,
                "min_speech_duration_ms": 0,
                "min_silence_duration_ms": 0,
            },
        )
