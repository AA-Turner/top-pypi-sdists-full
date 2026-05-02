import inject


class LiveStatus:
    """ Constants class for Live Status """

    @staticmethod
    def ONLINE():
        return 'Online'

    @staticmethod
    def OFFLINE():
        return 'Offline'


class ConnectedToPduResource:
    """This class manages a Cloudshell resource which is connected to the Cloudshell PDU resource. """

    def __init__(self, endpoints, api=None):
        """
        :param endpoints: the power sockets on the device we are managing, which get power from the PDU.
        The device we are managing is the ancestor (parent or parent of parents) resource of the endpoints we pass in.
        :type endpoints: list(cloudshell.shell.core.driver_context.ResourceContextDetails)
        :param api: api used for live status and resource details, default is Cloudshell API
        :type api: cloudshell.api.cloudshell_api.CloudShellAPISession
        """
        self.name = self._get_root_resource_name_by_path(endpoints)
        self._endpoints = endpoints
        if api is None:
            api = inject.instance('api')
        self._api = api
        self._details = self._get_resource_details(api)

    @property
    def details(self):
        """
        :rtype: cloudshell.api.cloudshell_api.ResourceInfo
        """
        return self._details

    def online(self):
        """ sets live status on the root resource of device we are managing to powered on

        :returns: message that endpoints of device have been powered on
        :rtype: str
        """
        status = 'Powered on'
        self._set_live_status_on_device(LiveStatus.ONLINE(), status)
        return self._output_for_all_endpoints(status.lower())

    def offline(self):
        """ sets live status on the root resource of device we are managing to powered off

        :returns: message that endpoints of device have been powered off
        :rtype: str
        """
        status = 'Powered off'
        self._set_live_status_on_device(LiveStatus.OFFLINE(), status)
        return self._output_for_all_endpoints(status.lower())

    def _get_root_resource_name_by_path(self, endpoints):
        """ returns the root resource name from the endpoints full name.

        :param endpoints: ['connectedDeviceName//connectedDevicePortName']
        :type endpoints: list(cloudshell.shell.core.driver_context.ResourceContextDetails)
        :returns: 'connectedDeviceName'
        :rtype: str
        """
        return endpoints[0].fullname.split('/')[0]

    def _get_resource_details(self, api):
        """ returns the root resource details of the device we are managing

        :param api: api used for live status and resource details, default is Cloudshell API
        :type api: qualipy.api.cloudshell_api.CloudShellAPISession
        :returns: The root resource details
        :rtype: cloudshell.api.cloudshell_api.ResourceInfo
        """
        return api.GetResourceDetails(self.name)

    def _set_live_status_on_device(self, status, description=''):
        """ Sets the live status on the Cloudshell resource we are managing

        :param status: live status name
        :type status: str
        :param description: live status additional info
        :type description: str
        :return: None
        """
        self._api.SetResourceLiveStatus(self.name, status, description)

    def _output_for_all_endpoints(self, msg):
        """ returns a message for all affected endpoints

        :param msg: what was done to the endpoint, example: powered on.
        :type msg: str
        :returns: example: 'PowerManagedResource/PowerPort1 powered on\nPowerManagedResource/PowerPort2 powered on'
        :rtype: str
        """
        result = [r.fullname + ' ' + msg for r in self._endpoints]
        out = '\n'.join(result)
        return out
