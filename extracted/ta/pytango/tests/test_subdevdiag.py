from tango import Util, DeviceProxy
from tango.server import Device, command
from tango.test_context import DeviceTestContext, MultiDeviceTestContext


class DeviceToTest1(Device):

    @command
    def check_device(self, device_instance: str):
        assert (
            Util.instance().get_sub_dev_diag().get_associated_device()
            == device_instance
        )


devices_info = (
    {
        "class": DeviceToTest1,
        "devices": [{"name": "test/device/1"}, {"name": "test/device/2"}],
    },
)


def test_associated_device_is_device_instance():

    # NOTE: this test works only with process=True
    with MultiDeviceTestContext(devices_info, process=True):
        dev1 = DeviceProxy("test/device/1")
        dev2 = DeviceProxy("test/device/2")

        dev1.check_device("test/device/1")
        dev2.check_device("test/device/2")


class DeviceToTest2(Device):

    sdd = None

    def init_device(self):
        super().init_device()
        self.sdd = Util.instance().get_sub_dev_diag()

    @command
    def add_device(self, device_instance: str):
        self.sdd.register_sub_device(device_instance, "test_device")

    @command
    def remove_device(self, device_instance: str):
        self.sdd.remove_sub_devices(device_instance)

    @command
    def check_device(self, test_string: str):
        if len(test_string) > 0:
            assert self.sdd.get_sub_devices() == [test_string]
        else:
            assert self.sdd.get_sub_devices() == []


def test_register_sub_device():

    with DeviceTestContext(
        DeviceToTest2, device_name="test/device/1", process=True
    ) as dev:
        dev.check_device("")
        dev.add_device("test/device/1")
        dev.check_device("test/device/1 test_device")
        dev.remove_device("test/device/1")
        dev.check_device("")
