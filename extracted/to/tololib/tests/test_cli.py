from argparse import ArgumentParser, Namespace
from unittest import TestCase, mock

from tests import TEST_PORT
from tests.templates import ServerCommunicationTestCase
from tololib.cli.common import Command
from tololib.cli.main import main


class CliDataStructureTest(TestCase):
    def test_command(self) -> None:
        command = Command(ArgumentParser())
        self.assertRaises(NotImplementedError, command, Namespace())


class CliInteractionTest(ServerCommunicationTestCase):
    def test_discover(self) -> None:
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=Namespace(
                log_level="INFO",
                command="discover",
                broadcast_address="127.0.0.1",
                port=TEST_PORT,
                retry_count=1,
                retry_timeout=1,
            ),
        ):
            result = main()
            self.assertEqual(0, result)

        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=Namespace(
                log_level="INFO",
                command="discover",
                broadcast_address="127.0.0.1",
                port=TEST_PORT + 1,
                retry_count=1,
                retry_timeout=1,
            ),
        ):
            result = main()
            self.assertEqual(1, result)

    def test_get_status(self) -> None:
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=Namespace(
                log_level="INFO",
                command="get-status",
                address="127.0.0.1",
                port=TEST_PORT,
                retry_count=1,
                retry_timeout=1,
            ),
        ):
            result = main()
            self.assertEqual(0, result)

        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=Namespace(
                log_level="INFO",
                command="get-status",
                address="127.0.0.1",
                port=TEST_PORT + 1,
                retry_count=1,
                retry_timeout=1,
            ),
        ):
            result = main()
            self.assertEqual(1, result)

    def test_get_settings(self) -> None:
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=Namespace(
                log_level="INFO",
                command="get-settings",
                address="127.0.0.1",
                port=TEST_PORT,
                retry_count=1,
                retry_timeout=1,
            ),
        ):
            result = main()
            self.assertEqual(0, result)

        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=Namespace(
                log_level="INFO",
                command="get-settings",
                address="127.0.0.1",
                port=TEST_PORT + 1,
                retry_count=1,
                retry_timeout=1,
            ),
        ):
            result = main()
            self.assertEqual(1, result)


class DeviceSimulatorTest(TestCase):
    @mock.patch("tololib.device_simulator.ToloDeviceSimulator.start", lambda x: None)
    @mock.patch("tololib.device_simulator.ToloDeviceSimulator.join", lambda x: None)
    def test_device_simulator(self) -> None:
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=Namespace(log_level="INFO", command="device-simulator", address="127.0.0.1", port=TEST_PORT),
        ):
            result = main()
            self.assertEqual(0, result)
