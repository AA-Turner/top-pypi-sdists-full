from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.node_disk_driver_enum import NodeDiskDriverEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ip_mapping import IPMapping


T = TypeVar("T", bound="MergedSecretOptions")


@_attrs_define
class MergedSecretOptions:
    """
    Attributes:
        heappe_cluster_password (Union[Unset, str]): HEAppE cluster password
        heappe_password (Union[Unset, str]): HEAppE password
        ipv4_external_ip_mapping (Union[Unset, list['IPMapping']]): OpenStack IPv4 external IP mapping
        openstack_api_tls_certificate (Union[Unset, str]): TLS certificate for OpenStack API connection verification
        dns_nameservers (Union[Unset, list[str]]): Default value for new subnets DNS name servers. Should be defined as
            list.
        shared_user_password (Union[Unset, str]): GLAuth shared user password
        template_confirmation_comment (Union[Unset, str]): Template confirmation comment
        language (Union[Unset, str]): Script language: Python or Bash
        environ (Union[Unset, Any]): Script environment variables
        create (Union[Unset, str]): Script for resource creation
        terminate (Union[Unset, str]): Script for resource termination
        update (Union[Unset, str]): Script for resource update
        pull (Union[Unset, str]): Script for regular resource pull
        api_url (Union[Unset, str]): API URL
        token (Union[Unset, str]): Waldur access token
        customer_uuid (Union[Unset, str]): Organization UUID
        backend_url (Union[Unset, str]):
        username (Union[Unset, str]):
        password (Union[Unset, str]):
        cloud_init_template (Union[Unset, str]): Cloud-init template for Rancher cluster node initialization
        managed_rancher_load_balancer_cloud_init_template (Union[Unset, str]): Cloud-init template for managed Rancher
            load balancer initialization
        vault_host (Union[Unset, str]): Host of the Vault server
        vault_port (Union[Unset, int]): Port of the Vault server
        vault_token (Union[Unset, str]): Token for the Vault server
        vault_tls_verify (Union[Unset, bool]): Whether to verify the Vault server certificate
        keycloak_url (Union[Unset, str]): URL of the Keycloak server
        keycloak_realm (Union[Unset, str]): Keycloak realm for Rancher
        keycloak_user_realm (Union[Unset, str]): Keycloak user realm for auth
        keycloak_username (Union[Unset, str]): Username of the Keycloak integration user
        keycloak_password (Union[Unset, str]): Password of the Keycloak integration user
        keycloak_sync_frequency (Union[Unset, int]): Frequency in minutes for syncing Keycloak users
        keycloak_ssl_verify (Union[Unset, bool]): Indicates whether verify SSL certificates
        argocd_k8s_namespace (Union[Unset, str]): Namespace where ArgoCD is deployed
        argocd_k8s_kubeconfig (Union[Unset, str]): Kubeconfig with access to namespace where ArgoCD is deployed
        base_image_name (Union[Unset, str]): Base image name
        private_registry_url (Union[Unset, str]): URL of a private registry for a cluster
        private_registry_user (Union[Unset, str]): Username for accessing a private registry
        private_registry_password (Union[Unset, str]): Password for accessing a private registry
        k8s_version (Union[Unset, str]): Kubernetes version
        node_disk_driver (Union[Unset, NodeDiskDriverEnum]):
    """

    heappe_cluster_password: Union[Unset, str] = UNSET
    heappe_password: Union[Unset, str] = UNSET
    ipv4_external_ip_mapping: Union[Unset, list["IPMapping"]] = UNSET
    openstack_api_tls_certificate: Union[Unset, str] = UNSET
    dns_nameservers: Union[Unset, list[str]] = UNSET
    shared_user_password: Union[Unset, str] = UNSET
    template_confirmation_comment: Union[Unset, str] = UNSET
    language: Union[Unset, str] = UNSET
    environ: Union[Unset, Any] = UNSET
    create: Union[Unset, str] = UNSET
    terminate: Union[Unset, str] = UNSET
    update: Union[Unset, str] = UNSET
    pull: Union[Unset, str] = UNSET
    api_url: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    customer_uuid: Union[Unset, str] = UNSET
    backend_url: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    cloud_init_template: Union[Unset, str] = UNSET
    managed_rancher_load_balancer_cloud_init_template: Union[Unset, str] = UNSET
    vault_host: Union[Unset, str] = UNSET
    vault_port: Union[Unset, int] = UNSET
    vault_token: Union[Unset, str] = UNSET
    vault_tls_verify: Union[Unset, bool] = UNSET
    keycloak_url: Union[Unset, str] = UNSET
    keycloak_realm: Union[Unset, str] = UNSET
    keycloak_user_realm: Union[Unset, str] = UNSET
    keycloak_username: Union[Unset, str] = UNSET
    keycloak_password: Union[Unset, str] = UNSET
    keycloak_sync_frequency: Union[Unset, int] = UNSET
    keycloak_ssl_verify: Union[Unset, bool] = UNSET
    argocd_k8s_namespace: Union[Unset, str] = UNSET
    argocd_k8s_kubeconfig: Union[Unset, str] = UNSET
    base_image_name: Union[Unset, str] = UNSET
    private_registry_url: Union[Unset, str] = UNSET
    private_registry_user: Union[Unset, str] = UNSET
    private_registry_password: Union[Unset, str] = UNSET
    k8s_version: Union[Unset, str] = UNSET
    node_disk_driver: Union[Unset, NodeDiskDriverEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        heappe_cluster_password = self.heappe_cluster_password

        heappe_password = self.heappe_password

        ipv4_external_ip_mapping: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ipv4_external_ip_mapping, Unset):
            ipv4_external_ip_mapping = []
            for ipv4_external_ip_mapping_item_data in self.ipv4_external_ip_mapping:
                ipv4_external_ip_mapping_item = ipv4_external_ip_mapping_item_data.to_dict()
                ipv4_external_ip_mapping.append(ipv4_external_ip_mapping_item)

        openstack_api_tls_certificate = self.openstack_api_tls_certificate

        dns_nameservers: Union[Unset, list[str]] = UNSET
        if not isinstance(self.dns_nameservers, Unset):
            dns_nameservers = self.dns_nameservers

        shared_user_password = self.shared_user_password

        template_confirmation_comment = self.template_confirmation_comment

        language = self.language

        environ = self.environ

        create = self.create

        terminate = self.terminate

        update = self.update

        pull = self.pull

        api_url = self.api_url

        token = self.token

        customer_uuid = self.customer_uuid

        backend_url = self.backend_url

        username = self.username

        password = self.password

        cloud_init_template = self.cloud_init_template

        managed_rancher_load_balancer_cloud_init_template = self.managed_rancher_load_balancer_cloud_init_template

        vault_host = self.vault_host

        vault_port = self.vault_port

        vault_token = self.vault_token

        vault_tls_verify = self.vault_tls_verify

        keycloak_url = self.keycloak_url

        keycloak_realm = self.keycloak_realm

        keycloak_user_realm = self.keycloak_user_realm

        keycloak_username = self.keycloak_username

        keycloak_password = self.keycloak_password

        keycloak_sync_frequency = self.keycloak_sync_frequency

        keycloak_ssl_verify = self.keycloak_ssl_verify

        argocd_k8s_namespace = self.argocd_k8s_namespace

        argocd_k8s_kubeconfig = self.argocd_k8s_kubeconfig

        base_image_name = self.base_image_name

        private_registry_url = self.private_registry_url

        private_registry_user = self.private_registry_user

        private_registry_password = self.private_registry_password

        k8s_version = self.k8s_version

        node_disk_driver: Union[Unset, str] = UNSET
        if not isinstance(self.node_disk_driver, Unset):
            node_disk_driver = self.node_disk_driver.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if heappe_cluster_password is not UNSET:
            field_dict["heappe_cluster_password"] = heappe_cluster_password
        if heappe_password is not UNSET:
            field_dict["heappe_password"] = heappe_password
        if ipv4_external_ip_mapping is not UNSET:
            field_dict["ipv4_external_ip_mapping"] = ipv4_external_ip_mapping
        if openstack_api_tls_certificate is not UNSET:
            field_dict["openstack_api_tls_certificate"] = openstack_api_tls_certificate
        if dns_nameservers is not UNSET:
            field_dict["dns_nameservers"] = dns_nameservers
        if shared_user_password is not UNSET:
            field_dict["shared_user_password"] = shared_user_password
        if template_confirmation_comment is not UNSET:
            field_dict["template_confirmation_comment"] = template_confirmation_comment
        if language is not UNSET:
            field_dict["language"] = language
        if environ is not UNSET:
            field_dict["environ"] = environ
        if create is not UNSET:
            field_dict["create"] = create
        if terminate is not UNSET:
            field_dict["terminate"] = terminate
        if update is not UNSET:
            field_dict["update"] = update
        if pull is not UNSET:
            field_dict["pull"] = pull
        if api_url is not UNSET:
            field_dict["api_url"] = api_url
        if token is not UNSET:
            field_dict["token"] = token
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if backend_url is not UNSET:
            field_dict["backend_url"] = backend_url
        if username is not UNSET:
            field_dict["username"] = username
        if password is not UNSET:
            field_dict["password"] = password
        if cloud_init_template is not UNSET:
            field_dict["cloud_init_template"] = cloud_init_template
        if managed_rancher_load_balancer_cloud_init_template is not UNSET:
            field_dict["managed_rancher_load_balancer_cloud_init_template"] = (
                managed_rancher_load_balancer_cloud_init_template
            )
        if vault_host is not UNSET:
            field_dict["vault_host"] = vault_host
        if vault_port is not UNSET:
            field_dict["vault_port"] = vault_port
        if vault_token is not UNSET:
            field_dict["vault_token"] = vault_token
        if vault_tls_verify is not UNSET:
            field_dict["vault_tls_verify"] = vault_tls_verify
        if keycloak_url is not UNSET:
            field_dict["keycloak_url"] = keycloak_url
        if keycloak_realm is not UNSET:
            field_dict["keycloak_realm"] = keycloak_realm
        if keycloak_user_realm is not UNSET:
            field_dict["keycloak_user_realm"] = keycloak_user_realm
        if keycloak_username is not UNSET:
            field_dict["keycloak_username"] = keycloak_username
        if keycloak_password is not UNSET:
            field_dict["keycloak_password"] = keycloak_password
        if keycloak_sync_frequency is not UNSET:
            field_dict["keycloak_sync_frequency"] = keycloak_sync_frequency
        if keycloak_ssl_verify is not UNSET:
            field_dict["keycloak_ssl_verify"] = keycloak_ssl_verify
        if argocd_k8s_namespace is not UNSET:
            field_dict["argocd_k8s_namespace"] = argocd_k8s_namespace
        if argocd_k8s_kubeconfig is not UNSET:
            field_dict["argocd_k8s_kubeconfig"] = argocd_k8s_kubeconfig
        if base_image_name is not UNSET:
            field_dict["base_image_name"] = base_image_name
        if private_registry_url is not UNSET:
            field_dict["private_registry_url"] = private_registry_url
        if private_registry_user is not UNSET:
            field_dict["private_registry_user"] = private_registry_user
        if private_registry_password is not UNSET:
            field_dict["private_registry_password"] = private_registry_password
        if k8s_version is not UNSET:
            field_dict["k8s_version"] = k8s_version
        if node_disk_driver is not UNSET:
            field_dict["node_disk_driver"] = node_disk_driver

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ip_mapping import IPMapping

        d = dict(src_dict)
        heappe_cluster_password = d.pop("heappe_cluster_password", UNSET)

        heappe_password = d.pop("heappe_password", UNSET)

        ipv4_external_ip_mapping = []
        _ipv4_external_ip_mapping = d.pop("ipv4_external_ip_mapping", UNSET)
        for ipv4_external_ip_mapping_item_data in _ipv4_external_ip_mapping or []:
            ipv4_external_ip_mapping_item = IPMapping.from_dict(ipv4_external_ip_mapping_item_data)

            ipv4_external_ip_mapping.append(ipv4_external_ip_mapping_item)

        openstack_api_tls_certificate = d.pop("openstack_api_tls_certificate", UNSET)

        dns_nameservers = cast(list[str], d.pop("dns_nameservers", UNSET))

        shared_user_password = d.pop("shared_user_password", UNSET)

        template_confirmation_comment = d.pop("template_confirmation_comment", UNSET)

        language = d.pop("language", UNSET)

        environ = d.pop("environ", UNSET)

        create = d.pop("create", UNSET)

        terminate = d.pop("terminate", UNSET)

        update = d.pop("update", UNSET)

        pull = d.pop("pull", UNSET)

        api_url = d.pop("api_url", UNSET)

        token = d.pop("token", UNSET)

        customer_uuid = d.pop("customer_uuid", UNSET)

        backend_url = d.pop("backend_url", UNSET)

        username = d.pop("username", UNSET)

        password = d.pop("password", UNSET)

        cloud_init_template = d.pop("cloud_init_template", UNSET)

        managed_rancher_load_balancer_cloud_init_template = d.pop(
            "managed_rancher_load_balancer_cloud_init_template", UNSET
        )

        vault_host = d.pop("vault_host", UNSET)

        vault_port = d.pop("vault_port", UNSET)

        vault_token = d.pop("vault_token", UNSET)

        vault_tls_verify = d.pop("vault_tls_verify", UNSET)

        keycloak_url = d.pop("keycloak_url", UNSET)

        keycloak_realm = d.pop("keycloak_realm", UNSET)

        keycloak_user_realm = d.pop("keycloak_user_realm", UNSET)

        keycloak_username = d.pop("keycloak_username", UNSET)

        keycloak_password = d.pop("keycloak_password", UNSET)

        keycloak_sync_frequency = d.pop("keycloak_sync_frequency", UNSET)

        keycloak_ssl_verify = d.pop("keycloak_ssl_verify", UNSET)

        argocd_k8s_namespace = d.pop("argocd_k8s_namespace", UNSET)

        argocd_k8s_kubeconfig = d.pop("argocd_k8s_kubeconfig", UNSET)

        base_image_name = d.pop("base_image_name", UNSET)

        private_registry_url = d.pop("private_registry_url", UNSET)

        private_registry_user = d.pop("private_registry_user", UNSET)

        private_registry_password = d.pop("private_registry_password", UNSET)

        k8s_version = d.pop("k8s_version", UNSET)

        _node_disk_driver = d.pop("node_disk_driver", UNSET)
        node_disk_driver: Union[Unset, NodeDiskDriverEnum]
        if isinstance(_node_disk_driver, Unset):
            node_disk_driver = UNSET
        else:
            node_disk_driver = NodeDiskDriverEnum(_node_disk_driver)

        merged_secret_options = cls(
            heappe_cluster_password=heappe_cluster_password,
            heappe_password=heappe_password,
            ipv4_external_ip_mapping=ipv4_external_ip_mapping,
            openstack_api_tls_certificate=openstack_api_tls_certificate,
            dns_nameservers=dns_nameservers,
            shared_user_password=shared_user_password,
            template_confirmation_comment=template_confirmation_comment,
            language=language,
            environ=environ,
            create=create,
            terminate=terminate,
            update=update,
            pull=pull,
            api_url=api_url,
            token=token,
            customer_uuid=customer_uuid,
            backend_url=backend_url,
            username=username,
            password=password,
            cloud_init_template=cloud_init_template,
            managed_rancher_load_balancer_cloud_init_template=managed_rancher_load_balancer_cloud_init_template,
            vault_host=vault_host,
            vault_port=vault_port,
            vault_token=vault_token,
            vault_tls_verify=vault_tls_verify,
            keycloak_url=keycloak_url,
            keycloak_realm=keycloak_realm,
            keycloak_user_realm=keycloak_user_realm,
            keycloak_username=keycloak_username,
            keycloak_password=keycloak_password,
            keycloak_sync_frequency=keycloak_sync_frequency,
            keycloak_ssl_verify=keycloak_ssl_verify,
            argocd_k8s_namespace=argocd_k8s_namespace,
            argocd_k8s_kubeconfig=argocd_k8s_kubeconfig,
            base_image_name=base_image_name,
            private_registry_url=private_registry_url,
            private_registry_user=private_registry_user,
            private_registry_password=private_registry_password,
            k8s_version=k8s_version,
            node_disk_driver=node_disk_driver,
        )

        merged_secret_options.additional_properties = d
        return merged_secret_options

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
