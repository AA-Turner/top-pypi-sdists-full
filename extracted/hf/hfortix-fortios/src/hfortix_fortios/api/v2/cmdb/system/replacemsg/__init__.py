"""FortiOS CMDB - Replacemsg category"""

from .admin import Admin
from .alertmail import Alertmail
from .auth import Auth
from .automation import Automation
from .fortiguard_wf import FortiguardWf
from .http import Http
from .mail import Mail
from .nac_quar import NacQuar
from .spam import Spam
from .sslvpn import Sslvpn
from .traffic_quota import TrafficQuota
from .utm import Utm

__all__ = [
    "Admin",
    "Alertmail",
    "Auth",
    "Automation",
    "FortiguardWf",
    "Http",
    "Mail",
    "NacQuar",
    "Replacemsg",
    "Spam",
    "Sslvpn",
    "TrafficQuota",
    "Utm",
]


class Replacemsg:
    """Replacemsg endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Replacemsg endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.admin = Admin(client)
        self.alertmail = Alertmail(client)
        self.auth = Auth(client)
        self.automation = Automation(client)
        self.fortiguard_wf = FortiguardWf(client)
        self.http = Http(client)
        self.mail = Mail(client)
        self.nac_quar = NacQuar(client)
        self.spam = Spam(client)
        self.sslvpn = Sslvpn(client)
        self.traffic_quota = TrafficQuota(client)
        self.utm = Utm(client)
