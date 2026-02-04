"""FortiOS CMDB - Hotspot20 category"""

from .anqp_3gpp_cellular import Anqp3gppCellular
from .anqp_ip_address_type import AnqpIpAddressType
from .anqp_nai_realm import AnqpNaiRealm
from .anqp_network_auth_type import AnqpNetworkAuthType
from .anqp_roaming_consortium import AnqpRoamingConsortium
from .anqp_venue_name import AnqpVenueName
from .anqp_venue_url import AnqpVenueUrl
from .h2qp_advice_of_charge import H2qpAdviceOfCharge
from .h2qp_conn_capability import H2qpConnCapability
from .h2qp_operator_name import H2qpOperatorName
from .h2qp_osu_provider import H2qpOsuProvider
from .h2qp_osu_provider_nai import H2qpOsuProviderNai
from .h2qp_terms_and_conditions import H2qpTermsAndConditions
from .h2qp_wan_metric import H2qpWanMetric
from .hs_profile import HsProfile
from .icon import Icon
from .qos_map import QosMap

__all__ = [
    "Anqp3gppCellular",
    "AnqpIpAddressType",
    "AnqpNaiRealm",
    "AnqpNetworkAuthType",
    "AnqpRoamingConsortium",
    "AnqpVenueName",
    "AnqpVenueUrl",
    "H2qpAdviceOfCharge",
    "H2qpConnCapability",
    "H2qpOperatorName",
    "H2qpOsuProvider",
    "H2qpOsuProviderNai",
    "H2qpTermsAndConditions",
    "H2qpWanMetric",
    "Hotspot20",
    "HsProfile",
    "Icon",
    "QosMap",
]


class Hotspot20:
    """Hotspot20 endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Hotspot20 endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.anqp_3gpp_cellular = Anqp3gppCellular(client)
        self.anqp_ip_address_type = AnqpIpAddressType(client)
        self.anqp_nai_realm = AnqpNaiRealm(client)
        self.anqp_network_auth_type = AnqpNetworkAuthType(client)
        self.anqp_roaming_consortium = AnqpRoamingConsortium(client)
        self.anqp_venue_name = AnqpVenueName(client)
        self.anqp_venue_url = AnqpVenueUrl(client)
        self.h2qp_advice_of_charge = H2qpAdviceOfCharge(client)
        self.h2qp_conn_capability = H2qpConnCapability(client)
        self.h2qp_operator_name = H2qpOperatorName(client)
        self.h2qp_osu_provider = H2qpOsuProvider(client)
        self.h2qp_osu_provider_nai = H2qpOsuProviderNai(client)
        self.h2qp_terms_and_conditions = H2qpTermsAndConditions(client)
        self.h2qp_wan_metric = H2qpWanMetric(client)
        self.hs_profile = HsProfile(client)
        self.icon = Icon(client)
        self.qos_map = QosMap(client)
