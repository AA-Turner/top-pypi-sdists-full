"""FortiOS CMDB - Firewall category"""

from . import ipmacbinding
from . import schedule
from . import service
from . import shaper
from . import ssh
from . import ssl
from . import wildcard_fqdn
from .DoS_policy import DosPolicy
from .DoS_policy6 import DosPolicy6
from .access_proxy import AccessProxy
from .access_proxy6 import AccessProxy6
from .access_proxy_ssh_client_cert import AccessProxySshClientCert
from .access_proxy_virtual_host import AccessProxyVirtualHost
from .address import Address
from .address6 import Address6
from .address6_template import Address6Template
from .addrgrp import Addrgrp
from .addrgrp6 import Addrgrp6
from .auth_portal import AuthPortal
from .central_snat_map import CentralSnatMap
from .city import City
from .country import Country
from .decrypted_traffic_mirror import DecryptedTrafficMirror
from .dnstranslation import Dnstranslation
from .global_ import Global
from .identity_based_route import IdentityBasedRoute
from .interface_policy import InterfacePolicy
from .interface_policy6 import InterfacePolicy6
from .internet_service import InternetService
from .internet_service_addition import InternetServiceAddition
from .internet_service_append import InternetServiceAppend
from .internet_service_botnet import InternetServiceBotnet
from .internet_service_custom import InternetServiceCustom
from .internet_service_custom_group import InternetServiceCustomGroup
from .internet_service_definition import InternetServiceDefinition
from .internet_service_extension import InternetServiceExtension
from .internet_service_fortiguard import InternetServiceFortiguard
from .internet_service_group import InternetServiceGroup
from .internet_service_ipbl_reason import InternetServiceIpblReason
from .internet_service_ipbl_vendor import InternetServiceIpblVendor
from .internet_service_list import InternetServiceList
from .internet_service_name import InternetServiceName
from .internet_service_owner import InternetServiceOwner
from .internet_service_reputation import InternetServiceReputation
from .internet_service_sld import InternetServiceSld
from .internet_service_subapp import InternetServiceSubapp
from .ip_translation import IpTranslation
from .ippool import Ippool
from .ippool6 import Ippool6
from .ldb_monitor import LdbMonitor
from .local_in_policy import LocalInPolicy
from .local_in_policy6 import LocalInPolicy6
from .multicast_address import MulticastAddress
from .multicast_address6 import MulticastAddress6
from .multicast_policy import MulticastPolicy
from .multicast_policy6 import MulticastPolicy6
from .network_service_dynamic import NetworkServiceDynamic
from .on_demand_sniffer import OnDemandSniffer
from .policy import Policy
from .profile_group import ProfileGroup
from .profile_protocol_options import ProfileProtocolOptions
from .proxy_address import ProxyAddress
from .proxy_addrgrp import ProxyAddrgrp
from .proxy_policy import ProxyPolicy
from .region import Region
from .security_policy import SecurityPolicy
from .shaping_policy import ShapingPolicy
from .shaping_profile import ShapingProfile
from .sniffer import Sniffer
from .ssl_server import SslServer
from .ssl_ssh_profile import SslSshProfile
from .traffic_class import TrafficClass
from .ttl_policy import TtlPolicy
from .vendor_mac import VendorMac
from .vendor_mac_summary import VendorMacSummary
from .vip import Vip
from .vip6 import Vip6
from .vipgrp import Vipgrp
from .vipgrp6 import Vipgrp6

__all__ = [
    "AccessProxy",
    "AccessProxy6",
    "AccessProxySshClientCert",
    "AccessProxyVirtualHost",
    "Address",
    "Address6",
    "Address6Template",
    "Addrgrp",
    "Addrgrp6",
    "AuthPortal",
    "CentralSnatMap",
    "City",
    "Country",
    "DecryptedTrafficMirror",
    "Dnstranslation",
    "DosPolicy",
    "DosPolicy6",
    "Firewall",
    "Global",
    "IdentityBasedRoute",
    "InterfacePolicy",
    "InterfacePolicy6",
    "InternetService",
    "InternetServiceAddition",
    "InternetServiceAppend",
    "InternetServiceBotnet",
    "InternetServiceCustom",
    "InternetServiceCustomGroup",
    "InternetServiceDefinition",
    "InternetServiceExtension",
    "InternetServiceFortiguard",
    "InternetServiceGroup",
    "InternetServiceIpblReason",
    "InternetServiceIpblVendor",
    "InternetServiceList",
    "InternetServiceName",
    "InternetServiceOwner",
    "InternetServiceReputation",
    "InternetServiceSld",
    "InternetServiceSubapp",
    "IpTranslation",
    "Ipmacbinding",
    "Ippool",
    "Ippool6",
    "LdbMonitor",
    "LocalInPolicy",
    "LocalInPolicy6",
    "MulticastAddress",
    "MulticastAddress6",
    "MulticastPolicy",
    "MulticastPolicy6",
    "NetworkServiceDynamic",
    "OnDemandSniffer",
    "Policy",
    "ProfileGroup",
    "ProfileProtocolOptions",
    "ProxyAddress",
    "ProxyAddrgrp",
    "ProxyPolicy",
    "Region",
    "Schedule",
    "SecurityPolicy",
    "Service",
    "Shaper",
    "ShapingPolicy",
    "ShapingProfile",
    "Sniffer",
    "Ssh",
    "Ssl",
    "SslServer",
    "SslSshProfile",
    "TrafficClass",
    "TtlPolicy",
    "VendorMac",
    "VendorMacSummary",
    "Vip",
    "Vip6",
    "Vipgrp",
    "Vipgrp6",
    "WildcardFqdn",
]


class Firewall:
    """Firewall endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Firewall endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.ipmacbinding = ipmacbinding.Ipmacbinding(client)
        self.schedule = schedule.Schedule(client)
        self.service = service.Service(client)
        self.shaper = shaper.Shaper(client)
        self.ssh = ssh.Ssh(client)
        self.ssl = ssl.Ssl(client)
        self.wildcard_fqdn = wildcard_fqdn.WildcardFqdn(client)
        self.DoS_policy = DosPolicy(client)
        self.DoS_policy6 = DosPolicy6(client)
        self.access_proxy = AccessProxy(client)
        self.access_proxy6 = AccessProxy6(client)
        self.access_proxy_ssh_client_cert = AccessProxySshClientCert(client)
        self.access_proxy_virtual_host = AccessProxyVirtualHost(client)
        self.address = Address(client)
        self.address6 = Address6(client)
        self.address6_template = Address6Template(client)
        self.addrgrp = Addrgrp(client)
        self.addrgrp6 = Addrgrp6(client)
        self.auth_portal = AuthPortal(client)
        self.central_snat_map = CentralSnatMap(client)
        self.city = City(client)
        self.country = Country(client)
        self.decrypted_traffic_mirror = DecryptedTrafficMirror(client)
        self.dnstranslation = Dnstranslation(client)
        self.global_ = Global(client)
        self.identity_based_route = IdentityBasedRoute(client)
        self.interface_policy = InterfacePolicy(client)
        self.interface_policy6 = InterfacePolicy6(client)
        self.internet_service = InternetService(client)
        self.internet_service_addition = InternetServiceAddition(client)
        self.internet_service_append = InternetServiceAppend(client)
        self.internet_service_botnet = InternetServiceBotnet(client)
        self.internet_service_custom = InternetServiceCustom(client)
        self.internet_service_custom_group = InternetServiceCustomGroup(client)
        self.internet_service_definition = InternetServiceDefinition(client)
        self.internet_service_extension = InternetServiceExtension(client)
        self.internet_service_fortiguard = InternetServiceFortiguard(client)
        self.internet_service_group = InternetServiceGroup(client)
        self.internet_service_ipbl_reason = InternetServiceIpblReason(client)
        self.internet_service_ipbl_vendor = InternetServiceIpblVendor(client)
        self.internet_service_list = InternetServiceList(client)
        self.internet_service_name = InternetServiceName(client)
        self.internet_service_owner = InternetServiceOwner(client)
        self.internet_service_reputation = InternetServiceReputation(client)
        self.internet_service_sld = InternetServiceSld(client)
        self.internet_service_subapp = InternetServiceSubapp(client)
        self.ip_translation = IpTranslation(client)
        self.ippool = Ippool(client)
        self.ippool6 = Ippool6(client)
        self.ldb_monitor = LdbMonitor(client)
        self.local_in_policy = LocalInPolicy(client)
        self.local_in_policy6 = LocalInPolicy6(client)
        self.multicast_address = MulticastAddress(client)
        self.multicast_address6 = MulticastAddress6(client)
        self.multicast_policy = MulticastPolicy(client)
        self.multicast_policy6 = MulticastPolicy6(client)
        self.network_service_dynamic = NetworkServiceDynamic(client)
        self.on_demand_sniffer = OnDemandSniffer(client)
        self.policy = Policy(client)
        self.profile_group = ProfileGroup(client)
        self.profile_protocol_options = ProfileProtocolOptions(client)
        self.proxy_address = ProxyAddress(client)
        self.proxy_addrgrp = ProxyAddrgrp(client)
        self.proxy_policy = ProxyPolicy(client)
        self.region = Region(client)
        self.security_policy = SecurityPolicy(client)
        self.shaping_policy = ShapingPolicy(client)
        self.shaping_profile = ShapingProfile(client)
        self.sniffer = Sniffer(client)
        self.ssl_server = SslServer(client)
        self.ssl_ssh_profile = SslSshProfile(client)
        self.traffic_class = TrafficClass(client)
        self.ttl_policy = TtlPolicy(client)
        self.vendor_mac = VendorMac(client)
        self.vendor_mac_summary = VendorMacSummary(client)
        self.vip = Vip(client)
        self.vip6 = Vip6(client)
        self.vipgrp = Vipgrp(client)
        self.vipgrp6 = Vipgrp6(client)
