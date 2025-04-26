import re
import subprocess
from typing import Optional, Union
import usb.core
import usb.util
import wmi

from mag_tools.bean.base_data import BaseData
from mag_tools.bean.sys.operate_system import OperateSystem
from mag_tools.enums.usb_type import UsbType


class UsbDevice(BaseData):
    def __init__(self, vendor_id: Optional[Union[int,str]], product_id: Optional[Union[int, str]],
                 device_id: Optional[str] = None,
                 caption: Optional[str] = None, system_name: Optional[str] = None, status: Optional[str] = None,
                 description: Optional[str] = None) -> None:
        self.vendor_id = int(vendor_id, 16) if isinstance(vendor_id, str) else vendor_id
        self.product_id = int(product_id, 16) if isinstance(product_id, str) else product_id
        self.device_id = device_id
        self.caption = caption
        self.system_name = system_name
        self.status = status
        self.description = description
        self.manufacturer = None
        self.product = None
        self.serial_number = None
        self.__device = None

    def initialize(self):
        self.__device = self.__find(self.vendor_id, self.product_id)

        self.manufacturer = usb.util.get_string(self.__device, self.__device.iManufacturer)
        self.product = usb.util.get_string(self.__device, self.__device.iProduct)
        self.serial_number = usb.util.get_string(self.__device, self.__device.iSerialNumber)

    def read_data(self, endpoint, size):
        try:
            return self.__device.read(endpoint, size)
        except usb.core.USBError as e:
            raise f"读取数据失败: {e}"

    def write_data(self, endpoint, data):
        try:
            self.__device.write(endpoint, data)
        except usb.core.USBError as e:
            raise f"写入数据失败: {e}"

    @classmethod
    def list_usb(cls, usb_type: UsbType = None):
        if OperateSystem.is_windows():
            return cls.__list_from_windows(usb_type)
        elif OperateSystem.is_linux():
            return cls.__list_from_linux(usb_type)

    @classmethod
    def __list_from_windows(cls, usb_type: UsbType = None):
        c = wmi.WMI()
        usb_devices = c.Win32_USBHub()
        device_list = []
        for device in usb_devices:
            match = re.search(r'VID[_]?([0-9A-F]+).*PID[_]?([0-9A-F]+)', device.PNPDeviceID, re.I)
            if not match:
                match = re.search(r'USB\\(?:ROOT_HUB30|HASP)\\([0-9A-F]+)&([0-9A-F]+)', device.PNPDeviceID, re.I)

            vendor_id = match.group(1) if match else None
            product_id = match.group(2) if match else None

            device_info = UsbDevice(vendor_id, product_id, device.DeviceID, device.Caption, device.SystemName,
                                    device.Status, device.Description)
            if usb_type is None or (
                    usb_type.desc in device_info.description or usb_type.code in device_info.description):
                device_list.append(device_info)
        return device_list

    @classmethod
    def __list_from_linux(cls, usb_type: UsbType = None):
        """
        从 Linux 系统获取 USB 设备信息
        """
        result = subprocess.run(['lsusb'], stdout=subprocess.PIPE)
        output = result.stdout.decode()

        device_list = []
        for line in output.split('\n'):
            if line:
                parts = line.split()
                bus = parts[1]
                device = parts[3][:-1]
                vendor_id, product_id = parts[5].split(':')
                description = ' '.join(parts[6:])

                device_info = UsbDevice(vendor_id, product_id, device_id=f"{bus}-{device}", description=description)
                if usb_type is None or (
                        usb_type.desc in device_info.description or usb_type.code in device_info.description):
                    device_list.append(device_info)
        return device_list

    @classmethod
    def __find(cls, vendor_id: Optional[int] = None, product_id: Optional[int] = None):
        devices = usb.core.find(find_all=True)
        for device in devices:
            if device.idVendor == vendor_id and device.idProduct == product_id:
                return device

        raise ValueError(f"[{vendor_id}.{product_id}]设备未找到")

    def __hash__(self):
        """
        返回 USB 设备对象的哈希值
        """
        return hash((self.vendor_id, self.product_id, self.device_id, self.serial_number))


# 示例使用
if __name__ == "__main__":
    _usbs = UsbDevice.list_usb(UsbType.STORAGE)
    for _usb in _usbs:
        print(_usb)
