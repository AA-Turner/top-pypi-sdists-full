# coding=utf-8
# Copyright (c) 2015-2026 Phidgets Inc.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import ctypes
from Phidget22._phidget_support import PhidgetSupport
from Phidget22.PhidgetServerType import PhidgetServerType
from Phidget22.PhidgetServer import PhidgetServer
from Phidget22.PhidgetServer import _CPhidgetServer
from Phidget22.PhidgetException import PhidgetException


class Net:
    r"""Net  class.

    The Phidget NET class controls all network functionality of a Phidget program, and allows for
    the use of remote Phidgets in your program. It can be used to enable automated Phidget server
    discovery over the local network, and to connect to or reject specific servers.

    For basic use of the Net class, the only functions you need to worry about are
    **EnableServerDiscovery** and **AddServer**. In most cases, you can use
    **EnableServerDiscovery** with server type **DEVICEREMOTE** to automatically connect to Phidget
    servers on your local network. You can use **AddServer** to connect to servers that aren't
    discoverable on your local network.

    To connect to a password-protected discoverable server on your local network, you can use
    **SetServerPassword** to specify the password to connect to that server.

    If for some reason you need to prevent your program from discovering a non-password-protected
    server on your local network, you can call **DisableServer** directly after calling
    **EnableServerDiscovery**.

    You must enable server discovery or add at least one server before setting other properties of
    this class, such as disabling servers, or setting server passwords. Similarly, server discovery
    must remain enabled, or at least one server must remain added, to maintain memory of those
    preferences.
    """

    def __init__(self):
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._ServerAddedFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.POINTER(_CPhidgetServer), ctypes.c_void_p
            )
        else:
            self._ServerAddedFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.POINTER(_CPhidgetServer), ctypes.c_void_p
            )
        self._ServerAdded = None
        self._onServerAdded = None

        if sys.platform == "win32":
            self._ServerRemovedFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.POINTER(_CPhidgetServer)
            )
        else:
            self._ServerRemovedFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.POINTER(_CPhidgetServer)
            )
        self._ServerRemoved = None
        self._onServerRemoved = None

    def _localServerAddedEvent(self, userPtr, server, kv):
        if self._ServerAdded is None:
            return
        if server is not None:
            server = server.contents._to_python()
        self._ServerAdded(self, server, kv)

    def setOnServerAddedHandler(self, handler):
        r"""ServerAdded event

        Subscribe to this event if you would like to know when a server has been added.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Net* - The object on which the event occurred.
            * **server** : *PhidgetServer* - The server that has been added.
            * **kv** : *object* - Opaque structure containing keys related to the server

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._ServerAdded = handler

        if self._onServerAdded is None:
            fptr = self._ServerAddedFactory(self._localServerAddedEvent)
            __func = PhidgetSupport.getDll().PhidgetNet_setOnServerAddedHandler
            __func.restype = ctypes.c_int32
            res = __func(fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onServerAdded = fptr

    def _localServerRemovedEvent(self, userPtr, server):
        if self._ServerRemoved is None:
            return
        if server is not None:
            server = server.contents._to_python()
        self._ServerRemoved(self, server)

    def setOnServerRemovedHandler(self, handler):
        r"""ServerRemoved event

        Subscribe to this event if you would like to know when a server has been removed.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Net* - The object on which the event occurred.
            * **server** : *PhidgetServer* - The server that has been removed.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._ServerRemoved = handler

        if self._onServerRemoved is None:
            fptr = self._ServerRemovedFactory(self._localServerRemovedEvent)
            __func = PhidgetSupport.getDll().PhidgetNet_setOnServerRemovedHandler
            __func.restype = ctypes.c_int32
            res = __func(fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onServerRemoved = fptr

    @staticmethod
    def _removeAllServers():
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Removes all server registrations

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetNet_removeAllServers
        __func.restype = ctypes.c_int32
        result = __func()

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def addServer(serverName, address, port, password, flags):
        r"""
        Registers a server that the client (your program) will try to connect to. The client will
        continually try to connect to the server, increasing the time between each attempt to a
        maximum interval of 16 seconds.

        This call is intended for use when server discovery is not enabled, or to connect to a
        server that is not discoverable.

        The server name used by this function does not have to match the name of the server running
        on the host machine. Only the address, port, and password need to match.

        This call will fail if a server with the same name has already been discovered.

        This call will fail if `setServerPassword()` has already been called with the same server
        name, as `setServerPassword()` registers the server entry anticipating the discovery of the
        server.

        See:

        *   `removeServer()`
        *   `enableServerDiscovery()`

        Parameters
        ----------
        serverName : str
            A unique name for the server (not the hostname)
        address : str
            The hostname or address of the server to connect to
        port : int
            The port number of the server to connect to
        password : str
            The password for the server to connect to (empty string if no password is required)
        flags : int
            connection flags: should be set to 0

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _serverName = ctypes.create_string_buffer(serverName.encode("utf-8"))
        _address = ctypes.create_string_buffer(address.encode("utf-8"))
        _port = ctypes.c_int(port)
        _password = ctypes.create_string_buffer(password.encode("utf-8"))
        _flags = ctypes.c_int(flags)

        __func = PhidgetSupport.getDll().PhidgetNet_addServer
        __func.restype = ctypes.c_int32
        result = __func(_serverName, _address, _port, _password, _flags)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def removeServer(serverName):
        r"""
        Removes a registration for a server that the client (your program) is trying to connect
        to.If the client is currently connected to the server, the connection will be closed.

        If the server was discovered (not added by `addServer()`), the connection may be
        reestablished if and when the server is rediscovered. `disableServer()` should be used to
        prevent the reconnection of a discovered server

        See:

        *   `addServer()`
        *   `disableServer()`
        *   `disableServerDiscovery()`

        Parameters
        ----------
        serverName : str
            The name of the server to remove

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _serverName = ctypes.create_string_buffer(serverName.encode("utf-8"))

        __func = PhidgetSupport.getDll().PhidgetNet_removeServer
        __func.restype = ctypes.c_int32
        result = __func(_serverName)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def enableServer(serverName):
        r"""
        Enables attempts to connect to a discovered server, if attempts were previously disabled by
        `disableServer()`. All servers are enabled by default.

        This call will fail if the server was not previously added, disabled or discovered.

        See:

        *   `disableServer()`

        Parameters
        ----------
        serverName : str
            The name of the server to enable

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _serverName = ctypes.create_string_buffer(serverName.encode("utf-8"))

        __func = PhidgetSupport.getDll().PhidgetNet_enableServer
        __func.restype = ctypes.c_int32
        result = __func(_serverName)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def disableServer(serverName, flags):
        r"""
        Prevents attempts to automatically connect to a server.

        By default the client (your program) will continually attempt to connect to added or
        discovered servers.This call will disable those attempts, but will not close an already
        established connection.

        See:

        *   `addServer()`
        *   `enableServer()`
        *   `enableServerDiscovery()`

        Parameters
        ----------
        serverName : str
            The name of the server to stop connections to
        flags : int
            Should be 0

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _serverName = ctypes.create_string_buffer(serverName.encode("utf-8"))
        _flags = ctypes.c_int(flags)

        __func = PhidgetSupport.getDll().PhidgetNet_disableServer
        __func.restype = ctypes.c_int32
        result = __func(_serverName, _flags)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def enableServerDiscovery(serverType):
        r"""
        Enables the dynamic discovery of servers that publish their identity to the network.
        Currently Multicast DNS is used to discover and publish Phidget servers.

        To connect to remote Phidgets, call this function with server type
        `Phidget22.PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE`.

        `enableServerDiscovery()` must be called once for each server type your program requires.
        Multiple calls for the same server type are ignored

        This call will fail with the error code `Phidget22.ErrorCode.EPHIDGET_UNSUPPORTED` if your
        computer does not have the required mDNS support. We recommend using Bonjour on Windows and
        Mac, and Avahi on Linux.

        For more information, visit our [Network Server
        Guide](https://www.phidgets.com/docs/Network_Server_Guide#Enabling_Server_Discovery)



        See:

        *   `disableServerDiscovery()`
        *   `addServer()`

        Parameters
        ----------
        serverType : PhidgetServerType
            The server type listen for

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _serverType = ctypes.c_int(serverType)

        __func = PhidgetSupport.getDll().PhidgetNet_enableServerDiscovery
        __func.restype = ctypes.c_int32
        result = __func(_serverType)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def disableServerDiscovery(serverType):
        r"""
        Disables the dynamic discovery of servers that publish their identity.

        `disableServerDiscovery()` does not disconnect already established connections.

        See:

        *   `enableServerDiscovery()`
        *   `disableServer()`
        *   `removeServer()`

        Parameters
        ----------
        serverType : PhidgetServerType
            The server type to disable

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _serverType = ctypes.c_int(serverType)

        __func = PhidgetSupport.getDll().PhidgetNet_disableServerDiscovery
        __func.restype = ctypes.c_int32
        result = __func(_serverType)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def setServerPassword(serverName, password):
        r"""
        Sets the password that will be used to attempt to connect to the server. If the server has
        not already been added or discovered, a placeholder server entry will be registered to use
        this password on the server once it is discovered.

        Parameters
        ----------
        serverName : str
            The name of the server
        password : str
            The password to use for the server (empty string if no password)

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _serverName = ctypes.create_string_buffer(serverName.encode("utf-8"))
        _password = ctypes.create_string_buffer(password.encode("utf-8"))

        __func = PhidgetSupport.getDll().PhidgetNet_setServerPassword
        __func.restype = ctypes.c_int32
        result = __func(_serverName, _password)

        if result > 0:
            raise PhidgetException(result)

    AUTHREQUIRED = 1
    """PhidgetServer flag indicating that the server requires a password to authenticate"""


__all__ = ["Net", "PhidgetServerType", "PhidgetServer", "PhidgetException"]
