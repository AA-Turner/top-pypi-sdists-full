import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Management(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def aaa_servers(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/aaa/servers", sn=self.sn)

    @computed_field
    @property
    def aaa_lines(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/aaa/lines", sn=self.sn)

    @computed_field
    @property
    def aaa_authentication(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/aaa/authentication", sn=self.sn)

    @computed_field
    @property
    def aaa_authorization(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/aaa/authorization", sn=self.sn)

    @computed_field
    @property
    def aaa_accounting(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/aaa/accounting", sn=self.sn)

    @computed_field
    @property
    def aaa_users(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/aaa/users", sn=self.sn)

    @computed_field
    @property
    def aaa_password_strength(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/aaa/password-strength", sn=self.sn)

    @computed_field
    @property
    def telnet_access(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/enabled-telnet", sn=self.sn)

    @computed_field
    @property
    def saved_config_consistency(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/configuration/saved", sn=self.sn)

    @computed_field
    @property
    def ntp_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/ntp/summary", sn=self.sn)

    @computed_field
    @property
    def ntp_sources(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/ntp/sources", sn=self.sn)

    @computed_field
    @property
    def port_mirroring(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/port-mirroring", sn=self.sn)

    @computed_field
    @property
    def logging_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/logging/summary", sn=self.sn)

    @computed_field
    @property
    def logging_remote(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/logging/remote", sn=self.sn)

    @computed_field
    @property
    def logging_local(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/logging/local", sn=self.sn)

    @computed_field
    @property
    def flow_overview(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/flow/overview", sn=self.sn)

    @computed_field
    @property
    def netflow_devices(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/flow/netflow/devices", sn=self.sn)

    @computed_field
    @property
    def netflow_collectors(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/flow/netflow/collectors", sn=self.sn)

    @computed_field
    @property
    def netflow_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/flow/netflow/interfaces", sn=self.sn)

    @computed_field
    @property
    def sflow_devices(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/flow/sflow/devices", sn=self.sn)

    @computed_field
    @property
    def sflow_collectors(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/flow/sflow/collectors", sn=self.sn)

    @computed_field
    @property
    def sflow_sources(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/flow/sflow/sources", sn=self.sn)

    @computed_field
    @property
    def snmp_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/snmp/summary", sn=self.sn)

    @computed_field
    @property
    def snmp_communities(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/snmp/communities", sn=self.sn)

    @computed_field
    @property
    def snmp_trap_hosts(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/snmp/trap-hosts", sn=self.sn)

    @computed_field
    @property
    def snmp_users(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/snmp/users", sn=self.sn)

    @computed_field
    @property
    def ptp_local_clock(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/ptp/local-clock", sn=self.sn)

    @computed_field
    @property
    def ptp_masters(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/ptp/masters", sn=self.sn)

    @computed_field
    @property
    def ptp_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/ptp/interfaces", sn=self.sn)

    @computed_field
    @property
    def license_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/licenses/summary", sn=self.sn)

    @computed_field
    @property
    def licenses(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/licenses", sn=self.sn)

    @computed_field
    @property
    def licenses_detail(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/licenses/detail", sn=self.sn)

    @computed_field
    @property
    def cisco_smart_licenses_authorization(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/management/licenses/cisco-smart-licenses/authorization", sn=self.sn
        )

    @computed_field
    @property
    def cisco_smart_licenses_registration(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/management/licenses/cisco-smart-licenses/registration", sn=self.sn
        )

    @computed_field
    @property
    def cisco_smart_licenses_reservations(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/management/licenses/cisco-smart-licenses/reservations", sn=self.sn
        )

    @computed_field
    @property
    def dns_resolver_settings(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/dns/settings", sn=self.sn)

    @computed_field
    @property
    def dns_resolver_servers(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/dns/servers", sn=self.sn)

    @computed_field
    @property
    def banners_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/banners/summary", sn=self.sn)

    @computed_field
    @property
    def banners_detail(self) -> Table:
        return Table(client=self.client, endpoint="tables/management/banners/banners", sn=self.sn)
