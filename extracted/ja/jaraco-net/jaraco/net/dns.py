#!python

import os
import sys
import socket
import winreg

import win32serviceutil
import win32service

port = socket.getservbyname('domain')


class Forwarder:
    """
    Windows Server 2008 and Windows Server 2008 R2 DNS Servers do not
    support listening on tunneled IPv6 addresses.  See
    http://social.technet.microsoft.com/Forums/en-US/winserverPN/thread/fe12c783-f6b8-4560-9a9a-8ab7c46b80cb
    for details.

    This forwarder can be installed as a service and run on any such server,
    and it will forward DNS requests to the IPv6 localhost address.
    """

    dest_addr = ('::1', port)

    def __init__(self, listen_address):
        self.socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        address = (listen_address, port)
        self.socket.bind(address)
        # set a timeout so the service can terminate gracefully
        self.socket.settimeout(2)
        self.dest = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.dest.settimeout(2)

    def stop(self):
        self.run = False

    def serve_forever(self):
        self.run = True
        while self.run:
            self.relay_message()

    def relay_message(self):
        try:
            mesg, requester = self.socket.recvfrom(2**16)
            print('received', mesg, 'from', requester)
            self.dest.sendto(mesg, self.dest_addr)
            resp, src = self.dest.recvfrom(2**16)
            print('response', resp)
            self.socket.sendto(resp, requester)
        except socket.timeout:
            pass


class RegConfig:
    def __init__(self, root_path, tree=winreg.HKEY_CURRENT_USER):
        self.root_path = root_path
        self.tree = tree

    def _get_key(self):
        return winreg.CreateKey(self.tree, self.root_path)

    @staticmethod
    def infer_key_type(value):
        if isinstance(value, int):
            return winreg.REG_DWORD
        if isinstance(value, str):
            if '%' in value:
                return winreg.REG_EXPAND_SZ
            return winreg.REG_SZ
        raise ValueError(f'Unable to infer type for {value}')

    def __setitem__(self, key, value):
        keytype = self.infer_key_type(value)
        self.set(key, value, keytype)

    def set(self, key, value, keytype):
        winreg.SetValueEx(self._get_key(), key, None, keytype, value)

    def __getitem__(self, key):
        try:
            value, type = winreg.QueryValueEx(self._get_key(), key)
        except OSError:
            raise KeyError(key)
        return value

    def get(self, key, default=None):
        try:
            value = self[key]
        except KeyError:
            value = default
        return value


class ForwardingService(win32serviceutil.ServiceFramework):
    r"""
    _svc_name_: The name of the service (used in the Windows registry).
    DEFAULT: The capitalized name of the current directory.

    _svc_display_name_: The name that will appear in the Windows Service Manager.
    DEFAULT: The capitalized name of the current directory.

    log_dir: The desired location of the stdout and stderr log files.
    DEFAULT: %system%\LogFiles\%(_svc_display_name_)s
    """

    _svc_name_ = 'dns_forward'
    "The name of the service"
    _svc_display_name_ = 'DNS Forwarding Service'
    "The Service Manager display name."
    log_dir = os.path.join(
        os.environ['SYSTEMROOT'], 'System32', 'LogFiles', _svc_display_name_
    )
    "The log directory for the stderr and stdout logs."

    config = RegConfig(
        r'Software\jaraco.net\DNS Forwarding Service', winreg.HKEY_LOCAL_MACHINE
    )

    def SvcDoRun(self):
        """Called when the Windows Service runs."""
        self.init_logging()
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.forwarder = Forwarder(self.config.get('Listen Address', '::0'))
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.forwarder.serve_forever()

    def SvcStop(self):
        """Called when Windows receives a service stop request."""

        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.forwarder.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def init_logging(self):
        "redirect output to avoid crashing the service"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        sys.stdout = open(os.path.join(ForwardingService.log_dir, 'stdout.log'), 'a')
        sys.stderr = open(os.path.join(ForwardingService.log_dir, 'stderr.log'), 'a')

    @classmethod
    def handle_command_line(cls):
        def listen_setter(opts):
            opts = dict(opts)
            if '-b' in opts:
                ForwardingService.config['Listen Address'] = opts['-b']

        params = dict(
            customInstallOptions='b:',  # use -b to specify bind address
            customOptionHandler=listen_setter,
        )
        win32serviceutil.HandleCommandLine(cls, **params)


def main():
    addr = ForwardingService.config['Listen Address']
    Forwarder(addr).serve_forever()


__name__ == '__main__' and main()
