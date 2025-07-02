r'''
# `azurerm_api_management`

Refer to the Terraform Registry for docs: [`azurerm_api_management`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ApiManagement(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagement",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management azurerm_api_management}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        publisher_email: builtins.str,
        publisher_name: builtins.str,
        resource_group_name: builtins.str,
        sku_name: builtins.str,
        additional_location: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementAdditionalLocation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delegation: typing.Optional[typing.Union["ApiManagementDelegation", typing.Dict[builtins.str, typing.Any]]] = None,
        gateway_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hostname_configuration: typing.Optional[typing.Union["ApiManagementHostnameConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ApiManagementIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        min_api_version: typing.Optional[builtins.str] = None,
        notification_sender_email: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.Union["ApiManagementProtocols", typing.Dict[builtins.str, typing.Any]]] = None,
        public_ip_address_id: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security: typing.Optional[typing.Union["ApiManagementSecurity", typing.Dict[builtins.str, typing.Any]]] = None,
        sign_in: typing.Optional[typing.Union["ApiManagementSignIn", typing.Dict[builtins.str, typing.Any]]] = None,
        sign_up: typing.Optional[typing.Union["ApiManagementSignUp", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenant_access: typing.Optional[typing.Union["ApiManagementTenantAccess", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_network_configuration: typing.Optional[typing.Union["ApiManagementVirtualNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_network_type: typing.Optional[builtins.str] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management azurerm_api_management} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#location ApiManagement#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#name ApiManagement#name}.
        :param publisher_email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#publisher_email ApiManagement#publisher_email}.
        :param publisher_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#publisher_name ApiManagement#publisher_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#resource_group_name ApiManagement#resource_group_name}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#sku_name ApiManagement#sku_name}.
        :param additional_location: additional_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#additional_location ApiManagement#additional_location}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate ApiManagement#certificate}
        :param client_certificate_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#client_certificate_enabled ApiManagement#client_certificate_enabled}.
        :param delegation: delegation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#delegation ApiManagement#delegation}
        :param gateway_disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#gateway_disabled ApiManagement#gateway_disabled}.
        :param hostname_configuration: hostname_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#hostname_configuration ApiManagement#hostname_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#id ApiManagement#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#identity ApiManagement#identity}
        :param min_api_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#min_api_version ApiManagement#min_api_version}.
        :param notification_sender_email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#notification_sender_email ApiManagement#notification_sender_email}.
        :param protocols: protocols block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#protocols ApiManagement#protocols}
        :param public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#public_ip_address_id ApiManagement#public_ip_address_id}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#public_network_access_enabled ApiManagement#public_network_access_enabled}.
        :param security: security block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#security ApiManagement#security}
        :param sign_in: sign_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#sign_in ApiManagement#sign_in}
        :param sign_up: sign_up block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#sign_up ApiManagement#sign_up}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tags ApiManagement#tags}.
        :param tenant_access: tenant_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tenant_access ApiManagement#tenant_access}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#timeouts ApiManagement#timeouts}
        :param virtual_network_configuration: virtual_network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#virtual_network_configuration ApiManagement#virtual_network_configuration}
        :param virtual_network_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#virtual_network_type ApiManagement#virtual_network_type}.
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#zones ApiManagement#zones}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b44d5684af6ef2c0057f2a29ff838cd55231aae6302954de3c78b9f0bf9c202)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApiManagementConfig(
            location=location,
            name=name,
            publisher_email=publisher_email,
            publisher_name=publisher_name,
            resource_group_name=resource_group_name,
            sku_name=sku_name,
            additional_location=additional_location,
            certificate=certificate,
            client_certificate_enabled=client_certificate_enabled,
            delegation=delegation,
            gateway_disabled=gateway_disabled,
            hostname_configuration=hostname_configuration,
            id=id,
            identity=identity,
            min_api_version=min_api_version,
            notification_sender_email=notification_sender_email,
            protocols=protocols,
            public_ip_address_id=public_ip_address_id,
            public_network_access_enabled=public_network_access_enabled,
            security=security,
            sign_in=sign_in,
            sign_up=sign_up,
            tags=tags,
            tenant_access=tenant_access,
            timeouts=timeouts,
            virtual_network_configuration=virtual_network_configuration,
            virtual_network_type=virtual_network_type,
            zones=zones,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ApiManagement resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApiManagement to import.
        :param import_from_id: The id of the existing ApiManagement that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApiManagement to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc547e6824dddbfce14726f08678f4744eeb5b6b9286f72a52b9487f87ff39e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdditionalLocation")
    def put_additional_location(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementAdditionalLocation", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3346c7ddc80d7f5f07dc48e412c3e28751de7323cf1c05927705bc5f19a3ef30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalLocation", [value]))

    @jsii.member(jsii_name="putCertificate")
    def put_certificate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCertificate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a3ccca5fc530272d561fedd22e250b0fa35f6f6f5a525f2ec7db0327ea705d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCertificate", [value]))

    @jsii.member(jsii_name="putDelegation")
    def put_delegation(
        self,
        *,
        subscriptions_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        url: typing.Optional[builtins.str] = None,
        user_registration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        validation_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subscriptions_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#subscriptions_enabled ApiManagement#subscriptions_enabled}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#url ApiManagement#url}.
        :param user_registration_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#user_registration_enabled ApiManagement#user_registration_enabled}.
        :param validation_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#validation_key ApiManagement#validation_key}.
        '''
        value = ApiManagementDelegation(
            subscriptions_enabled=subscriptions_enabled,
            url=url,
            user_registration_enabled=user_registration_enabled,
            validation_key=validation_key,
        )

        return typing.cast(None, jsii.invoke(self, "putDelegation", [value]))

    @jsii.member(jsii_name="putHostnameConfiguration")
    def put_hostname_configuration(
        self,
        *,
        developer_portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementHostnameConfigurationDeveloperPortal", typing.Dict[builtins.str, typing.Any]]]]] = None,
        management: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementHostnameConfigurationManagement", typing.Dict[builtins.str, typing.Any]]]]] = None,
        portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementHostnameConfigurationPortal", typing.Dict[builtins.str, typing.Any]]]]] = None,
        proxy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementHostnameConfigurationProxy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementHostnameConfigurationScm", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param developer_portal: developer_portal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#developer_portal ApiManagement#developer_portal}
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#management ApiManagement#management}
        :param portal: portal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#portal ApiManagement#portal}
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#proxy ApiManagement#proxy}
        :param scm: scm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#scm ApiManagement#scm}
        '''
        value = ApiManagementHostnameConfiguration(
            developer_portal=developer_portal,
            management=management,
            portal=portal,
            proxy=proxy,
            scm=scm,
        )

        return typing.cast(None, jsii.invoke(self, "putHostnameConfiguration", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#type ApiManagement#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#identity_ids ApiManagement#identity_ids}.
        '''
        value = ApiManagementIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putProtocols")
    def put_protocols(
        self,
        *,
        enable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_http2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_http2 ApiManagement#enable_http2}.
        :param http2_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#http2_enabled ApiManagement#http2_enabled}.
        '''
        value = ApiManagementProtocols(
            enable_http2=enable_http2, http2_enabled=http2_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putProtocols", [value]))

    @jsii.member(jsii_name="putSecurity")
    def put_security(
        self,
        *,
        backend_ssl30_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backend_tls10_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backend_tls11_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_backend_ssl30: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_backend_tls10: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_backend_tls11: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_frontend_ssl30: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_frontend_tls10: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_frontend_tls11: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        frontend_ssl30_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        frontend_tls10_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        frontend_tls11_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_rsa_with_aes128_cbc_sha256_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_rsa_with_aes128_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_rsa_with_aes128_gcm_sha256_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_rsa_with_aes256_cbc_sha256_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_rsa_with_aes256_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_rsa_with_aes256_gcm_sha384_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        triple_des_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param backend_ssl30_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#backend_ssl30_enabled ApiManagement#backend_ssl30_enabled}.
        :param backend_tls10_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#backend_tls10_enabled ApiManagement#backend_tls10_enabled}.
        :param backend_tls11_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#backend_tls11_enabled ApiManagement#backend_tls11_enabled}.
        :param enable_backend_ssl30: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_backend_ssl30 ApiManagement#enable_backend_ssl30}.
        :param enable_backend_tls10: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_backend_tls10 ApiManagement#enable_backend_tls10}.
        :param enable_backend_tls11: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_backend_tls11 ApiManagement#enable_backend_tls11}.
        :param enable_frontend_ssl30: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_frontend_ssl30 ApiManagement#enable_frontend_ssl30}.
        :param enable_frontend_tls10: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_frontend_tls10 ApiManagement#enable_frontend_tls10}.
        :param enable_frontend_tls11: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_frontend_tls11 ApiManagement#enable_frontend_tls11}.
        :param frontend_ssl30_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#frontend_ssl30_enabled ApiManagement#frontend_ssl30_enabled}.
        :param frontend_tls10_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#frontend_tls10_enabled ApiManagement#frontend_tls10_enabled}.
        :param frontend_tls11_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#frontend_tls11_enabled ApiManagement#frontend_tls11_enabled}.
        :param tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled ApiManagement#tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled}.
        :param tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled ApiManagement#tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled}.
        :param tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled ApiManagement#tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled}.
        :param tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled ApiManagement#tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled}.
        :param tls_rsa_with_aes128_cbc_sha256_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes128_cbc_sha256_ciphers_enabled ApiManagement#tls_rsa_with_aes128_cbc_sha256_ciphers_enabled}.
        :param tls_rsa_with_aes128_cbc_sha_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes128_cbc_sha_ciphers_enabled ApiManagement#tls_rsa_with_aes128_cbc_sha_ciphers_enabled}.
        :param tls_rsa_with_aes128_gcm_sha256_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes128_gcm_sha256_ciphers_enabled ApiManagement#tls_rsa_with_aes128_gcm_sha256_ciphers_enabled}.
        :param tls_rsa_with_aes256_cbc_sha256_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes256_cbc_sha256_ciphers_enabled ApiManagement#tls_rsa_with_aes256_cbc_sha256_ciphers_enabled}.
        :param tls_rsa_with_aes256_cbc_sha_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes256_cbc_sha_ciphers_enabled ApiManagement#tls_rsa_with_aes256_cbc_sha_ciphers_enabled}.
        :param tls_rsa_with_aes256_gcm_sha384_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes256_gcm_sha384_ciphers_enabled ApiManagement#tls_rsa_with_aes256_gcm_sha384_ciphers_enabled}.
        :param triple_des_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#triple_des_ciphers_enabled ApiManagement#triple_des_ciphers_enabled}.
        '''
        value = ApiManagementSecurity(
            backend_ssl30_enabled=backend_ssl30_enabled,
            backend_tls10_enabled=backend_tls10_enabled,
            backend_tls11_enabled=backend_tls11_enabled,
            enable_backend_ssl30=enable_backend_ssl30,
            enable_backend_tls10=enable_backend_tls10,
            enable_backend_tls11=enable_backend_tls11,
            enable_frontend_ssl30=enable_frontend_ssl30,
            enable_frontend_tls10=enable_frontend_tls10,
            enable_frontend_tls11=enable_frontend_tls11,
            frontend_ssl30_enabled=frontend_ssl30_enabled,
            frontend_tls10_enabled=frontend_tls10_enabled,
            frontend_tls11_enabled=frontend_tls11_enabled,
            tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled=tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled,
            tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled=tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled,
            tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled=tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled,
            tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled=tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled,
            tls_rsa_with_aes128_cbc_sha256_ciphers_enabled=tls_rsa_with_aes128_cbc_sha256_ciphers_enabled,
            tls_rsa_with_aes128_cbc_sha_ciphers_enabled=tls_rsa_with_aes128_cbc_sha_ciphers_enabled,
            tls_rsa_with_aes128_gcm_sha256_ciphers_enabled=tls_rsa_with_aes128_gcm_sha256_ciphers_enabled,
            tls_rsa_with_aes256_cbc_sha256_ciphers_enabled=tls_rsa_with_aes256_cbc_sha256_ciphers_enabled,
            tls_rsa_with_aes256_cbc_sha_ciphers_enabled=tls_rsa_with_aes256_cbc_sha_ciphers_enabled,
            tls_rsa_with_aes256_gcm_sha384_ciphers_enabled=tls_rsa_with_aes256_gcm_sha384_ciphers_enabled,
            triple_des_ciphers_enabled=triple_des_ciphers_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putSecurity", [value]))

    @jsii.member(jsii_name="putSignIn")
    def put_sign_in(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enabled ApiManagement#enabled}.
        '''
        value = ApiManagementSignIn(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putSignIn", [value]))

    @jsii.member(jsii_name="putSignUp")
    def put_sign_up(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        terms_of_service: typing.Union["ApiManagementSignUpTermsOfService", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enabled ApiManagement#enabled}.
        :param terms_of_service: terms_of_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#terms_of_service ApiManagement#terms_of_service}
        '''
        value = ApiManagementSignUp(enabled=enabled, terms_of_service=terms_of_service)

        return typing.cast(None, jsii.invoke(self, "putSignUp", [value]))

    @jsii.member(jsii_name="putTenantAccess")
    def put_tenant_access(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enabled ApiManagement#enabled}.
        '''
        value = ApiManagementTenantAccess(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putTenantAccess", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#create ApiManagement#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#delete ApiManagement#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#read ApiManagement#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#update ApiManagement#update}.
        '''
        value = ApiManagementTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualNetworkConfiguration")
    def put_virtual_network_configuration(self, *, subnet_id: builtins.str) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#subnet_id ApiManagement#subnet_id}.
        '''
        value = ApiManagementVirtualNetworkConfiguration(subnet_id=subnet_id)

        return typing.cast(None, jsii.invoke(self, "putVirtualNetworkConfiguration", [value]))

    @jsii.member(jsii_name="resetAdditionalLocation")
    def reset_additional_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalLocation", []))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetClientCertificateEnabled")
    def reset_client_certificate_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateEnabled", []))

    @jsii.member(jsii_name="resetDelegation")
    def reset_delegation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelegation", []))

    @jsii.member(jsii_name="resetGatewayDisabled")
    def reset_gateway_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayDisabled", []))

    @jsii.member(jsii_name="resetHostnameConfiguration")
    def reset_hostname_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostnameConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetMinApiVersion")
    def reset_min_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinApiVersion", []))

    @jsii.member(jsii_name="resetNotificationSenderEmail")
    def reset_notification_sender_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationSenderEmail", []))

    @jsii.member(jsii_name="resetProtocols")
    def reset_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocols", []))

    @jsii.member(jsii_name="resetPublicIpAddressId")
    def reset_public_ip_address_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIpAddressId", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetSecurity")
    def reset_security(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurity", []))

    @jsii.member(jsii_name="resetSignIn")
    def reset_sign_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignIn", []))

    @jsii.member(jsii_name="resetSignUp")
    def reset_sign_up(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignUp", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTenantAccess")
    def reset_tenant_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantAccess", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualNetworkConfiguration")
    def reset_virtual_network_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkConfiguration", []))

    @jsii.member(jsii_name="resetVirtualNetworkType")
    def reset_virtual_network_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkType", []))

    @jsii.member(jsii_name="resetZones")
    def reset_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZones", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="additionalLocation")
    def additional_location(self) -> "ApiManagementAdditionalLocationList":
        return typing.cast("ApiManagementAdditionalLocationList", jsii.get(self, "additionalLocation"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> "ApiManagementCertificateList":
        return typing.cast("ApiManagementCertificateList", jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="delegation")
    def delegation(self) -> "ApiManagementDelegationOutputReference":
        return typing.cast("ApiManagementDelegationOutputReference", jsii.get(self, "delegation"))

    @builtins.property
    @jsii.member(jsii_name="developerPortalUrl")
    def developer_portal_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "developerPortalUrl"))

    @builtins.property
    @jsii.member(jsii_name="gatewayRegionalUrl")
    def gateway_regional_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayRegionalUrl"))

    @builtins.property
    @jsii.member(jsii_name="gatewayUrl")
    def gateway_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayUrl"))

    @builtins.property
    @jsii.member(jsii_name="hostnameConfiguration")
    def hostname_configuration(
        self,
    ) -> "ApiManagementHostnameConfigurationOutputReference":
        return typing.cast("ApiManagementHostnameConfigurationOutputReference", jsii.get(self, "hostnameConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "ApiManagementIdentityOutputReference":
        return typing.cast("ApiManagementIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="managementApiUrl")
    def management_api_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managementApiUrl"))

    @builtins.property
    @jsii.member(jsii_name="portalUrl")
    def portal_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portalUrl"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddresses")
    def private_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "privateIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> "ApiManagementProtocolsOutputReference":
        return typing.cast("ApiManagementProtocolsOutputReference", jsii.get(self, "protocols"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddresses")
    def public_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="scmUrl")
    def scm_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scmUrl"))

    @builtins.property
    @jsii.member(jsii_name="security")
    def security(self) -> "ApiManagementSecurityOutputReference":
        return typing.cast("ApiManagementSecurityOutputReference", jsii.get(self, "security"))

    @builtins.property
    @jsii.member(jsii_name="signIn")
    def sign_in(self) -> "ApiManagementSignInOutputReference":
        return typing.cast("ApiManagementSignInOutputReference", jsii.get(self, "signIn"))

    @builtins.property
    @jsii.member(jsii_name="signUp")
    def sign_up(self) -> "ApiManagementSignUpOutputReference":
        return typing.cast("ApiManagementSignUpOutputReference", jsii.get(self, "signUp"))

    @builtins.property
    @jsii.member(jsii_name="tenantAccess")
    def tenant_access(self) -> "ApiManagementTenantAccessOutputReference":
        return typing.cast("ApiManagementTenantAccessOutputReference", jsii.get(self, "tenantAccess"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApiManagementTimeoutsOutputReference":
        return typing.cast("ApiManagementTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkConfiguration")
    def virtual_network_configuration(
        self,
    ) -> "ApiManagementVirtualNetworkConfigurationOutputReference":
        return typing.cast("ApiManagementVirtualNetworkConfigurationOutputReference", jsii.get(self, "virtualNetworkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="additionalLocationInput")
    def additional_location_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementAdditionalLocation"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementAdditionalLocation"]]], jsii.get(self, "additionalLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCertificate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCertificate"]]], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateEnabledInput")
    def client_certificate_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientCertificateEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="delegationInput")
    def delegation_input(self) -> typing.Optional["ApiManagementDelegation"]:
        return typing.cast(typing.Optional["ApiManagementDelegation"], jsii.get(self, "delegationInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayDisabledInput")
    def gateway_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "gatewayDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameConfigurationInput")
    def hostname_configuration_input(
        self,
    ) -> typing.Optional["ApiManagementHostnameConfiguration"]:
        return typing.cast(typing.Optional["ApiManagementHostnameConfiguration"], jsii.get(self, "hostnameConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["ApiManagementIdentity"]:
        return typing.cast(typing.Optional["ApiManagementIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="minApiVersionInput")
    def min_api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minApiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationSenderEmailInput")
    def notification_sender_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationSenderEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolsInput")
    def protocols_input(self) -> typing.Optional["ApiManagementProtocols"]:
        return typing.cast(typing.Optional["ApiManagementProtocols"], jsii.get(self, "protocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressIdInput")
    def public_ip_address_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicIpAddressIdInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherEmailInput")
    def publisher_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherNameInput")
    def publisher_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityInput")
    def security_input(self) -> typing.Optional["ApiManagementSecurity"]:
        return typing.cast(typing.Optional["ApiManagementSecurity"], jsii.get(self, "securityInput"))

    @builtins.property
    @jsii.member(jsii_name="signInInput")
    def sign_in_input(self) -> typing.Optional["ApiManagementSignIn"]:
        return typing.cast(typing.Optional["ApiManagementSignIn"], jsii.get(self, "signInInput"))

    @builtins.property
    @jsii.member(jsii_name="signUpInput")
    def sign_up_input(self) -> typing.Optional["ApiManagementSignUp"]:
        return typing.cast(typing.Optional["ApiManagementSignUp"], jsii.get(self, "signUpInput"))

    @builtins.property
    @jsii.member(jsii_name="skuNameInput")
    def sku_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantAccessInput")
    def tenant_access_input(self) -> typing.Optional["ApiManagementTenantAccess"]:
        return typing.cast(typing.Optional["ApiManagementTenantAccess"], jsii.get(self, "tenantAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkConfigurationInput")
    def virtual_network_configuration_input(
        self,
    ) -> typing.Optional["ApiManagementVirtualNetworkConfiguration"]:
        return typing.cast(typing.Optional["ApiManagementVirtualNetworkConfiguration"], jsii.get(self, "virtualNetworkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkTypeInput")
    def virtual_network_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateEnabled")
    def client_certificate_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientCertificateEnabled"))

    @client_certificate_enabled.setter
    def client_certificate_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e55750df29b9951e4a44ee37b86425d4d33fdf15477dbed38368bc89e7e982c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gatewayDisabled")
    def gateway_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "gatewayDisabled"))

    @gateway_disabled.setter
    def gateway_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54cf0680e74fc4c1ed638b7a307036154b2cbf476e9c4b810392d3ba01db569c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed817cf42715c3982bc0ade4a3f91fac2ebb9fb39f8a5f5e0dc3ad7f530d4090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9457b4154122a6d6baaf37977a1509304c9f43e02d88de123f96164d64d4b33b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minApiVersion")
    def min_api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minApiVersion"))

    @min_api_version.setter
    def min_api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7adea66550c738dc81dfb00f08ebdb7f27b46447b00fae9e630f7d3d27d766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minApiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9dd8425b7dc91230e981e690ed1d33001cc71f6cb62e97cc309052d161ed087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationSenderEmail")
    def notification_sender_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationSenderEmail"))

    @notification_sender_email.setter
    def notification_sender_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de5ca8a7f12a3314bec4f27010299b0ceeac34d82607943cd5c4074340e997e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationSenderEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressId")
    def public_ip_address_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddressId"))

    @public_ip_address_id.setter
    def public_ip_address_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c800456a5381e4da24d7fa7df264e806bfe7e3b00082ef73e591dd5ad9159e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddressId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabled")
    def public_network_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicNetworkAccessEnabled"))

    @public_network_access_enabled.setter
    def public_network_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d8812250721ec17cb6c23d8f99b35188fdb7a8333874da9ec62adeec349e42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisherEmail")
    def publisher_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisherEmail"))

    @publisher_email.setter
    def publisher_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467acddbf91e4eb130de510e461fcc2043684163ce17f76cfd1e06a458b01f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisherEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisherName")
    def publisher_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisherName"))

    @publisher_name.setter
    def publisher_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ea522ca2e93e21cecc219392a0c097d26aa3ea40deb728b18a769621e72e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisherName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cca6beda6a9920325a8d6b39f69483aa46daea3f22bb783b3142a4378d76fe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b5c11926a9c066cb9329531c9a65671ebf0e9507e6756f5399d77715422f95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ea75c6ac31a3460907b3a961e0b8a83192e37a6ce26766c9d9c78e0bdc429b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkType")
    def virtual_network_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkType"))

    @virtual_network_type.setter
    def virtual_network_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d9e9cfe73ed5aed2698c3b2d94a6b51671f3456315a03823f52710c3ea130bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e73d5e50c9265770bd924d4699093ea24d03be081d3a39d7f14ef02f5c63c926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementAdditionalLocation",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "capacity": "capacity",
        "gateway_disabled": "gatewayDisabled",
        "public_ip_address_id": "publicIpAddressId",
        "virtual_network_configuration": "virtualNetworkConfiguration",
        "zones": "zones",
    },
)
class ApiManagementAdditionalLocation:
    def __init__(
        self,
        *,
        location: builtins.str,
        capacity: typing.Optional[jsii.Number] = None,
        gateway_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_ip_address_id: typing.Optional[builtins.str] = None,
        virtual_network_configuration: typing.Optional[typing.Union["ApiManagementAdditionalLocationVirtualNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#location ApiManagement#location}.
        :param capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#capacity ApiManagement#capacity}.
        :param gateway_disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#gateway_disabled ApiManagement#gateway_disabled}.
        :param public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#public_ip_address_id ApiManagement#public_ip_address_id}.
        :param virtual_network_configuration: virtual_network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#virtual_network_configuration ApiManagement#virtual_network_configuration}
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#zones ApiManagement#zones}.
        '''
        if isinstance(virtual_network_configuration, dict):
            virtual_network_configuration = ApiManagementAdditionalLocationVirtualNetworkConfiguration(**virtual_network_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c95f763e943b886ae7570545cc957bc8747f11b9cc8aa45ebf757d9273ac1c)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument gateway_disabled", value=gateway_disabled, expected_type=type_hints["gateway_disabled"])
            check_type(argname="argument public_ip_address_id", value=public_ip_address_id, expected_type=type_hints["public_ip_address_id"])
            check_type(argname="argument virtual_network_configuration", value=virtual_network_configuration, expected_type=type_hints["virtual_network_configuration"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
        }
        if capacity is not None:
            self._values["capacity"] = capacity
        if gateway_disabled is not None:
            self._values["gateway_disabled"] = gateway_disabled
        if public_ip_address_id is not None:
            self._values["public_ip_address_id"] = public_ip_address_id
        if virtual_network_configuration is not None:
            self._values["virtual_network_configuration"] = virtual_network_configuration
        if zones is not None:
            self._values["zones"] = zones

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#location ApiManagement#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#capacity ApiManagement#capacity}.'''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gateway_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#gateway_disabled ApiManagement#gateway_disabled}.'''
        result = self._values.get("gateway_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_ip_address_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#public_ip_address_id ApiManagement#public_ip_address_id}.'''
        result = self._values.get("public_ip_address_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_configuration(
        self,
    ) -> typing.Optional["ApiManagementAdditionalLocationVirtualNetworkConfiguration"]:
        '''virtual_network_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#virtual_network_configuration ApiManagement#virtual_network_configuration}
        '''
        result = self._values.get("virtual_network_configuration")
        return typing.cast(typing.Optional["ApiManagementAdditionalLocationVirtualNetworkConfiguration"], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#zones ApiManagement#zones}.'''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementAdditionalLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementAdditionalLocationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementAdditionalLocationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b159f8b43c85e83af449ae6a61c4e93c112ecacfbef9ca711e4cc06f40a974f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementAdditionalLocationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf91b95a44451e1a4a947ac609d19aa78e190cbfb3f7d82308ce3263224f1373)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementAdditionalLocationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6410342cd17640e1e62fd067fa270d7b3d8143b7d0ac151dc50aa29dd2451ca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a594f51c8bf106b8d7960ea0a0ae27fbe290523a336d8c3d5caefa0bb333c432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e1ba57d7251f07f05d811f57fe3d186017036bcd3707a36cd45a781639a4ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementAdditionalLocation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementAdditionalLocation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementAdditionalLocation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8828037c618bf8207d1afda7eb144f29c504266c6a24f8d5d616cb878d9353e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementAdditionalLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementAdditionalLocationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c40fa838405e95c3666d596e797d59c3955d6b94ee642fe73f67519feea61d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putVirtualNetworkConfiguration")
    def put_virtual_network_configuration(self, *, subnet_id: builtins.str) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#subnet_id ApiManagement#subnet_id}.
        '''
        value = ApiManagementAdditionalLocationVirtualNetworkConfiguration(
            subnet_id=subnet_id
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualNetworkConfiguration", [value]))

    @jsii.member(jsii_name="resetCapacity")
    def reset_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacity", []))

    @jsii.member(jsii_name="resetGatewayDisabled")
    def reset_gateway_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayDisabled", []))

    @jsii.member(jsii_name="resetPublicIpAddressId")
    def reset_public_ip_address_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIpAddressId", []))

    @jsii.member(jsii_name="resetVirtualNetworkConfiguration")
    def reset_virtual_network_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkConfiguration", []))

    @jsii.member(jsii_name="resetZones")
    def reset_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZones", []))

    @builtins.property
    @jsii.member(jsii_name="gatewayRegionalUrl")
    def gateway_regional_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayRegionalUrl"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddresses")
    def private_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "privateIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddresses")
    def public_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkConfiguration")
    def virtual_network_configuration(
        self,
    ) -> "ApiManagementAdditionalLocationVirtualNetworkConfigurationOutputReference":
        return typing.cast("ApiManagementAdditionalLocationVirtualNetworkConfigurationOutputReference", jsii.get(self, "virtualNetworkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayDisabledInput")
    def gateway_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "gatewayDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressIdInput")
    def public_ip_address_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicIpAddressIdInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkConfigurationInput")
    def virtual_network_configuration_input(
        self,
    ) -> typing.Optional["ApiManagementAdditionalLocationVirtualNetworkConfiguration"]:
        return typing.cast(typing.Optional["ApiManagementAdditionalLocationVirtualNetworkConfiguration"], jsii.get(self, "virtualNetworkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "capacity"))

    @capacity.setter
    def capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac9807c14eb214f8fe7e6ce9ec7b5c9c36cb91a66d8ce6b6ff03d9d662f7efeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gatewayDisabled")
    def gateway_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "gatewayDisabled"))

    @gateway_disabled.setter
    def gateway_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__802face2936beeb6c32511d0b09cf89698af2cbd1d03b6f44483677a83a9713a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773b6b67cb14244c690dfa2fdc6d631cac8b254038861a149344e314d960d8bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressId")
    def public_ip_address_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddressId"))

    @public_ip_address_id.setter
    def public_ip_address_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87e88bec4f803e916ac0cd9672e2d4e7b679c27850b7477aae2a6093692096b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddressId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8113b83161b3275366e70319f5448cdb578c3c9ba3b2d7187bc3786235f46d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementAdditionalLocation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementAdditionalLocation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementAdditionalLocation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33add858655ebfbe99981b8801c3f760afc2b581b08f140e30d6533c27e0e70c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementAdditionalLocationVirtualNetworkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"subnet_id": "subnetId"},
)
class ApiManagementAdditionalLocationVirtualNetworkConfiguration:
    def __init__(self, *, subnet_id: builtins.str) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#subnet_id ApiManagement#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7657433b9d5df10caab86480e597363634156b720bf9188fcc4745a1a80cbc8b)
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_id": subnet_id,
        }

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#subnet_id ApiManagement#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementAdditionalLocationVirtualNetworkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementAdditionalLocationVirtualNetworkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementAdditionalLocationVirtualNetworkConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__535cd7cb0163aa64c850c7e6160ddc5ad39c296c2f04a46caa3059a589da2b7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bedc46608cf8f9ff74ff9a5206d58749ba9f7c0109d9ec3b712634c4e4cbc5f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementAdditionalLocationVirtualNetworkConfiguration]:
        return typing.cast(typing.Optional[ApiManagementAdditionalLocationVirtualNetworkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementAdditionalLocationVirtualNetworkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dac134c18fa39f52dc40fef710862f90a70b73511957d76c3f3995f9c9dca373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "encoded_certificate": "encodedCertificate",
        "store_name": "storeName",
        "certificate_password": "certificatePassword",
    },
)
class ApiManagementCertificate:
    def __init__(
        self,
        *,
        encoded_certificate: builtins.str,
        store_name: builtins.str,
        certificate_password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encoded_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#encoded_certificate ApiManagement#encoded_certificate}.
        :param store_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#store_name ApiManagement#store_name}.
        :param certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate_password ApiManagement#certificate_password}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__197011cbd95ffd4975e08887eb007b06cbde7d3be5d565d8fe97234f48030af3)
            check_type(argname="argument encoded_certificate", value=encoded_certificate, expected_type=type_hints["encoded_certificate"])
            check_type(argname="argument store_name", value=store_name, expected_type=type_hints["store_name"])
            check_type(argname="argument certificate_password", value=certificate_password, expected_type=type_hints["certificate_password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "encoded_certificate": encoded_certificate,
            "store_name": store_name,
        }
        if certificate_password is not None:
            self._values["certificate_password"] = certificate_password

    @builtins.property
    def encoded_certificate(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#encoded_certificate ApiManagement#encoded_certificate}.'''
        result = self._values.get("encoded_certificate")
        assert result is not None, "Required property 'encoded_certificate' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def store_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#store_name ApiManagement#store_name}.'''
        result = self._values.get("store_name")
        assert result is not None, "Required property 'store_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate_password ApiManagement#certificate_password}.'''
        result = self._values.get("certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementCertificateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementCertificateList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a63d3288a2b018d123018c7efd79f7ee5a78b30df894f8b2eab6c0815309408)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApiManagementCertificateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec8c105c62e85f3fd53c47feb4e566446e367edc976fb9ef3e9063d22db34f9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementCertificateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dae2c277186d4e0de9e5f241c920a084a295fadc3862f5fcdb14df12cd8d185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07c29a9d6a1da391868a99244d97b713b8b4fc753e7f896238b009a5373bc47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac70ee16e3a4a9e0459273d7550a02cad5641f13881923296391456640dbe897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCertificate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCertificate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c13cd5b883c2043fbc5c5f4d735d1eb2fc4268e3fa9d894877f45136e0505ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementCertificateOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6bc7cd0f57f6feecff461d00d2c0301714b16bfc571df2e96e87efe2621ed6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificatePassword")
    def reset_certificate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificatePassword", []))

    @builtins.property
    @jsii.member(jsii_name="expiry")
    def expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiry"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="certificatePasswordInput")
    def certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="encodedCertificateInput")
    def encoded_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodedCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="storeNameInput")
    def store_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatePassword")
    def certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificatePassword"))

    @certificate_password.setter
    def certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9a86ed03dd18678f26a298b26b19e757acaa8228e2f40104f5a2319de44d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encodedCertificate")
    def encoded_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encodedCertificate"))

    @encoded_certificate.setter
    def encoded_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff91f1c4f8018a6252c6762836ac5c585485b73cb1c794d412af2e539fd0b0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encodedCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storeName")
    def store_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storeName"))

    @store_name.setter
    def store_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ab0bc9f096d91ced1fccb2d105f98cdedb94aaf9a39b59e717bdbabc982c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCertificate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCertificate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCertificate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27a7ff00984b55066ece7746fbc5e8bbbe12b1e84aed2996dc8a01b46d2f9d60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "publisher_email": "publisherEmail",
        "publisher_name": "publisherName",
        "resource_group_name": "resourceGroupName",
        "sku_name": "skuName",
        "additional_location": "additionalLocation",
        "certificate": "certificate",
        "client_certificate_enabled": "clientCertificateEnabled",
        "delegation": "delegation",
        "gateway_disabled": "gatewayDisabled",
        "hostname_configuration": "hostnameConfiguration",
        "id": "id",
        "identity": "identity",
        "min_api_version": "minApiVersion",
        "notification_sender_email": "notificationSenderEmail",
        "protocols": "protocols",
        "public_ip_address_id": "publicIpAddressId",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "security": "security",
        "sign_in": "signIn",
        "sign_up": "signUp",
        "tags": "tags",
        "tenant_access": "tenantAccess",
        "timeouts": "timeouts",
        "virtual_network_configuration": "virtualNetworkConfiguration",
        "virtual_network_type": "virtualNetworkType",
        "zones": "zones",
    },
)
class ApiManagementConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        location: builtins.str,
        name: builtins.str,
        publisher_email: builtins.str,
        publisher_name: builtins.str,
        resource_group_name: builtins.str,
        sku_name: builtins.str,
        additional_location: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementAdditionalLocation, typing.Dict[builtins.str, typing.Any]]]]] = None,
        certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
        client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delegation: typing.Optional[typing.Union["ApiManagementDelegation", typing.Dict[builtins.str, typing.Any]]] = None,
        gateway_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hostname_configuration: typing.Optional[typing.Union["ApiManagementHostnameConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ApiManagementIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        min_api_version: typing.Optional[builtins.str] = None,
        notification_sender_email: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.Union["ApiManagementProtocols", typing.Dict[builtins.str, typing.Any]]] = None,
        public_ip_address_id: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security: typing.Optional[typing.Union["ApiManagementSecurity", typing.Dict[builtins.str, typing.Any]]] = None,
        sign_in: typing.Optional[typing.Union["ApiManagementSignIn", typing.Dict[builtins.str, typing.Any]]] = None,
        sign_up: typing.Optional[typing.Union["ApiManagementSignUp", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenant_access: typing.Optional[typing.Union["ApiManagementTenantAccess", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_network_configuration: typing.Optional[typing.Union["ApiManagementVirtualNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_network_type: typing.Optional[builtins.str] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#location ApiManagement#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#name ApiManagement#name}.
        :param publisher_email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#publisher_email ApiManagement#publisher_email}.
        :param publisher_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#publisher_name ApiManagement#publisher_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#resource_group_name ApiManagement#resource_group_name}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#sku_name ApiManagement#sku_name}.
        :param additional_location: additional_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#additional_location ApiManagement#additional_location}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate ApiManagement#certificate}
        :param client_certificate_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#client_certificate_enabled ApiManagement#client_certificate_enabled}.
        :param delegation: delegation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#delegation ApiManagement#delegation}
        :param gateway_disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#gateway_disabled ApiManagement#gateway_disabled}.
        :param hostname_configuration: hostname_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#hostname_configuration ApiManagement#hostname_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#id ApiManagement#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#identity ApiManagement#identity}
        :param min_api_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#min_api_version ApiManagement#min_api_version}.
        :param notification_sender_email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#notification_sender_email ApiManagement#notification_sender_email}.
        :param protocols: protocols block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#protocols ApiManagement#protocols}
        :param public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#public_ip_address_id ApiManagement#public_ip_address_id}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#public_network_access_enabled ApiManagement#public_network_access_enabled}.
        :param security: security block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#security ApiManagement#security}
        :param sign_in: sign_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#sign_in ApiManagement#sign_in}
        :param sign_up: sign_up block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#sign_up ApiManagement#sign_up}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tags ApiManagement#tags}.
        :param tenant_access: tenant_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tenant_access ApiManagement#tenant_access}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#timeouts ApiManagement#timeouts}
        :param virtual_network_configuration: virtual_network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#virtual_network_configuration ApiManagement#virtual_network_configuration}
        :param virtual_network_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#virtual_network_type ApiManagement#virtual_network_type}.
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#zones ApiManagement#zones}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(delegation, dict):
            delegation = ApiManagementDelegation(**delegation)
        if isinstance(hostname_configuration, dict):
            hostname_configuration = ApiManagementHostnameConfiguration(**hostname_configuration)
        if isinstance(identity, dict):
            identity = ApiManagementIdentity(**identity)
        if isinstance(protocols, dict):
            protocols = ApiManagementProtocols(**protocols)
        if isinstance(security, dict):
            security = ApiManagementSecurity(**security)
        if isinstance(sign_in, dict):
            sign_in = ApiManagementSignIn(**sign_in)
        if isinstance(sign_up, dict):
            sign_up = ApiManagementSignUp(**sign_up)
        if isinstance(tenant_access, dict):
            tenant_access = ApiManagementTenantAccess(**tenant_access)
        if isinstance(timeouts, dict):
            timeouts = ApiManagementTimeouts(**timeouts)
        if isinstance(virtual_network_configuration, dict):
            virtual_network_configuration = ApiManagementVirtualNetworkConfiguration(**virtual_network_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__154b2056b4af27a46187afe2f4b6d9f62d27cc27062f18765e0017f35475fc49)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument publisher_email", value=publisher_email, expected_type=type_hints["publisher_email"])
            check_type(argname="argument publisher_name", value=publisher_name, expected_type=type_hints["publisher_name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument sku_name", value=sku_name, expected_type=type_hints["sku_name"])
            check_type(argname="argument additional_location", value=additional_location, expected_type=type_hints["additional_location"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument client_certificate_enabled", value=client_certificate_enabled, expected_type=type_hints["client_certificate_enabled"])
            check_type(argname="argument delegation", value=delegation, expected_type=type_hints["delegation"])
            check_type(argname="argument gateway_disabled", value=gateway_disabled, expected_type=type_hints["gateway_disabled"])
            check_type(argname="argument hostname_configuration", value=hostname_configuration, expected_type=type_hints["hostname_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument min_api_version", value=min_api_version, expected_type=type_hints["min_api_version"])
            check_type(argname="argument notification_sender_email", value=notification_sender_email, expected_type=type_hints["notification_sender_email"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument public_ip_address_id", value=public_ip_address_id, expected_type=type_hints["public_ip_address_id"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument security", value=security, expected_type=type_hints["security"])
            check_type(argname="argument sign_in", value=sign_in, expected_type=type_hints["sign_in"])
            check_type(argname="argument sign_up", value=sign_up, expected_type=type_hints["sign_up"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tenant_access", value=tenant_access, expected_type=type_hints["tenant_access"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_network_configuration", value=virtual_network_configuration, expected_type=type_hints["virtual_network_configuration"])
            check_type(argname="argument virtual_network_type", value=virtual_network_type, expected_type=type_hints["virtual_network_type"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "publisher_email": publisher_email,
            "publisher_name": publisher_name,
            "resource_group_name": resource_group_name,
            "sku_name": sku_name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if additional_location is not None:
            self._values["additional_location"] = additional_location
        if certificate is not None:
            self._values["certificate"] = certificate
        if client_certificate_enabled is not None:
            self._values["client_certificate_enabled"] = client_certificate_enabled
        if delegation is not None:
            self._values["delegation"] = delegation
        if gateway_disabled is not None:
            self._values["gateway_disabled"] = gateway_disabled
        if hostname_configuration is not None:
            self._values["hostname_configuration"] = hostname_configuration
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if min_api_version is not None:
            self._values["min_api_version"] = min_api_version
        if notification_sender_email is not None:
            self._values["notification_sender_email"] = notification_sender_email
        if protocols is not None:
            self._values["protocols"] = protocols
        if public_ip_address_id is not None:
            self._values["public_ip_address_id"] = public_ip_address_id
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if security is not None:
            self._values["security"] = security
        if sign_in is not None:
            self._values["sign_in"] = sign_in
        if sign_up is not None:
            self._values["sign_up"] = sign_up
        if tags is not None:
            self._values["tags"] = tags
        if tenant_access is not None:
            self._values["tenant_access"] = tenant_access
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_network_configuration is not None:
            self._values["virtual_network_configuration"] = virtual_network_configuration
        if virtual_network_type is not None:
            self._values["virtual_network_type"] = virtual_network_type
        if zones is not None:
            self._values["zones"] = zones

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#location ApiManagement#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#name ApiManagement#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher_email(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#publisher_email ApiManagement#publisher_email}.'''
        result = self._values.get("publisher_email")
        assert result is not None, "Required property 'publisher_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#publisher_name ApiManagement#publisher_name}.'''
        result = self._values.get("publisher_name")
        assert result is not None, "Required property 'publisher_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#resource_group_name ApiManagement#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#sku_name ApiManagement#sku_name}.'''
        result = self._values.get("sku_name")
        assert result is not None, "Required property 'sku_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_location(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementAdditionalLocation]]]:
        '''additional_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#additional_location ApiManagement#additional_location}
        '''
        result = self._values.get("additional_location")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementAdditionalLocation]]], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCertificate]]]:
        '''certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate ApiManagement#certificate}
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCertificate]]], result)

    @builtins.property
    def client_certificate_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#client_certificate_enabled ApiManagement#client_certificate_enabled}.'''
        result = self._values.get("client_certificate_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delegation(self) -> typing.Optional["ApiManagementDelegation"]:
        '''delegation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#delegation ApiManagement#delegation}
        '''
        result = self._values.get("delegation")
        return typing.cast(typing.Optional["ApiManagementDelegation"], result)

    @builtins.property
    def gateway_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#gateway_disabled ApiManagement#gateway_disabled}.'''
        result = self._values.get("gateway_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hostname_configuration(
        self,
    ) -> typing.Optional["ApiManagementHostnameConfiguration"]:
        '''hostname_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#hostname_configuration ApiManagement#hostname_configuration}
        '''
        result = self._values.get("hostname_configuration")
        return typing.cast(typing.Optional["ApiManagementHostnameConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#id ApiManagement#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["ApiManagementIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#identity ApiManagement#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["ApiManagementIdentity"], result)

    @builtins.property
    def min_api_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#min_api_version ApiManagement#min_api_version}.'''
        result = self._values.get("min_api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_sender_email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#notification_sender_email ApiManagement#notification_sender_email}.'''
        result = self._values.get("notification_sender_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocols(self) -> typing.Optional["ApiManagementProtocols"]:
        '''protocols block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#protocols ApiManagement#protocols}
        '''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional["ApiManagementProtocols"], result)

    @builtins.property
    def public_ip_address_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#public_ip_address_id ApiManagement#public_ip_address_id}.'''
        result = self._values.get("public_ip_address_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#public_network_access_enabled ApiManagement#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security(self) -> typing.Optional["ApiManagementSecurity"]:
        '''security block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#security ApiManagement#security}
        '''
        result = self._values.get("security")
        return typing.cast(typing.Optional["ApiManagementSecurity"], result)

    @builtins.property
    def sign_in(self) -> typing.Optional["ApiManagementSignIn"]:
        '''sign_in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#sign_in ApiManagement#sign_in}
        '''
        result = self._values.get("sign_in")
        return typing.cast(typing.Optional["ApiManagementSignIn"], result)

    @builtins.property
    def sign_up(self) -> typing.Optional["ApiManagementSignUp"]:
        '''sign_up block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#sign_up ApiManagement#sign_up}
        '''
        result = self._values.get("sign_up")
        return typing.cast(typing.Optional["ApiManagementSignUp"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tags ApiManagement#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tenant_access(self) -> typing.Optional["ApiManagementTenantAccess"]:
        '''tenant_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tenant_access ApiManagement#tenant_access}
        '''
        result = self._values.get("tenant_access")
        return typing.cast(typing.Optional["ApiManagementTenantAccess"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApiManagementTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#timeouts ApiManagement#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApiManagementTimeouts"], result)

    @builtins.property
    def virtual_network_configuration(
        self,
    ) -> typing.Optional["ApiManagementVirtualNetworkConfiguration"]:
        '''virtual_network_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#virtual_network_configuration ApiManagement#virtual_network_configuration}
        '''
        result = self._values.get("virtual_network_configuration")
        return typing.cast(typing.Optional["ApiManagementVirtualNetworkConfiguration"], result)

    @builtins.property
    def virtual_network_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#virtual_network_type ApiManagement#virtual_network_type}.'''
        result = self._values.get("virtual_network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#zones ApiManagement#zones}.'''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementDelegation",
    jsii_struct_bases=[],
    name_mapping={
        "subscriptions_enabled": "subscriptionsEnabled",
        "url": "url",
        "user_registration_enabled": "userRegistrationEnabled",
        "validation_key": "validationKey",
    },
)
class ApiManagementDelegation:
    def __init__(
        self,
        *,
        subscriptions_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        url: typing.Optional[builtins.str] = None,
        user_registration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        validation_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subscriptions_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#subscriptions_enabled ApiManagement#subscriptions_enabled}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#url ApiManagement#url}.
        :param user_registration_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#user_registration_enabled ApiManagement#user_registration_enabled}.
        :param validation_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#validation_key ApiManagement#validation_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0712329f3dd35e44106d5d40fa220cf0bb42a10184eb55b384b228cd651bcf13)
            check_type(argname="argument subscriptions_enabled", value=subscriptions_enabled, expected_type=type_hints["subscriptions_enabled"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument user_registration_enabled", value=user_registration_enabled, expected_type=type_hints["user_registration_enabled"])
            check_type(argname="argument validation_key", value=validation_key, expected_type=type_hints["validation_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if subscriptions_enabled is not None:
            self._values["subscriptions_enabled"] = subscriptions_enabled
        if url is not None:
            self._values["url"] = url
        if user_registration_enabled is not None:
            self._values["user_registration_enabled"] = user_registration_enabled
        if validation_key is not None:
            self._values["validation_key"] = validation_key

    @builtins.property
    def subscriptions_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#subscriptions_enabled ApiManagement#subscriptions_enabled}.'''
        result = self._values.get("subscriptions_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#url ApiManagement#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_registration_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#user_registration_enabled ApiManagement#user_registration_enabled}.'''
        result = self._values.get("user_registration_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def validation_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#validation_key ApiManagement#validation_key}.'''
        result = self._values.get("validation_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDelegation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementDelegationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementDelegationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a1fc7e3996793315733f3bb4b90358179acaba5811841ee1daa9893bb2b0cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSubscriptionsEnabled")
    def reset_subscriptions_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubscriptionsEnabled", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @jsii.member(jsii_name="resetUserRegistrationEnabled")
    def reset_user_registration_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserRegistrationEnabled", []))

    @jsii.member(jsii_name="resetValidationKey")
    def reset_validation_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidationKey", []))

    @builtins.property
    @jsii.member(jsii_name="subscriptionsEnabledInput")
    def subscriptions_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "subscriptionsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="userRegistrationEnabledInput")
    def user_registration_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "userRegistrationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="validationKeyInput")
    def validation_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "validationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionsEnabled")
    def subscriptions_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "subscriptionsEnabled"))

    @subscriptions_enabled.setter
    def subscriptions_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65355a4c0633229b5b451a94287c00dc1200ad345c136e4e828b41326b0913c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2681aca027109f4fd35706c63f55745d6d81d5bd0e3a0239a2ebd2daf102dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userRegistrationEnabled")
    def user_registration_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "userRegistrationEnabled"))

    @user_registration_enabled.setter
    def user_registration_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4cf521f690980af4661fde5e58b8f442ec4fa306a0f2da0275fb4d930ad6b79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userRegistrationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validationKey")
    def validation_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validationKey"))

    @validation_key.setter
    def validation_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02773d83f814d40c8ecf2741fe568fafad53020d3986f62aa0b376393cbef033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validationKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementDelegation]:
        return typing.cast(typing.Optional[ApiManagementDelegation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApiManagementDelegation]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0419d952a56106b10b5d76e7c858aacb763a0018f14ab1878fcaa6f062a17a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "developer_portal": "developerPortal",
        "management": "management",
        "portal": "portal",
        "proxy": "proxy",
        "scm": "scm",
    },
)
class ApiManagementHostnameConfiguration:
    def __init__(
        self,
        *,
        developer_portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementHostnameConfigurationDeveloperPortal", typing.Dict[builtins.str, typing.Any]]]]] = None,
        management: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementHostnameConfigurationManagement", typing.Dict[builtins.str, typing.Any]]]]] = None,
        portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementHostnameConfigurationPortal", typing.Dict[builtins.str, typing.Any]]]]] = None,
        proxy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementHostnameConfigurationProxy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementHostnameConfigurationScm", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param developer_portal: developer_portal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#developer_portal ApiManagement#developer_portal}
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#management ApiManagement#management}
        :param portal: portal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#portal ApiManagement#portal}
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#proxy ApiManagement#proxy}
        :param scm: scm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#scm ApiManagement#scm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecddf5ef14f8d3c1686f1d2262b0039d26f23f1249d99854fbe1f8b8973ea21)
            check_type(argname="argument developer_portal", value=developer_portal, expected_type=type_hints["developer_portal"])
            check_type(argname="argument management", value=management, expected_type=type_hints["management"])
            check_type(argname="argument portal", value=portal, expected_type=type_hints["portal"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument scm", value=scm, expected_type=type_hints["scm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if developer_portal is not None:
            self._values["developer_portal"] = developer_portal
        if management is not None:
            self._values["management"] = management
        if portal is not None:
            self._values["portal"] = portal
        if proxy is not None:
            self._values["proxy"] = proxy
        if scm is not None:
            self._values["scm"] = scm

    @builtins.property
    def developer_portal(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationDeveloperPortal"]]]:
        '''developer_portal block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#developer_portal ApiManagement#developer_portal}
        '''
        result = self._values.get("developer_portal")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationDeveloperPortal"]]], result)

    @builtins.property
    def management(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationManagement"]]]:
        '''management block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#management ApiManagement#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationManagement"]]], result)

    @builtins.property
    def portal(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationPortal"]]]:
        '''portal block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#portal ApiManagement#portal}
        '''
        result = self._values.get("portal")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationPortal"]]], result)

    @builtins.property
    def proxy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationProxy"]]]:
        '''proxy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#proxy ApiManagement#proxy}
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationProxy"]]], result)

    @builtins.property
    def scm(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationScm"]]]:
        '''scm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#scm ApiManagement#scm}
        '''
        result = self._values.get("scm")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationScm"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementHostnameConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationDeveloperPortal",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "certificate": "certificate",
        "certificate_password": "certificatePassword",
        "key_vault_certificate_id": "keyVaultCertificateId",
        "key_vault_id": "keyVaultId",
        "negotiate_client_certificate": "negotiateClientCertificate",
        "ssl_keyvault_identity_client_id": "sslKeyvaultIdentityClientId",
    },
)
class ApiManagementHostnameConfigurationDeveloperPortal:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        certificate: typing.Optional[builtins.str] = None,
        certificate_password: typing.Optional[builtins.str] = None,
        key_vault_certificate_id: typing.Optional[builtins.str] = None,
        key_vault_id: typing.Optional[builtins.str] = None,
        negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#host_name ApiManagement#host_name}.
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate ApiManagement#certificate}.
        :param certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate_password ApiManagement#certificate_password}.
        :param key_vault_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_certificate_id ApiManagement#key_vault_certificate_id}.
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_id ApiManagement#key_vault_id}.
        :param negotiate_client_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#negotiate_client_certificate ApiManagement#negotiate_client_certificate}.
        :param ssl_keyvault_identity_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#ssl_keyvault_identity_client_id ApiManagement#ssl_keyvault_identity_client_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3d9265cd3f7dcc6f50e185a5cd12c976157c8f836cf30dacb1f53fc89a0d39)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_password", value=certificate_password, expected_type=type_hints["certificate_password"])
            check_type(argname="argument key_vault_certificate_id", value=key_vault_certificate_id, expected_type=type_hints["key_vault_certificate_id"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument negotiate_client_certificate", value=negotiate_client_certificate, expected_type=type_hints["negotiate_client_certificate"])
            check_type(argname="argument ssl_keyvault_identity_client_id", value=ssl_keyvault_identity_client_id, expected_type=type_hints["ssl_keyvault_identity_client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_password is not None:
            self._values["certificate_password"] = certificate_password
        if key_vault_certificate_id is not None:
            self._values["key_vault_certificate_id"] = key_vault_certificate_id
        if key_vault_id is not None:
            self._values["key_vault_id"] = key_vault_id
        if negotiate_client_certificate is not None:
            self._values["negotiate_client_certificate"] = negotiate_client_certificate
        if ssl_keyvault_identity_client_id is not None:
            self._values["ssl_keyvault_identity_client_id"] = ssl_keyvault_identity_client_id

    @builtins.property
    def host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#host_name ApiManagement#host_name}.'''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate ApiManagement#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate_password ApiManagement#certificate_password}.'''
        result = self._values.get("certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_certificate_id ApiManagement#key_vault_certificate_id}.'''
        result = self._values.get("key_vault_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_id ApiManagement#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negotiate_client_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#negotiate_client_certificate ApiManagement#negotiate_client_certificate}.'''
        result = self._values.get("negotiate_client_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_keyvault_identity_client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#ssl_keyvault_identity_client_id ApiManagement#ssl_keyvault_identity_client_id}.'''
        result = self._values.get("ssl_keyvault_identity_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementHostnameConfigurationDeveloperPortal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementHostnameConfigurationDeveloperPortalList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationDeveloperPortalList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cff0938b204e07325867913f3aeee79f5d6ca6b4977ce3ed048afb52b12905c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementHostnameConfigurationDeveloperPortalOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__229d69978a7af9d331db1f2bd8b77c8d25bc0dce8b063e0001d90a3509e5339c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementHostnameConfigurationDeveloperPortalOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3c1a4f10409370309911d5bd1a948c1b892a95e04ab2f2b08e5e319cc97a43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a97c00e4b777e66ddc9fc21bc01faa23ed5808f90879a9d0c5c1cb3da9736d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0d9fd8793887f3df5e945141c661e7b814d8ccf832711835392a5374babbc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationDeveloperPortal]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationDeveloperPortal]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationDeveloperPortal]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924e5449510927a1e04e9a133f4deddd2c2fcd307ce48dfd568300541c02ddda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementHostnameConfigurationDeveloperPortalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationDeveloperPortalOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35befb40be54ff06e41a1915e2366eefe267e2b41c2ec23a8d1d2beb2530ce0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCertificatePassword")
    def reset_certificate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificatePassword", []))

    @jsii.member(jsii_name="resetKeyVaultCertificateId")
    def reset_key_vault_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultCertificateId", []))

    @jsii.member(jsii_name="resetKeyVaultId")
    def reset_key_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultId", []))

    @jsii.member(jsii_name="resetNegotiateClientCertificate")
    def reset_negotiate_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegotiateClientCertificate", []))

    @jsii.member(jsii_name="resetSslKeyvaultIdentityClientId")
    def reset_ssl_keyvault_identity_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslKeyvaultIdentityClientId", []))

    @builtins.property
    @jsii.member(jsii_name="certificateSource")
    def certificate_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateSource"))

    @builtins.property
    @jsii.member(jsii_name="certificateStatus")
    def certificate_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateStatus"))

    @builtins.property
    @jsii.member(jsii_name="expiry")
    def expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiry"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatePasswordInput")
    def certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateIdInput")
    def key_vault_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificateInput")
    def negotiate_client_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negotiateClientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientIdInput")
    def ssl_keyvault_identity_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslKeyvaultIdentityClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dac09e8bc7a850d2b0e54b1a1ae7e971292d737a25c5d337f1285eb8dcc1d5e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificatePassword")
    def certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificatePassword"))

    @certificate_password.setter
    def certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23801d0e4038401ef25e458f262b383620feebee549c400a51218499d206ef36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3815f0ecbbce583eb06316b225f27969ddd8113c7d3e303f4fcffefc4f55715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateId")
    def key_vault_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultCertificateId"))

    @key_vault_certificate_id.setter
    def key_vault_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6e216b544839ed2411e6f8dd567727717de8d37f4f7fb536ef0a599319ee4bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6bd1269350ed2974815210175f75241b4cbb40b3a739312de4c67799bb69721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificate")
    def negotiate_client_certificate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negotiateClientCertificate"))

    @negotiate_client_certificate.setter
    def negotiate_client_certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273058c3aadff20de80e750db1fabd8f7523e36f65ee3d90278286fd111d61cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negotiateClientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientId")
    def ssl_keyvault_identity_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslKeyvaultIdentityClientId"))

    @ssl_keyvault_identity_client_id.setter
    def ssl_keyvault_identity_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9787b61530e8bd4bc69f3fa17246693df101e64a752c139942b539c63126206e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslKeyvaultIdentityClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationDeveloperPortal]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationDeveloperPortal]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationDeveloperPortal]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c69ac571420e48ba506c9d35476166cda25b340daa6d95bfa1c9d550776d482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationManagement",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "certificate": "certificate",
        "certificate_password": "certificatePassword",
        "key_vault_certificate_id": "keyVaultCertificateId",
        "key_vault_id": "keyVaultId",
        "negotiate_client_certificate": "negotiateClientCertificate",
        "ssl_keyvault_identity_client_id": "sslKeyvaultIdentityClientId",
    },
)
class ApiManagementHostnameConfigurationManagement:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        certificate: typing.Optional[builtins.str] = None,
        certificate_password: typing.Optional[builtins.str] = None,
        key_vault_certificate_id: typing.Optional[builtins.str] = None,
        key_vault_id: typing.Optional[builtins.str] = None,
        negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#host_name ApiManagement#host_name}.
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate ApiManagement#certificate}.
        :param certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate_password ApiManagement#certificate_password}.
        :param key_vault_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_certificate_id ApiManagement#key_vault_certificate_id}.
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_id ApiManagement#key_vault_id}.
        :param negotiate_client_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#negotiate_client_certificate ApiManagement#negotiate_client_certificate}.
        :param ssl_keyvault_identity_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#ssl_keyvault_identity_client_id ApiManagement#ssl_keyvault_identity_client_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53fcc9c9c9c970f8427661bbe91fb0f9b3f7640289e39e2b4047ee3f73256c4b)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_password", value=certificate_password, expected_type=type_hints["certificate_password"])
            check_type(argname="argument key_vault_certificate_id", value=key_vault_certificate_id, expected_type=type_hints["key_vault_certificate_id"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument negotiate_client_certificate", value=negotiate_client_certificate, expected_type=type_hints["negotiate_client_certificate"])
            check_type(argname="argument ssl_keyvault_identity_client_id", value=ssl_keyvault_identity_client_id, expected_type=type_hints["ssl_keyvault_identity_client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_password is not None:
            self._values["certificate_password"] = certificate_password
        if key_vault_certificate_id is not None:
            self._values["key_vault_certificate_id"] = key_vault_certificate_id
        if key_vault_id is not None:
            self._values["key_vault_id"] = key_vault_id
        if negotiate_client_certificate is not None:
            self._values["negotiate_client_certificate"] = negotiate_client_certificate
        if ssl_keyvault_identity_client_id is not None:
            self._values["ssl_keyvault_identity_client_id"] = ssl_keyvault_identity_client_id

    @builtins.property
    def host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#host_name ApiManagement#host_name}.'''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate ApiManagement#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate_password ApiManagement#certificate_password}.'''
        result = self._values.get("certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_certificate_id ApiManagement#key_vault_certificate_id}.'''
        result = self._values.get("key_vault_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_id ApiManagement#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negotiate_client_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#negotiate_client_certificate ApiManagement#negotiate_client_certificate}.'''
        result = self._values.get("negotiate_client_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_keyvault_identity_client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#ssl_keyvault_identity_client_id ApiManagement#ssl_keyvault_identity_client_id}.'''
        result = self._values.get("ssl_keyvault_identity_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementHostnameConfigurationManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementHostnameConfigurationManagementList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationManagementList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb98a57f0b730c1265b28619efcd4be2fc9384c02f7159fff4e250c511114f56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementHostnameConfigurationManagementOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b440b6d3e48efa3c7f0714fb21f984e28421df7c1121eed514627459cd65824)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementHostnameConfigurationManagementOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57db6a39db66a1fd5f950dc425d9edd8a66238218314c1f923db3b592e51526b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b89fed1fb8adc58f55ad81b1ea08ac0e418eb712cf903da4009a54cddfef16f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f00c85a1061ec114f6eaa247c2d8ab7903f57a28b55d8c8e20c1daf2893478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationManagement]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationManagement]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationManagement]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17e62d3fbde3d65d3202fbec0c2adc3f15233d69d91f2180ed6199a693932115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementHostnameConfigurationManagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationManagementOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb26404c1c81e9cf99efa3846433738d8329c47724d26261f91b3d95a4271bb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCertificatePassword")
    def reset_certificate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificatePassword", []))

    @jsii.member(jsii_name="resetKeyVaultCertificateId")
    def reset_key_vault_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultCertificateId", []))

    @jsii.member(jsii_name="resetKeyVaultId")
    def reset_key_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultId", []))

    @jsii.member(jsii_name="resetNegotiateClientCertificate")
    def reset_negotiate_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegotiateClientCertificate", []))

    @jsii.member(jsii_name="resetSslKeyvaultIdentityClientId")
    def reset_ssl_keyvault_identity_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslKeyvaultIdentityClientId", []))

    @builtins.property
    @jsii.member(jsii_name="certificateSource")
    def certificate_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateSource"))

    @builtins.property
    @jsii.member(jsii_name="certificateStatus")
    def certificate_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateStatus"))

    @builtins.property
    @jsii.member(jsii_name="expiry")
    def expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiry"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatePasswordInput")
    def certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateIdInput")
    def key_vault_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificateInput")
    def negotiate_client_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negotiateClientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientIdInput")
    def ssl_keyvault_identity_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslKeyvaultIdentityClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73225bce93d04ed820565b78d1c341c4a78efb18e908ceb5c26ca583a0fa0051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificatePassword")
    def certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificatePassword"))

    @certificate_password.setter
    def certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc48c33e0ec07cb8cc5b140f1a90a0e3d2c6dc598ff055dcc970939d9615cd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc2c1f259c51fae257cdd469ee541e378ce1e950521a32089fe51da3ef5d8cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateId")
    def key_vault_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultCertificateId"))

    @key_vault_certificate_id.setter
    def key_vault_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0709702882a743b219aed472e9995052716546ac7e864cf8d698056e777b50f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb2d1ed506a24d3165d63619b7fee90bb0e421942db1b3fe353520bca89ead6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificate")
    def negotiate_client_certificate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negotiateClientCertificate"))

    @negotiate_client_certificate.setter
    def negotiate_client_certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8eb7e1434fd4b7ca7de6b3734c3433fb4b3751425bf079e178bbfeb737f0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negotiateClientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientId")
    def ssl_keyvault_identity_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslKeyvaultIdentityClientId"))

    @ssl_keyvault_identity_client_id.setter
    def ssl_keyvault_identity_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0de9f145361140232225d615d4d658942bc4d8d4d65d0f1f114d2295a7fe4b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslKeyvaultIdentityClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationManagement]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationManagement]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationManagement]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7d13c3fbd35729be139955b00483c968e4ca1733429144d3abf612abefb23f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementHostnameConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a715a630e2a1e09996528a938796f2000a5bf71bb2e8cdc5dc8e46905ba4d14b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeveloperPortal")
    def put_developer_portal(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementHostnameConfigurationDeveloperPortal, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391b138000f890646edf52756cd0e41019be72f759e5a63993a454a328deb76f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeveloperPortal", [value]))

    @jsii.member(jsii_name="putManagement")
    def put_management(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementHostnameConfigurationManagement, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef1fc56fd8d42b5f0ec68020889136ea69dc342020bbd7396aee14895c0edcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManagement", [value]))

    @jsii.member(jsii_name="putPortal")
    def put_portal(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementHostnameConfigurationPortal", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87f2989407cdd3b03f0e44b73132c0e753dce8460535c87b3dd8145fc64e594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPortal", [value]))

    @jsii.member(jsii_name="putProxy")
    def put_proxy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementHostnameConfigurationProxy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff9b52bd2776a5798dfc91a25897e8c666e800bd075f5419e1c2c3a21d883858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProxy", [value]))

    @jsii.member(jsii_name="putScm")
    def put_scm(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementHostnameConfigurationScm", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92a0654103fe6ae123cb4740edf85098a0fe2cc2e439f6461e1eb8bacebe710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScm", [value]))

    @jsii.member(jsii_name="resetDeveloperPortal")
    def reset_developer_portal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeveloperPortal", []))

    @jsii.member(jsii_name="resetManagement")
    def reset_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagement", []))

    @jsii.member(jsii_name="resetPortal")
    def reset_portal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortal", []))

    @jsii.member(jsii_name="resetProxy")
    def reset_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxy", []))

    @jsii.member(jsii_name="resetScm")
    def reset_scm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScm", []))

    @builtins.property
    @jsii.member(jsii_name="developerPortal")
    def developer_portal(self) -> ApiManagementHostnameConfigurationDeveloperPortalList:
        return typing.cast(ApiManagementHostnameConfigurationDeveloperPortalList, jsii.get(self, "developerPortal"))

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> ApiManagementHostnameConfigurationManagementList:
        return typing.cast(ApiManagementHostnameConfigurationManagementList, jsii.get(self, "management"))

    @builtins.property
    @jsii.member(jsii_name="portal")
    def portal(self) -> "ApiManagementHostnameConfigurationPortalList":
        return typing.cast("ApiManagementHostnameConfigurationPortalList", jsii.get(self, "portal"))

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> "ApiManagementHostnameConfigurationProxyList":
        return typing.cast("ApiManagementHostnameConfigurationProxyList", jsii.get(self, "proxy"))

    @builtins.property
    @jsii.member(jsii_name="scm")
    def scm(self) -> "ApiManagementHostnameConfigurationScmList":
        return typing.cast("ApiManagementHostnameConfigurationScmList", jsii.get(self, "scm"))

    @builtins.property
    @jsii.member(jsii_name="developerPortalInput")
    def developer_portal_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationDeveloperPortal]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationDeveloperPortal]]], jsii.get(self, "developerPortalInput"))

    @builtins.property
    @jsii.member(jsii_name="managementInput")
    def management_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationManagement]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationManagement]]], jsii.get(self, "managementInput"))

    @builtins.property
    @jsii.member(jsii_name="portalInput")
    def portal_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationPortal"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationPortal"]]], jsii.get(self, "portalInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationProxy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationProxy"]]], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="scmInput")
    def scm_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationScm"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementHostnameConfigurationScm"]]], jsii.get(self, "scmInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementHostnameConfiguration]:
        return typing.cast(typing.Optional[ApiManagementHostnameConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementHostnameConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8688bf71bf77ec9ab36e058a83e268bb097b1f670f8800d7508044e6de853ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationPortal",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "certificate": "certificate",
        "certificate_password": "certificatePassword",
        "key_vault_certificate_id": "keyVaultCertificateId",
        "key_vault_id": "keyVaultId",
        "negotiate_client_certificate": "negotiateClientCertificate",
        "ssl_keyvault_identity_client_id": "sslKeyvaultIdentityClientId",
    },
)
class ApiManagementHostnameConfigurationPortal:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        certificate: typing.Optional[builtins.str] = None,
        certificate_password: typing.Optional[builtins.str] = None,
        key_vault_certificate_id: typing.Optional[builtins.str] = None,
        key_vault_id: typing.Optional[builtins.str] = None,
        negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#host_name ApiManagement#host_name}.
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate ApiManagement#certificate}.
        :param certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate_password ApiManagement#certificate_password}.
        :param key_vault_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_certificate_id ApiManagement#key_vault_certificate_id}.
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_id ApiManagement#key_vault_id}.
        :param negotiate_client_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#negotiate_client_certificate ApiManagement#negotiate_client_certificate}.
        :param ssl_keyvault_identity_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#ssl_keyvault_identity_client_id ApiManagement#ssl_keyvault_identity_client_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fc69c12ad9cf5ebce2d9c1697b3023908d733643cc3b7a582bb7eb1319a104)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_password", value=certificate_password, expected_type=type_hints["certificate_password"])
            check_type(argname="argument key_vault_certificate_id", value=key_vault_certificate_id, expected_type=type_hints["key_vault_certificate_id"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument negotiate_client_certificate", value=negotiate_client_certificate, expected_type=type_hints["negotiate_client_certificate"])
            check_type(argname="argument ssl_keyvault_identity_client_id", value=ssl_keyvault_identity_client_id, expected_type=type_hints["ssl_keyvault_identity_client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_password is not None:
            self._values["certificate_password"] = certificate_password
        if key_vault_certificate_id is not None:
            self._values["key_vault_certificate_id"] = key_vault_certificate_id
        if key_vault_id is not None:
            self._values["key_vault_id"] = key_vault_id
        if negotiate_client_certificate is not None:
            self._values["negotiate_client_certificate"] = negotiate_client_certificate
        if ssl_keyvault_identity_client_id is not None:
            self._values["ssl_keyvault_identity_client_id"] = ssl_keyvault_identity_client_id

    @builtins.property
    def host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#host_name ApiManagement#host_name}.'''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate ApiManagement#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate_password ApiManagement#certificate_password}.'''
        result = self._values.get("certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_certificate_id ApiManagement#key_vault_certificate_id}.'''
        result = self._values.get("key_vault_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_id ApiManagement#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negotiate_client_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#negotiate_client_certificate ApiManagement#negotiate_client_certificate}.'''
        result = self._values.get("negotiate_client_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_keyvault_identity_client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#ssl_keyvault_identity_client_id ApiManagement#ssl_keyvault_identity_client_id}.'''
        result = self._values.get("ssl_keyvault_identity_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementHostnameConfigurationPortal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementHostnameConfigurationPortalList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationPortalList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8ad0e5f1f424d974b2304d9130bdb4b362e75fc661b651c2b7ea197c668696)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementHostnameConfigurationPortalOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b14163c42180eaf14566d7554d8b8ce160c170f4c16f5fc0a6ea6f11bacfef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementHostnameConfigurationPortalOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9fa926ff0bd7a2106ccc2c90b4006721e419d035a0037ca95cc872b9b9ee7e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abbe30067caa207fe60de581496a55541e822421f710a0784029d9c75052293d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17eb9297851f649825c2bdac08758d6231f767ab6977362ee8e75e379b86d7fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationPortal]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationPortal]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationPortal]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27bbb56cec2d5ddb547940aa49709d91445cb87e53e95ff068449cfec679cfed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementHostnameConfigurationPortalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationPortalOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb1a6e535da76d9309132bbd225867cbc2095414cc58c6cb5297e300845bc62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCertificatePassword")
    def reset_certificate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificatePassword", []))

    @jsii.member(jsii_name="resetKeyVaultCertificateId")
    def reset_key_vault_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultCertificateId", []))

    @jsii.member(jsii_name="resetKeyVaultId")
    def reset_key_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultId", []))

    @jsii.member(jsii_name="resetNegotiateClientCertificate")
    def reset_negotiate_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegotiateClientCertificate", []))

    @jsii.member(jsii_name="resetSslKeyvaultIdentityClientId")
    def reset_ssl_keyvault_identity_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslKeyvaultIdentityClientId", []))

    @builtins.property
    @jsii.member(jsii_name="certificateSource")
    def certificate_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateSource"))

    @builtins.property
    @jsii.member(jsii_name="certificateStatus")
    def certificate_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateStatus"))

    @builtins.property
    @jsii.member(jsii_name="expiry")
    def expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiry"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatePasswordInput")
    def certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateIdInput")
    def key_vault_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificateInput")
    def negotiate_client_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negotiateClientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientIdInput")
    def ssl_keyvault_identity_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslKeyvaultIdentityClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e97cb5f73512a27a8aa9cd4905cf46d06b6ad71e8dcdf1dca010cde954ff23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificatePassword")
    def certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificatePassword"))

    @certificate_password.setter
    def certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d628b4c35c9be8bad2d015cb92ca862bd8ec77025666d87c6f373c06d029fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ee1494449fa2ee9b911e3333dfecfffff174748680968db737280b63c55a07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateId")
    def key_vault_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultCertificateId"))

    @key_vault_certificate_id.setter
    def key_vault_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd1e62ae75f679dcd4e65657209b6cac1ab3c7e319645a3f4ad9c36f881f4b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cd3dfb581b24263c074246173fe78feee443e418c2da943087a94425c99772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificate")
    def negotiate_client_certificate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negotiateClientCertificate"))

    @negotiate_client_certificate.setter
    def negotiate_client_certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c0d60e6dc47ab3e661266b06160422833b5acce5735431b51e91c9433325a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negotiateClientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientId")
    def ssl_keyvault_identity_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslKeyvaultIdentityClientId"))

    @ssl_keyvault_identity_client_id.setter
    def ssl_keyvault_identity_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2535e70578957e236dcdb385e879bd27af82493e277364065587e3c97486f103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslKeyvaultIdentityClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationPortal]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationPortal]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationPortal]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0107f6aa75095420b05988990ec8b811699a3d3b862bc371b13cd2419ee4de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationProxy",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "certificate": "certificate",
        "certificate_password": "certificatePassword",
        "default_ssl_binding": "defaultSslBinding",
        "key_vault_certificate_id": "keyVaultCertificateId",
        "key_vault_id": "keyVaultId",
        "negotiate_client_certificate": "negotiateClientCertificate",
        "ssl_keyvault_identity_client_id": "sslKeyvaultIdentityClientId",
    },
)
class ApiManagementHostnameConfigurationProxy:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        certificate: typing.Optional[builtins.str] = None,
        certificate_password: typing.Optional[builtins.str] = None,
        default_ssl_binding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_vault_certificate_id: typing.Optional[builtins.str] = None,
        key_vault_id: typing.Optional[builtins.str] = None,
        negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#host_name ApiManagement#host_name}.
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate ApiManagement#certificate}.
        :param certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate_password ApiManagement#certificate_password}.
        :param default_ssl_binding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#default_ssl_binding ApiManagement#default_ssl_binding}.
        :param key_vault_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_certificate_id ApiManagement#key_vault_certificate_id}.
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_id ApiManagement#key_vault_id}.
        :param negotiate_client_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#negotiate_client_certificate ApiManagement#negotiate_client_certificate}.
        :param ssl_keyvault_identity_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#ssl_keyvault_identity_client_id ApiManagement#ssl_keyvault_identity_client_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4c58fdd0a73f286cf2163bf500c861ac2f367112c9758935f28fe1dfede083d)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_password", value=certificate_password, expected_type=type_hints["certificate_password"])
            check_type(argname="argument default_ssl_binding", value=default_ssl_binding, expected_type=type_hints["default_ssl_binding"])
            check_type(argname="argument key_vault_certificate_id", value=key_vault_certificate_id, expected_type=type_hints["key_vault_certificate_id"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument negotiate_client_certificate", value=negotiate_client_certificate, expected_type=type_hints["negotiate_client_certificate"])
            check_type(argname="argument ssl_keyvault_identity_client_id", value=ssl_keyvault_identity_client_id, expected_type=type_hints["ssl_keyvault_identity_client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_password is not None:
            self._values["certificate_password"] = certificate_password
        if default_ssl_binding is not None:
            self._values["default_ssl_binding"] = default_ssl_binding
        if key_vault_certificate_id is not None:
            self._values["key_vault_certificate_id"] = key_vault_certificate_id
        if key_vault_id is not None:
            self._values["key_vault_id"] = key_vault_id
        if negotiate_client_certificate is not None:
            self._values["negotiate_client_certificate"] = negotiate_client_certificate
        if ssl_keyvault_identity_client_id is not None:
            self._values["ssl_keyvault_identity_client_id"] = ssl_keyvault_identity_client_id

    @builtins.property
    def host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#host_name ApiManagement#host_name}.'''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate ApiManagement#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate_password ApiManagement#certificate_password}.'''
        result = self._values.get("certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_ssl_binding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#default_ssl_binding ApiManagement#default_ssl_binding}.'''
        result = self._values.get("default_ssl_binding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_vault_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_certificate_id ApiManagement#key_vault_certificate_id}.'''
        result = self._values.get("key_vault_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_id ApiManagement#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negotiate_client_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#negotiate_client_certificate ApiManagement#negotiate_client_certificate}.'''
        result = self._values.get("negotiate_client_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_keyvault_identity_client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#ssl_keyvault_identity_client_id ApiManagement#ssl_keyvault_identity_client_id}.'''
        result = self._values.get("ssl_keyvault_identity_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementHostnameConfigurationProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementHostnameConfigurationProxyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationProxyList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8454aad4e922c0816c10374dd2e7795b86283324a75bb594bc10045dbc574bc2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementHostnameConfigurationProxyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f1242550d1276512c83b98f5a7f4f8df8943bf6ebe44af6d1c2d257016bc53a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementHostnameConfigurationProxyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2df80cdffccb0a4744445ed38706319ac9d31b6f391f0de596e6993f535c7a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b95afd42ca7fbf0cb0fa152a1655f05067abe2ac1cad0ceb51a57f79c15a70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__909933a5aa10560129f59e4a9ae0f2efd155b6f47f0ae4dc3d3c952240da5f77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationProxy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationProxy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationProxy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1282b42e5bfa8bb63abef5444d86b1f81b83a4a086e9e14ebd5b7aa9f94715d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementHostnameConfigurationProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationProxyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d08d8200ee4fa5f8a30cea5abbc155e2627d0b42da44f2de64b3c6e05c1c3abf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCertificatePassword")
    def reset_certificate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificatePassword", []))

    @jsii.member(jsii_name="resetDefaultSslBinding")
    def reset_default_ssl_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultSslBinding", []))

    @jsii.member(jsii_name="resetKeyVaultCertificateId")
    def reset_key_vault_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultCertificateId", []))

    @jsii.member(jsii_name="resetKeyVaultId")
    def reset_key_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultId", []))

    @jsii.member(jsii_name="resetNegotiateClientCertificate")
    def reset_negotiate_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegotiateClientCertificate", []))

    @jsii.member(jsii_name="resetSslKeyvaultIdentityClientId")
    def reset_ssl_keyvault_identity_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslKeyvaultIdentityClientId", []))

    @builtins.property
    @jsii.member(jsii_name="certificateSource")
    def certificate_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateSource"))

    @builtins.property
    @jsii.member(jsii_name="certificateStatus")
    def certificate_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateStatus"))

    @builtins.property
    @jsii.member(jsii_name="expiry")
    def expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiry"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatePasswordInput")
    def certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSslBindingInput")
    def default_ssl_binding_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultSslBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateIdInput")
    def key_vault_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificateInput")
    def negotiate_client_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negotiateClientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientIdInput")
    def ssl_keyvault_identity_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslKeyvaultIdentityClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8278aa6c382c67810e6a396e942ebaacadb2fb12a9c950c2a31af74a12a52fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificatePassword")
    def certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificatePassword"))

    @certificate_password.setter
    def certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf39eeed32ab624c5d9650f871442fe256522b9b7da799f6b4d9bfcef5bab808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultSslBinding")
    def default_ssl_binding(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultSslBinding"))

    @default_ssl_binding.setter
    def default_ssl_binding(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb600daa1519189bd8f6dc283c2e71416f0d6465d10dab9328c21414ff383285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSslBinding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60def97d75901d1bde0714729e268e549c282be500aa828f2161068735470cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateId")
    def key_vault_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultCertificateId"))

    @key_vault_certificate_id.setter
    def key_vault_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9d76f61b3ac8167bb50632d6441a225acb6b77f764fa6e0d02e01fcc123413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a94f1204fb99ca131e56bdab44e5a6438ff969dda83d951c61496897db468f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificate")
    def negotiate_client_certificate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negotiateClientCertificate"))

    @negotiate_client_certificate.setter
    def negotiate_client_certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21cc1dedef70d1bfe4a7e577decc926bb56dabb610f8671fcbdb1595a47478be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negotiateClientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientId")
    def ssl_keyvault_identity_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslKeyvaultIdentityClientId"))

    @ssl_keyvault_identity_client_id.setter
    def ssl_keyvault_identity_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d3e3c0a324e596ac910b4517f695f1d68cf6a3707d62dd472f5efb5c4f5d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslKeyvaultIdentityClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationProxy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationProxy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationProxy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5ab774458db6e12350c383579969107a3857103752f941e961c64f291125cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationScm",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "certificate": "certificate",
        "certificate_password": "certificatePassword",
        "key_vault_certificate_id": "keyVaultCertificateId",
        "key_vault_id": "keyVaultId",
        "negotiate_client_certificate": "negotiateClientCertificate",
        "ssl_keyvault_identity_client_id": "sslKeyvaultIdentityClientId",
    },
)
class ApiManagementHostnameConfigurationScm:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        certificate: typing.Optional[builtins.str] = None,
        certificate_password: typing.Optional[builtins.str] = None,
        key_vault_certificate_id: typing.Optional[builtins.str] = None,
        key_vault_id: typing.Optional[builtins.str] = None,
        negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#host_name ApiManagement#host_name}.
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate ApiManagement#certificate}.
        :param certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate_password ApiManagement#certificate_password}.
        :param key_vault_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_certificate_id ApiManagement#key_vault_certificate_id}.
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_id ApiManagement#key_vault_id}.
        :param negotiate_client_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#negotiate_client_certificate ApiManagement#negotiate_client_certificate}.
        :param ssl_keyvault_identity_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#ssl_keyvault_identity_client_id ApiManagement#ssl_keyvault_identity_client_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d875e58e91aabd133dda7af3da03f414a3b3b2cd3e0d4f1a7d01e1ec401359)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_password", value=certificate_password, expected_type=type_hints["certificate_password"])
            check_type(argname="argument key_vault_certificate_id", value=key_vault_certificate_id, expected_type=type_hints["key_vault_certificate_id"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument negotiate_client_certificate", value=negotiate_client_certificate, expected_type=type_hints["negotiate_client_certificate"])
            check_type(argname="argument ssl_keyvault_identity_client_id", value=ssl_keyvault_identity_client_id, expected_type=type_hints["ssl_keyvault_identity_client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_password is not None:
            self._values["certificate_password"] = certificate_password
        if key_vault_certificate_id is not None:
            self._values["key_vault_certificate_id"] = key_vault_certificate_id
        if key_vault_id is not None:
            self._values["key_vault_id"] = key_vault_id
        if negotiate_client_certificate is not None:
            self._values["negotiate_client_certificate"] = negotiate_client_certificate
        if ssl_keyvault_identity_client_id is not None:
            self._values["ssl_keyvault_identity_client_id"] = ssl_keyvault_identity_client_id

    @builtins.property
    def host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#host_name ApiManagement#host_name}.'''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate ApiManagement#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#certificate_password ApiManagement#certificate_password}.'''
        result = self._values.get("certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_certificate_id ApiManagement#key_vault_certificate_id}.'''
        result = self._values.get("key_vault_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#key_vault_id ApiManagement#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negotiate_client_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#negotiate_client_certificate ApiManagement#negotiate_client_certificate}.'''
        result = self._values.get("negotiate_client_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_keyvault_identity_client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#ssl_keyvault_identity_client_id ApiManagement#ssl_keyvault_identity_client_id}.'''
        result = self._values.get("ssl_keyvault_identity_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementHostnameConfigurationScm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementHostnameConfigurationScmList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationScmList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac20acba3367d13533b527b584e8b267fff0f1e09ad0927f1dec1a52fb553db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementHostnameConfigurationScmOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1547dbfb4019376c7e9a000588bf3a82c6e6d5934842c9a4354f4fd589f5d99f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementHostnameConfigurationScmOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5150b14176d47c300e62aaa94c5ef5a2c4ee2d9e084028de06ef3e50821c941d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0dffd974ce4a7b008ff390fee824471d2a35241ba208ec4962e22dbef9abf5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09aaaf538efc844a9cff0306a1a300069e20dab108ad5b15bf4663e1b8eb10b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationScm]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationScm]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationScm]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80acf94d3fbfe23d2af4ea42af6aa9eea8aa6f9e814204321aac6053bbee0769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementHostnameConfigurationScmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementHostnameConfigurationScmOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f30d1051f7c8a4b77c739f016a10333fcc182e18c727502fbbe21ea1aed5828)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCertificatePassword")
    def reset_certificate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificatePassword", []))

    @jsii.member(jsii_name="resetKeyVaultCertificateId")
    def reset_key_vault_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultCertificateId", []))

    @jsii.member(jsii_name="resetKeyVaultId")
    def reset_key_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultId", []))

    @jsii.member(jsii_name="resetNegotiateClientCertificate")
    def reset_negotiate_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegotiateClientCertificate", []))

    @jsii.member(jsii_name="resetSslKeyvaultIdentityClientId")
    def reset_ssl_keyvault_identity_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslKeyvaultIdentityClientId", []))

    @builtins.property
    @jsii.member(jsii_name="certificateSource")
    def certificate_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateSource"))

    @builtins.property
    @jsii.member(jsii_name="certificateStatus")
    def certificate_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateStatus"))

    @builtins.property
    @jsii.member(jsii_name="expiry")
    def expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiry"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatePasswordInput")
    def certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateIdInput")
    def key_vault_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificateInput")
    def negotiate_client_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negotiateClientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientIdInput")
    def ssl_keyvault_identity_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslKeyvaultIdentityClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e771a698f1261c58e6c654cdc188999c382c1deefa6c65f8bc9276ff23886b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificatePassword")
    def certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificatePassword"))

    @certificate_password.setter
    def certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ac2a1554a1aa5fe235c26327f45cb601c725cbd8c83014a18b0732a5676add)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b905ae4e8f480849fabf47bc6199c516c5cd56ef6565a12b30e6dc9b86784104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateId")
    def key_vault_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultCertificateId"))

    @key_vault_certificate_id.setter
    def key_vault_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce230c7932849360c559e0a34b08efc7b03f46cac6504ab2bb1d6f03940ec1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4d5bc9892a7b39662e53e3698ce3cbc75d40801f9cc8f25498d0ef81d3b860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificate")
    def negotiate_client_certificate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negotiateClientCertificate"))

    @negotiate_client_certificate.setter
    def negotiate_client_certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5dc8b70fc09a9f9c0119d761b51c12c05e12e09b786ee01d428e1834815f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negotiateClientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientId")
    def ssl_keyvault_identity_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslKeyvaultIdentityClientId"))

    @ssl_keyvault_identity_client_id.setter
    def ssl_keyvault_identity_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4275df00fc832caf89b3d8a479a19a2e23185911686d147434c3cd7821729528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslKeyvaultIdentityClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationScm]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationScm]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationScm]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c2d0fe3a1593d2fa681694ae9eaa6415455642d234b3f884ed14707fd2b8f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class ApiManagementIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#type ApiManagement#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#identity_ids ApiManagement#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ebb50749da3be1aaa91016c940d1d303d711ded4dcae4df53456befaba96a07)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#type ApiManagement#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#identity_ids ApiManagement#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementIdentityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe50a52b8151e0a730d998e2d0c2e29dc05c2b5d9d2c9f26941be64ef1b8792)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a541f0fd0b6ec51155d7e187384ec5a9f333bffc7b8f2fbdacccd23fd27df711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__340632f92da70df5fe36cbaf5b7cfcf8ef74661d64277e81e8a161857cf57138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementIdentity]:
        return typing.cast(typing.Optional[ApiManagementIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApiManagementIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbeb5dcda97f2cfb10048dca2919571465077e25ed229d070a5f4779da7c96f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementProtocols",
    jsii_struct_bases=[],
    name_mapping={"enable_http2": "enableHttp2", "http2_enabled": "http2Enabled"},
)
class ApiManagementProtocols:
    def __init__(
        self,
        *,
        enable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_http2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_http2 ApiManagement#enable_http2}.
        :param http2_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#http2_enabled ApiManagement#http2_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f33ffc92308f03d5b10d6fc2038e3f47eb547ffdbd79c414eb542ed21add255)
            check_type(argname="argument enable_http2", value=enable_http2, expected_type=type_hints["enable_http2"])
            check_type(argname="argument http2_enabled", value=http2_enabled, expected_type=type_hints["http2_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_http2 is not None:
            self._values["enable_http2"] = enable_http2
        if http2_enabled is not None:
            self._values["http2_enabled"] = http2_enabled

    @builtins.property
    def enable_http2(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_http2 ApiManagement#enable_http2}.'''
        result = self._values.get("enable_http2")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http2_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#http2_enabled ApiManagement#http2_enabled}.'''
        result = self._values.get("http2_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementProtocols(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementProtocolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementProtocolsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e80fe60aef246c44726fd716befd3d3c00a18a0efa247c9adea76eabffe942e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableHttp2")
    def reset_enable_http2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableHttp2", []))

    @jsii.member(jsii_name="resetHttp2Enabled")
    def reset_http2_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp2Enabled", []))

    @builtins.property
    @jsii.member(jsii_name="enableHttp2Input")
    def enable_http2_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHttp2Input"))

    @builtins.property
    @jsii.member(jsii_name="http2EnabledInput")
    def http2_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "http2EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHttp2")
    def enable_http2(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHttp2"))

    @enable_http2.setter
    def enable_http2(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2741f43a9dbd864de0fb35ff0147fb3246eedd69196002f0746b5458a4e3f87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHttp2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="http2Enabled")
    def http2_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "http2Enabled"))

    @http2_enabled.setter
    def http2_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5bafa598fb126fe2cd2c6120bec3540706f0379d8c994443757c3105b1dccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "http2Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementProtocols]:
        return typing.cast(typing.Optional[ApiManagementProtocols], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApiManagementProtocols]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d8f9a1f9004a0445e7561129e42d4d673cf41033344543b8e8726770d3055a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementSecurity",
    jsii_struct_bases=[],
    name_mapping={
        "backend_ssl30_enabled": "backendSsl30Enabled",
        "backend_tls10_enabled": "backendTls10Enabled",
        "backend_tls11_enabled": "backendTls11Enabled",
        "enable_backend_ssl30": "enableBackendSsl30",
        "enable_backend_tls10": "enableBackendTls10",
        "enable_backend_tls11": "enableBackendTls11",
        "enable_frontend_ssl30": "enableFrontendSsl30",
        "enable_frontend_tls10": "enableFrontendTls10",
        "enable_frontend_tls11": "enableFrontendTls11",
        "frontend_ssl30_enabled": "frontendSsl30Enabled",
        "frontend_tls10_enabled": "frontendTls10Enabled",
        "frontend_tls11_enabled": "frontendTls11Enabled",
        "tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled": "tlsEcdheEcdsaWithAes128CbcShaCiphersEnabled",
        "tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled": "tlsEcdheEcdsaWithAes256CbcShaCiphersEnabled",
        "tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled": "tlsEcdheRsaWithAes128CbcShaCiphersEnabled",
        "tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled": "tlsEcdheRsaWithAes256CbcShaCiphersEnabled",
        "tls_rsa_with_aes128_cbc_sha256_ciphers_enabled": "tlsRsaWithAes128CbcSha256CiphersEnabled",
        "tls_rsa_with_aes128_cbc_sha_ciphers_enabled": "tlsRsaWithAes128CbcShaCiphersEnabled",
        "tls_rsa_with_aes128_gcm_sha256_ciphers_enabled": "tlsRsaWithAes128GcmSha256CiphersEnabled",
        "tls_rsa_with_aes256_cbc_sha256_ciphers_enabled": "tlsRsaWithAes256CbcSha256CiphersEnabled",
        "tls_rsa_with_aes256_cbc_sha_ciphers_enabled": "tlsRsaWithAes256CbcShaCiphersEnabled",
        "tls_rsa_with_aes256_gcm_sha384_ciphers_enabled": "tlsRsaWithAes256GcmSha384CiphersEnabled",
        "triple_des_ciphers_enabled": "tripleDesCiphersEnabled",
    },
)
class ApiManagementSecurity:
    def __init__(
        self,
        *,
        backend_ssl30_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backend_tls10_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backend_tls11_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_backend_ssl30: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_backend_tls10: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_backend_tls11: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_frontend_ssl30: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_frontend_tls10: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_frontend_tls11: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        frontend_ssl30_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        frontend_tls10_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        frontend_tls11_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_rsa_with_aes128_cbc_sha256_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_rsa_with_aes128_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_rsa_with_aes128_gcm_sha256_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_rsa_with_aes256_cbc_sha256_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_rsa_with_aes256_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_rsa_with_aes256_gcm_sha384_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        triple_des_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param backend_ssl30_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#backend_ssl30_enabled ApiManagement#backend_ssl30_enabled}.
        :param backend_tls10_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#backend_tls10_enabled ApiManagement#backend_tls10_enabled}.
        :param backend_tls11_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#backend_tls11_enabled ApiManagement#backend_tls11_enabled}.
        :param enable_backend_ssl30: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_backend_ssl30 ApiManagement#enable_backend_ssl30}.
        :param enable_backend_tls10: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_backend_tls10 ApiManagement#enable_backend_tls10}.
        :param enable_backend_tls11: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_backend_tls11 ApiManagement#enable_backend_tls11}.
        :param enable_frontend_ssl30: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_frontend_ssl30 ApiManagement#enable_frontend_ssl30}.
        :param enable_frontend_tls10: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_frontend_tls10 ApiManagement#enable_frontend_tls10}.
        :param enable_frontend_tls11: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_frontend_tls11 ApiManagement#enable_frontend_tls11}.
        :param frontend_ssl30_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#frontend_ssl30_enabled ApiManagement#frontend_ssl30_enabled}.
        :param frontend_tls10_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#frontend_tls10_enabled ApiManagement#frontend_tls10_enabled}.
        :param frontend_tls11_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#frontend_tls11_enabled ApiManagement#frontend_tls11_enabled}.
        :param tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled ApiManagement#tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled}.
        :param tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled ApiManagement#tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled}.
        :param tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled ApiManagement#tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled}.
        :param tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled ApiManagement#tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled}.
        :param tls_rsa_with_aes128_cbc_sha256_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes128_cbc_sha256_ciphers_enabled ApiManagement#tls_rsa_with_aes128_cbc_sha256_ciphers_enabled}.
        :param tls_rsa_with_aes128_cbc_sha_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes128_cbc_sha_ciphers_enabled ApiManagement#tls_rsa_with_aes128_cbc_sha_ciphers_enabled}.
        :param tls_rsa_with_aes128_gcm_sha256_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes128_gcm_sha256_ciphers_enabled ApiManagement#tls_rsa_with_aes128_gcm_sha256_ciphers_enabled}.
        :param tls_rsa_with_aes256_cbc_sha256_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes256_cbc_sha256_ciphers_enabled ApiManagement#tls_rsa_with_aes256_cbc_sha256_ciphers_enabled}.
        :param tls_rsa_with_aes256_cbc_sha_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes256_cbc_sha_ciphers_enabled ApiManagement#tls_rsa_with_aes256_cbc_sha_ciphers_enabled}.
        :param tls_rsa_with_aes256_gcm_sha384_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes256_gcm_sha384_ciphers_enabled ApiManagement#tls_rsa_with_aes256_gcm_sha384_ciphers_enabled}.
        :param triple_des_ciphers_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#triple_des_ciphers_enabled ApiManagement#triple_des_ciphers_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d583cef33a75d205188512d8e56e76a3a1ebacb0c2b679c1a8db76e1302badca)
            check_type(argname="argument backend_ssl30_enabled", value=backend_ssl30_enabled, expected_type=type_hints["backend_ssl30_enabled"])
            check_type(argname="argument backend_tls10_enabled", value=backend_tls10_enabled, expected_type=type_hints["backend_tls10_enabled"])
            check_type(argname="argument backend_tls11_enabled", value=backend_tls11_enabled, expected_type=type_hints["backend_tls11_enabled"])
            check_type(argname="argument enable_backend_ssl30", value=enable_backend_ssl30, expected_type=type_hints["enable_backend_ssl30"])
            check_type(argname="argument enable_backend_tls10", value=enable_backend_tls10, expected_type=type_hints["enable_backend_tls10"])
            check_type(argname="argument enable_backend_tls11", value=enable_backend_tls11, expected_type=type_hints["enable_backend_tls11"])
            check_type(argname="argument enable_frontend_ssl30", value=enable_frontend_ssl30, expected_type=type_hints["enable_frontend_ssl30"])
            check_type(argname="argument enable_frontend_tls10", value=enable_frontend_tls10, expected_type=type_hints["enable_frontend_tls10"])
            check_type(argname="argument enable_frontend_tls11", value=enable_frontend_tls11, expected_type=type_hints["enable_frontend_tls11"])
            check_type(argname="argument frontend_ssl30_enabled", value=frontend_ssl30_enabled, expected_type=type_hints["frontend_ssl30_enabled"])
            check_type(argname="argument frontend_tls10_enabled", value=frontend_tls10_enabled, expected_type=type_hints["frontend_tls10_enabled"])
            check_type(argname="argument frontend_tls11_enabled", value=frontend_tls11_enabled, expected_type=type_hints["frontend_tls11_enabled"])
            check_type(argname="argument tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled", value=tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled, expected_type=type_hints["tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled"])
            check_type(argname="argument tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled", value=tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled, expected_type=type_hints["tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled"])
            check_type(argname="argument tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled", value=tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled, expected_type=type_hints["tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled"])
            check_type(argname="argument tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled", value=tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled, expected_type=type_hints["tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled"])
            check_type(argname="argument tls_rsa_with_aes128_cbc_sha256_ciphers_enabled", value=tls_rsa_with_aes128_cbc_sha256_ciphers_enabled, expected_type=type_hints["tls_rsa_with_aes128_cbc_sha256_ciphers_enabled"])
            check_type(argname="argument tls_rsa_with_aes128_cbc_sha_ciphers_enabled", value=tls_rsa_with_aes128_cbc_sha_ciphers_enabled, expected_type=type_hints["tls_rsa_with_aes128_cbc_sha_ciphers_enabled"])
            check_type(argname="argument tls_rsa_with_aes128_gcm_sha256_ciphers_enabled", value=tls_rsa_with_aes128_gcm_sha256_ciphers_enabled, expected_type=type_hints["tls_rsa_with_aes128_gcm_sha256_ciphers_enabled"])
            check_type(argname="argument tls_rsa_with_aes256_cbc_sha256_ciphers_enabled", value=tls_rsa_with_aes256_cbc_sha256_ciphers_enabled, expected_type=type_hints["tls_rsa_with_aes256_cbc_sha256_ciphers_enabled"])
            check_type(argname="argument tls_rsa_with_aes256_cbc_sha_ciphers_enabled", value=tls_rsa_with_aes256_cbc_sha_ciphers_enabled, expected_type=type_hints["tls_rsa_with_aes256_cbc_sha_ciphers_enabled"])
            check_type(argname="argument tls_rsa_with_aes256_gcm_sha384_ciphers_enabled", value=tls_rsa_with_aes256_gcm_sha384_ciphers_enabled, expected_type=type_hints["tls_rsa_with_aes256_gcm_sha384_ciphers_enabled"])
            check_type(argname="argument triple_des_ciphers_enabled", value=triple_des_ciphers_enabled, expected_type=type_hints["triple_des_ciphers_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backend_ssl30_enabled is not None:
            self._values["backend_ssl30_enabled"] = backend_ssl30_enabled
        if backend_tls10_enabled is not None:
            self._values["backend_tls10_enabled"] = backend_tls10_enabled
        if backend_tls11_enabled is not None:
            self._values["backend_tls11_enabled"] = backend_tls11_enabled
        if enable_backend_ssl30 is not None:
            self._values["enable_backend_ssl30"] = enable_backend_ssl30
        if enable_backend_tls10 is not None:
            self._values["enable_backend_tls10"] = enable_backend_tls10
        if enable_backend_tls11 is not None:
            self._values["enable_backend_tls11"] = enable_backend_tls11
        if enable_frontend_ssl30 is not None:
            self._values["enable_frontend_ssl30"] = enable_frontend_ssl30
        if enable_frontend_tls10 is not None:
            self._values["enable_frontend_tls10"] = enable_frontend_tls10
        if enable_frontend_tls11 is not None:
            self._values["enable_frontend_tls11"] = enable_frontend_tls11
        if frontend_ssl30_enabled is not None:
            self._values["frontend_ssl30_enabled"] = frontend_ssl30_enabled
        if frontend_tls10_enabled is not None:
            self._values["frontend_tls10_enabled"] = frontend_tls10_enabled
        if frontend_tls11_enabled is not None:
            self._values["frontend_tls11_enabled"] = frontend_tls11_enabled
        if tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled is not None:
            self._values["tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled"] = tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled
        if tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled is not None:
            self._values["tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled"] = tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled
        if tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled is not None:
            self._values["tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled"] = tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled
        if tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled is not None:
            self._values["tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled"] = tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled
        if tls_rsa_with_aes128_cbc_sha256_ciphers_enabled is not None:
            self._values["tls_rsa_with_aes128_cbc_sha256_ciphers_enabled"] = tls_rsa_with_aes128_cbc_sha256_ciphers_enabled
        if tls_rsa_with_aes128_cbc_sha_ciphers_enabled is not None:
            self._values["tls_rsa_with_aes128_cbc_sha_ciphers_enabled"] = tls_rsa_with_aes128_cbc_sha_ciphers_enabled
        if tls_rsa_with_aes128_gcm_sha256_ciphers_enabled is not None:
            self._values["tls_rsa_with_aes128_gcm_sha256_ciphers_enabled"] = tls_rsa_with_aes128_gcm_sha256_ciphers_enabled
        if tls_rsa_with_aes256_cbc_sha256_ciphers_enabled is not None:
            self._values["tls_rsa_with_aes256_cbc_sha256_ciphers_enabled"] = tls_rsa_with_aes256_cbc_sha256_ciphers_enabled
        if tls_rsa_with_aes256_cbc_sha_ciphers_enabled is not None:
            self._values["tls_rsa_with_aes256_cbc_sha_ciphers_enabled"] = tls_rsa_with_aes256_cbc_sha_ciphers_enabled
        if tls_rsa_with_aes256_gcm_sha384_ciphers_enabled is not None:
            self._values["tls_rsa_with_aes256_gcm_sha384_ciphers_enabled"] = tls_rsa_with_aes256_gcm_sha384_ciphers_enabled
        if triple_des_ciphers_enabled is not None:
            self._values["triple_des_ciphers_enabled"] = triple_des_ciphers_enabled

    @builtins.property
    def backend_ssl30_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#backend_ssl30_enabled ApiManagement#backend_ssl30_enabled}.'''
        result = self._values.get("backend_ssl30_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def backend_tls10_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#backend_tls10_enabled ApiManagement#backend_tls10_enabled}.'''
        result = self._values.get("backend_tls10_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def backend_tls11_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#backend_tls11_enabled ApiManagement#backend_tls11_enabled}.'''
        result = self._values.get("backend_tls11_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_backend_ssl30(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_backend_ssl30 ApiManagement#enable_backend_ssl30}.'''
        result = self._values.get("enable_backend_ssl30")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_backend_tls10(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_backend_tls10 ApiManagement#enable_backend_tls10}.'''
        result = self._values.get("enable_backend_tls10")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_backend_tls11(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_backend_tls11 ApiManagement#enable_backend_tls11}.'''
        result = self._values.get("enable_backend_tls11")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_frontend_ssl30(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_frontend_ssl30 ApiManagement#enable_frontend_ssl30}.'''
        result = self._values.get("enable_frontend_ssl30")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_frontend_tls10(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_frontend_tls10 ApiManagement#enable_frontend_tls10}.'''
        result = self._values.get("enable_frontend_tls10")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_frontend_tls11(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enable_frontend_tls11 ApiManagement#enable_frontend_tls11}.'''
        result = self._values.get("enable_frontend_tls11")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def frontend_ssl30_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#frontend_ssl30_enabled ApiManagement#frontend_ssl30_enabled}.'''
        result = self._values.get("frontend_ssl30_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def frontend_tls10_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#frontend_tls10_enabled ApiManagement#frontend_tls10_enabled}.'''
        result = self._values.get("frontend_tls10_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def frontend_tls11_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#frontend_tls11_enabled ApiManagement#frontend_tls11_enabled}.'''
        result = self._values.get("frontend_tls11_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled ApiManagement#tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled}.'''
        result = self._values.get("tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled ApiManagement#tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled}.'''
        result = self._values.get("tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled ApiManagement#tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled}.'''
        result = self._values.get("tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled ApiManagement#tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled}.'''
        result = self._values.get("tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tls_rsa_with_aes128_cbc_sha256_ciphers_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes128_cbc_sha256_ciphers_enabled ApiManagement#tls_rsa_with_aes128_cbc_sha256_ciphers_enabled}.'''
        result = self._values.get("tls_rsa_with_aes128_cbc_sha256_ciphers_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tls_rsa_with_aes128_cbc_sha_ciphers_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes128_cbc_sha_ciphers_enabled ApiManagement#tls_rsa_with_aes128_cbc_sha_ciphers_enabled}.'''
        result = self._values.get("tls_rsa_with_aes128_cbc_sha_ciphers_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tls_rsa_with_aes128_gcm_sha256_ciphers_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes128_gcm_sha256_ciphers_enabled ApiManagement#tls_rsa_with_aes128_gcm_sha256_ciphers_enabled}.'''
        result = self._values.get("tls_rsa_with_aes128_gcm_sha256_ciphers_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tls_rsa_with_aes256_cbc_sha256_ciphers_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes256_cbc_sha256_ciphers_enabled ApiManagement#tls_rsa_with_aes256_cbc_sha256_ciphers_enabled}.'''
        result = self._values.get("tls_rsa_with_aes256_cbc_sha256_ciphers_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tls_rsa_with_aes256_cbc_sha_ciphers_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes256_cbc_sha_ciphers_enabled ApiManagement#tls_rsa_with_aes256_cbc_sha_ciphers_enabled}.'''
        result = self._values.get("tls_rsa_with_aes256_cbc_sha_ciphers_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tls_rsa_with_aes256_gcm_sha384_ciphers_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#tls_rsa_with_aes256_gcm_sha384_ciphers_enabled ApiManagement#tls_rsa_with_aes256_gcm_sha384_ciphers_enabled}.'''
        result = self._values.get("tls_rsa_with_aes256_gcm_sha384_ciphers_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def triple_des_ciphers_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#triple_des_ciphers_enabled ApiManagement#triple_des_ciphers_enabled}.'''
        result = self._values.get("triple_des_ciphers_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementSecurity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementSecurityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementSecurityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a51892296824ccc6b1390a45c9c523115cc3ddbc26a906d0b03ad20fbad6c2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackendSsl30Enabled")
    def reset_backend_ssl30_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendSsl30Enabled", []))

    @jsii.member(jsii_name="resetBackendTls10Enabled")
    def reset_backend_tls10_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendTls10Enabled", []))

    @jsii.member(jsii_name="resetBackendTls11Enabled")
    def reset_backend_tls11_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendTls11Enabled", []))

    @jsii.member(jsii_name="resetEnableBackendSsl30")
    def reset_enable_backend_ssl30(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableBackendSsl30", []))

    @jsii.member(jsii_name="resetEnableBackendTls10")
    def reset_enable_backend_tls10(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableBackendTls10", []))

    @jsii.member(jsii_name="resetEnableBackendTls11")
    def reset_enable_backend_tls11(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableBackendTls11", []))

    @jsii.member(jsii_name="resetEnableFrontendSsl30")
    def reset_enable_frontend_ssl30(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableFrontendSsl30", []))

    @jsii.member(jsii_name="resetEnableFrontendTls10")
    def reset_enable_frontend_tls10(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableFrontendTls10", []))

    @jsii.member(jsii_name="resetEnableFrontendTls11")
    def reset_enable_frontend_tls11(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableFrontendTls11", []))

    @jsii.member(jsii_name="resetFrontendSsl30Enabled")
    def reset_frontend_ssl30_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrontendSsl30Enabled", []))

    @jsii.member(jsii_name="resetFrontendTls10Enabled")
    def reset_frontend_tls10_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrontendTls10Enabled", []))

    @jsii.member(jsii_name="resetFrontendTls11Enabled")
    def reset_frontend_tls11_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrontendTls11Enabled", []))

    @jsii.member(jsii_name="resetTlsEcdheEcdsaWithAes128CbcShaCiphersEnabled")
    def reset_tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsEcdheEcdsaWithAes128CbcShaCiphersEnabled", []))

    @jsii.member(jsii_name="resetTlsEcdheEcdsaWithAes256CbcShaCiphersEnabled")
    def reset_tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsEcdheEcdsaWithAes256CbcShaCiphersEnabled", []))

    @jsii.member(jsii_name="resetTlsEcdheRsaWithAes128CbcShaCiphersEnabled")
    def reset_tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsEcdheRsaWithAes128CbcShaCiphersEnabled", []))

    @jsii.member(jsii_name="resetTlsEcdheRsaWithAes256CbcShaCiphersEnabled")
    def reset_tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsEcdheRsaWithAes256CbcShaCiphersEnabled", []))

    @jsii.member(jsii_name="resetTlsRsaWithAes128CbcSha256CiphersEnabled")
    def reset_tls_rsa_with_aes128_cbc_sha256_ciphers_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsRsaWithAes128CbcSha256CiphersEnabled", []))

    @jsii.member(jsii_name="resetTlsRsaWithAes128CbcShaCiphersEnabled")
    def reset_tls_rsa_with_aes128_cbc_sha_ciphers_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsRsaWithAes128CbcShaCiphersEnabled", []))

    @jsii.member(jsii_name="resetTlsRsaWithAes128GcmSha256CiphersEnabled")
    def reset_tls_rsa_with_aes128_gcm_sha256_ciphers_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsRsaWithAes128GcmSha256CiphersEnabled", []))

    @jsii.member(jsii_name="resetTlsRsaWithAes256CbcSha256CiphersEnabled")
    def reset_tls_rsa_with_aes256_cbc_sha256_ciphers_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsRsaWithAes256CbcSha256CiphersEnabled", []))

    @jsii.member(jsii_name="resetTlsRsaWithAes256CbcShaCiphersEnabled")
    def reset_tls_rsa_with_aes256_cbc_sha_ciphers_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsRsaWithAes256CbcShaCiphersEnabled", []))

    @jsii.member(jsii_name="resetTlsRsaWithAes256GcmSha384CiphersEnabled")
    def reset_tls_rsa_with_aes256_gcm_sha384_ciphers_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsRsaWithAes256GcmSha384CiphersEnabled", []))

    @jsii.member(jsii_name="resetTripleDesCiphersEnabled")
    def reset_triple_des_ciphers_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTripleDesCiphersEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="backendSsl30EnabledInput")
    def backend_ssl30_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "backendSsl30EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="backendTls10EnabledInput")
    def backend_tls10_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "backendTls10EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="backendTls11EnabledInput")
    def backend_tls11_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "backendTls11EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enableBackendSsl30Input")
    def enable_backend_ssl30_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableBackendSsl30Input"))

    @builtins.property
    @jsii.member(jsii_name="enableBackendTls10Input")
    def enable_backend_tls10_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableBackendTls10Input"))

    @builtins.property
    @jsii.member(jsii_name="enableBackendTls11Input")
    def enable_backend_tls11_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableBackendTls11Input"))

    @builtins.property
    @jsii.member(jsii_name="enableFrontendSsl30Input")
    def enable_frontend_ssl30_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableFrontendSsl30Input"))

    @builtins.property
    @jsii.member(jsii_name="enableFrontendTls10Input")
    def enable_frontend_tls10_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableFrontendTls10Input"))

    @builtins.property
    @jsii.member(jsii_name="enableFrontendTls11Input")
    def enable_frontend_tls11_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableFrontendTls11Input"))

    @builtins.property
    @jsii.member(jsii_name="frontendSsl30EnabledInput")
    def frontend_ssl30_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "frontendSsl30EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendTls10EnabledInput")
    def frontend_tls10_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "frontendTls10EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendTls11EnabledInput")
    def frontend_tls11_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "frontendTls11EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsEcdheEcdsaWithAes128CbcShaCiphersEnabledInput")
    def tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsEcdheEcdsaWithAes128CbcShaCiphersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsEcdheEcdsaWithAes256CbcShaCiphersEnabledInput")
    def tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsEcdheEcdsaWithAes256CbcShaCiphersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsEcdheRsaWithAes128CbcShaCiphersEnabledInput")
    def tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsEcdheRsaWithAes128CbcShaCiphersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsEcdheRsaWithAes256CbcShaCiphersEnabledInput")
    def tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsEcdheRsaWithAes256CbcShaCiphersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsRsaWithAes128CbcSha256CiphersEnabledInput")
    def tls_rsa_with_aes128_cbc_sha256_ciphers_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsRsaWithAes128CbcSha256CiphersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsRsaWithAes128CbcShaCiphersEnabledInput")
    def tls_rsa_with_aes128_cbc_sha_ciphers_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsRsaWithAes128CbcShaCiphersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsRsaWithAes128GcmSha256CiphersEnabledInput")
    def tls_rsa_with_aes128_gcm_sha256_ciphers_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsRsaWithAes128GcmSha256CiphersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsRsaWithAes256CbcSha256CiphersEnabledInput")
    def tls_rsa_with_aes256_cbc_sha256_ciphers_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsRsaWithAes256CbcSha256CiphersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsRsaWithAes256CbcShaCiphersEnabledInput")
    def tls_rsa_with_aes256_cbc_sha_ciphers_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsRsaWithAes256CbcShaCiphersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsRsaWithAes256GcmSha384CiphersEnabledInput")
    def tls_rsa_with_aes256_gcm_sha384_ciphers_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsRsaWithAes256GcmSha384CiphersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tripleDesCiphersEnabledInput")
    def triple_des_ciphers_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tripleDesCiphersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="backendSsl30Enabled")
    def backend_ssl30_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "backendSsl30Enabled"))

    @backend_ssl30_enabled.setter
    def backend_ssl30_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9e38d989893ab7b0fe27e1a1ce334ea0ec3fdc3857e282baf005c17c85c2f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendSsl30Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backendTls10Enabled")
    def backend_tls10_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "backendTls10Enabled"))

    @backend_tls10_enabled.setter
    def backend_tls10_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__757519f97e9033b463da62f03c55491cde1cc0d427ab4c0f28aa48a4b4cce85b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendTls10Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backendTls11Enabled")
    def backend_tls11_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "backendTls11Enabled"))

    @backend_tls11_enabled.setter
    def backend_tls11_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d89f23997732d958447bb9a6ba0d3ad0e651961995bfb35dd888e93f99191b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendTls11Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableBackendSsl30")
    def enable_backend_ssl30(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableBackendSsl30"))

    @enable_backend_ssl30.setter
    def enable_backend_ssl30(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a4669bd63928fd9f0ce9e44cea7018b9f2f09e1eae685c3b0b06dffee81eba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableBackendSsl30", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableBackendTls10")
    def enable_backend_tls10(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableBackendTls10"))

    @enable_backend_tls10.setter
    def enable_backend_tls10(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb767c6da094787fc0fbfc8c5eccc0a20ce2a784b0ee8394255953b995490b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableBackendTls10", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableBackendTls11")
    def enable_backend_tls11(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableBackendTls11"))

    @enable_backend_tls11.setter
    def enable_backend_tls11(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882eaa6550972d7f1696e4a79781306c170134828bd7d8b93407bcf07da306b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableBackendTls11", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableFrontendSsl30")
    def enable_frontend_ssl30(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableFrontendSsl30"))

    @enable_frontend_ssl30.setter
    def enable_frontend_ssl30(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f91de5e55a4134385cba3ce39093c52f1f4cfb32be97aa279dffaec657818f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableFrontendSsl30", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableFrontendTls10")
    def enable_frontend_tls10(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableFrontendTls10"))

    @enable_frontend_tls10.setter
    def enable_frontend_tls10(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b28579376caa9408b22c66b84ff5ad9097220059ccbdc0d6c9cd2cb6b1953b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableFrontendTls10", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableFrontendTls11")
    def enable_frontend_tls11(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableFrontendTls11"))

    @enable_frontend_tls11.setter
    def enable_frontend_tls11(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f189c3fd0b56ba0cb26154e4a16df53bc5f4991b1ae2b4a31a074f325fbaab33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableFrontendTls11", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frontendSsl30Enabled")
    def frontend_ssl30_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "frontendSsl30Enabled"))

    @frontend_ssl30_enabled.setter
    def frontend_ssl30_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31cbcb2cb595435e37f2783303eb0be8382faf0e96ab4a92e754180c73367ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frontendSsl30Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frontendTls10Enabled")
    def frontend_tls10_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "frontendTls10Enabled"))

    @frontend_tls10_enabled.setter
    def frontend_tls10_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa62f179f7b52ef7e90c5a800411cabbf41bf84db151ade6ca2f7711d16f20e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frontendTls10Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frontendTls11Enabled")
    def frontend_tls11_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "frontendTls11Enabled"))

    @frontend_tls11_enabled.setter
    def frontend_tls11_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ece2848fe139c1bd108b01b412387a48108055473c73fb6d97b23ed98ffa713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frontendTls11Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsEcdheEcdsaWithAes128CbcShaCiphersEnabled")
    def tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsEcdheEcdsaWithAes128CbcShaCiphersEnabled"))

    @tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled.setter
    def tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__260bb5674d4985e203c935fcf0ae473c965e69e6b367ea71c5f063806a655ae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsEcdheEcdsaWithAes128CbcShaCiphersEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsEcdheEcdsaWithAes256CbcShaCiphersEnabled")
    def tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsEcdheEcdsaWithAes256CbcShaCiphersEnabled"))

    @tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled.setter
    def tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be08522a481247a83ad8e839774e2be33a569bc5bb2d0bbaa867f311db5b18d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsEcdheEcdsaWithAes256CbcShaCiphersEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsEcdheRsaWithAes128CbcShaCiphersEnabled")
    def tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsEcdheRsaWithAes128CbcShaCiphersEnabled"))

    @tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled.setter
    def tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efbd3a4fb3386f8601698a127953ecf1e7c5f36a4f3814a0d0599cde3fa8467f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsEcdheRsaWithAes128CbcShaCiphersEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsEcdheRsaWithAes256CbcShaCiphersEnabled")
    def tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsEcdheRsaWithAes256CbcShaCiphersEnabled"))

    @tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled.setter
    def tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bcd3ff5494e1a5c59aa6912189cf3c8d8b206709a1f47e468546f05b344c9ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsEcdheRsaWithAes256CbcShaCiphersEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsRsaWithAes128CbcSha256CiphersEnabled")
    def tls_rsa_with_aes128_cbc_sha256_ciphers_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsRsaWithAes128CbcSha256CiphersEnabled"))

    @tls_rsa_with_aes128_cbc_sha256_ciphers_enabled.setter
    def tls_rsa_with_aes128_cbc_sha256_ciphers_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf0493044cd76a0f64548ce706625b3eee7fe56ba7e17b56321329750fa50ab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsRsaWithAes128CbcSha256CiphersEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsRsaWithAes128CbcShaCiphersEnabled")
    def tls_rsa_with_aes128_cbc_sha_ciphers_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsRsaWithAes128CbcShaCiphersEnabled"))

    @tls_rsa_with_aes128_cbc_sha_ciphers_enabled.setter
    def tls_rsa_with_aes128_cbc_sha_ciphers_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeef43043f47fe03e2114d0732c99e9873642758b2b3df357d66b57c33b595ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsRsaWithAes128CbcShaCiphersEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsRsaWithAes128GcmSha256CiphersEnabled")
    def tls_rsa_with_aes128_gcm_sha256_ciphers_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsRsaWithAes128GcmSha256CiphersEnabled"))

    @tls_rsa_with_aes128_gcm_sha256_ciphers_enabled.setter
    def tls_rsa_with_aes128_gcm_sha256_ciphers_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9271b2393eaf562a9a64fdfec47a673c3d787f6002c75c46e1f311e151ccc817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsRsaWithAes128GcmSha256CiphersEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsRsaWithAes256CbcSha256CiphersEnabled")
    def tls_rsa_with_aes256_cbc_sha256_ciphers_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsRsaWithAes256CbcSha256CiphersEnabled"))

    @tls_rsa_with_aes256_cbc_sha256_ciphers_enabled.setter
    def tls_rsa_with_aes256_cbc_sha256_ciphers_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8151e5a5c4ba71225274ef4facc429273525fe183fb5dea0f5c60132a1cb14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsRsaWithAes256CbcSha256CiphersEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsRsaWithAes256CbcShaCiphersEnabled")
    def tls_rsa_with_aes256_cbc_sha_ciphers_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsRsaWithAes256CbcShaCiphersEnabled"))

    @tls_rsa_with_aes256_cbc_sha_ciphers_enabled.setter
    def tls_rsa_with_aes256_cbc_sha_ciphers_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62517af00ec5c572bb64778d3187f49fa101a9c0b42ad6a238645b183005d298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsRsaWithAes256CbcShaCiphersEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsRsaWithAes256GcmSha384CiphersEnabled")
    def tls_rsa_with_aes256_gcm_sha384_ciphers_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsRsaWithAes256GcmSha384CiphersEnabled"))

    @tls_rsa_with_aes256_gcm_sha384_ciphers_enabled.setter
    def tls_rsa_with_aes256_gcm_sha384_ciphers_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1205cd032d6e61792edaf83147001f15f6fe6aa21f099b61a2c21f5f925f7bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsRsaWithAes256GcmSha384CiphersEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tripleDesCiphersEnabled")
    def triple_des_ciphers_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tripleDesCiphersEnabled"))

    @triple_des_ciphers_enabled.setter
    def triple_des_ciphers_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8479289494aae1216737d5d2415f6b0d845ba1480079a3058debdd237a37e08f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tripleDesCiphersEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementSecurity]:
        return typing.cast(typing.Optional[ApiManagementSecurity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApiManagementSecurity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a0f8848c96c017e7ff2f9c9685b519933d8fc5b7ed8c6a610c9f4415aafa25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementSignIn",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ApiManagementSignIn:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enabled ApiManagement#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796929d80808a76b4688649b8d94dcc9c58ee821ef46950ff8f4955af98a1fc3)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enabled ApiManagement#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementSignIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementSignInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementSignInOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71b84d7990eca23bf67ec15c68ad594265c16d08d531532228ac3e3e0bd800ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515b68e6a8bccbc36a8ad2d7f87c9039a1445d4bd499a49dd19616e10849c946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementSignIn]:
        return typing.cast(typing.Optional[ApiManagementSignIn], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApiManagementSignIn]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df7769cf8003ace39d100de07e47877b032c19ff35c90bb74ea56865859f45d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementSignUp",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "terms_of_service": "termsOfService"},
)
class ApiManagementSignUp:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        terms_of_service: typing.Union["ApiManagementSignUpTermsOfService", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enabled ApiManagement#enabled}.
        :param terms_of_service: terms_of_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#terms_of_service ApiManagement#terms_of_service}
        '''
        if isinstance(terms_of_service, dict):
            terms_of_service = ApiManagementSignUpTermsOfService(**terms_of_service)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0e23fd23e9c78e8f67488c7125604055ad621ed47a1699c8e2abf176ef348e7)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument terms_of_service", value=terms_of_service, expected_type=type_hints["terms_of_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "terms_of_service": terms_of_service,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enabled ApiManagement#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def terms_of_service(self) -> "ApiManagementSignUpTermsOfService":
        '''terms_of_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#terms_of_service ApiManagement#terms_of_service}
        '''
        result = self._values.get("terms_of_service")
        assert result is not None, "Required property 'terms_of_service' is missing"
        return typing.cast("ApiManagementSignUpTermsOfService", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementSignUp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementSignUpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementSignUpOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076d8c474c9fec2b13b609475a5e0ead5d0c6ef61138bb46c0df43b1c15d4193)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTermsOfService")
    def put_terms_of_service(
        self,
        *,
        consent_required: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consent_required: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#consent_required ApiManagement#consent_required}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enabled ApiManagement#enabled}.
        :param text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#text ApiManagement#text}.
        '''
        value = ApiManagementSignUpTermsOfService(
            consent_required=consent_required, enabled=enabled, text=text
        )

        return typing.cast(None, jsii.invoke(self, "putTermsOfService", [value]))

    @builtins.property
    @jsii.member(jsii_name="termsOfService")
    def terms_of_service(self) -> "ApiManagementSignUpTermsOfServiceOutputReference":
        return typing.cast("ApiManagementSignUpTermsOfServiceOutputReference", jsii.get(self, "termsOfService"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="termsOfServiceInput")
    def terms_of_service_input(
        self,
    ) -> typing.Optional["ApiManagementSignUpTermsOfService"]:
        return typing.cast(typing.Optional["ApiManagementSignUpTermsOfService"], jsii.get(self, "termsOfServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3073dbaad0d5c51705128d57cda51243cb4271a5afad13c7f91e847166650e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementSignUp]:
        return typing.cast(typing.Optional[ApiManagementSignUp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApiManagementSignUp]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687a2e00c3ccf03c8d44198a313cc96f820d956659c48e47cb83cd6c0477751e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementSignUpTermsOfService",
    jsii_struct_bases=[],
    name_mapping={
        "consent_required": "consentRequired",
        "enabled": "enabled",
        "text": "text",
    },
)
class ApiManagementSignUpTermsOfService:
    def __init__(
        self,
        *,
        consent_required: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consent_required: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#consent_required ApiManagement#consent_required}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enabled ApiManagement#enabled}.
        :param text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#text ApiManagement#text}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7004be08674f4b3cbbb2c43045aaec6497756c23ba6bd829b957ad1a6fe0dd0)
            check_type(argname="argument consent_required", value=consent_required, expected_type=type_hints["consent_required"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consent_required": consent_required,
            "enabled": enabled,
        }
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def consent_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#consent_required ApiManagement#consent_required}.'''
        result = self._values.get("consent_required")
        assert result is not None, "Required property 'consent_required' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enabled ApiManagement#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#text ApiManagement#text}.'''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementSignUpTermsOfService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementSignUpTermsOfServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementSignUpTermsOfServiceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28eba8a46aa40ec6d70523a5d7153d693c1a106707574c641bcda372dbc5ca7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="consentRequiredInput")
    def consent_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "consentRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="consentRequired")
    def consent_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "consentRequired"))

    @consent_required.setter
    def consent_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f395011d4601e0b216a91ebde6b9826668b25e7ea9c6900e6e65f868319f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consentRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e5b1611c3c4c2aa352446c23aed2756e5d1855941932122ec09fea9968e4f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e5759dbb3c77e55c11ac57d13c787b5009b7ecc508d2920dcb41b21aec3434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementSignUpTermsOfService]:
        return typing.cast(typing.Optional[ApiManagementSignUpTermsOfService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementSignUpTermsOfService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dfdcba6a6f4ce6f07bd2e906393c97dc9fe0c789946353aee9c976584a71486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementTenantAccess",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ApiManagementTenantAccess:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enabled ApiManagement#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997a9c2c1cc2a0c4f9dbb35f814e955961796e4b55efe309b34cc5fcf927e45f)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#enabled ApiManagement#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementTenantAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementTenantAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementTenantAccessOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e385991994af0a35a85a7558e8980177c17eb9bb81be02892a1ab320e30e4936)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryKey"))

    @builtins.property
    @jsii.member(jsii_name="secondaryKey")
    def secondary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryKey"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb281e19e7e891024eabf2f67b2d45fc454097e3046e8824cfd6ebb0a3bbae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementTenantAccess]:
        return typing.cast(typing.Optional[ApiManagementTenantAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApiManagementTenantAccess]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755350f9cbe1740b838637bb2dbc9250dfd351b9321a62b1ef8ee5c41c50358a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ApiManagementTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#create ApiManagement#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#delete ApiManagement#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#read ApiManagement#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#update ApiManagement#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12a092164613dca7f9a834517e4e036fb573095b00a7766cbb99aa2cb5f19f7)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#create ApiManagement#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#delete ApiManagement#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#read ApiManagement#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#update ApiManagement#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0314fa7118513d75bc42b2583c8aea4ad38e50a85f0abe2221b9ebfd8cc764d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba0bad7415c43b093d49f8c506b86d6ef8ce72f8ccd238c123821b628171f88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__732e0f0d7a775d973a2d8732bc51b8257c6a914761d33c52fc71621608a55c51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143c7869c07860e7f967482d4d17527035294b16a641db7c299662d1f2cf8f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832f931961cba7975db4c212cb4b456476a0d0fa9ba0846dbb7859f2e551a9a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0385905812b0e701b78a4316a64aa2af8f9c79abc7630de32bfda189a63068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementVirtualNetworkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"subnet_id": "subnetId"},
)
class ApiManagementVirtualNetworkConfiguration:
    def __init__(self, *, subnet_id: builtins.str) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#subnet_id ApiManagement#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8fe91cbb9ad33219ceb44302c4c8d29b53b24f90eb989423c56bcdc4e41179a)
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_id": subnet_id,
        }

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management#subnet_id ApiManagement#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementVirtualNetworkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementVirtualNetworkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagement.ApiManagementVirtualNetworkConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e0e45f0bac3fc3d234f1eddf57b90a8c42ac6613882f5014d779b3ca8d78ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7feda800974bd45ed597ca48592f0859631f510e3bf08ec162858c5fdbce18c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementVirtualNetworkConfiguration]:
        return typing.cast(typing.Optional[ApiManagementVirtualNetworkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementVirtualNetworkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af978443eafe9c57fd1ecec45a28276e9637814dcbb3ee9523bd6d3afe1db667)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApiManagement",
    "ApiManagementAdditionalLocation",
    "ApiManagementAdditionalLocationList",
    "ApiManagementAdditionalLocationOutputReference",
    "ApiManagementAdditionalLocationVirtualNetworkConfiguration",
    "ApiManagementAdditionalLocationVirtualNetworkConfigurationOutputReference",
    "ApiManagementCertificate",
    "ApiManagementCertificateList",
    "ApiManagementCertificateOutputReference",
    "ApiManagementConfig",
    "ApiManagementDelegation",
    "ApiManagementDelegationOutputReference",
    "ApiManagementHostnameConfiguration",
    "ApiManagementHostnameConfigurationDeveloperPortal",
    "ApiManagementHostnameConfigurationDeveloperPortalList",
    "ApiManagementHostnameConfigurationDeveloperPortalOutputReference",
    "ApiManagementHostnameConfigurationManagement",
    "ApiManagementHostnameConfigurationManagementList",
    "ApiManagementHostnameConfigurationManagementOutputReference",
    "ApiManagementHostnameConfigurationOutputReference",
    "ApiManagementHostnameConfigurationPortal",
    "ApiManagementHostnameConfigurationPortalList",
    "ApiManagementHostnameConfigurationPortalOutputReference",
    "ApiManagementHostnameConfigurationProxy",
    "ApiManagementHostnameConfigurationProxyList",
    "ApiManagementHostnameConfigurationProxyOutputReference",
    "ApiManagementHostnameConfigurationScm",
    "ApiManagementHostnameConfigurationScmList",
    "ApiManagementHostnameConfigurationScmOutputReference",
    "ApiManagementIdentity",
    "ApiManagementIdentityOutputReference",
    "ApiManagementProtocols",
    "ApiManagementProtocolsOutputReference",
    "ApiManagementSecurity",
    "ApiManagementSecurityOutputReference",
    "ApiManagementSignIn",
    "ApiManagementSignInOutputReference",
    "ApiManagementSignUp",
    "ApiManagementSignUpOutputReference",
    "ApiManagementSignUpTermsOfService",
    "ApiManagementSignUpTermsOfServiceOutputReference",
    "ApiManagementTenantAccess",
    "ApiManagementTenantAccessOutputReference",
    "ApiManagementTimeouts",
    "ApiManagementTimeoutsOutputReference",
    "ApiManagementVirtualNetworkConfiguration",
    "ApiManagementVirtualNetworkConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__5b44d5684af6ef2c0057f2a29ff838cd55231aae6302954de3c78b9f0bf9c202(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    publisher_email: builtins.str,
    publisher_name: builtins.str,
    resource_group_name: builtins.str,
    sku_name: builtins.str,
    additional_location: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementAdditionalLocation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delegation: typing.Optional[typing.Union[ApiManagementDelegation, typing.Dict[builtins.str, typing.Any]]] = None,
    gateway_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hostname_configuration: typing.Optional[typing.Union[ApiManagementHostnameConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ApiManagementIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    min_api_version: typing.Optional[builtins.str] = None,
    notification_sender_email: typing.Optional[builtins.str] = None,
    protocols: typing.Optional[typing.Union[ApiManagementProtocols, typing.Dict[builtins.str, typing.Any]]] = None,
    public_ip_address_id: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security: typing.Optional[typing.Union[ApiManagementSecurity, typing.Dict[builtins.str, typing.Any]]] = None,
    sign_in: typing.Optional[typing.Union[ApiManagementSignIn, typing.Dict[builtins.str, typing.Any]]] = None,
    sign_up: typing.Optional[typing.Union[ApiManagementSignUp, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenant_access: typing.Optional[typing.Union[ApiManagementTenantAccess, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_network_configuration: typing.Optional[typing.Union[ApiManagementVirtualNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_network_type: typing.Optional[builtins.str] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc547e6824dddbfce14726f08678f4744eeb5b6b9286f72a52b9487f87ff39e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3346c7ddc80d7f5f07dc48e412c3e28751de7323cf1c05927705bc5f19a3ef30(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementAdditionalLocation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3ccca5fc530272d561fedd22e250b0fa35f6f6f5a525f2ec7db0327ea705d8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCertificate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e55750df29b9951e4a44ee37b86425d4d33fdf15477dbed38368bc89e7e982c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cf0680e74fc4c1ed638b7a307036154b2cbf476e9c4b810392d3ba01db569c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed817cf42715c3982bc0ade4a3f91fac2ebb9fb39f8a5f5e0dc3ad7f530d4090(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9457b4154122a6d6baaf37977a1509304c9f43e02d88de123f96164d64d4b33b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7adea66550c738dc81dfb00f08ebdb7f27b46447b00fae9e630f7d3d27d766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9dd8425b7dc91230e981e690ed1d33001cc71f6cb62e97cc309052d161ed087(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5ca8a7f12a3314bec4f27010299b0ceeac34d82607943cd5c4074340e997e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c800456a5381e4da24d7fa7df264e806bfe7e3b00082ef73e591dd5ad9159e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d8812250721ec17cb6c23d8f99b35188fdb7a8333874da9ec62adeec349e42(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467acddbf91e4eb130de510e461fcc2043684163ce17f76cfd1e06a458b01f51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ea522ca2e93e21cecc219392a0c097d26aa3ea40deb728b18a769621e72e4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cca6beda6a9920325a8d6b39f69483aa46daea3f22bb783b3142a4378d76fe9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b5c11926a9c066cb9329531c9a65671ebf0e9507e6756f5399d77715422f95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ea75c6ac31a3460907b3a961e0b8a83192e37a6ce26766c9d9c78e0bdc429b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d9e9cfe73ed5aed2698c3b2d94a6b51671f3456315a03823f52710c3ea130bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73d5e50c9265770bd924d4699093ea24d03be081d3a39d7f14ef02f5c63c926(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c95f763e943b886ae7570545cc957bc8747f11b9cc8aa45ebf757d9273ac1c(
    *,
    location: builtins.str,
    capacity: typing.Optional[jsii.Number] = None,
    gateway_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_ip_address_id: typing.Optional[builtins.str] = None,
    virtual_network_configuration: typing.Optional[typing.Union[ApiManagementAdditionalLocationVirtualNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b159f8b43c85e83af449ae6a61c4e93c112ecacfbef9ca711e4cc06f40a974f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf91b95a44451e1a4a947ac609d19aa78e190cbfb3f7d82308ce3263224f1373(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6410342cd17640e1e62fd067fa270d7b3d8143b7d0ac151dc50aa29dd2451ca1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a594f51c8bf106b8d7960ea0a0ae27fbe290523a336d8c3d5caefa0bb333c432(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e1ba57d7251f07f05d811f57fe3d186017036bcd3707a36cd45a781639a4ca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8828037c618bf8207d1afda7eb144f29c504266c6a24f8d5d616cb878d9353e8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementAdditionalLocation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c40fa838405e95c3666d596e797d59c3955d6b94ee642fe73f67519feea61d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac9807c14eb214f8fe7e6ce9ec7b5c9c36cb91a66d8ce6b6ff03d9d662f7efeb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802face2936beeb6c32511d0b09cf89698af2cbd1d03b6f44483677a83a9713a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773b6b67cb14244c690dfa2fdc6d631cac8b254038861a149344e314d960d8bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87e88bec4f803e916ac0cd9672e2d4e7b679c27850b7477aae2a6093692096b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8113b83161b3275366e70319f5448cdb578c3c9ba3b2d7187bc3786235f46d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33add858655ebfbe99981b8801c3f760afc2b581b08f140e30d6533c27e0e70c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementAdditionalLocation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7657433b9d5df10caab86480e597363634156b720bf9188fcc4745a1a80cbc8b(
    *,
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535cd7cb0163aa64c850c7e6160ddc5ad39c296c2f04a46caa3059a589da2b7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bedc46608cf8f9ff74ff9a5206d58749ba9f7c0109d9ec3b712634c4e4cbc5f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac134c18fa39f52dc40fef710862f90a70b73511957d76c3f3995f9c9dca373(
    value: typing.Optional[ApiManagementAdditionalLocationVirtualNetworkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197011cbd95ffd4975e08887eb007b06cbde7d3be5d565d8fe97234f48030af3(
    *,
    encoded_certificate: builtins.str,
    store_name: builtins.str,
    certificate_password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a63d3288a2b018d123018c7efd79f7ee5a78b30df894f8b2eab6c0815309408(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec8c105c62e85f3fd53c47feb4e566446e367edc976fb9ef3e9063d22db34f9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dae2c277186d4e0de9e5f241c920a084a295fadc3862f5fcdb14df12cd8d185(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07c29a9d6a1da391868a99244d97b713b8b4fc753e7f896238b009a5373bc47(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac70ee16e3a4a9e0459273d7550a02cad5641f13881923296391456640dbe897(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c13cd5b883c2043fbc5c5f4d735d1eb2fc4268e3fa9d894877f45136e0505ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCertificate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6bc7cd0f57f6feecff461d00d2c0301714b16bfc571df2e96e87efe2621ed6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9a86ed03dd18678f26a298b26b19e757acaa8228e2f40104f5a2319de44d76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff91f1c4f8018a6252c6762836ac5c585485b73cb1c794d412af2e539fd0b0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ab0bc9f096d91ced1fccb2d105f98cdedb94aaf9a39b59e717bdbabc982c41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a7ff00984b55066ece7746fbc5e8bbbe12b1e84aed2996dc8a01b46d2f9d60(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCertificate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154b2056b4af27a46187afe2f4b6d9f62d27cc27062f18765e0017f35475fc49(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    publisher_email: builtins.str,
    publisher_name: builtins.str,
    resource_group_name: builtins.str,
    sku_name: builtins.str,
    additional_location: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementAdditionalLocation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delegation: typing.Optional[typing.Union[ApiManagementDelegation, typing.Dict[builtins.str, typing.Any]]] = None,
    gateway_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hostname_configuration: typing.Optional[typing.Union[ApiManagementHostnameConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ApiManagementIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    min_api_version: typing.Optional[builtins.str] = None,
    notification_sender_email: typing.Optional[builtins.str] = None,
    protocols: typing.Optional[typing.Union[ApiManagementProtocols, typing.Dict[builtins.str, typing.Any]]] = None,
    public_ip_address_id: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security: typing.Optional[typing.Union[ApiManagementSecurity, typing.Dict[builtins.str, typing.Any]]] = None,
    sign_in: typing.Optional[typing.Union[ApiManagementSignIn, typing.Dict[builtins.str, typing.Any]]] = None,
    sign_up: typing.Optional[typing.Union[ApiManagementSignUp, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenant_access: typing.Optional[typing.Union[ApiManagementTenantAccess, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_network_configuration: typing.Optional[typing.Union[ApiManagementVirtualNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_network_type: typing.Optional[builtins.str] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0712329f3dd35e44106d5d40fa220cf0bb42a10184eb55b384b228cd651bcf13(
    *,
    subscriptions_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    url: typing.Optional[builtins.str] = None,
    user_registration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    validation_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a1fc7e3996793315733f3bb4b90358179acaba5811841ee1daa9893bb2b0cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65355a4c0633229b5b451a94287c00dc1200ad345c136e4e828b41326b0913c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2681aca027109f4fd35706c63f55745d6d81d5bd0e3a0239a2ebd2daf102dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4cf521f690980af4661fde5e58b8f442ec4fa306a0f2da0275fb4d930ad6b79(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02773d83f814d40c8ecf2741fe568fafad53020d3986f62aa0b376393cbef033(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0419d952a56106b10b5d76e7c858aacb763a0018f14ab1878fcaa6f062a17a5(
    value: typing.Optional[ApiManagementDelegation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecddf5ef14f8d3c1686f1d2262b0039d26f23f1249d99854fbe1f8b8973ea21(
    *,
    developer_portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementHostnameConfigurationDeveloperPortal, typing.Dict[builtins.str, typing.Any]]]]] = None,
    management: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementHostnameConfigurationManagement, typing.Dict[builtins.str, typing.Any]]]]] = None,
    portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementHostnameConfigurationPortal, typing.Dict[builtins.str, typing.Any]]]]] = None,
    proxy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementHostnameConfigurationProxy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementHostnameConfigurationScm, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3d9265cd3f7dcc6f50e185a5cd12c976157c8f836cf30dacb1f53fc89a0d39(
    *,
    host_name: builtins.str,
    certificate: typing.Optional[builtins.str] = None,
    certificate_password: typing.Optional[builtins.str] = None,
    key_vault_certificate_id: typing.Optional[builtins.str] = None,
    key_vault_id: typing.Optional[builtins.str] = None,
    negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cff0938b204e07325867913f3aeee79f5d6ca6b4977ce3ed048afb52b12905c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229d69978a7af9d331db1f2bd8b77c8d25bc0dce8b063e0001d90a3509e5339c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3c1a4f10409370309911d5bd1a948c1b892a95e04ab2f2b08e5e319cc97a43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a97c00e4b777e66ddc9fc21bc01faa23ed5808f90879a9d0c5c1cb3da9736d8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0d9fd8793887f3df5e945141c661e7b814d8ccf832711835392a5374babbc2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924e5449510927a1e04e9a133f4deddd2c2fcd307ce48dfd568300541c02ddda(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationDeveloperPortal]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35befb40be54ff06e41a1915e2366eefe267e2b41c2ec23a8d1d2beb2530ce0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac09e8bc7a850d2b0e54b1a1ae7e971292d737a25c5d337f1285eb8dcc1d5e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23801d0e4038401ef25e458f262b383620feebee549c400a51218499d206ef36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3815f0ecbbce583eb06316b225f27969ddd8113c7d3e303f4fcffefc4f55715(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e216b544839ed2411e6f8dd567727717de8d37f4f7fb536ef0a599319ee4bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6bd1269350ed2974815210175f75241b4cbb40b3a739312de4c67799bb69721(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273058c3aadff20de80e750db1fabd8f7523e36f65ee3d90278286fd111d61cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9787b61530e8bd4bc69f3fa17246693df101e64a752c139942b539c63126206e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c69ac571420e48ba506c9d35476166cda25b340daa6d95bfa1c9d550776d482(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationDeveloperPortal]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fcc9c9c9c970f8427661bbe91fb0f9b3f7640289e39e2b4047ee3f73256c4b(
    *,
    host_name: builtins.str,
    certificate: typing.Optional[builtins.str] = None,
    certificate_password: typing.Optional[builtins.str] = None,
    key_vault_certificate_id: typing.Optional[builtins.str] = None,
    key_vault_id: typing.Optional[builtins.str] = None,
    negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb98a57f0b730c1265b28619efcd4be2fc9384c02f7159fff4e250c511114f56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b440b6d3e48efa3c7f0714fb21f984e28421df7c1121eed514627459cd65824(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57db6a39db66a1fd5f950dc425d9edd8a66238218314c1f923db3b592e51526b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89fed1fb8adc58f55ad81b1ea08ac0e418eb712cf903da4009a54cddfef16f3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f00c85a1061ec114f6eaa247c2d8ab7903f57a28b55d8c8e20c1daf2893478(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e62d3fbde3d65d3202fbec0c2adc3f15233d69d91f2180ed6199a693932115(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationManagement]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb26404c1c81e9cf99efa3846433738d8329c47724d26261f91b3d95a4271bb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73225bce93d04ed820565b78d1c341c4a78efb18e908ceb5c26ca583a0fa0051(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc48c33e0ec07cb8cc5b140f1a90a0e3d2c6dc598ff055dcc970939d9615cd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc2c1f259c51fae257cdd469ee541e378ce1e950521a32089fe51da3ef5d8cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0709702882a743b219aed472e9995052716546ac7e864cf8d698056e777b50f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2d1ed506a24d3165d63619b7fee90bb0e421942db1b3fe353520bca89ead6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8eb7e1434fd4b7ca7de6b3734c3433fb4b3751425bf079e178bbfeb737f0ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0de9f145361140232225d615d4d658942bc4d8d4d65d0f1f114d2295a7fe4b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7d13c3fbd35729be139955b00483c968e4ca1733429144d3abf612abefb23f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationManagement]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a715a630e2a1e09996528a938796f2000a5bf71bb2e8cdc5dc8e46905ba4d14b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391b138000f890646edf52756cd0e41019be72f759e5a63993a454a328deb76f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementHostnameConfigurationDeveloperPortal, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef1fc56fd8d42b5f0ec68020889136ea69dc342020bbd7396aee14895c0edcd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementHostnameConfigurationManagement, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87f2989407cdd3b03f0e44b73132c0e753dce8460535c87b3dd8145fc64e594(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementHostnameConfigurationPortal, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9b52bd2776a5798dfc91a25897e8c666e800bd075f5419e1c2c3a21d883858(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementHostnameConfigurationProxy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92a0654103fe6ae123cb4740edf85098a0fe2cc2e439f6461e1eb8bacebe710(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementHostnameConfigurationScm, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8688bf71bf77ec9ab36e058a83e268bb097b1f670f8800d7508044e6de853ff(
    value: typing.Optional[ApiManagementHostnameConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fc69c12ad9cf5ebce2d9c1697b3023908d733643cc3b7a582bb7eb1319a104(
    *,
    host_name: builtins.str,
    certificate: typing.Optional[builtins.str] = None,
    certificate_password: typing.Optional[builtins.str] = None,
    key_vault_certificate_id: typing.Optional[builtins.str] = None,
    key_vault_id: typing.Optional[builtins.str] = None,
    negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8ad0e5f1f424d974b2304d9130bdb4b362e75fc661b651c2b7ea197c668696(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b14163c42180eaf14566d7554d8b8ce160c170f4c16f5fc0a6ea6f11bacfef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9fa926ff0bd7a2106ccc2c90b4006721e419d035a0037ca95cc872b9b9ee7e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abbe30067caa207fe60de581496a55541e822421f710a0784029d9c75052293d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17eb9297851f649825c2bdac08758d6231f767ab6977362ee8e75e379b86d7fc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27bbb56cec2d5ddb547940aa49709d91445cb87e53e95ff068449cfec679cfed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationPortal]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb1a6e535da76d9309132bbd225867cbc2095414cc58c6cb5297e300845bc62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e97cb5f73512a27a8aa9cd4905cf46d06b6ad71e8dcdf1dca010cde954ff23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d628b4c35c9be8bad2d015cb92ca862bd8ec77025666d87c6f373c06d029fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ee1494449fa2ee9b911e3333dfecfffff174748680968db737280b63c55a07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1e62ae75f679dcd4e65657209b6cac1ab3c7e319645a3f4ad9c36f881f4b6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cd3dfb581b24263c074246173fe78feee443e418c2da943087a94425c99772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c0d60e6dc47ab3e661266b06160422833b5acce5735431b51e91c9433325a6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2535e70578957e236dcdb385e879bd27af82493e277364065587e3c97486f103(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0107f6aa75095420b05988990ec8b811699a3d3b862bc371b13cd2419ee4de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationPortal]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c58fdd0a73f286cf2163bf500c861ac2f367112c9758935f28fe1dfede083d(
    *,
    host_name: builtins.str,
    certificate: typing.Optional[builtins.str] = None,
    certificate_password: typing.Optional[builtins.str] = None,
    default_ssl_binding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_vault_certificate_id: typing.Optional[builtins.str] = None,
    key_vault_id: typing.Optional[builtins.str] = None,
    negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8454aad4e922c0816c10374dd2e7795b86283324a75bb594bc10045dbc574bc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1242550d1276512c83b98f5a7f4f8df8943bf6ebe44af6d1c2d257016bc53a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df80cdffccb0a4744445ed38706319ac9d31b6f391f0de596e6993f535c7a66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b95afd42ca7fbf0cb0fa152a1655f05067abe2ac1cad0ceb51a57f79c15a70(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909933a5aa10560129f59e4a9ae0f2efd155b6f47f0ae4dc3d3c952240da5f77(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1282b42e5bfa8bb63abef5444d86b1f81b83a4a086e9e14ebd5b7aa9f94715d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationProxy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08d8200ee4fa5f8a30cea5abbc155e2627d0b42da44f2de64b3c6e05c1c3abf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8278aa6c382c67810e6a396e942ebaacadb2fb12a9c950c2a31af74a12a52fef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf39eeed32ab624c5d9650f871442fe256522b9b7da799f6b4d9bfcef5bab808(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb600daa1519189bd8f6dc283c2e71416f0d6465d10dab9328c21414ff383285(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60def97d75901d1bde0714729e268e549c282be500aa828f2161068735470cdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9d76f61b3ac8167bb50632d6441a225acb6b77f764fa6e0d02e01fcc123413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94f1204fb99ca131e56bdab44e5a6438ff969dda83d951c61496897db468f80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21cc1dedef70d1bfe4a7e577decc926bb56dabb610f8671fcbdb1595a47478be(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d3e3c0a324e596ac910b4517f695f1d68cf6a3707d62dd472f5efb5c4f5d96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5ab774458db6e12350c383579969107a3857103752f941e961c64f291125cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationProxy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d875e58e91aabd133dda7af3da03f414a3b3b2cd3e0d4f1a7d01e1ec401359(
    *,
    host_name: builtins.str,
    certificate: typing.Optional[builtins.str] = None,
    certificate_password: typing.Optional[builtins.str] = None,
    key_vault_certificate_id: typing.Optional[builtins.str] = None,
    key_vault_id: typing.Optional[builtins.str] = None,
    negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac20acba3367d13533b527b584e8b267fff0f1e09ad0927f1dec1a52fb553db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1547dbfb4019376c7e9a000588bf3a82c6e6d5934842c9a4354f4fd589f5d99f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5150b14176d47c300e62aaa94c5ef5a2c4ee2d9e084028de06ef3e50821c941d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0dffd974ce4a7b008ff390fee824471d2a35241ba208ec4962e22dbef9abf5e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09aaaf538efc844a9cff0306a1a300069e20dab108ad5b15bf4663e1b8eb10b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80acf94d3fbfe23d2af4ea42af6aa9eea8aa6f9e814204321aac6053bbee0769(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementHostnameConfigurationScm]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f30d1051f7c8a4b77c739f016a10333fcc182e18c727502fbbe21ea1aed5828(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e771a698f1261c58e6c654cdc188999c382c1deefa6c65f8bc9276ff23886b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ac2a1554a1aa5fe235c26327f45cb601c725cbd8c83014a18b0732a5676add(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b905ae4e8f480849fabf47bc6199c516c5cd56ef6565a12b30e6dc9b86784104(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce230c7932849360c559e0a34b08efc7b03f46cac6504ab2bb1d6f03940ec1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4d5bc9892a7b39662e53e3698ce3cbc75d40801f9cc8f25498d0ef81d3b860(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5dc8b70fc09a9f9c0119d761b51c12c05e12e09b786ee01d428e1834815f4f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4275df00fc832caf89b3d8a479a19a2e23185911686d147434c3cd7821729528(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c2d0fe3a1593d2fa681694ae9eaa6415455642d234b3f884ed14707fd2b8f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementHostnameConfigurationScm]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebb50749da3be1aaa91016c940d1d303d711ded4dcae4df53456befaba96a07(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe50a52b8151e0a730d998e2d0c2e29dc05c2b5d9d2c9f26941be64ef1b8792(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a541f0fd0b6ec51155d7e187384ec5a9f333bffc7b8f2fbdacccd23fd27df711(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340632f92da70df5fe36cbaf5b7cfcf8ef74661d64277e81e8a161857cf57138(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbeb5dcda97f2cfb10048dca2919571465077e25ed229d070a5f4779da7c96f0(
    value: typing.Optional[ApiManagementIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f33ffc92308f03d5b10d6fc2038e3f47eb547ffdbd79c414eb542ed21add255(
    *,
    enable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e80fe60aef246c44726fd716befd3d3c00a18a0efa247c9adea76eabffe942e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2741f43a9dbd864de0fb35ff0147fb3246eedd69196002f0746b5458a4e3f87(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5bafa598fb126fe2cd2c6120bec3540706f0379d8c994443757c3105b1dccd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d8f9a1f9004a0445e7561129e42d4d673cf41033344543b8e8726770d3055a(
    value: typing.Optional[ApiManagementProtocols],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d583cef33a75d205188512d8e56e76a3a1ebacb0c2b679c1a8db76e1302badca(
    *,
    backend_ssl30_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backend_tls10_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backend_tls11_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_backend_ssl30: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_backend_tls10: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_backend_tls11: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_frontend_ssl30: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_frontend_tls10: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_frontend_tls11: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    frontend_ssl30_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    frontend_tls10_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    frontend_tls11_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tls_rsa_with_aes128_cbc_sha256_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tls_rsa_with_aes128_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tls_rsa_with_aes128_gcm_sha256_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tls_rsa_with_aes256_cbc_sha256_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tls_rsa_with_aes256_cbc_sha_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tls_rsa_with_aes256_gcm_sha384_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    triple_des_ciphers_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a51892296824ccc6b1390a45c9c523115cc3ddbc26a906d0b03ad20fbad6c2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9e38d989893ab7b0fe27e1a1ce334ea0ec3fdc3857e282baf005c17c85c2f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757519f97e9033b463da62f03c55491cde1cc0d427ab4c0f28aa48a4b4cce85b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d89f23997732d958447bb9a6ba0d3ad0e651961995bfb35dd888e93f99191b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a4669bd63928fd9f0ce9e44cea7018b9f2f09e1eae685c3b0b06dffee81eba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb767c6da094787fc0fbfc8c5eccc0a20ce2a784b0ee8394255953b995490b7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882eaa6550972d7f1696e4a79781306c170134828bd7d8b93407bcf07da306b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f91de5e55a4134385cba3ce39093c52f1f4cfb32be97aa279dffaec657818f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b28579376caa9408b22c66b84ff5ad9097220059ccbdc0d6c9cd2cb6b1953b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f189c3fd0b56ba0cb26154e4a16df53bc5f4991b1ae2b4a31a074f325fbaab33(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31cbcb2cb595435e37f2783303eb0be8382faf0e96ab4a92e754180c73367ee4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa62f179f7b52ef7e90c5a800411cabbf41bf84db151ade6ca2f7711d16f20e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ece2848fe139c1bd108b01b412387a48108055473c73fb6d97b23ed98ffa713(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__260bb5674d4985e203c935fcf0ae473c965e69e6b367ea71c5f063806a655ae1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be08522a481247a83ad8e839774e2be33a569bc5bb2d0bbaa867f311db5b18d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbd3a4fb3386f8601698a127953ecf1e7c5f36a4f3814a0d0599cde3fa8467f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bcd3ff5494e1a5c59aa6912189cf3c8d8b206709a1f47e468546f05b344c9ce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0493044cd76a0f64548ce706625b3eee7fe56ba7e17b56321329750fa50ab5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeef43043f47fe03e2114d0732c99e9873642758b2b3df357d66b57c33b595ca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9271b2393eaf562a9a64fdfec47a673c3d787f6002c75c46e1f311e151ccc817(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8151e5a5c4ba71225274ef4facc429273525fe183fb5dea0f5c60132a1cb14(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62517af00ec5c572bb64778d3187f49fa101a9c0b42ad6a238645b183005d298(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1205cd032d6e61792edaf83147001f15f6fe6aa21f099b61a2c21f5f925f7bac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8479289494aae1216737d5d2415f6b0d845ba1480079a3058debdd237a37e08f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a0f8848c96c017e7ff2f9c9685b519933d8fc5b7ed8c6a610c9f4415aafa25(
    value: typing.Optional[ApiManagementSecurity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796929d80808a76b4688649b8d94dcc9c58ee821ef46950ff8f4955af98a1fc3(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b84d7990eca23bf67ec15c68ad594265c16d08d531532228ac3e3e0bd800ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515b68e6a8bccbc36a8ad2d7f87c9039a1445d4bd499a49dd19616e10849c946(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df7769cf8003ace39d100de07e47877b032c19ff35c90bb74ea56865859f45d(
    value: typing.Optional[ApiManagementSignIn],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e23fd23e9c78e8f67488c7125604055ad621ed47a1699c8e2abf176ef348e7(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    terms_of_service: typing.Union[ApiManagementSignUpTermsOfService, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076d8c474c9fec2b13b609475a5e0ead5d0c6ef61138bb46c0df43b1c15d4193(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3073dbaad0d5c51705128d57cda51243cb4271a5afad13c7f91e847166650e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687a2e00c3ccf03c8d44198a313cc96f820d956659c48e47cb83cd6c0477751e(
    value: typing.Optional[ApiManagementSignUp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7004be08674f4b3cbbb2c43045aaec6497756c23ba6bd829b957ad1a6fe0dd0(
    *,
    consent_required: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28eba8a46aa40ec6d70523a5d7153d693c1a106707574c641bcda372dbc5ca7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f395011d4601e0b216a91ebde6b9826668b25e7ea9c6900e6e65f868319f6a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e5b1611c3c4c2aa352446c23aed2756e5d1855941932122ec09fea9968e4f9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e5759dbb3c77e55c11ac57d13c787b5009b7ecc508d2920dcb41b21aec3434(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dfdcba6a6f4ce6f07bd2e906393c97dc9fe0c789946353aee9c976584a71486(
    value: typing.Optional[ApiManagementSignUpTermsOfService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997a9c2c1cc2a0c4f9dbb35f814e955961796e4b55efe309b34cc5fcf927e45f(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e385991994af0a35a85a7558e8980177c17eb9bb81be02892a1ab320e30e4936(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb281e19e7e891024eabf2f67b2d45fc454097e3046e8824cfd6ebb0a3bbae8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755350f9cbe1740b838637bb2dbc9250dfd351b9321a62b1ef8ee5c41c50358a(
    value: typing.Optional[ApiManagementTenantAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12a092164613dca7f9a834517e4e036fb573095b00a7766cbb99aa2cb5f19f7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0314fa7118513d75bc42b2583c8aea4ad38e50a85f0abe2221b9ebfd8cc764d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba0bad7415c43b093d49f8c506b86d6ef8ce72f8ccd238c123821b628171f88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732e0f0d7a775d973a2d8732bc51b8257c6a914761d33c52fc71621608a55c51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143c7869c07860e7f967482d4d17527035294b16a641db7c299662d1f2cf8f60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832f931961cba7975db4c212cb4b456476a0d0fa9ba0846dbb7859f2e551a9a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0385905812b0e701b78a4316a64aa2af8f9c79abc7630de32bfda189a63068(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fe91cbb9ad33219ceb44302c4c8d29b53b24f90eb989423c56bcdc4e41179a(
    *,
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e0e45f0bac3fc3d234f1eddf57b90a8c42ac6613882f5014d779b3ca8d78ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7feda800974bd45ed597ca48592f0859631f510e3bf08ec162858c5fdbce18c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af978443eafe9c57fd1ecec45a28276e9637814dcbb3ee9523bd6d3afe1db667(
    value: typing.Optional[ApiManagementVirtualNetworkConfiguration],
) -> None:
    """Type checking stubs"""
    pass
