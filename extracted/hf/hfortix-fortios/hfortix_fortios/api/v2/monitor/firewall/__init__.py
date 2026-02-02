"""FortiOS CMDB - Firewall category"""

from . import acl
from . import acl6
from . import central_snat_map
from . import clearpass_address
from . import dnat
from . import gtp
from . import ippool
from . import multicast_policy
from . import multicast_policy6
from . import per_ip_shaper
from . import policy
from . import proxy
from . import proxy_policy
from . import security_policy
from . import session
from . import session6
from . import shaper
from . import ztna_firewall_policy
from .address6_dynamic import Address6Dynamic
from .address_dynamic import AddressDynamic
from .address_fqdns import AddressFqdns
from .address_fqdns6 import AddressFqdns6
from .check_addrgrp_exclude_mac_member import CheckAddrgrpExcludeMacMember
from .gtp_runtime_statistics import GtpRuntimeStatistics
from .gtp_statistics import GtpStatistics
from .health import Health
from .internet_service_basic import InternetServiceBasic
from .internet_service_details import InternetServiceDetails
from .internet_service_fqdn import InternetServiceFqdn
from .internet_service_fqdn_icon_ids import InternetServiceFqdnIconIds
from .internet_service_match import InternetServiceMatch
from .internet_service_reputation import InternetServiceReputation
from .load_balance import LoadBalance
from .local_in import LocalIn
from .local_in6 import LocalIn6
from .network_service_dynamic import NetworkServiceDynamic
from .policy_lookup import PolicyLookup
from .saas_application import SaasApplication
from .sdn_connector_filters import SdnConnectorFilters
from .sessions import Sessions
from .uuid_list import UuidList
from .uuid_type_lookup import UuidTypeLookup
from .vip_overlap import VipOverlap

__all__ = [
    "Acl",
    "Acl6",
    "Address6Dynamic",
    "AddressDynamic",
    "AddressFqdns",
    "AddressFqdns6",
    "CentralSnatMap",
    "CheckAddrgrpExcludeMacMember",
    "ClearpassAddress",
    "Dnat",
    "Firewall",
    "Gtp",
    "GtpRuntimeStatistics",
    "GtpStatistics",
    "Health",
    "InternetServiceBasic",
    "InternetServiceDetails",
    "InternetServiceFqdn",
    "InternetServiceFqdnIconIds",
    "InternetServiceMatch",
    "InternetServiceReputation",
    "Ippool",
    "LoadBalance",
    "LocalIn",
    "LocalIn6",
    "MulticastPolicy",
    "MulticastPolicy6",
    "NetworkServiceDynamic",
    "PerIpShaper",
    "Policy",
    "PolicyLookup",
    "Proxy",
    "ProxyPolicy",
    "SaasApplication",
    "SdnConnectorFilters",
    "SecurityPolicy",
    "Session",
    "Session6",
    "Sessions",
    "Shaper",
    "UuidList",
    "UuidTypeLookup",
    "VipOverlap",
    "ZtnaFirewallPolicy",
]


class Firewall:
    """Firewall endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Firewall endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.acl = acl.Acl(client)
        self.acl6 = acl6.Acl6(client)
        self.central_snat_map = central_snat_map.CentralSnatMap(client)
        self.clearpass_address = clearpass_address.ClearpassAddress(client)
        self.dnat = dnat.Dnat(client)
        self.gtp = gtp.Gtp(client)
        self.ippool = ippool.Ippool(client)
        self.multicast_policy = multicast_policy.MulticastPolicy(client)
        self.multicast_policy6 = multicast_policy6.MulticastPolicy6(client)
        self.per_ip_shaper = per_ip_shaper.PerIpShaper(client)
        self.policy = policy.Policy(client)
        self.proxy = proxy.Proxy(client)
        self.proxy_policy = proxy_policy.ProxyPolicy(client)
        self.security_policy = security_policy.SecurityPolicy(client)
        self.session = session.Session(client)
        self.session6 = session6.Session6(client)
        self.shaper = shaper.Shaper(client)
        self.ztna_firewall_policy = ztna_firewall_policy.ZtnaFirewallPolicy(client)
        self.address6_dynamic = Address6Dynamic(client)
        self.address_dynamic = AddressDynamic(client)
        self.address_fqdns = AddressFqdns(client)
        self.address_fqdns6 = AddressFqdns6(client)
        self.check_addrgrp_exclude_mac_member = CheckAddrgrpExcludeMacMember(client)
        self.gtp_runtime_statistics = GtpRuntimeStatistics(client)
        self.gtp_statistics = GtpStatistics(client)
        self.health = Health(client)
        self.internet_service_basic = InternetServiceBasic(client)
        self.internet_service_details = InternetServiceDetails(client)
        self.internet_service_fqdn = InternetServiceFqdn(client)
        self.internet_service_fqdn_icon_ids = InternetServiceFqdnIconIds(client)
        self.internet_service_match = InternetServiceMatch(client)
        self.internet_service_reputation = InternetServiceReputation(client)
        self.load_balance = LoadBalance(client)
        self.local_in = LocalIn(client)
        self.local_in6 = LocalIn6(client)
        self.network_service_dynamic = NetworkServiceDynamic(client)
        self.policy_lookup = PolicyLookup(client)
        self.saas_application = SaasApplication(client)
        self.sdn_connector_filters = SdnConnectorFilters(client)
        self.sessions = Sessions(client)
        self.uuid_list = UuidList(client)
        self.uuid_type_lookup = UuidTypeLookup(client)
        self.vip_overlap = VipOverlap(client)
