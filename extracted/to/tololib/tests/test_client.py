from unittest.mock import MagicMock

from tests import TEST_PORT
from tests.templates import ServerCommunicationTestCase
from tololib import (
    TARGET_TEMPERATURE_MAX,
    TARGET_TEMPERATURE_MIN,
    AromaTherapySlot,
    LampMode,
    ToloClient,
)


class ClientOnlineTest(ServerCommunicationTestCase):
    def test_discover(self) -> None:
        result = list(ToloClient.discover(broadcast_address="127.0.0.1", port=TEST_PORT))
        self.assertEqual(len(result), 1)

    def test_address_and_port(self) -> None:
        self.assertEqual(self.client.address, "127.0.0.1")
        self.assertEqual(self.client.port, TEST_PORT)

    def test_get_status(self) -> None:
        self.client.get_status()

    def test_get_settings(self) -> None:
        self.client.get_settings()

    def test_set_power_on(self) -> None:
        self.assertTrue(self.client.set_power_on(True))
        status = self.client.get_status()
        self.assertTrue(status.power_on)

        self.assertTrue(self.client.set_power_on(False))
        status = self.client.get_status()
        self.assertFalse(status.power_on)

    def test_set_fan_on(self) -> None:
        self.assertTrue(self.client.set_fan_on(True))
        status = self.client.get_status()
        self.assertTrue(status.fan_on)

        self.assertTrue(self.client.set_fan_on(False))
        status = self.client.get_status()
        self.assertFalse(status.fan_on)

    def test_set_aroma_therapy_on(self) -> None:
        self.assertTrue(self.client.set_aroma_therapy_on(True))
        status = self.client.get_status()
        self.assertTrue(status.aroma_therapy_on)

        self.assertTrue(self.client.set_aroma_therapy_on(False))
        status = self.client.get_status()
        self.assertFalse(status.aroma_therapy_on)

    def test_set_lamp_on(self) -> None:
        self.assertTrue(self.client.set_lamp_on(True))
        status = self.client.get_status()
        self.assertTrue(status.lamp_on)

        self.assertTrue(self.client.set_lamp_on(False))
        status = self.client.get_status()
        self.assertFalse(status.lamp_on)

    def test_set_sweep_on(self) -> None:
        self.assertTrue(self.client.set_sweep_on(True))
        status = self.client.get_status()
        self.assertTrue(status.sweep_on)

        self.assertTrue(self.client.set_sweep_on(False))
        status = self.client.get_status()
        self.assertFalse(status.sweep_on)

    def test_set_salt_bath_on(self) -> None:
        self.assertTrue(self.client.set_salt_bath_on(True))
        status = self.client.get_status()
        self.assertTrue(status.salt_bath_on)

        self.assertTrue(self.client.set_salt_bath_on(False))
        status = self.client.get_status()
        self.assertFalse(status.salt_bath_on)

    def test_set_target_temperature(self) -> None:
        self.assertTrue(self.client.set_target_temperature(40))
        settings = self.client.get_settings()
        self.assertEqual(settings.target_temperature, 40)
        self.assertTrue(self.client.set_target_temperature(50))
        settings = self.client.get_settings()
        self.assertEqual(settings.target_temperature, 50)
        self.assertTrue(self.client.set_target_temperature(60))
        settings = self.client.get_settings()
        self.assertEqual(settings.target_temperature, 60)

        self.assertRaises(ValueError, self.client.set_target_temperature, TARGET_TEMPERATURE_MIN - 1)
        self.assertRaises(ValueError, self.client.set_target_temperature, TARGET_TEMPERATURE_MAX + 1)

    def test_set_target_humidity(self) -> None:
        self.assertTrue(self.client.set_target_humidity(70))
        settings = self.client.get_settings()
        self.assertEqual(settings.target_humidity, 70)

    def test_set_power_timer(self) -> None:
        self.assertTrue(self.client.set_power_timer(42))
        settings = self.client.get_settings()
        self.assertEqual(settings.power_timer, 42)

        self.assertTrue(self.client.set_power_timer(None))
        settings = self.client.get_settings()
        self.assertEqual(settings.power_timer, None)

    def test_set_salt_bath_timer(self) -> None:
        self.assertTrue(self.client.set_salt_bath_timer(42))
        settings = self.client.get_settings()
        self.assertEqual(settings.salt_bath_timer, 42)

        self.assertTrue(self.client.set_salt_bath_timer(None))
        settings = self.client.get_settings()
        self.assertEqual(settings.salt_bath_timer, None)

    def test_set_aroma_therapy(self) -> None:
        self.assertTrue(self.client.set_aroma_therapy_slot(AromaTherapySlot.B))
        settings = self.client.get_settings()
        self.assertEqual(settings.aroma_therapy_slot, AromaTherapySlot.B)
        self.assertEqual(self.client.get_aroma_therapy_slot(), AromaTherapySlot.B)

        self.assertTrue(self.client.set_aroma_therapy_slot(AromaTherapySlot.A))
        settings = self.client.get_settings()
        self.assertEqual(settings.aroma_therapy_slot, AromaTherapySlot.A)
        self.assertEqual(self.client.get_aroma_therapy_slot(), AromaTherapySlot.A)

        self.client._send_get_command = MagicMock(return_value="foobar")  # type: ignore[method-assign]
        self.assertRaises(ValueError, self.client.get_aroma_therapy_slot)

    def test_set_sweep_timer(self) -> None:
        self.assertTrue(self.client.set_sweep_timer(7))
        settings = self.client.get_settings()
        self.assertEqual(settings.sweep_timer, 7)

        self.assertTrue(self.client.set_sweep_timer(None))
        settings = self.client.get_settings()
        self.assertEqual(settings.sweep_timer, None)

    def test_set_lamp_mode(self) -> None:
        self.assertTrue(self.client.set_lamp_mode(LampMode.AUTOMATIC))
        settings = self.client.get_settings()
        self.assertEqual(settings.lamp_mode, LampMode.AUTOMATIC)
        self.assertEqual(self.client.get_lamp_mode(), LampMode.AUTOMATIC)

        self.assertTrue(self.client.set_lamp_mode(LampMode.MANUAL))
        settings = self.client.get_settings()
        self.assertEqual(settings.lamp_mode, LampMode.MANUAL)
        self.assertEqual(self.client.get_lamp_mode(), LampMode.MANUAL)

        self.client._send_get_command = MagicMock(return_value="foobar")  # type: ignore[method-assign]
        self.assertRaises(ValueError, self.client.get_lamp_mode)

    def test_set_fan_timer(self) -> None:
        self.assertTrue(self.client.set_fan_timer(30))
        settings = self.client.get_settings()
        self.assertEqual(settings.fan_timer, 30)

        self.assertTrue(self.client.set_fan_timer(None))
        settings = self.client.get_settings()
        self.assertEqual(settings.fan_timer, None)

    def test_lamp_change_color(self) -> None:
        self.assertTrue(self.client.lamp_change_color())

    def test_get_fan_timer(self) -> None:
        self.assertTrue(self.client.set_fan_timer(30))
        self.assertTrue(self.client.set_fan_on(True))
        self.assertEqual(self.client.get_fan_timer(), 30)
        self.assertTrue(self.client.set_fan_on(False))
        self.assertTrue(self.client.set_fan_timer(None))
        self.assertTrue(self.client.set_fan_on(True))
        self.assertEqual(self.client.get_fan_timer(), None)

        self.client._send_get_command = MagicMock(return_value="foobar")  # type: ignore[method-assign]
        self.assertRaises(ValueError, self.client.get_fan_timer)

    def test_salt_bath_timer(self) -> None:
        self.assertTrue(self.client.set_salt_bath_timer(30))
        self.assertTrue(self.client.set_salt_bath_on(True))
        self.assertEqual(self.client.get_salt_bath_timer(), 30)
        self.assertTrue(self.client.set_salt_bath_on(False))
        self.assertTrue(self.client.set_salt_bath_timer(None))
        self.assertTrue(self.client.set_salt_bath_on(True))
        self.assertEqual(self.client.get_salt_bath_timer(), None)

        self.client._send_get_command = MagicMock(return_value="foobar")  # type: ignore[method-assign]
        self.assertRaises(ValueError, self.client.get_salt_bath_timer)

    def test_sweep_timer(self) -> None:
        self.assertTrue(self.client.set_sweep_timer(7))
        self.assertTrue(self.client.set_sweep_on(True))
        self.assertEqual(self.client.get_sweep_timer(), 7)
        self.assertTrue(self.client.set_sweep_on(False))
        self.assertTrue(self.client.set_sweep_timer(None))
        self.assertTrue(self.client.set_sweep_on(True))
        self.assertEqual(self.client.get_sweep_timer(), None)

        self.client._send_get_command = MagicMock(return_value="foobar")  # type: ignore[method-assign]
        self.assertRaises(ValueError, self.client.get_sweep_timer)
