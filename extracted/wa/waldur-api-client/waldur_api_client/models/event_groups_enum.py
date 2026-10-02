from enum import Enum


class EventGroupsEnum(str, Enum):
    ACCESS_SUBNETS = "access_subnets"
    AUTH = "auth"
    CALL = "call"
    CHAT = "chat"
    CREDITS = "credits"
    CUSTOMERS = "customers"
    INVOICES = "invoices"
    OFFERING_ACCOUNTING = "offering_accounting"
    ONBOARDING = "onboarding"
    OPENSTACK_FLOATING_IP = "openstack_floating_ip"
    OPENSTACK_NETWORK = "openstack_network"
    OPENSTACK_PORT = "openstack_port"
    OPENSTACK_RBAC = "openstack_rbac"
    OPENSTACK_ROUTER = "openstack_router"
    OPENSTACK_SECURITY_GROUP = "openstack_security_group"
    OPENSTACK_SUBNET = "openstack_subnet"
    PERMISSIONS = "permissions"
    PROJECTS = "projects"
    PROPOSAL = "proposal"
    PROVIDERS = "providers"
    RESOURCES = "resources"
    REVIEW = "review"
    SSH = "ssh"
    SUPPORT = "support"
    TERMS_OF_SERVICE = "terms_of_service"
    USERS = "users"

    def __str__(self) -> str:
        return str(self.value)
