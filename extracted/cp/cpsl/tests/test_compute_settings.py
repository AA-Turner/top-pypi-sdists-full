import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl
from cpsl.utils import build_image_spec


class ComputeSettingsTests(unittest.TestCase):
    def test_functional_app_serializes_gpu_compute_setting(self):
        app = cpsl.App(
            name="gpu-functional-test",
            image=cpsl.Image(),
            cpu=2,
            memory=4096,
            gpu="T4",
        )

        cfg = app._serialize()

        self.assertEqual(cfg["cpu"], 2)
        self.assertEqual(cfg["memory"], 4096)
        self.assertEqual(cfg["gpu"], "T4")

    def test_class_app_serializes_gpu_compute_setting(self):
        app = cpsl.App(name="gpu-class-test")

        @app.cls(image=cpsl.Image(), cpu=4, memory=8192, gpu="A100:2")
        class Worker:
            pass

        cfg = app._serialize()

        self.assertEqual(cfg["cpu"], 4)
        self.assertEqual(cfg["memory"], 8192)
        self.assertEqual(cfg["gpu"], "A100:2")

    def test_build_image_spec_includes_gpu(self):
        spec = build_image_spec({}, cpu=1, memory=1024, gpu="L4")

        self.assertEqual(spec.cpu, 1)
        self.assertEqual(spec.memory_mib, 1024)
        self.assertEqual(spec.gpu, "L4")


if __name__ == "__main__":
    unittest.main()
