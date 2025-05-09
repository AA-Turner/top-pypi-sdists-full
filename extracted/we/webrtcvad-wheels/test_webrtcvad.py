from contextlib import contextmanager
import os
import platform
import wave

import psutil
import unittest

import webrtcvad


class WebRtcVadTests(unittest.TestCase):
    @staticmethod
    def _load_wave(file_name):
        fp = wave.open(file_name, 'rb')
        try:
            assert fp.getnchannels() == 1, (
                '{0}: sound format is incorrect! Sound must be mono.'.format(
                    file_name))
            assert fp.getsampwidth() == 2, (
                '{0}: sound format is incorrect! '
                'Sample width of sound must be 2 bytes.').format(file_name)
            assert fp.getframerate() in (8000, 16000, 32000), (
                '{0}: sound format is incorrect! '
                'Sampling frequency must be 8000 Hz, 16000 Hz or 32000 Hz.')
            sampling_frequency = fp.getframerate()
            sound_data = fp.readframes(fp.getnframes())
        finally:
            fp.close()
            del fp
        return sound_data, sampling_frequency

    def test_constructor(self):
        vad = webrtcvad.Vad()

    def test_set_mode(self):
        vad = webrtcvad.Vad()
        vad.set_mode(0)
        vad.set_mode(1)
        vad.set_mode(2)
        vad.set_mode(3)
        self.assertRaises(
            ValueError,
            vad.set_mode, 4)

    def test_valid_rate_and_frame_length(self):
        self.assertTrue(webrtcvad.valid_rate_and_frame_length(8000, 160))
        self.assertTrue(webrtcvad.valid_rate_and_frame_length(16000, 160))
        self.assertFalse(webrtcvad.valid_rate_and_frame_length(32000, 160))
        self.assertRaises(
            (ValueError, OverflowError),
            webrtcvad.valid_rate_and_frame_length, 2 ** 35, 10)

    def test_process_zeroes(self):
        frame_len = 160
        self.assertTrue(
            webrtcvad.valid_rate_and_frame_length(8000, frame_len))
        sample = b'\x00' * frame_len * 2
        vad = webrtcvad.Vad()
        self.assertFalse(vad.is_speech(sample, 16000))

    def test_process_file(self):
        file_name = os.path.join(os.path.dirname(__file__), 'test-audio.raw')
        with open(file_name, 'rb') as f:
            data = f.read()
        frame_ms = 30
        n = int(8000 * 2 * 30 / 1000.0)
        frame_len = int(n / 2)
        self.assertTrue(
            webrtcvad.valid_rate_and_frame_length(8000, frame_len))
        chunks = list(data[pos:pos + n] for pos in range(0, len(data), n))
        if len(chunks[-1]) != n:
            chunks = chunks[:-1]
        expecteds = [
            '011110111111111111111111111100',
            '011110111111111111111111111100',
            '000000111111111111111111110000',
            '000000111111111111111100000000'
        ]
        for mode in (0, 1, 2, 3):
            vad = webrtcvad.Vad(mode)
            result = ''
            for chunk in chunks:
                voiced = vad.is_speech(chunk, 8000)
                result += '1' if voiced else '0'
            self.assertEqual(expecteds[mode], result)

    @contextmanager
    def _profile_memory(self, threshold_ratio):
        process = psutil.Process()
        start_memory = process.memory_info().rss
        yield
        end_memory = process.memory_info().rss
        self.assertLessEqual(
            end_memory - start_memory,
            start_memory * threshold_ratio)

    @unittest.skipIf(platform.python_implementation() == 'PyPy', "fails on pypy, possibly due to inaccuracy in memory tracking")
    def test_leak_linear_usage(self):
        file_name = os.path.join(os.path.dirname(__file__), 'leak-test.wav')
        sound, fs = self._load_wave(file_name)
        frame_ms = 0.010
        frame_len = int(round(fs * frame_ms))
        n = int(len(sound) / (2 * frame_len))
        nrepeats = 1000
        vad = webrtcvad.Vad(3)
        with self._profile_memory(0.2):
            for _ in range(nrepeats):
                find_voice = False
                for frame_ind in range(n):
                    slice_start = (frame_ind * 2 * frame_len)
                    slice_end = ((frame_ind + 1) * 2 * frame_len)
                    if vad.is_speech(sound[slice_start:slice_end], fs):
                        find_voice = True
                self.assertTrue(find_voice)

    @unittest.skipIf(platform.python_implementation() == 'PyPy', "fails on pypy, possibly due to inaccuracy in memory tracking")
    def test_leak_constructor(self):
        nrepeats = 100000
        with self._profile_memory(0.1):
            for _ in range(nrepeats):
                vad = webrtcvad.Vad(3)
                del vad


if __name__ == '__main__':
    unittest.main(verbosity=2)
