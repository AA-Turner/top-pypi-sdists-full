from unittest import TestCase

from tests import TEST_PORT
from tololib import AromaTherapySlot, LampMode, ToloClient, ToloDeviceSimulator


class DeviceSimulatorTest(TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._device_simulator: ToloDeviceSimulator | None = None
        self._client = ToloClient(address="127.0.0.1", port=TEST_PORT)

    def setUp(self) -> None:
        self._device_simulator = ToloDeviceSimulator(address="127.0.0.1", port=TEST_PORT)
        self._device_simulator.start()

    def tearDown(self) -> None:
        if self._device_simulator is None:
            raise RuntimeError("device simulator not initialized")

        self._device_simulator.stop()
        self._device_simulator.join()

    @property
    def device_simulator(self) -> ToloDeviceSimulator:
        if self._device_simulator is None:
            raise RuntimeError("device simulator not initialized")

        return self._device_simulator

    @property
    def client(self) -> ToloClient:
        return self._client

    def test_get_status(self) -> None:
        self.client.get_status()

    def test_get_settings(self) -> None:
        self.client.get_settings()

    def test_set_target_temperature(self) -> None:
        result = self.client.set_target_temperature(42)
        self.assertEqual(result, True)

        settings = self.client.get_settings()
        self.assertEqual(settings.target_temperature, 42)

    def test_set_power_timer(self) -> None:
        result = self.client.set_power_timer(5)
        self.assertEqual(result, True)

        settings = self.client.get_settings()
        self.assertEqual(settings.power_timer, 5)

    def test_set_power_on(self) -> None:
        result = self.client.set_power_on(True)
        self.assertEqual(result, True)

        status = self.client.get_status()
        self.assertEqual(status.power_on, True)

        result = self.client.set_power_on(False)
        self.assertEqual(result, True)

        status = self.client.get_status()
        self.assertEqual(status.power_on, False)

    def test_set_aroma_therapy_on(self) -> None:
        result = self.client.set_aroma_therapy_on(True)
        self.assertEqual(result, True)

        status = self.client.get_status()
        self.assertEqual(status.aroma_therapy_on, True)

        result = self.client.set_aroma_therapy_on(False)
        self.assertEqual(result, True)

        status = self.client.get_status()
        self.assertEqual(status.aroma_therapy_on, False)

    def test_set_aroma_therapy_slot(self) -> None:
        result = self.client.set_aroma_therapy_slot(AromaTherapySlot.B)
        self.assertEqual(result, True)

        settings = self.client.get_settings()
        self.assertEqual(settings.aroma_therapy_slot, AromaTherapySlot.B)
        self.assertEqual(self.client.get_aroma_therapy_slot(), AromaTherapySlot.B)

        result = self.client.set_aroma_therapy_slot(AromaTherapySlot.A)
        self.assertEqual(result, True)

        settings = self.client.get_settings()
        self.assertEqual(settings.aroma_therapy_slot, AromaTherapySlot.A)
        self.assertEqual(self.client.get_aroma_therapy_slot(), AromaTherapySlot.A)

    def test_set_sweep_timer(self) -> None:
        result = self.client.set_sweep_timer(3)
        self.assertEqual(result, True)

        settings = self.client.get_settings()
        self.assertEqual(settings.sweep_timer, 3)
        self.assertEqual(self.client.get_sweep_timer(), 3)

    def test_set_lamp_on(self) -> None:
        result = self.client.set_lamp_on(True)
        self.assertEqual(result, True)

        status = self.client.get_status()
        self.assertEqual(status.lamp_on, True)

        result = self.client.set_lamp_on(False)
        self.assertEqual(result, True)

        status = self.client.get_status()
        self.assertEqual(status.lamp_on, False)

    def test_set_fan_on(self) -> None:
        result = self.client.set_fan_on(True)
        self.assertEqual(result, True)

        status = self.client.get_status()
        self.assertEqual(status.fan_on, True)

        result = self.client.set_fan_on(False)
        self.assertEqual(result, True)

        status = self.client.get_status()
        self.assertEqual(status.fan_on, False)

    def test_set_fan_timer(self) -> None:
        result = self.client.set_fan_timer(6)
        self.assertEqual(result, True)

        settings = self.client.get_settings()
        self.assertEqual(settings.fan_timer, 6)
        self.assertEqual(self.client.get_fan_timer(), 6)

    def test_set_target_humidity(self) -> None:
        result = self.client.set_target_humidity(93)
        self.assertEqual(result, True)

        settings = self.client.get_settings()
        self.assertEqual(settings.target_humidity, 93)

    def test_set_sweep_on(self) -> None:
        result = self.client.set_sweep_on(True)
        self.assertEqual(result, True)

        status = self.client.get_status()
        self.assertEqual(status.sweep_on, True)

        result = self.client.set_sweep_on(False)
        self.assertEqual(result, True)

        status = self.client.get_status()
        self.assertEqual(status.sweep_on, False)

    def test_set_salt_bath_on(self) -> None:
        result = self.client.set_salt_bath_on(True)
        self.assertEqual(result, True)

        status = self.client.get_status()
        self.assertEqual(status.salt_bath_on, True)

        result = self.client.set_salt_bath_on(False)
        self.assertEqual(result, True)

        status = self.client.get_status()
        self.assertEqual(status.salt_bath_on, False)

    def test_set_salt_bath_timer(self) -> None:
        result = self.client.set_salt_bath_timer(15)
        self.assertEqual(result, True)

        settings = self.client.get_settings()
        self.assertEqual(settings.salt_bath_timer, 15)
        self.assertEqual(self.client.get_salt_bath_timer(), 15)

    def test_set_lamp_mode(self) -> None:
        result = self.client.set_lamp_mode(LampMode.AUTOMATIC)
        self.assertEqual(result, True)

        settings = self.client.get_settings()
        self.assertEqual(settings.lamp_mode, LampMode.AUTOMATIC)
        self.assertEqual(self.client.get_lamp_mode(), LampMode.AUTOMATIC)

        result = self.client.set_lamp_mode(LampMode.MANUAL)
        self.assertEqual(result, True)

        settings = self.client.get_settings()
        self.assertEqual(settings.lamp_mode, LampMode.MANUAL)
        self.assertEqual(self.client.get_lamp_mode(), LampMode.MANUAL)

    def test_lamp_change_color(self) -> None:
        result = self.client.lamp_change_color()
        self.assertTrue(result)
