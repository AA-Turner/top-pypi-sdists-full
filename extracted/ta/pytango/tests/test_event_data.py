import pytest

from tango import (
    AttrConfEventData,
    AttributeInfoEx,
    AttributeInfoListEx,
    CommandInfo,
    CommandInfoList,
    DataReadyEventData,
    DeviceAttribute,
    DevIntrChangeEventData,
    EventData,
    EventReason,
)
from tango.server import Device
from tango.test_utils import DeviceTestContext


@pytest.fixture
def device_proxy():
    with DeviceTestContext(Device) as proxy:
        yield proxy


# this fixture need to check correct destruction behavior, so value it is important
@pytest.fixture
def attr_value():
    attr_value = DeviceAttribute()
    attr_value.name = "test_attribute"
    return attr_value


class TestEventDataConstructors:
    def test_event_data_all_none(self):
        event = EventData()
        assert event is not None
        assert event.attr_name == ""
        assert event.event == ""
        assert event.event_reason == EventReason.Update

    def test_event_data_with_device_proxy(self, device_proxy):
        event = EventData(device_proxy=device_proxy)
        assert event is not None
        assert event.device == device_proxy

    def test_event_data_with_strings(self):
        event = EventData(attr_name="voltage", event_name="periodic")
        assert event is not None
        assert event.attr_name == "voltage"
        assert event.event == "periodic"

    def test_event_data_with_value(self, attr_value):
        # here we just test that EventData does not crash at construction/destruction
        # since the extraction of attr_value back to python happens in the callback
        # probably this functionally will be added later

        event = EventData(attr_value=attr_value)
        assert event is not None

    def test_event_data_with_event_reason(self):
        """Test EventData with specific EventReason"""
        event = EventData(event_reason=EventReason.SubSuccess)
        assert event is not None
        assert event.event_reason == EventReason.SubSuccess

    def test_event_data_copy_constructor(self):
        """Test EventData copy constructor"""
        event1 = EventData()
        event2 = EventData(event1)
        assert event2 is not None


class TestAttrConfEventDataConstructors:
    """Test AttrConfEventData constructor with None values"""

    def test_attr_conf_event_data_all_none(self):
        """Test AttrConfEventData with all None arguments"""
        event = AttrConfEventData()
        assert event is not None
        assert event.attr_name == ""
        assert event.event == ""
        assert event.event_reason == EventReason.Update

    def test_attr_conf_event_data_with_names(self):
        event = AttrConfEventData(attr_name="config_attr", event_name="attr_conf")
        assert event is not None
        assert event.attr_name == "config_attr"
        assert event.event == "attr_conf"

    def test_attr_conf_event_data_with_device_proxy(self, device_proxy):
        event = AttrConfEventData(device_proxy=device_proxy)
        assert event is not None
        assert event.device == device_proxy

    def test_attr_conf_event_data_with_attr_conf(self):
        attr_info = AttributeInfoEx()
        attr_info.name = "test_attribute"

        event = AttrConfEventData(attr_conf=attr_info)
        assert event is not None

        assert repr(event.attr_conf) == repr(attr_info)

    def test_attr_conf_event_data_copy_constructor(self):
        event1 = AttrConfEventData()
        event2 = AttrConfEventData(event1)
        assert event2 is not None


class TestDataReadyEventDataConstructors:
    def test_data_ready_event_data_all_none(self):
        event = DataReadyEventData()
        assert event is not None
        assert event.attr_name == "Unknown"
        assert event.event == ""
        assert event.event_reason == EventReason.Update

    def test_data_ready_event_data_with_device_proxy(self, device_proxy):
        event = DataReadyEventData(device_proxy=device_proxy)
        assert event is not None
        assert event.device == device_proxy

    def test_data_ready_event_data_with_event_name(self):
        event = DataReadyEventData(event_name="data_ready")
        assert event is not None
        assert event.event == "data_ready"

    def test_data_ready_event_data_with_event_reason(self):
        event = DataReadyEventData(event_reason=EventReason.SubSuccess)
        assert event is not None
        assert event.event_reason == EventReason.SubSuccess

    def test_data_ready_event_data_copy_constructor(self):
        event1 = DataReadyEventData()
        event2 = DataReadyEventData(event1)
        assert event2 is not None


class TestDevIntrChangeEventDataConstructors:
    def test_dev_intr_change_event_data_all_none(self):
        event = DevIntrChangeEventData()
        assert event is not None
        assert not event.dev_started
        assert event.device_name == ""
        assert event.event_reason == EventReason.Update

    def test_dev_intr_change_event_data_with_device_proxy(self, device_proxy):
        event = DevIntrChangeEventData(device_proxy=device_proxy)
        assert event is not None
        assert event.device == device_proxy

    def test_dev_intr_change_event_data_with_strings_and_bools(self):
        event = DevIntrChangeEventData(device_name="interface_change", event_name="intr_change", dev_started=True)
        assert event is not None
        assert event.device_name == "interface_change"
        assert event.event == "intr_change"
        assert event.dev_started

    def test_dev_intr_change_event_data_with_cmd_and_attr_list(self):
        cmd_list = CommandInfoList()
        cmd_list.append(CommandInfo())

        att_list = AttributeInfoListEx()
        attr_info = AttributeInfoEx()
        att_list.append(attr_info)

        event = DevIntrChangeEventData(cmd_list=cmd_list, att_list=att_list)
        assert event is not None

        assert repr(event.cmd_list) == repr(cmd_list)
        assert repr(event.att_list) == repr(att_list)

    def test_dev_intr_change_event_data_copy_constructor(self):
        event1 = DevIntrChangeEventData()
        event2 = DevIntrChangeEventData(event1)
        assert event2 is not None


# Parametrized tests for edge cases
class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_multiple_instantiations(self):
        """Test creating multiple instances doesn't cause issues"""
        events = [EventData() for _ in range(10)]
        assert len(events) == 10
        assert all(e is not None for e in events)
