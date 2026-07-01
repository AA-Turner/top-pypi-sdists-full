import unittest

from koyeb.sandbox.utils import create_docker_source


class TestCreateDockerSource(unittest.TestCase):
    """Tests for create_docker_source entrypoint, command, and args support."""

    def test_default_no_entrypoint_no_command(self):
        ds = create_docker_source("myimage")
        self.assertIsNone(ds.command)
        self.assertIsNone(ds.args)
        self.assertIsNone(ds.entrypoint)

    def test_command_and_args(self):
        ds = create_docker_source("myimage", command="python", args=["-u", "app.py"])
        self.assertEqual(ds.command, "python")
        self.assertEqual(ds.args, ["-u", "app.py"])
        self.assertIsNone(ds.entrypoint)

    def test_command_only(self):
        ds = create_docker_source("myimage", command="python app.py")
        self.assertEqual(ds.command, "python app.py")
        self.assertIsNone(ds.args)
        self.assertIsNone(ds.entrypoint)

    def test_entrypoint_only(self):
        ds = create_docker_source("myimage", entrypoint=["/bin/sh", "-c"])
        self.assertIsNone(ds.command)
        self.assertIsNone(ds.args)
        self.assertEqual(ds.entrypoint, ["/bin/sh", "-c"])

    def test_entrypoint_and_command(self):
        ds = create_docker_source(
            "myimage", entrypoint=["/bin/sh", "-c"], command="python app.py"
        )
        self.assertEqual(ds.command, "python app.py")
        self.assertEqual(ds.entrypoint, ["/bin/sh", "-c"])
        self.assertIsNone(ds.args)

    def test_entrypoint_command_and_args(self):
        ds = create_docker_source(
            "myimage", entrypoint=["/bin/sh", "-c"], command="python", args=["app.py"]
        )
        self.assertEqual(ds.command, "python")
        self.assertEqual(ds.entrypoint, ["/bin/sh", "-c"])
        self.assertEqual(ds.args, ["app.py"])

    def test_privileged_and_registry_secret_still_work(self):
        ds = create_docker_source(
            "myimage",
            privileged=True,
            image_registry_secret="my-secret",
            entrypoint=["/entrypoint.sh"],
            command="serve",
        )
        self.assertTrue(ds.privileged)
        self.assertEqual(ds.image_registry_secret, "my-secret")
        self.assertEqual(ds.entrypoint, ["/entrypoint.sh"])
        self.assertEqual(ds.command, "serve")


if __name__ == "__main__":
    unittest.main()
