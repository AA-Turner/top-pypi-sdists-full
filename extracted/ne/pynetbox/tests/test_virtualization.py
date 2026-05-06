import unittest
from unittest.mock import patch

import pynetbox
from pynetbox.models.dcim import Devices
from pynetbox.models.virtualization import VirtualMachineTypes

from .util import Response

api = pynetbox.api(
    "http://localhost:8000",
)

nb = api.virtualization

HEADERS = {"accept": "application/json"}


class Generic:
    class Tests(unittest.TestCase):
        name = ""
        ret = pynetbox.core.response.Record
        app = "virtualization"

        def test_get_all(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture="{}/{}.json".format(self.app, self.name)),
            ) as mock:
                ret = list(getattr(nb, self.name).all())
                self.assertTrue(ret)
                self.assertTrue(isinstance(ret[0], self.ret))
                mock.assert_called_with(
                    "http://localhost:8000/api/{}/{}/".format(
                        self.app, self.name.replace("_", "-")
                    ),
                    params={"limit": 0},
                    json=None,
                    headers=HEADERS,
                )

        def test_filter(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture="{}/{}.json".format(self.app, self.name)),
            ) as mock:
                ret = list(getattr(nb, self.name).filter(name="test"))
                self.assertTrue(ret)
                self.assertTrue(isinstance(ret[0], self.ret))
                mock.assert_called_with(
                    "http://localhost:8000/api/{}/{}/".format(
                        self.app, self.name.replace("_", "-")
                    ),
                    params={"name": "test", "limit": 0},
                    json=None,
                    headers=HEADERS,
                )

        def test_get(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(
                    fixture="{}/{}.json".format(self.app, self.name[:-1])
                ),
            ) as mock:
                ret = getattr(nb, self.name).get(1)
                self.assertTrue(ret)
                self.assertTrue(isinstance(ret, self.ret))
                mock.assert_called_with(
                    "http://localhost:8000/api/{}/{}/1/".format(
                        self.app, self.name.replace("_", "-")
                    ),
                    params={},
                    json=None,
                    headers=HEADERS,
                )


class ClusterTypesTestCase(Generic.Tests):
    name = "cluster_types"


class ClusterGroupsTestCase(Generic.Tests):
    name = "cluster_groups"


class ClustersTestCase(Generic.Tests):
    name = "clusters"


class VirtualMachinesTestCase(Generic.Tests):
    name = "virtual_machines"

    @patch(
        "requests.sessions.Session.get",
        return_value=Response(fixture="virtualization/virtual_machine.json"),
    )
    def test_device_attr(self, _):
        vm = nb.virtual_machines.get(1)
        self.assertIsInstance(vm.device, Devices)
        self.assertEqual(vm.device.name, "test-device")

    @patch(
        "requests.sessions.Session.get",
        return_value=Response(fixture="virtualization/virtual_machine.json"),
    )
    def test_virtual_machine_type_attr(self, _):
        vm = nb.virtual_machines.get(1)
        self.assertIsInstance(vm.virtual_machine_type, VirtualMachineTypes)
        self.assertEqual(vm.virtual_machine_type.name, "Standard")


class VirtualMachineTypesTestCase(Generic.Tests):
    name = "virtual_machine_types"


class InterfacesTestCase(Generic.Tests):
    name = "interfaces"
