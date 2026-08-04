    def listAllPorts(self, flags: Optional[int] = 0) -> list['virNetworkPort']:
        """List all ports on the network and returns a list of network port objects"""
        ret = libvirtmod.virNetworkListAllPorts(self._o, flags)
        if ret is None:
            raise libvirtError("virNetworkListAllPorts() failed")

        return [virNetworkPort(self, _obj=domptr) for domptr in ret]
