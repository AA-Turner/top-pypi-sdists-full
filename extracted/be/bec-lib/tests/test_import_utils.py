from bec_lib.device import DeviceBase
from bec_lib.utils.import_utils import isinstance_based_on_class_name


def test_isinstance_based_on_class_name():
    obj = DeviceBase(name="test_obj")

    assert isinstance_based_on_class_name(obj, "bec_lib.device.DeviceBase")
    assert not isinstance_based_on_class_name(obj, "bec_lib.device.Status")
