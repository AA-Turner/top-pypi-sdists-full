import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Cloud(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def virtual_machines(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/endpoints/virtual-machines", sn=self.sn)

    @computed_field
    @property
    def virtual_machines_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/endpoints/virtual-machines-interfaces", sn=self.sn)

    @computed_field
    @property
    def endpoint_groups(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/endpoints/endpoint-groups", sn=self.sn)

    @computed_field
    @property
    def private_link_endpoints(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/private-link/endpoints", sn=self.sn)

    @computed_field
    @property
    def private_link_services_connections(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/private-link/services/connections", sn=self.sn)

    @computed_field
    @property
    def private_link_services_inventory(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/private-link/services/inventory", sn=self.sn)

    @computed_field
    @property
    def public_ips_ipv4_addresses(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/public-ips/ipv4-addresses", sn=self.sn)

    @computed_field
    @property
    def public_ips_ipv6_addresses(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/public-ips/ipv6-addresses", sn=self.sn)

    @computed_field
    @property
    def subnets_inventory(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/subnets/inventory", sn=self.sn)

    @computed_field
    @property
    def aws_inventory(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/aws/inventory", sn=self.sn)

    @computed_field
    @property
    def aws_private_link_vpc_endpoints(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/aws/private-link/vpc-endpoints", sn=self.sn)

    @computed_field
    @property
    def aws_scaling_groups(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/aws/scaling-groups", sn=self.sn)

    @computed_field
    @property
    def aws_subnets(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/aws/subnets", sn=self.sn)

    @computed_field
    @property
    def azure_inventory(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/azure/inventory", sn=self.sn)

    @computed_field
    @property
    def azure_private_link_connections(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/azure/private-link/connections", sn=self.sn)

    @computed_field
    @property
    def azure_private_link_endpoints(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/azure/private-link/endpoints", sn=self.sn)

    @computed_field
    @property
    def azure_private_link_services(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/azure/private-link/services", sn=self.sn)

    @computed_field
    @property
    def azure_service_endpoints(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/azure/service-endpoints", sn=self.sn)

    @computed_field
    @property
    def azure_subnets(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/azure/subnets", sn=self.sn)

    @computed_field
    @property
    def azure_virtual_machine_scale_sets(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/azure/virtual-machine-scale-sets", sn=self.sn)

    @computed_field
    @property
    def azure_vnet_integration_app_services(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/cloud/vendors/azure/vnet-integration/app-services", sn=self.sn
        )

    @computed_field
    @property
    def azure_vnet_integration_container_apps(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/cloud/vendors/azure/vnet-integration/container-apps", sn=self.sn
        )

    @computed_field
    @property
    def azure_vnet_integration_flexible_servers(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/cloud/vendors/azure/vnet-integration/flexible-servers", sn=self.sn
        )

    @computed_field
    @property
    def azure_vnet_integration_sql_managed_instances(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/cloud/vendors/azure/vnet-integration/sql-managed-instances", sn=self.sn
        )

    @computed_field
    @property
    def azure_dns_forwarding_rules(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/azure/dns/forwarding-rules", sn=self.sn)

    @computed_field
    @property
    def azure_dns_forwarding_rulesets(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/azure/dns/forwarding-rulesets", sn=self.sn)

    @computed_field
    @property
    def azure_dns_private_resolvers(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/azure/dns/private-resolvers", sn=self.sn)

    @computed_field
    @property
    def azure_dns_private_resolvers_endpoints(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/cloud/vendors/azure/dns/private-resolvers-endpoints", sn=self.sn
        )

    @computed_field
    @property
    def azure_dns_vnet(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/azure/dns/vnet", sn=self.sn)

    @computed_field
    @property
    def gcp_inventory(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/gcp/inventory", sn=self.sn)

    @computed_field
    @property
    def gcp_instance_network_endpoint_groups(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/cloud/vendors/gcp/instance-network-endpoint-groups", sn=self.sn
        )

    @computed_field
    @property
    def gcp_private_service_connect_endpoints(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/cloud/vendors/gcp/private-service-connect/endpoints", sn=self.sn
        )

    @computed_field
    @property
    def gcp_private_service_connect_published_services(self) -> Table:
        return Table(
            client=self.client,
            endpoint="tables/cloud/vendors/gcp/private-service-connect/published-services",
            sn=self.sn,
        )

    @computed_field
    @property
    def gcp_private_service_connect_published_services_connections(self) -> Table:
        return Table(
            client=self.client,
            endpoint="tables/cloud/vendors/gcp/private-service-connect/published-services-connections",
            sn=self.sn,
        )

    @computed_field
    @property
    def gcp_subnets(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/gcp/subnets", sn=self.sn)

    @computed_field
    @property
    def gcp_serverless_services_app_engine(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/gcp/serverless-services/app-engine", sn=self.sn)

    @computed_field
    @property
    def gcp_serverless_services_cloud_functions(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/cloud/vendors/gcp/serverless-services/cloud-functions", sn=self.sn
        )

    @computed_field
    @property
    def gcp_serverless_services_cloud_run(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/gcp/serverless-services/cloud-run", sn=self.sn)

    @computed_field
    @property
    def inventory(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/nodes/inventory", sn=self.sn)

    @computed_field
    @property
    def tags(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/nodes/tags", sn=self.sn)
