r'''
# `azurerm_service_fabric_cluster`

Refer to the Terraform Registry for docs: [`azurerm_service_fabric_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster).
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


class ServiceFabricCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster azurerm_service_fabric_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        management_endpoint: builtins.str,
        name: builtins.str,
        node_type: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterNodeType", typing.Dict[builtins.str, typing.Any]]]],
        reliability_level: builtins.str,
        resource_group_name: builtins.str,
        upgrade_mode: builtins.str,
        vm_image: builtins.str,
        add_on_features: typing.Optional[typing.Sequence[builtins.str]] = None,
        azure_active_directory: typing.Optional[typing.Union["ServiceFabricClusterAzureActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate: typing.Optional[typing.Union["ServiceFabricClusterCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_common_names: typing.Optional[typing.Union["ServiceFabricClusterCertificateCommonNames", typing.Dict[builtins.str, typing.Any]]] = None,
        client_certificate_common_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterClientCertificateCommonName", typing.Dict[builtins.str, typing.Any]]]]] = None,
        client_certificate_thumbprint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterClientCertificateThumbprint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cluster_code_version: typing.Optional[builtins.str] = None,
        diagnostics_config: typing.Optional[typing.Union["ServiceFabricClusterDiagnosticsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        fabric_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterFabricSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        reverse_proxy_certificate: typing.Optional[typing.Union["ServiceFabricClusterReverseProxyCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        reverse_proxy_certificate_common_names: typing.Optional[typing.Union["ServiceFabricClusterReverseProxyCertificateCommonNames", typing.Dict[builtins.str, typing.Any]]] = None,
        service_fabric_zonal_upgrade_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ServiceFabricClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_policy: typing.Optional[typing.Union["ServiceFabricClusterUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        vmss_zonal_upgrade_mode: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster azurerm_service_fabric_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#location ServiceFabricCluster#location}.
        :param management_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#management_endpoint ServiceFabricCluster#management_endpoint}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#name ServiceFabricCluster#name}.
        :param node_type: node_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#node_type ServiceFabricCluster#node_type}
        :param reliability_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#reliability_level ServiceFabricCluster#reliability_level}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#resource_group_name ServiceFabricCluster#resource_group_name}.
        :param upgrade_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_mode ServiceFabricCluster#upgrade_mode}.
        :param vm_image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#vm_image ServiceFabricCluster#vm_image}.
        :param add_on_features: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#add_on_features ServiceFabricCluster#add_on_features}.
        :param azure_active_directory: azure_active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#azure_active_directory ServiceFabricCluster#azure_active_directory}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate ServiceFabricCluster#certificate}
        :param certificate_common_names: certificate_common_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate_common_names ServiceFabricCluster#certificate_common_names}
        :param client_certificate_common_name: client_certificate_common_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#client_certificate_common_name ServiceFabricCluster#client_certificate_common_name}
        :param client_certificate_thumbprint: client_certificate_thumbprint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#client_certificate_thumbprint ServiceFabricCluster#client_certificate_thumbprint}
        :param cluster_code_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#cluster_code_version ServiceFabricCluster#cluster_code_version}.
        :param diagnostics_config: diagnostics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#diagnostics_config ServiceFabricCluster#diagnostics_config}
        :param fabric_settings: fabric_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#fabric_settings ServiceFabricCluster#fabric_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#id ServiceFabricCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param reverse_proxy_certificate: reverse_proxy_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#reverse_proxy_certificate ServiceFabricCluster#reverse_proxy_certificate}
        :param reverse_proxy_certificate_common_names: reverse_proxy_certificate_common_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#reverse_proxy_certificate_common_names ServiceFabricCluster#reverse_proxy_certificate_common_names}
        :param service_fabric_zonal_upgrade_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#service_fabric_zonal_upgrade_mode ServiceFabricCluster#service_fabric_zonal_upgrade_mode}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#tags ServiceFabricCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#timeouts ServiceFabricCluster#timeouts}
        :param upgrade_policy: upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_policy ServiceFabricCluster#upgrade_policy}
        :param vmss_zonal_upgrade_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#vmss_zonal_upgrade_mode ServiceFabricCluster#vmss_zonal_upgrade_mode}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d7b121ce003664e03eedb5db95cc39ba5cdbbbb035e8afc7d32a3bf9d038c4e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceFabricClusterConfig(
            location=location,
            management_endpoint=management_endpoint,
            name=name,
            node_type=node_type,
            reliability_level=reliability_level,
            resource_group_name=resource_group_name,
            upgrade_mode=upgrade_mode,
            vm_image=vm_image,
            add_on_features=add_on_features,
            azure_active_directory=azure_active_directory,
            certificate=certificate,
            certificate_common_names=certificate_common_names,
            client_certificate_common_name=client_certificate_common_name,
            client_certificate_thumbprint=client_certificate_thumbprint,
            cluster_code_version=cluster_code_version,
            diagnostics_config=diagnostics_config,
            fabric_settings=fabric_settings,
            id=id,
            reverse_proxy_certificate=reverse_proxy_certificate,
            reverse_proxy_certificate_common_names=reverse_proxy_certificate_common_names,
            service_fabric_zonal_upgrade_mode=service_fabric_zonal_upgrade_mode,
            tags=tags,
            timeouts=timeouts,
            upgrade_policy=upgrade_policy,
            vmss_zonal_upgrade_mode=vmss_zonal_upgrade_mode,
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
        '''Generates CDKTF code for importing a ServiceFabricCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ServiceFabricCluster to import.
        :param import_from_id: The id of the existing ServiceFabricCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ServiceFabricCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a870ff83ebdaed745c9342b5c0ebf5999f1fa171ff4fd12080931e4d6101d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAzureActiveDirectory")
    def put_azure_active_directory(
        self,
        *,
        client_application_id: builtins.str,
        cluster_application_id: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''
        :param client_application_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#client_application_id ServiceFabricCluster#client_application_id}.
        :param cluster_application_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#cluster_application_id ServiceFabricCluster#cluster_application_id}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#tenant_id ServiceFabricCluster#tenant_id}.
        '''
        value = ServiceFabricClusterAzureActiveDirectory(
            client_application_id=client_application_id,
            cluster_application_id=cluster_application_id,
            tenant_id=tenant_id,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureActiveDirectory", [value]))

    @jsii.member(jsii_name="putCertificate")
    def put_certificate(
        self,
        *,
        thumbprint: builtins.str,
        x509_store_name: builtins.str,
        thumbprint_secondary: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param thumbprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint ServiceFabricCluster#thumbprint}.
        :param x509_store_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#x509_store_name ServiceFabricCluster#x509_store_name}.
        :param thumbprint_secondary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint_secondary ServiceFabricCluster#thumbprint_secondary}.
        '''
        value = ServiceFabricClusterCertificate(
            thumbprint=thumbprint,
            x509_store_name=x509_store_name,
            thumbprint_secondary=thumbprint_secondary,
        )

        return typing.cast(None, jsii.invoke(self, "putCertificate", [value]))

    @jsii.member(jsii_name="putCertificateCommonNames")
    def put_certificate_common_names(
        self,
        *,
        common_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterCertificateCommonNamesCommonNames", typing.Dict[builtins.str, typing.Any]]]],
        x509_store_name: builtins.str,
    ) -> None:
        '''
        :param common_names: common_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#common_names ServiceFabricCluster#common_names}
        :param x509_store_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#x509_store_name ServiceFabricCluster#x509_store_name}.
        '''
        value = ServiceFabricClusterCertificateCommonNames(
            common_names=common_names, x509_store_name=x509_store_name
        )

        return typing.cast(None, jsii.invoke(self, "putCertificateCommonNames", [value]))

    @jsii.member(jsii_name="putClientCertificateCommonName")
    def put_client_certificate_common_name(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterClientCertificateCommonName", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d85bf78cc986a26cf632940187f7659f905808bbdd362a54abb5e322d50cff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putClientCertificateCommonName", [value]))

    @jsii.member(jsii_name="putClientCertificateThumbprint")
    def put_client_certificate_thumbprint(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterClientCertificateThumbprint", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcd04d9a17209b859b0300cd4ec5c857bfdb0b3e8d09c65b857419ea686312af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putClientCertificateThumbprint", [value]))

    @jsii.member(jsii_name="putDiagnosticsConfig")
    def put_diagnostics_config(
        self,
        *,
        blob_endpoint: builtins.str,
        protected_account_key_name: builtins.str,
        queue_endpoint: builtins.str,
        storage_account_name: builtins.str,
        table_endpoint: builtins.str,
    ) -> None:
        '''
        :param blob_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#blob_endpoint ServiceFabricCluster#blob_endpoint}.
        :param protected_account_key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#protected_account_key_name ServiceFabricCluster#protected_account_key_name}.
        :param queue_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#queue_endpoint ServiceFabricCluster#queue_endpoint}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#storage_account_name ServiceFabricCluster#storage_account_name}.
        :param table_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#table_endpoint ServiceFabricCluster#table_endpoint}.
        '''
        value = ServiceFabricClusterDiagnosticsConfig(
            blob_endpoint=blob_endpoint,
            protected_account_key_name=protected_account_key_name,
            queue_endpoint=queue_endpoint,
            storage_account_name=storage_account_name,
            table_endpoint=table_endpoint,
        )

        return typing.cast(None, jsii.invoke(self, "putDiagnosticsConfig", [value]))

    @jsii.member(jsii_name="putFabricSettings")
    def put_fabric_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterFabricSettings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56730839f30763e4b166aca15a082be917e43f9238bf6f397f460b89321749ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFabricSettings", [value]))

    @jsii.member(jsii_name="putNodeType")
    def put_node_type(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterNodeType", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ddb09be8fe3321754a817bf3fb9de7c7ab8a3d78f84d4f6bb018170ce8076e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeType", [value]))

    @jsii.member(jsii_name="putReverseProxyCertificate")
    def put_reverse_proxy_certificate(
        self,
        *,
        thumbprint: builtins.str,
        x509_store_name: builtins.str,
        thumbprint_secondary: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param thumbprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint ServiceFabricCluster#thumbprint}.
        :param x509_store_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#x509_store_name ServiceFabricCluster#x509_store_name}.
        :param thumbprint_secondary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint_secondary ServiceFabricCluster#thumbprint_secondary}.
        '''
        value = ServiceFabricClusterReverseProxyCertificate(
            thumbprint=thumbprint,
            x509_store_name=x509_store_name,
            thumbprint_secondary=thumbprint_secondary,
        )

        return typing.cast(None, jsii.invoke(self, "putReverseProxyCertificate", [value]))

    @jsii.member(jsii_name="putReverseProxyCertificateCommonNames")
    def put_reverse_proxy_certificate_common_names(
        self,
        *,
        common_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames", typing.Dict[builtins.str, typing.Any]]]],
        x509_store_name: builtins.str,
    ) -> None:
        '''
        :param common_names: common_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#common_names ServiceFabricCluster#common_names}
        :param x509_store_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#x509_store_name ServiceFabricCluster#x509_store_name}.
        '''
        value = ServiceFabricClusterReverseProxyCertificateCommonNames(
            common_names=common_names, x509_store_name=x509_store_name
        )

        return typing.cast(None, jsii.invoke(self, "putReverseProxyCertificateCommonNames", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#create ServiceFabricCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#delete ServiceFabricCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#read ServiceFabricCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#update ServiceFabricCluster#update}.
        '''
        value = ServiceFabricClusterTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUpgradePolicy")
    def put_upgrade_policy(
        self,
        *,
        delta_health_policy: typing.Optional[typing.Union["ServiceFabricClusterUpgradePolicyDeltaHealthPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        force_restart_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        health_check_retry_timeout: typing.Optional[builtins.str] = None,
        health_check_stable_duration: typing.Optional[builtins.str] = None,
        health_check_wait_duration: typing.Optional[builtins.str] = None,
        health_policy: typing.Optional[typing.Union["ServiceFabricClusterUpgradePolicyHealthPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_domain_timeout: typing.Optional[builtins.str] = None,
        upgrade_replica_set_check_timeout: typing.Optional[builtins.str] = None,
        upgrade_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delta_health_policy: delta_health_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#delta_health_policy ServiceFabricCluster#delta_health_policy}
        :param force_restart_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#force_restart_enabled ServiceFabricCluster#force_restart_enabled}.
        :param health_check_retry_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#health_check_retry_timeout ServiceFabricCluster#health_check_retry_timeout}.
        :param health_check_stable_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#health_check_stable_duration ServiceFabricCluster#health_check_stable_duration}.
        :param health_check_wait_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#health_check_wait_duration ServiceFabricCluster#health_check_wait_duration}.
        :param health_policy: health_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#health_policy ServiceFabricCluster#health_policy}
        :param upgrade_domain_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_domain_timeout ServiceFabricCluster#upgrade_domain_timeout}.
        :param upgrade_replica_set_check_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_replica_set_check_timeout ServiceFabricCluster#upgrade_replica_set_check_timeout}.
        :param upgrade_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_timeout ServiceFabricCluster#upgrade_timeout}.
        '''
        value = ServiceFabricClusterUpgradePolicy(
            delta_health_policy=delta_health_policy,
            force_restart_enabled=force_restart_enabled,
            health_check_retry_timeout=health_check_retry_timeout,
            health_check_stable_duration=health_check_stable_duration,
            health_check_wait_duration=health_check_wait_duration,
            health_policy=health_policy,
            upgrade_domain_timeout=upgrade_domain_timeout,
            upgrade_replica_set_check_timeout=upgrade_replica_set_check_timeout,
            upgrade_timeout=upgrade_timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putUpgradePolicy", [value]))

    @jsii.member(jsii_name="resetAddOnFeatures")
    def reset_add_on_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddOnFeatures", []))

    @jsii.member(jsii_name="resetAzureActiveDirectory")
    def reset_azure_active_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureActiveDirectory", []))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCertificateCommonNames")
    def reset_certificate_common_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateCommonNames", []))

    @jsii.member(jsii_name="resetClientCertificateCommonName")
    def reset_client_certificate_common_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateCommonName", []))

    @jsii.member(jsii_name="resetClientCertificateThumbprint")
    def reset_client_certificate_thumbprint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateThumbprint", []))

    @jsii.member(jsii_name="resetClusterCodeVersion")
    def reset_cluster_code_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterCodeVersion", []))

    @jsii.member(jsii_name="resetDiagnosticsConfig")
    def reset_diagnostics_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiagnosticsConfig", []))

    @jsii.member(jsii_name="resetFabricSettings")
    def reset_fabric_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFabricSettings", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetReverseProxyCertificate")
    def reset_reverse_proxy_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReverseProxyCertificate", []))

    @jsii.member(jsii_name="resetReverseProxyCertificateCommonNames")
    def reset_reverse_proxy_certificate_common_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReverseProxyCertificateCommonNames", []))

    @jsii.member(jsii_name="resetServiceFabricZonalUpgradeMode")
    def reset_service_fabric_zonal_upgrade_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceFabricZonalUpgradeMode", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUpgradePolicy")
    def reset_upgrade_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpgradePolicy", []))

    @jsii.member(jsii_name="resetVmssZonalUpgradeMode")
    def reset_vmss_zonal_upgrade_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmssZonalUpgradeMode", []))

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
    @jsii.member(jsii_name="azureActiveDirectory")
    def azure_active_directory(
        self,
    ) -> "ServiceFabricClusterAzureActiveDirectoryOutputReference":
        return typing.cast("ServiceFabricClusterAzureActiveDirectoryOutputReference", jsii.get(self, "azureActiveDirectory"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> "ServiceFabricClusterCertificateOutputReference":
        return typing.cast("ServiceFabricClusterCertificateOutputReference", jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="certificateCommonNames")
    def certificate_common_names(
        self,
    ) -> "ServiceFabricClusterCertificateCommonNamesOutputReference":
        return typing.cast("ServiceFabricClusterCertificateCommonNamesOutputReference", jsii.get(self, "certificateCommonNames"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateCommonName")
    def client_certificate_common_name(
        self,
    ) -> "ServiceFabricClusterClientCertificateCommonNameList":
        return typing.cast("ServiceFabricClusterClientCertificateCommonNameList", jsii.get(self, "clientCertificateCommonName"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateThumbprint")
    def client_certificate_thumbprint(
        self,
    ) -> "ServiceFabricClusterClientCertificateThumbprintList":
        return typing.cast("ServiceFabricClusterClientCertificateThumbprintList", jsii.get(self, "clientCertificateThumbprint"))

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="diagnosticsConfig")
    def diagnostics_config(
        self,
    ) -> "ServiceFabricClusterDiagnosticsConfigOutputReference":
        return typing.cast("ServiceFabricClusterDiagnosticsConfigOutputReference", jsii.get(self, "diagnosticsConfig"))

    @builtins.property
    @jsii.member(jsii_name="fabricSettings")
    def fabric_settings(self) -> "ServiceFabricClusterFabricSettingsList":
        return typing.cast("ServiceFabricClusterFabricSettingsList", jsii.get(self, "fabricSettings"))

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> "ServiceFabricClusterNodeTypeList":
        return typing.cast("ServiceFabricClusterNodeTypeList", jsii.get(self, "nodeType"))

    @builtins.property
    @jsii.member(jsii_name="reverseProxyCertificate")
    def reverse_proxy_certificate(
        self,
    ) -> "ServiceFabricClusterReverseProxyCertificateOutputReference":
        return typing.cast("ServiceFabricClusterReverseProxyCertificateOutputReference", jsii.get(self, "reverseProxyCertificate"))

    @builtins.property
    @jsii.member(jsii_name="reverseProxyCertificateCommonNames")
    def reverse_proxy_certificate_common_names(
        self,
    ) -> "ServiceFabricClusterReverseProxyCertificateCommonNamesOutputReference":
        return typing.cast("ServiceFabricClusterReverseProxyCertificateCommonNamesOutputReference", jsii.get(self, "reverseProxyCertificateCommonNames"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ServiceFabricClusterTimeoutsOutputReference":
        return typing.cast("ServiceFabricClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="upgradePolicy")
    def upgrade_policy(self) -> "ServiceFabricClusterUpgradePolicyOutputReference":
        return typing.cast("ServiceFabricClusterUpgradePolicyOutputReference", jsii.get(self, "upgradePolicy"))

    @builtins.property
    @jsii.member(jsii_name="addOnFeaturesInput")
    def add_on_features_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addOnFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="azureActiveDirectoryInput")
    def azure_active_directory_input(
        self,
    ) -> typing.Optional["ServiceFabricClusterAzureActiveDirectory"]:
        return typing.cast(typing.Optional["ServiceFabricClusterAzureActiveDirectory"], jsii.get(self, "azureActiveDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateCommonNamesInput")
    def certificate_common_names_input(
        self,
    ) -> typing.Optional["ServiceFabricClusterCertificateCommonNames"]:
        return typing.cast(typing.Optional["ServiceFabricClusterCertificateCommonNames"], jsii.get(self, "certificateCommonNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional["ServiceFabricClusterCertificate"]:
        return typing.cast(typing.Optional["ServiceFabricClusterCertificate"], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateCommonNameInput")
    def client_certificate_common_name_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterClientCertificateCommonName"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterClientCertificateCommonName"]]], jsii.get(self, "clientCertificateCommonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateThumbprintInput")
    def client_certificate_thumbprint_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterClientCertificateThumbprint"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterClientCertificateThumbprint"]]], jsii.get(self, "clientCertificateThumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterCodeVersionInput")
    def cluster_code_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterCodeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="diagnosticsConfigInput")
    def diagnostics_config_input(
        self,
    ) -> typing.Optional["ServiceFabricClusterDiagnosticsConfig"]:
        return typing.cast(typing.Optional["ServiceFabricClusterDiagnosticsConfig"], jsii.get(self, "diagnosticsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fabricSettingsInput")
    def fabric_settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterFabricSettings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterFabricSettings"]]], jsii.get(self, "fabricSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managementEndpointInput")
    def management_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managementEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeInput")
    def node_type_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterNodeType"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterNodeType"]]], jsii.get(self, "nodeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="reliabilityLevelInput")
    def reliability_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reliabilityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="reverseProxyCertificateCommonNamesInput")
    def reverse_proxy_certificate_common_names_input(
        self,
    ) -> typing.Optional["ServiceFabricClusterReverseProxyCertificateCommonNames"]:
        return typing.cast(typing.Optional["ServiceFabricClusterReverseProxyCertificateCommonNames"], jsii.get(self, "reverseProxyCertificateCommonNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="reverseProxyCertificateInput")
    def reverse_proxy_certificate_input(
        self,
    ) -> typing.Optional["ServiceFabricClusterReverseProxyCertificate"]:
        return typing.cast(typing.Optional["ServiceFabricClusterReverseProxyCertificate"], jsii.get(self, "reverseProxyCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceFabricZonalUpgradeModeInput")
    def service_fabric_zonal_upgrade_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceFabricZonalUpgradeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServiceFabricClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServiceFabricClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeModeInput")
    def upgrade_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "upgradeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradePolicyInput")
    def upgrade_policy_input(
        self,
    ) -> typing.Optional["ServiceFabricClusterUpgradePolicy"]:
        return typing.cast(typing.Optional["ServiceFabricClusterUpgradePolicy"], jsii.get(self, "upgradePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="vmImageInput")
    def vm_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmImageInput"))

    @builtins.property
    @jsii.member(jsii_name="vmssZonalUpgradeModeInput")
    def vmss_zonal_upgrade_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmssZonalUpgradeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="addOnFeatures")
    def add_on_features(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addOnFeatures"))

    @add_on_features.setter
    def add_on_features(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c261cc5eb215687386ac95141cfdb98cc5010c0833472d767e5641e03714a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addOnFeatures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterCodeVersion")
    def cluster_code_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterCodeVersion"))

    @cluster_code_version.setter
    def cluster_code_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dfcddcfdd11a533720597d0251278f276fc666544a885b8e6c267905e29f787)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterCodeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a94d2d6b39b4163b8565f13c7eb4d32f72b7113c8da05814501327cd1d33b7f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26526a5bd513ee72962cce1921181cee92117fda914155650309dd0b53ca4f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managementEndpoint")
    def management_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managementEndpoint"))

    @management_endpoint.setter
    def management_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e553575d19bcecc45bb928727bc30303ea77270ad829232eb9ece580e633bd47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managementEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feef05690eed73c617d2bd214517d011d74de9a403c4ee718d92ec5f1c071940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reliabilityLevel")
    def reliability_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reliabilityLevel"))

    @reliability_level.setter
    def reliability_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279c2f025269107bb58d42b32adfdf5b7f91fe531d3ae89fb688d904c61b0a95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reliabilityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7885a9d08114fe4a4355a7858db2fa9a2f5dad5ec4a5bd8a0a8acde5c18d357c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceFabricZonalUpgradeMode")
    def service_fabric_zonal_upgrade_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceFabricZonalUpgradeMode"))

    @service_fabric_zonal_upgrade_mode.setter
    def service_fabric_zonal_upgrade_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af1a95ec5da1b4758e92ba6b6eba07f6162cb5ce317e516a2339c5d4215fa2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceFabricZonalUpgradeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f0c434f84b36f4f4c884b8f91993d735e183d513584a4b83566bca984c6b791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="upgradeMode")
    def upgrade_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "upgradeMode"))

    @upgrade_mode.setter
    def upgrade_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177fe8743e4d6f38e7887e5217d5a25a32865367786bdcc3707805a733f3a825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upgradeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmImage")
    def vm_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmImage"))

    @vm_image.setter
    def vm_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd2b2a4c5844fe4b6940ed47bda7bf1240f6ae20656a6b53f5acff8950063e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmssZonalUpgradeMode")
    def vmss_zonal_upgrade_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmssZonalUpgradeMode"))

    @vmss_zonal_upgrade_mode.setter
    def vmss_zonal_upgrade_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36eda299292bd52bed6e09bcca7a547d53e04b7e04976d94fd4ee7a477e41a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmssZonalUpgradeMode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterAzureActiveDirectory",
    jsii_struct_bases=[],
    name_mapping={
        "client_application_id": "clientApplicationId",
        "cluster_application_id": "clusterApplicationId",
        "tenant_id": "tenantId",
    },
)
class ServiceFabricClusterAzureActiveDirectory:
    def __init__(
        self,
        *,
        client_application_id: builtins.str,
        cluster_application_id: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''
        :param client_application_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#client_application_id ServiceFabricCluster#client_application_id}.
        :param cluster_application_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#cluster_application_id ServiceFabricCluster#cluster_application_id}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#tenant_id ServiceFabricCluster#tenant_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e6fc8b821874f37a38872261fb6fc73fa0d80a0a146c2f1320a4383491a8ec)
            check_type(argname="argument client_application_id", value=client_application_id, expected_type=type_hints["client_application_id"])
            check_type(argname="argument cluster_application_id", value=cluster_application_id, expected_type=type_hints["cluster_application_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_application_id": client_application_id,
            "cluster_application_id": cluster_application_id,
            "tenant_id": tenant_id,
        }

    @builtins.property
    def client_application_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#client_application_id ServiceFabricCluster#client_application_id}.'''
        result = self._values.get("client_application_id")
        assert result is not None, "Required property 'client_application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_application_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#cluster_application_id ServiceFabricCluster#cluster_application_id}.'''
        result = self._values.get("cluster_application_id")
        assert result is not None, "Required property 'cluster_application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#tenant_id ServiceFabricCluster#tenant_id}.'''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterAzureActiveDirectory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricClusterAzureActiveDirectoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterAzureActiveDirectoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d93c5fc5fe7abca3228197febecc057586d243e15aabc009f25a1c9321729d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clientApplicationIdInput")
    def client_application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientApplicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterApplicationIdInput")
    def cluster_application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterApplicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientApplicationId")
    def client_application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientApplicationId"))

    @client_application_id.setter
    def client_application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91010a8b446ab3d812df19974fa2ee34e65aa64a25e9aa50122c8237750031e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientApplicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterApplicationId")
    def cluster_application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterApplicationId"))

    @cluster_application_id.setter
    def cluster_application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de8de991c0efa0d986219e07dddc3a77fbafd8de22dc5988a40658f92214d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterApplicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e021d7ba6a55da2523534030e79ade9d00b98ab75990d5ab67622769a620bf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceFabricClusterAzureActiveDirectory]:
        return typing.cast(typing.Optional[ServiceFabricClusterAzureActiveDirectory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFabricClusterAzureActiveDirectory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c5a6c5ac7c5c0024005e2d78ba09ed59c358fb78772babe7bc350562c25dd7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "thumbprint": "thumbprint",
        "x509_store_name": "x509StoreName",
        "thumbprint_secondary": "thumbprintSecondary",
    },
)
class ServiceFabricClusterCertificate:
    def __init__(
        self,
        *,
        thumbprint: builtins.str,
        x509_store_name: builtins.str,
        thumbprint_secondary: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param thumbprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint ServiceFabricCluster#thumbprint}.
        :param x509_store_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#x509_store_name ServiceFabricCluster#x509_store_name}.
        :param thumbprint_secondary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint_secondary ServiceFabricCluster#thumbprint_secondary}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de7a34f0cf56d68c4c11f5086ff6755b3420e3896103c188d75d5e0c2cb2e35)
            check_type(argname="argument thumbprint", value=thumbprint, expected_type=type_hints["thumbprint"])
            check_type(argname="argument x509_store_name", value=x509_store_name, expected_type=type_hints["x509_store_name"])
            check_type(argname="argument thumbprint_secondary", value=thumbprint_secondary, expected_type=type_hints["thumbprint_secondary"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "thumbprint": thumbprint,
            "x509_store_name": x509_store_name,
        }
        if thumbprint_secondary is not None:
            self._values["thumbprint_secondary"] = thumbprint_secondary

    @builtins.property
    def thumbprint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint ServiceFabricCluster#thumbprint}.'''
        result = self._values.get("thumbprint")
        assert result is not None, "Required property 'thumbprint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def x509_store_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#x509_store_name ServiceFabricCluster#x509_store_name}.'''
        result = self._values.get("x509_store_name")
        assert result is not None, "Required property 'x509_store_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def thumbprint_secondary(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint_secondary ServiceFabricCluster#thumbprint_secondary}.'''
        result = self._values.get("thumbprint_secondary")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterCertificateCommonNames",
    jsii_struct_bases=[],
    name_mapping={"common_names": "commonNames", "x509_store_name": "x509StoreName"},
)
class ServiceFabricClusterCertificateCommonNames:
    def __init__(
        self,
        *,
        common_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterCertificateCommonNamesCommonNames", typing.Dict[builtins.str, typing.Any]]]],
        x509_store_name: builtins.str,
    ) -> None:
        '''
        :param common_names: common_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#common_names ServiceFabricCluster#common_names}
        :param x509_store_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#x509_store_name ServiceFabricCluster#x509_store_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfc4e2dd2319de1931f8df3e3422524c35d82573f13010b8066b9f8fafb230d)
            check_type(argname="argument common_names", value=common_names, expected_type=type_hints["common_names"])
            check_type(argname="argument x509_store_name", value=x509_store_name, expected_type=type_hints["x509_store_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "common_names": common_names,
            "x509_store_name": x509_store_name,
        }

    @builtins.property
    def common_names(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterCertificateCommonNamesCommonNames"]]:
        '''common_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#common_names ServiceFabricCluster#common_names}
        '''
        result = self._values.get("common_names")
        assert result is not None, "Required property 'common_names' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterCertificateCommonNamesCommonNames"]], result)

    @builtins.property
    def x509_store_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#x509_store_name ServiceFabricCluster#x509_store_name}.'''
        result = self._values.get("x509_store_name")
        assert result is not None, "Required property 'x509_store_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterCertificateCommonNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterCertificateCommonNamesCommonNames",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_common_name": "certificateCommonName",
        "certificate_issuer_thumbprint": "certificateIssuerThumbprint",
    },
)
class ServiceFabricClusterCertificateCommonNamesCommonNames:
    def __init__(
        self,
        *,
        certificate_common_name: builtins.str,
        certificate_issuer_thumbprint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param certificate_common_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate_common_name ServiceFabricCluster#certificate_common_name}.
        :param certificate_issuer_thumbprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate_issuer_thumbprint ServiceFabricCluster#certificate_issuer_thumbprint}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb63f613634bd5533867ccb791c09b27c8d0bbb07f7502f003e246a2ab55ca7)
            check_type(argname="argument certificate_common_name", value=certificate_common_name, expected_type=type_hints["certificate_common_name"])
            check_type(argname="argument certificate_issuer_thumbprint", value=certificate_issuer_thumbprint, expected_type=type_hints["certificate_issuer_thumbprint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_common_name": certificate_common_name,
        }
        if certificate_issuer_thumbprint is not None:
            self._values["certificate_issuer_thumbprint"] = certificate_issuer_thumbprint

    @builtins.property
    def certificate_common_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate_common_name ServiceFabricCluster#certificate_common_name}.'''
        result = self._values.get("certificate_common_name")
        assert result is not None, "Required property 'certificate_common_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_issuer_thumbprint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate_issuer_thumbprint ServiceFabricCluster#certificate_issuer_thumbprint}.'''
        result = self._values.get("certificate_issuer_thumbprint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterCertificateCommonNamesCommonNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricClusterCertificateCommonNamesCommonNamesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterCertificateCommonNamesCommonNamesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__303bc467940fa49cd801315e9432a53b739cfeec68655d3bbd66132a8c12f8b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceFabricClusterCertificateCommonNamesCommonNamesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e00287ee631050e20d159099d22602402bb40306019bb54df53ebd3a19e22a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceFabricClusterCertificateCommonNamesCommonNamesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbfd87615ef01ebb4d81ed97bb75e1649d2818ac32789ea9eb5d3bc59f9fe387)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c55698c7ee321697a58c75f462508a3b6ba929cecc29854f5ffb43caf1842990)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d15bd016e2d6d95d8a0551cb26521102675811e092cf322cc019c3cdb0d24594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterCertificateCommonNamesCommonNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterCertificateCommonNamesCommonNames]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterCertificateCommonNamesCommonNames]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f34886302bb8e11792883ded5c5d01dd267dbd4f7f4103da7e5dabb7ce834e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricClusterCertificateCommonNamesCommonNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterCertificateCommonNamesCommonNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d80aa828a10c51217074eebf34a5faa2190d7037f4aa460857e2ad330de0651)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificateIssuerThumbprint")
    def reset_certificate_issuer_thumbprint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateIssuerThumbprint", []))

    @builtins.property
    @jsii.member(jsii_name="certificateCommonNameInput")
    def certificate_common_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateCommonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateIssuerThumbprintInput")
    def certificate_issuer_thumbprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateIssuerThumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateCommonName")
    def certificate_common_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateCommonName"))

    @certificate_common_name.setter
    def certificate_common_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35a8928bd762ebdf7ddab7f9507760a40430e62569d8112c1c4c2e3e043c297)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateCommonName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificateIssuerThumbprint")
    def certificate_issuer_thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateIssuerThumbprint"))

    @certificate_issuer_thumbprint.setter
    def certificate_issuer_thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4817a73d59e1d2fecb764c2987db39c72d7faa99bb913002e19f7a1b25eb54b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateIssuerThumbprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterCertificateCommonNamesCommonNames]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterCertificateCommonNamesCommonNames]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterCertificateCommonNamesCommonNames]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb79fe52a53d5c1f4e537327757655979bdbdfedcca7b3d980bcf7a40e93ce6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricClusterCertificateCommonNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterCertificateCommonNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66ba855629e8679333351e232ef3b5bb7e4393777c7dd7f7e5bdfb51fb527201)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCommonNames")
    def put_common_names(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterCertificateCommonNamesCommonNames, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd308b1769c1d35fd7b4705dacc210e68580ef6252787468455250e6a4e768a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCommonNames", [value]))

    @builtins.property
    @jsii.member(jsii_name="commonNames")
    def common_names(self) -> ServiceFabricClusterCertificateCommonNamesCommonNamesList:
        return typing.cast(ServiceFabricClusterCertificateCommonNamesCommonNamesList, jsii.get(self, "commonNames"))

    @builtins.property
    @jsii.member(jsii_name="commonNamesInput")
    def common_names_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterCertificateCommonNamesCommonNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterCertificateCommonNamesCommonNames]]], jsii.get(self, "commonNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="x509StoreNameInput")
    def x509_store_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "x509StoreNameInput"))

    @builtins.property
    @jsii.member(jsii_name="x509StoreName")
    def x509_store_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "x509StoreName"))

    @x509_store_name.setter
    def x509_store_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e39dbaea0797b4405b0119bc827e618d8e09730e6336746fcc717af9bfd6de3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x509StoreName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceFabricClusterCertificateCommonNames]:
        return typing.cast(typing.Optional[ServiceFabricClusterCertificateCommonNames], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFabricClusterCertificateCommonNames],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978d456a86a2fbee25d144abfa52d9ffb257f8b41be40ff756ebfafb3bc24142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricClusterCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46e6e2f94b5bf3dc3b7565e6d5d3a4b22b6d911f8b86eb9b3b234c77869a124b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetThumbprintSecondary")
    def reset_thumbprint_secondary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThumbprintSecondary", []))

    @builtins.property
    @jsii.member(jsii_name="thumbprintInput")
    def thumbprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="thumbprintSecondaryInput")
    def thumbprint_secondary_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thumbprintSecondaryInput"))

    @builtins.property
    @jsii.member(jsii_name="x509StoreNameInput")
    def x509_store_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "x509StoreNameInput"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @thumbprint.setter
    def thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089e98c85a01e07e24b6fcd12430e8bb4181da23e617f42e4abf979b0ddfea8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thumbprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thumbprintSecondary")
    def thumbprint_secondary(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprintSecondary"))

    @thumbprint_secondary.setter
    def thumbprint_secondary(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b024c5207472463bcd4e03585e8ea1033053b84b9f5646d1ad697b2239e007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thumbprintSecondary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="x509StoreName")
    def x509_store_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "x509StoreName"))

    @x509_store_name.setter
    def x509_store_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1295ecba720239de0fd3ac31c8ed7ecbabc79480aa039346cad8f6d7f6ff68a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x509StoreName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceFabricClusterCertificate]:
        return typing.cast(typing.Optional[ServiceFabricClusterCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFabricClusterCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb9f2835e234f77bbc925cd85148f7406624f50ecff182bac660a802912a93b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterClientCertificateCommonName",
    jsii_struct_bases=[],
    name_mapping={
        "common_name": "commonName",
        "is_admin": "isAdmin",
        "issuer_thumbprint": "issuerThumbprint",
    },
)
class ServiceFabricClusterClientCertificateCommonName:
    def __init__(
        self,
        *,
        common_name: builtins.str,
        is_admin: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        issuer_thumbprint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param common_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#common_name ServiceFabricCluster#common_name}.
        :param is_admin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#is_admin ServiceFabricCluster#is_admin}.
        :param issuer_thumbprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#issuer_thumbprint ServiceFabricCluster#issuer_thumbprint}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b6ef950df47cbe51d9da1686dbfe8d6e29e27c4a0bef72d4d1ac077c782f5e)
            check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
            check_type(argname="argument is_admin", value=is_admin, expected_type=type_hints["is_admin"])
            check_type(argname="argument issuer_thumbprint", value=issuer_thumbprint, expected_type=type_hints["issuer_thumbprint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "common_name": common_name,
            "is_admin": is_admin,
        }
        if issuer_thumbprint is not None:
            self._values["issuer_thumbprint"] = issuer_thumbprint

    @builtins.property
    def common_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#common_name ServiceFabricCluster#common_name}.'''
        result = self._values.get("common_name")
        assert result is not None, "Required property 'common_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_admin(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#is_admin ServiceFabricCluster#is_admin}.'''
        result = self._values.get("is_admin")
        assert result is not None, "Required property 'is_admin' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def issuer_thumbprint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#issuer_thumbprint ServiceFabricCluster#issuer_thumbprint}.'''
        result = self._values.get("issuer_thumbprint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterClientCertificateCommonName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricClusterClientCertificateCommonNameList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterClientCertificateCommonNameList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d5e65e1368dbb3302df6382f8dc4faad292a9f823a68f8191f3498be795bcb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceFabricClusterClientCertificateCommonNameOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8934838d5894ff79524ee7c72feea7fca8739226f3bea4007c7148f87c64e183)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceFabricClusterClientCertificateCommonNameOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb6ed7ac2da2db20825a3051d820609b73806e4ff20244db84c1d28bea665e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0d0357cebcae154980a0da624e6aecc5c3e958373f7d0e121cf4a9174904ad5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1abe4ceaa6b357587bdf9afe7c1dd54790f207bb414d73db8f18c68241fb5a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterClientCertificateCommonName]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterClientCertificateCommonName]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterClientCertificateCommonName]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3075c1a09f3eab2d1fdfb57098e62c2ec8c193f6ac27287e6debe75180f7db9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricClusterClientCertificateCommonNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterClientCertificateCommonNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__312c9d8c6f06ba54a206dbb151e8d80852d500237a794cf4f6378a3e81a5a346)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIssuerThumbprint")
    def reset_issuer_thumbprint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuerThumbprint", []))

    @builtins.property
    @jsii.member(jsii_name="commonNameInput")
    def common_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="isAdminInput")
    def is_admin_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isAdminInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerThumbprintInput")
    def issuer_thumbprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerThumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="commonName")
    def common_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commonName"))

    @common_name.setter
    def common_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f317878febe2da060e3e943956e6eccbed03aa30ff5e35595a7c7de0db5766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isAdmin")
    def is_admin(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isAdmin"))

    @is_admin.setter
    def is_admin(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad82646d2fa34c72b04e76bb92202fb763faa64d07ab0e194344e810efa7e2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isAdmin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuerThumbprint")
    def issuer_thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerThumbprint"))

    @issuer_thumbprint.setter
    def issuer_thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528535d52287ec34594b5aba73f128fda9bb8e9c0e662b582d9822caa3a56f98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerThumbprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterClientCertificateCommonName]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterClientCertificateCommonName]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterClientCertificateCommonName]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e19295157ca3253a6baf4140ae4a86e7ce3b17b24fed4e311ef4dc9e5d4bc6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterClientCertificateThumbprint",
    jsii_struct_bases=[],
    name_mapping={"is_admin": "isAdmin", "thumbprint": "thumbprint"},
)
class ServiceFabricClusterClientCertificateThumbprint:
    def __init__(
        self,
        *,
        is_admin: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        thumbprint: builtins.str,
    ) -> None:
        '''
        :param is_admin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#is_admin ServiceFabricCluster#is_admin}.
        :param thumbprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint ServiceFabricCluster#thumbprint}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28feff4373043f5a3c33e88b21b57bf3a6eae2cc80dc0fe5e883afb0fa550969)
            check_type(argname="argument is_admin", value=is_admin, expected_type=type_hints["is_admin"])
            check_type(argname="argument thumbprint", value=thumbprint, expected_type=type_hints["thumbprint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "is_admin": is_admin,
            "thumbprint": thumbprint,
        }

    @builtins.property
    def is_admin(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#is_admin ServiceFabricCluster#is_admin}.'''
        result = self._values.get("is_admin")
        assert result is not None, "Required property 'is_admin' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def thumbprint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint ServiceFabricCluster#thumbprint}.'''
        result = self._values.get("thumbprint")
        assert result is not None, "Required property 'thumbprint' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterClientCertificateThumbprint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricClusterClientCertificateThumbprintList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterClientCertificateThumbprintList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05148e07f5d6595c34f3acc45cf2af45e08df215bee17516f7d673702a859904)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceFabricClusterClientCertificateThumbprintOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f6fa372a543448b142a11a9d1af9a6eb320ac820693c28b7c5ca8ec1c5ecda4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceFabricClusterClientCertificateThumbprintOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff165ac35dc41b124d91f665c1f543ade065014f5e062c22dc5fbab91e44b3ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a23ece02aa589b4d92494025820a238329d16c99f5c57f88fe6c51bce259e37a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e48a04d9ae99187b364b43a46d9b734bbb3984b30068f281daa1125b7306156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterClientCertificateThumbprint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterClientCertificateThumbprint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterClientCertificateThumbprint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758095b0e22e660615ffcb8f6476fcbc3de234b3637d011e8f70604ed949830e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricClusterClientCertificateThumbprintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterClientCertificateThumbprintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6284258c7bad9010db0f80e54d7f6a978f86838399c2c964a9d9dffceacf6b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="isAdminInput")
    def is_admin_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isAdminInput"))

    @builtins.property
    @jsii.member(jsii_name="thumbprintInput")
    def thumbprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="isAdmin")
    def is_admin(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isAdmin"))

    @is_admin.setter
    def is_admin(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f72cc44fddf0c049bb5c5a05579529700177ba9c12d9bc9923af31573adf2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isAdmin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @thumbprint.setter
    def thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c872f81384765a04e541a78abf4c3973ac74bf44ae13a8e9dba2620fc3d223ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thumbprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterClientCertificateThumbprint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterClientCertificateThumbprint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterClientCertificateThumbprint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5f35f0f5399050a6f2652395daada76499e8062895c73c61b6de4cfc7e248c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterConfig",
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
        "management_endpoint": "managementEndpoint",
        "name": "name",
        "node_type": "nodeType",
        "reliability_level": "reliabilityLevel",
        "resource_group_name": "resourceGroupName",
        "upgrade_mode": "upgradeMode",
        "vm_image": "vmImage",
        "add_on_features": "addOnFeatures",
        "azure_active_directory": "azureActiveDirectory",
        "certificate": "certificate",
        "certificate_common_names": "certificateCommonNames",
        "client_certificate_common_name": "clientCertificateCommonName",
        "client_certificate_thumbprint": "clientCertificateThumbprint",
        "cluster_code_version": "clusterCodeVersion",
        "diagnostics_config": "diagnosticsConfig",
        "fabric_settings": "fabricSettings",
        "id": "id",
        "reverse_proxy_certificate": "reverseProxyCertificate",
        "reverse_proxy_certificate_common_names": "reverseProxyCertificateCommonNames",
        "service_fabric_zonal_upgrade_mode": "serviceFabricZonalUpgradeMode",
        "tags": "tags",
        "timeouts": "timeouts",
        "upgrade_policy": "upgradePolicy",
        "vmss_zonal_upgrade_mode": "vmssZonalUpgradeMode",
    },
)
class ServiceFabricClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        management_endpoint: builtins.str,
        name: builtins.str,
        node_type: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterNodeType", typing.Dict[builtins.str, typing.Any]]]],
        reliability_level: builtins.str,
        resource_group_name: builtins.str,
        upgrade_mode: builtins.str,
        vm_image: builtins.str,
        add_on_features: typing.Optional[typing.Sequence[builtins.str]] = None,
        azure_active_directory: typing.Optional[typing.Union[ServiceFabricClusterAzureActiveDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
        certificate: typing.Optional[typing.Union[ServiceFabricClusterCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_common_names: typing.Optional[typing.Union[ServiceFabricClusterCertificateCommonNames, typing.Dict[builtins.str, typing.Any]]] = None,
        client_certificate_common_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterClientCertificateCommonName, typing.Dict[builtins.str, typing.Any]]]]] = None,
        client_certificate_thumbprint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterClientCertificateThumbprint, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cluster_code_version: typing.Optional[builtins.str] = None,
        diagnostics_config: typing.Optional[typing.Union["ServiceFabricClusterDiagnosticsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        fabric_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterFabricSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        reverse_proxy_certificate: typing.Optional[typing.Union["ServiceFabricClusterReverseProxyCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        reverse_proxy_certificate_common_names: typing.Optional[typing.Union["ServiceFabricClusterReverseProxyCertificateCommonNames", typing.Dict[builtins.str, typing.Any]]] = None,
        service_fabric_zonal_upgrade_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ServiceFabricClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_policy: typing.Optional[typing.Union["ServiceFabricClusterUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        vmss_zonal_upgrade_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#location ServiceFabricCluster#location}.
        :param management_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#management_endpoint ServiceFabricCluster#management_endpoint}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#name ServiceFabricCluster#name}.
        :param node_type: node_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#node_type ServiceFabricCluster#node_type}
        :param reliability_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#reliability_level ServiceFabricCluster#reliability_level}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#resource_group_name ServiceFabricCluster#resource_group_name}.
        :param upgrade_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_mode ServiceFabricCluster#upgrade_mode}.
        :param vm_image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#vm_image ServiceFabricCluster#vm_image}.
        :param add_on_features: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#add_on_features ServiceFabricCluster#add_on_features}.
        :param azure_active_directory: azure_active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#azure_active_directory ServiceFabricCluster#azure_active_directory}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate ServiceFabricCluster#certificate}
        :param certificate_common_names: certificate_common_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate_common_names ServiceFabricCluster#certificate_common_names}
        :param client_certificate_common_name: client_certificate_common_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#client_certificate_common_name ServiceFabricCluster#client_certificate_common_name}
        :param client_certificate_thumbprint: client_certificate_thumbprint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#client_certificate_thumbprint ServiceFabricCluster#client_certificate_thumbprint}
        :param cluster_code_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#cluster_code_version ServiceFabricCluster#cluster_code_version}.
        :param diagnostics_config: diagnostics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#diagnostics_config ServiceFabricCluster#diagnostics_config}
        :param fabric_settings: fabric_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#fabric_settings ServiceFabricCluster#fabric_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#id ServiceFabricCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param reverse_proxy_certificate: reverse_proxy_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#reverse_proxy_certificate ServiceFabricCluster#reverse_proxy_certificate}
        :param reverse_proxy_certificate_common_names: reverse_proxy_certificate_common_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#reverse_proxy_certificate_common_names ServiceFabricCluster#reverse_proxy_certificate_common_names}
        :param service_fabric_zonal_upgrade_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#service_fabric_zonal_upgrade_mode ServiceFabricCluster#service_fabric_zonal_upgrade_mode}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#tags ServiceFabricCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#timeouts ServiceFabricCluster#timeouts}
        :param upgrade_policy: upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_policy ServiceFabricCluster#upgrade_policy}
        :param vmss_zonal_upgrade_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#vmss_zonal_upgrade_mode ServiceFabricCluster#vmss_zonal_upgrade_mode}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(azure_active_directory, dict):
            azure_active_directory = ServiceFabricClusterAzureActiveDirectory(**azure_active_directory)
        if isinstance(certificate, dict):
            certificate = ServiceFabricClusterCertificate(**certificate)
        if isinstance(certificate_common_names, dict):
            certificate_common_names = ServiceFabricClusterCertificateCommonNames(**certificate_common_names)
        if isinstance(diagnostics_config, dict):
            diagnostics_config = ServiceFabricClusterDiagnosticsConfig(**diagnostics_config)
        if isinstance(reverse_proxy_certificate, dict):
            reverse_proxy_certificate = ServiceFabricClusterReverseProxyCertificate(**reverse_proxy_certificate)
        if isinstance(reverse_proxy_certificate_common_names, dict):
            reverse_proxy_certificate_common_names = ServiceFabricClusterReverseProxyCertificateCommonNames(**reverse_proxy_certificate_common_names)
        if isinstance(timeouts, dict):
            timeouts = ServiceFabricClusterTimeouts(**timeouts)
        if isinstance(upgrade_policy, dict):
            upgrade_policy = ServiceFabricClusterUpgradePolicy(**upgrade_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7006e5b8e427f5efcc75f1a9947fe3aad4ac02143bc5bf8264568372f990bd15)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument management_endpoint", value=management_endpoint, expected_type=type_hints["management_endpoint"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument reliability_level", value=reliability_level, expected_type=type_hints["reliability_level"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument upgrade_mode", value=upgrade_mode, expected_type=type_hints["upgrade_mode"])
            check_type(argname="argument vm_image", value=vm_image, expected_type=type_hints["vm_image"])
            check_type(argname="argument add_on_features", value=add_on_features, expected_type=type_hints["add_on_features"])
            check_type(argname="argument azure_active_directory", value=azure_active_directory, expected_type=type_hints["azure_active_directory"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_common_names", value=certificate_common_names, expected_type=type_hints["certificate_common_names"])
            check_type(argname="argument client_certificate_common_name", value=client_certificate_common_name, expected_type=type_hints["client_certificate_common_name"])
            check_type(argname="argument client_certificate_thumbprint", value=client_certificate_thumbprint, expected_type=type_hints["client_certificate_thumbprint"])
            check_type(argname="argument cluster_code_version", value=cluster_code_version, expected_type=type_hints["cluster_code_version"])
            check_type(argname="argument diagnostics_config", value=diagnostics_config, expected_type=type_hints["diagnostics_config"])
            check_type(argname="argument fabric_settings", value=fabric_settings, expected_type=type_hints["fabric_settings"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument reverse_proxy_certificate", value=reverse_proxy_certificate, expected_type=type_hints["reverse_proxy_certificate"])
            check_type(argname="argument reverse_proxy_certificate_common_names", value=reverse_proxy_certificate_common_names, expected_type=type_hints["reverse_proxy_certificate_common_names"])
            check_type(argname="argument service_fabric_zonal_upgrade_mode", value=service_fabric_zonal_upgrade_mode, expected_type=type_hints["service_fabric_zonal_upgrade_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument upgrade_policy", value=upgrade_policy, expected_type=type_hints["upgrade_policy"])
            check_type(argname="argument vmss_zonal_upgrade_mode", value=vmss_zonal_upgrade_mode, expected_type=type_hints["vmss_zonal_upgrade_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "management_endpoint": management_endpoint,
            "name": name,
            "node_type": node_type,
            "reliability_level": reliability_level,
            "resource_group_name": resource_group_name,
            "upgrade_mode": upgrade_mode,
            "vm_image": vm_image,
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
        if add_on_features is not None:
            self._values["add_on_features"] = add_on_features
        if azure_active_directory is not None:
            self._values["azure_active_directory"] = azure_active_directory
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_common_names is not None:
            self._values["certificate_common_names"] = certificate_common_names
        if client_certificate_common_name is not None:
            self._values["client_certificate_common_name"] = client_certificate_common_name
        if client_certificate_thumbprint is not None:
            self._values["client_certificate_thumbprint"] = client_certificate_thumbprint
        if cluster_code_version is not None:
            self._values["cluster_code_version"] = cluster_code_version
        if diagnostics_config is not None:
            self._values["diagnostics_config"] = diagnostics_config
        if fabric_settings is not None:
            self._values["fabric_settings"] = fabric_settings
        if id is not None:
            self._values["id"] = id
        if reverse_proxy_certificate is not None:
            self._values["reverse_proxy_certificate"] = reverse_proxy_certificate
        if reverse_proxy_certificate_common_names is not None:
            self._values["reverse_proxy_certificate_common_names"] = reverse_proxy_certificate_common_names
        if service_fabric_zonal_upgrade_mode is not None:
            self._values["service_fabric_zonal_upgrade_mode"] = service_fabric_zonal_upgrade_mode
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if upgrade_policy is not None:
            self._values["upgrade_policy"] = upgrade_policy
        if vmss_zonal_upgrade_mode is not None:
            self._values["vmss_zonal_upgrade_mode"] = vmss_zonal_upgrade_mode

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#location ServiceFabricCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def management_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#management_endpoint ServiceFabricCluster#management_endpoint}.'''
        result = self._values.get("management_endpoint")
        assert result is not None, "Required property 'management_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#name ServiceFabricCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_type(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterNodeType"]]:
        '''node_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#node_type ServiceFabricCluster#node_type}
        '''
        result = self._values.get("node_type")
        assert result is not None, "Required property 'node_type' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterNodeType"]], result)

    @builtins.property
    def reliability_level(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#reliability_level ServiceFabricCluster#reliability_level}.'''
        result = self._values.get("reliability_level")
        assert result is not None, "Required property 'reliability_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#resource_group_name ServiceFabricCluster#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def upgrade_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_mode ServiceFabricCluster#upgrade_mode}.'''
        result = self._values.get("upgrade_mode")
        assert result is not None, "Required property 'upgrade_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_image(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#vm_image ServiceFabricCluster#vm_image}.'''
        result = self._values.get("vm_image")
        assert result is not None, "Required property 'vm_image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def add_on_features(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#add_on_features ServiceFabricCluster#add_on_features}.'''
        result = self._values.get("add_on_features")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def azure_active_directory(
        self,
    ) -> typing.Optional[ServiceFabricClusterAzureActiveDirectory]:
        '''azure_active_directory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#azure_active_directory ServiceFabricCluster#azure_active_directory}
        '''
        result = self._values.get("azure_active_directory")
        return typing.cast(typing.Optional[ServiceFabricClusterAzureActiveDirectory], result)

    @builtins.property
    def certificate(self) -> typing.Optional[ServiceFabricClusterCertificate]:
        '''certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate ServiceFabricCluster#certificate}
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[ServiceFabricClusterCertificate], result)

    @builtins.property
    def certificate_common_names(
        self,
    ) -> typing.Optional[ServiceFabricClusterCertificateCommonNames]:
        '''certificate_common_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate_common_names ServiceFabricCluster#certificate_common_names}
        '''
        result = self._values.get("certificate_common_names")
        return typing.cast(typing.Optional[ServiceFabricClusterCertificateCommonNames], result)

    @builtins.property
    def client_certificate_common_name(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterClientCertificateCommonName]]]:
        '''client_certificate_common_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#client_certificate_common_name ServiceFabricCluster#client_certificate_common_name}
        '''
        result = self._values.get("client_certificate_common_name")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterClientCertificateCommonName]]], result)

    @builtins.property
    def client_certificate_thumbprint(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterClientCertificateThumbprint]]]:
        '''client_certificate_thumbprint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#client_certificate_thumbprint ServiceFabricCluster#client_certificate_thumbprint}
        '''
        result = self._values.get("client_certificate_thumbprint")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterClientCertificateThumbprint]]], result)

    @builtins.property
    def cluster_code_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#cluster_code_version ServiceFabricCluster#cluster_code_version}.'''
        result = self._values.get("cluster_code_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def diagnostics_config(
        self,
    ) -> typing.Optional["ServiceFabricClusterDiagnosticsConfig"]:
        '''diagnostics_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#diagnostics_config ServiceFabricCluster#diagnostics_config}
        '''
        result = self._values.get("diagnostics_config")
        return typing.cast(typing.Optional["ServiceFabricClusterDiagnosticsConfig"], result)

    @builtins.property
    def fabric_settings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterFabricSettings"]]]:
        '''fabric_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#fabric_settings ServiceFabricCluster#fabric_settings}
        '''
        result = self._values.get("fabric_settings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterFabricSettings"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#id ServiceFabricCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reverse_proxy_certificate(
        self,
    ) -> typing.Optional["ServiceFabricClusterReverseProxyCertificate"]:
        '''reverse_proxy_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#reverse_proxy_certificate ServiceFabricCluster#reverse_proxy_certificate}
        '''
        result = self._values.get("reverse_proxy_certificate")
        return typing.cast(typing.Optional["ServiceFabricClusterReverseProxyCertificate"], result)

    @builtins.property
    def reverse_proxy_certificate_common_names(
        self,
    ) -> typing.Optional["ServiceFabricClusterReverseProxyCertificateCommonNames"]:
        '''reverse_proxy_certificate_common_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#reverse_proxy_certificate_common_names ServiceFabricCluster#reverse_proxy_certificate_common_names}
        '''
        result = self._values.get("reverse_proxy_certificate_common_names")
        return typing.cast(typing.Optional["ServiceFabricClusterReverseProxyCertificateCommonNames"], result)

    @builtins.property
    def service_fabric_zonal_upgrade_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#service_fabric_zonal_upgrade_mode ServiceFabricCluster#service_fabric_zonal_upgrade_mode}.'''
        result = self._values.get("service_fabric_zonal_upgrade_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#tags ServiceFabricCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ServiceFabricClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#timeouts ServiceFabricCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ServiceFabricClusterTimeouts"], result)

    @builtins.property
    def upgrade_policy(self) -> typing.Optional["ServiceFabricClusterUpgradePolicy"]:
        '''upgrade_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_policy ServiceFabricCluster#upgrade_policy}
        '''
        result = self._values.get("upgrade_policy")
        return typing.cast(typing.Optional["ServiceFabricClusterUpgradePolicy"], result)

    @builtins.property
    def vmss_zonal_upgrade_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#vmss_zonal_upgrade_mode ServiceFabricCluster#vmss_zonal_upgrade_mode}.'''
        result = self._values.get("vmss_zonal_upgrade_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterDiagnosticsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "blob_endpoint": "blobEndpoint",
        "protected_account_key_name": "protectedAccountKeyName",
        "queue_endpoint": "queueEndpoint",
        "storage_account_name": "storageAccountName",
        "table_endpoint": "tableEndpoint",
    },
)
class ServiceFabricClusterDiagnosticsConfig:
    def __init__(
        self,
        *,
        blob_endpoint: builtins.str,
        protected_account_key_name: builtins.str,
        queue_endpoint: builtins.str,
        storage_account_name: builtins.str,
        table_endpoint: builtins.str,
    ) -> None:
        '''
        :param blob_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#blob_endpoint ServiceFabricCluster#blob_endpoint}.
        :param protected_account_key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#protected_account_key_name ServiceFabricCluster#protected_account_key_name}.
        :param queue_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#queue_endpoint ServiceFabricCluster#queue_endpoint}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#storage_account_name ServiceFabricCluster#storage_account_name}.
        :param table_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#table_endpoint ServiceFabricCluster#table_endpoint}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac01a4f93923d121137459d7e6f1043aec7b793bafe3aa8a3b150e5f707423e)
            check_type(argname="argument blob_endpoint", value=blob_endpoint, expected_type=type_hints["blob_endpoint"])
            check_type(argname="argument protected_account_key_name", value=protected_account_key_name, expected_type=type_hints["protected_account_key_name"])
            check_type(argname="argument queue_endpoint", value=queue_endpoint, expected_type=type_hints["queue_endpoint"])
            check_type(argname="argument storage_account_name", value=storage_account_name, expected_type=type_hints["storage_account_name"])
            check_type(argname="argument table_endpoint", value=table_endpoint, expected_type=type_hints["table_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "blob_endpoint": blob_endpoint,
            "protected_account_key_name": protected_account_key_name,
            "queue_endpoint": queue_endpoint,
            "storage_account_name": storage_account_name,
            "table_endpoint": table_endpoint,
        }

    @builtins.property
    def blob_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#blob_endpoint ServiceFabricCluster#blob_endpoint}.'''
        result = self._values.get("blob_endpoint")
        assert result is not None, "Required property 'blob_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protected_account_key_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#protected_account_key_name ServiceFabricCluster#protected_account_key_name}.'''
        result = self._values.get("protected_account_key_name")
        assert result is not None, "Required property 'protected_account_key_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def queue_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#queue_endpoint ServiceFabricCluster#queue_endpoint}.'''
        result = self._values.get("queue_endpoint")
        assert result is not None, "Required property 'queue_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#storage_account_name ServiceFabricCluster#storage_account_name}.'''
        result = self._values.get("storage_account_name")
        assert result is not None, "Required property 'storage_account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#table_endpoint ServiceFabricCluster#table_endpoint}.'''
        result = self._values.get("table_endpoint")
        assert result is not None, "Required property 'table_endpoint' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterDiagnosticsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricClusterDiagnosticsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterDiagnosticsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c436ab80a33d7026b72df27d70d61971e5f301c7be8bf9771ef33168ab08e73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="blobEndpointInput")
    def blob_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blobEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="protectedAccountKeyNameInput")
    def protected_account_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protectedAccountKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="queueEndpointInput")
    def queue_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountNameInput")
    def storage_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tableEndpointInput")
    def table_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="blobEndpoint")
    def blob_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blobEndpoint"))

    @blob_endpoint.setter
    def blob_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b08dc4d707cecdbc57de7352db8f6bceed4344f282c7f65d5ecf1a5c57dcc7e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blobEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protectedAccountKeyName")
    def protected_account_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectedAccountKeyName"))

    @protected_account_key_name.setter
    def protected_account_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b46783b7ef92e6c24f9b2ee187e366f20fd2692798ab94a90288da9319904d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectedAccountKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueEndpoint")
    def queue_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueEndpoint"))

    @queue_endpoint.setter
    def queue_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d96b83d4d31c57f9ba462ae050457cf4c960496e7fa02d56c52f25f583d38b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountName")
    def storage_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountName"))

    @storage_account_name.setter
    def storage_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9efb7de991399fc42b454a74bfc3a33804c132e915cc538881078bd8933388f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableEndpoint")
    def table_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableEndpoint"))

    @table_endpoint.setter
    def table_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d458a2208868f41606a70a164ce4e030abe1b8a8c60326522bde06f7d9b87970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceFabricClusterDiagnosticsConfig]:
        return typing.cast(typing.Optional[ServiceFabricClusterDiagnosticsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFabricClusterDiagnosticsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0619ef725eb5ee44f4ecd985b0410e3747d8476ca6b7b2adb7c10d6a17453472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterFabricSettings",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parameters": "parameters"},
)
class ServiceFabricClusterFabricSettings:
    def __init__(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#name ServiceFabricCluster#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#parameters ServiceFabricCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32a4e0c4d2a26bab1fb9749ab177b1fc9c9cd3bc06c678db3a8be82857ce9588)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#name ServiceFabricCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#parameters ServiceFabricCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterFabricSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricClusterFabricSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterFabricSettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d05fd25fc82c7ec493b7c16890cf3c104c74466dcab428522cabb10836b17fe1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceFabricClusterFabricSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44fafd345fd53980fef97429ac867d83681f52ea38713942cb41bcb6d4ddac78)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceFabricClusterFabricSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd67f6922dcc878e0010ab624049a56b52b3d0a4c87ec14b79e1775711d889e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dcfdc52188b8e1555ef90ca9afde9a79923316f06555aa0ecf34253c7605cd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bd0fe75ae7e355d11728c1e3a23d6a08dbe3f4ec2463571e14b2d40886d0242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterFabricSettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterFabricSettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterFabricSettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430eeabae0fdff766c164c5aca2a45a202db75ebc47dab4cb65d76e6ae91abd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricClusterFabricSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterFabricSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a7c79e992c4d4947f329a5a533e5bdb6aea34ed0198e52071fd7cbfea8e9f86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b623b7d71ac978eafdaddebaca26f8c86e18c59b8dd3f9d93dadc9f9f0daaa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1fd28d0f934faa3c9143b72966f324c945cd2cabdf0a97fc360fbc3a029d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterFabricSettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterFabricSettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterFabricSettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__070ecc837780bbe7c5fcef1422dab635266f9ba4e6f478b8894efe63d87210db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterNodeType",
    jsii_struct_bases=[],
    name_mapping={
        "client_endpoint_port": "clientEndpointPort",
        "http_endpoint_port": "httpEndpointPort",
        "instance_count": "instanceCount",
        "is_primary": "isPrimary",
        "name": "name",
        "application_ports": "applicationPorts",
        "capacities": "capacities",
        "durability_level": "durabilityLevel",
        "ephemeral_ports": "ephemeralPorts",
        "is_stateless": "isStateless",
        "multiple_availability_zones": "multipleAvailabilityZones",
        "placement_properties": "placementProperties",
        "reverse_proxy_endpoint_port": "reverseProxyEndpointPort",
    },
)
class ServiceFabricClusterNodeType:
    def __init__(
        self,
        *,
        client_endpoint_port: jsii.Number,
        http_endpoint_port: jsii.Number,
        instance_count: jsii.Number,
        is_primary: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        application_ports: typing.Optional[typing.Union["ServiceFabricClusterNodeTypeApplicationPorts", typing.Dict[builtins.str, typing.Any]]] = None,
        capacities: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        durability_level: typing.Optional[builtins.str] = None,
        ephemeral_ports: typing.Optional[typing.Union["ServiceFabricClusterNodeTypeEphemeralPorts", typing.Dict[builtins.str, typing.Any]]] = None,
        is_stateless: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        multiple_availability_zones: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        placement_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        reverse_proxy_endpoint_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param client_endpoint_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#client_endpoint_port ServiceFabricCluster#client_endpoint_port}.
        :param http_endpoint_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#http_endpoint_port ServiceFabricCluster#http_endpoint_port}.
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#instance_count ServiceFabricCluster#instance_count}.
        :param is_primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#is_primary ServiceFabricCluster#is_primary}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#name ServiceFabricCluster#name}.
        :param application_ports: application_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#application_ports ServiceFabricCluster#application_ports}
        :param capacities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#capacities ServiceFabricCluster#capacities}.
        :param durability_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#durability_level ServiceFabricCluster#durability_level}.
        :param ephemeral_ports: ephemeral_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#ephemeral_ports ServiceFabricCluster#ephemeral_ports}
        :param is_stateless: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#is_stateless ServiceFabricCluster#is_stateless}.
        :param multiple_availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#multiple_availability_zones ServiceFabricCluster#multiple_availability_zones}.
        :param placement_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#placement_properties ServiceFabricCluster#placement_properties}.
        :param reverse_proxy_endpoint_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#reverse_proxy_endpoint_port ServiceFabricCluster#reverse_proxy_endpoint_port}.
        '''
        if isinstance(application_ports, dict):
            application_ports = ServiceFabricClusterNodeTypeApplicationPorts(**application_ports)
        if isinstance(ephemeral_ports, dict):
            ephemeral_ports = ServiceFabricClusterNodeTypeEphemeralPorts(**ephemeral_ports)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03cd6fabdc156c3c5422ef24d457cbdedffa683f278f5274911f7a43bba2099d)
            check_type(argname="argument client_endpoint_port", value=client_endpoint_port, expected_type=type_hints["client_endpoint_port"])
            check_type(argname="argument http_endpoint_port", value=http_endpoint_port, expected_type=type_hints["http_endpoint_port"])
            check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
            check_type(argname="argument is_primary", value=is_primary, expected_type=type_hints["is_primary"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument application_ports", value=application_ports, expected_type=type_hints["application_ports"])
            check_type(argname="argument capacities", value=capacities, expected_type=type_hints["capacities"])
            check_type(argname="argument durability_level", value=durability_level, expected_type=type_hints["durability_level"])
            check_type(argname="argument ephemeral_ports", value=ephemeral_ports, expected_type=type_hints["ephemeral_ports"])
            check_type(argname="argument is_stateless", value=is_stateless, expected_type=type_hints["is_stateless"])
            check_type(argname="argument multiple_availability_zones", value=multiple_availability_zones, expected_type=type_hints["multiple_availability_zones"])
            check_type(argname="argument placement_properties", value=placement_properties, expected_type=type_hints["placement_properties"])
            check_type(argname="argument reverse_proxy_endpoint_port", value=reverse_proxy_endpoint_port, expected_type=type_hints["reverse_proxy_endpoint_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_endpoint_port": client_endpoint_port,
            "http_endpoint_port": http_endpoint_port,
            "instance_count": instance_count,
            "is_primary": is_primary,
            "name": name,
        }
        if application_ports is not None:
            self._values["application_ports"] = application_ports
        if capacities is not None:
            self._values["capacities"] = capacities
        if durability_level is not None:
            self._values["durability_level"] = durability_level
        if ephemeral_ports is not None:
            self._values["ephemeral_ports"] = ephemeral_ports
        if is_stateless is not None:
            self._values["is_stateless"] = is_stateless
        if multiple_availability_zones is not None:
            self._values["multiple_availability_zones"] = multiple_availability_zones
        if placement_properties is not None:
            self._values["placement_properties"] = placement_properties
        if reverse_proxy_endpoint_port is not None:
            self._values["reverse_proxy_endpoint_port"] = reverse_proxy_endpoint_port

    @builtins.property
    def client_endpoint_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#client_endpoint_port ServiceFabricCluster#client_endpoint_port}.'''
        result = self._values.get("client_endpoint_port")
        assert result is not None, "Required property 'client_endpoint_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def http_endpoint_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#http_endpoint_port ServiceFabricCluster#http_endpoint_port}.'''
        result = self._values.get("http_endpoint_port")
        assert result is not None, "Required property 'http_endpoint_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#instance_count ServiceFabricCluster#instance_count}.'''
        result = self._values.get("instance_count")
        assert result is not None, "Required property 'instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def is_primary(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#is_primary ServiceFabricCluster#is_primary}.'''
        result = self._values.get("is_primary")
        assert result is not None, "Required property 'is_primary' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#name ServiceFabricCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_ports(
        self,
    ) -> typing.Optional["ServiceFabricClusterNodeTypeApplicationPorts"]:
        '''application_ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#application_ports ServiceFabricCluster#application_ports}
        '''
        result = self._values.get("application_ports")
        return typing.cast(typing.Optional["ServiceFabricClusterNodeTypeApplicationPorts"], result)

    @builtins.property
    def capacities(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#capacities ServiceFabricCluster#capacities}.'''
        result = self._values.get("capacities")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def durability_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#durability_level ServiceFabricCluster#durability_level}.'''
        result = self._values.get("durability_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ephemeral_ports(
        self,
    ) -> typing.Optional["ServiceFabricClusterNodeTypeEphemeralPorts"]:
        '''ephemeral_ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#ephemeral_ports ServiceFabricCluster#ephemeral_ports}
        '''
        result = self._values.get("ephemeral_ports")
        return typing.cast(typing.Optional["ServiceFabricClusterNodeTypeEphemeralPorts"], result)

    @builtins.property
    def is_stateless(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#is_stateless ServiceFabricCluster#is_stateless}.'''
        result = self._values.get("is_stateless")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def multiple_availability_zones(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#multiple_availability_zones ServiceFabricCluster#multiple_availability_zones}.'''
        result = self._values.get("multiple_availability_zones")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def placement_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#placement_properties ServiceFabricCluster#placement_properties}.'''
        result = self._values.get("placement_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def reverse_proxy_endpoint_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#reverse_proxy_endpoint_port ServiceFabricCluster#reverse_proxy_endpoint_port}.'''
        result = self._values.get("reverse_proxy_endpoint_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterNodeType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterNodeTypeApplicationPorts",
    jsii_struct_bases=[],
    name_mapping={"end_port": "endPort", "start_port": "startPort"},
)
class ServiceFabricClusterNodeTypeApplicationPorts:
    def __init__(self, *, end_port: jsii.Number, start_port: jsii.Number) -> None:
        '''
        :param end_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#end_port ServiceFabricCluster#end_port}.
        :param start_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#start_port ServiceFabricCluster#start_port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76536b620d87e133397e36cbe5d5a3f38b8ed65e5afe18c5d545ff25aa95599d)
            check_type(argname="argument end_port", value=end_port, expected_type=type_hints["end_port"])
            check_type(argname="argument start_port", value=start_port, expected_type=type_hints["start_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_port": end_port,
            "start_port": start_port,
        }

    @builtins.property
    def end_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#end_port ServiceFabricCluster#end_port}.'''
        result = self._values.get("end_port")
        assert result is not None, "Required property 'end_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#start_port ServiceFabricCluster#start_port}.'''
        result = self._values.get("start_port")
        assert result is not None, "Required property 'start_port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterNodeTypeApplicationPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricClusterNodeTypeApplicationPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterNodeTypeApplicationPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57c6dda839f6852db5f1943c830922326d852c011c839793663bb08392f3fa3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endPortInput")
    def end_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endPortInput"))

    @builtins.property
    @jsii.member(jsii_name="startPortInput")
    def start_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startPortInput"))

    @builtins.property
    @jsii.member(jsii_name="endPort")
    def end_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "endPort"))

    @end_port.setter
    def end_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68aee28f93742ebce5cc18ce1de5b95489bb60a0e7fb22c04dc841ebbfe76928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startPort")
    def start_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startPort"))

    @start_port.setter
    def start_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e460d0a343b97154aeecb814c8e413d95d757e617a669999973db56910c925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceFabricClusterNodeTypeApplicationPorts]:
        return typing.cast(typing.Optional[ServiceFabricClusterNodeTypeApplicationPorts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFabricClusterNodeTypeApplicationPorts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd3faad9702265f4b6a6b794fcfbafa2ddb8c56045c4c97c9754f15b47d10e43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterNodeTypeEphemeralPorts",
    jsii_struct_bases=[],
    name_mapping={"end_port": "endPort", "start_port": "startPort"},
)
class ServiceFabricClusterNodeTypeEphemeralPorts:
    def __init__(self, *, end_port: jsii.Number, start_port: jsii.Number) -> None:
        '''
        :param end_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#end_port ServiceFabricCluster#end_port}.
        :param start_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#start_port ServiceFabricCluster#start_port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33322a04e6f4ed1edfe207e2c4d36601447edc9456118e95ea67fc11b2e3332b)
            check_type(argname="argument end_port", value=end_port, expected_type=type_hints["end_port"])
            check_type(argname="argument start_port", value=start_port, expected_type=type_hints["start_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_port": end_port,
            "start_port": start_port,
        }

    @builtins.property
    def end_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#end_port ServiceFabricCluster#end_port}.'''
        result = self._values.get("end_port")
        assert result is not None, "Required property 'end_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#start_port ServiceFabricCluster#start_port}.'''
        result = self._values.get("start_port")
        assert result is not None, "Required property 'start_port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterNodeTypeEphemeralPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricClusterNodeTypeEphemeralPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterNodeTypeEphemeralPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f800f82790fd04a1d99f0391cbed4036e667993820c553fd7f1ed2cd4814c64c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endPortInput")
    def end_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endPortInput"))

    @builtins.property
    @jsii.member(jsii_name="startPortInput")
    def start_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startPortInput"))

    @builtins.property
    @jsii.member(jsii_name="endPort")
    def end_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "endPort"))

    @end_port.setter
    def end_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8f9a52c7347a23570cb53008bd3e50417b2d1e3b026e1bd22a8522a60852c0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startPort")
    def start_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startPort"))

    @start_port.setter
    def start_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3757fbe66e269a8136764d10661fc9a082f73d96e42a40262837d7cb99ac5a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceFabricClusterNodeTypeEphemeralPorts]:
        return typing.cast(typing.Optional[ServiceFabricClusterNodeTypeEphemeralPorts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFabricClusterNodeTypeEphemeralPorts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a746d333751d319ddac64394290b296df63192402bcc21bcd4a5f166b32868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricClusterNodeTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterNodeTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8dd72eea7ad12ba9881464a0240a59e8badc2c07af65154458e89bffed174c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceFabricClusterNodeTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e93ad6b0836271d19e0dc625c13d3d9ec096114b5d9fabea81d8911f2479c821)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceFabricClusterNodeTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e730718464f478eacac7265c68dd2e561250622da188b4be078fd565437e2d07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__254a9de5464429de7cc0adc29904f457aa520bd8b72e7beb541af22d18def1e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9624e19123ff423c6f0ae2389a9896d41d55bac5e0289843fbc6324a94b0142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterNodeType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterNodeType]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterNodeType]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__723dd911b53b8a07e9f3545ec68b886afb9f9fd4dee1697a399f3f50d176d659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricClusterNodeTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterNodeTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a1dbdd0fdf7cd8e632408cc21f78455030411342af45fc5c4f1dc260c95e4ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putApplicationPorts")
    def put_application_ports(
        self,
        *,
        end_port: jsii.Number,
        start_port: jsii.Number,
    ) -> None:
        '''
        :param end_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#end_port ServiceFabricCluster#end_port}.
        :param start_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#start_port ServiceFabricCluster#start_port}.
        '''
        value = ServiceFabricClusterNodeTypeApplicationPorts(
            end_port=end_port, start_port=start_port
        )

        return typing.cast(None, jsii.invoke(self, "putApplicationPorts", [value]))

    @jsii.member(jsii_name="putEphemeralPorts")
    def put_ephemeral_ports(
        self,
        *,
        end_port: jsii.Number,
        start_port: jsii.Number,
    ) -> None:
        '''
        :param end_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#end_port ServiceFabricCluster#end_port}.
        :param start_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#start_port ServiceFabricCluster#start_port}.
        '''
        value = ServiceFabricClusterNodeTypeEphemeralPorts(
            end_port=end_port, start_port=start_port
        )

        return typing.cast(None, jsii.invoke(self, "putEphemeralPorts", [value]))

    @jsii.member(jsii_name="resetApplicationPorts")
    def reset_application_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationPorts", []))

    @jsii.member(jsii_name="resetCapacities")
    def reset_capacities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacities", []))

    @jsii.member(jsii_name="resetDurabilityLevel")
    def reset_durability_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDurabilityLevel", []))

    @jsii.member(jsii_name="resetEphemeralPorts")
    def reset_ephemeral_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEphemeralPorts", []))

    @jsii.member(jsii_name="resetIsStateless")
    def reset_is_stateless(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsStateless", []))

    @jsii.member(jsii_name="resetMultipleAvailabilityZones")
    def reset_multiple_availability_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultipleAvailabilityZones", []))

    @jsii.member(jsii_name="resetPlacementProperties")
    def reset_placement_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacementProperties", []))

    @jsii.member(jsii_name="resetReverseProxyEndpointPort")
    def reset_reverse_proxy_endpoint_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReverseProxyEndpointPort", []))

    @builtins.property
    @jsii.member(jsii_name="applicationPorts")
    def application_ports(
        self,
    ) -> ServiceFabricClusterNodeTypeApplicationPortsOutputReference:
        return typing.cast(ServiceFabricClusterNodeTypeApplicationPortsOutputReference, jsii.get(self, "applicationPorts"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralPorts")
    def ephemeral_ports(
        self,
    ) -> ServiceFabricClusterNodeTypeEphemeralPortsOutputReference:
        return typing.cast(ServiceFabricClusterNodeTypeEphemeralPortsOutputReference, jsii.get(self, "ephemeralPorts"))

    @builtins.property
    @jsii.member(jsii_name="applicationPortsInput")
    def application_ports_input(
        self,
    ) -> typing.Optional[ServiceFabricClusterNodeTypeApplicationPorts]:
        return typing.cast(typing.Optional[ServiceFabricClusterNodeTypeApplicationPorts], jsii.get(self, "applicationPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="capacitiesInput")
    def capacities_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "capacitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientEndpointPortInput")
    def client_endpoint_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clientEndpointPortInput"))

    @builtins.property
    @jsii.member(jsii_name="durabilityLevelInput")
    def durability_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durabilityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralPortsInput")
    def ephemeral_ports_input(
        self,
    ) -> typing.Optional[ServiceFabricClusterNodeTypeEphemeralPorts]:
        return typing.cast(typing.Optional[ServiceFabricClusterNodeTypeEphemeralPorts], jsii.get(self, "ephemeralPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpEndpointPortInput")
    def http_endpoint_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpEndpointPortInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceCountInput")
    def instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="isPrimaryInput")
    def is_primary_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isPrimaryInput"))

    @builtins.property
    @jsii.member(jsii_name="isStatelessInput")
    def is_stateless_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isStatelessInput"))

    @builtins.property
    @jsii.member(jsii_name="multipleAvailabilityZonesInput")
    def multiple_availability_zones_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "multipleAvailabilityZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="placementPropertiesInput")
    def placement_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "placementPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="reverseProxyEndpointPortInput")
    def reverse_proxy_endpoint_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "reverseProxyEndpointPortInput"))

    @builtins.property
    @jsii.member(jsii_name="capacities")
    def capacities(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "capacities"))

    @capacities.setter
    def capacities(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246e7b6d570c3fa5904e1f19cb444dbda6eb0f2e7cd66e60fa88c62d29dcada3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientEndpointPort")
    def client_endpoint_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientEndpointPort"))

    @client_endpoint_port.setter
    def client_endpoint_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69010fbc7a3430fd1c7b1d767cd9a7696d7bfb5af7864a8a971b6322e6e5a8ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientEndpointPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="durabilityLevel")
    def durability_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "durabilityLevel"))

    @durability_level.setter
    def durability_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c22df8454261bd4ea1fb549a7756f482312bc6cb1f8df5f65e989386f94fd1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durabilityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpEndpointPort")
    def http_endpoint_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpEndpointPort"))

    @http_endpoint_port.setter
    def http_endpoint_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd390244df67d8a3235353f64a93ccc65114063415bb3c85e4b27a54d11e7431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpEndpointPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceCount")
    def instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceCount"))

    @instance_count.setter
    def instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b49f00f1dfda7746267907166dbdd671cbc45c81a8080d2366ab4ccb49467b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isPrimary")
    def is_primary(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isPrimary"))

    @is_primary.setter
    def is_primary(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__831e7c13936585bdfd8a39ddc40a0376e601fcf28ec341aaf478881a6c26aa0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPrimary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isStateless")
    def is_stateless(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isStateless"))

    @is_stateless.setter
    def is_stateless(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e71f0348c084a54b761a4419ed697904fafafa084b06b8e109dd4381b3c7639f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isStateless", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multipleAvailabilityZones")
    def multiple_availability_zones(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "multipleAvailabilityZones"))

    @multiple_availability_zones.setter
    def multiple_availability_zones(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67a5ed6ef30c6a1d8950a3002ba91d2ce66a32a4dccc92228611c27f6e20da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multipleAvailabilityZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1558feab2c96062a36f2489b5def01ce7dcafa596551182cb60c2884ce41d408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="placementProperties")
    def placement_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "placementProperties"))

    @placement_properties.setter
    def placement_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4650a49a6d5f236209e5fa0e76460350a0642fd07d693241ad98870077395c97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "placementProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reverseProxyEndpointPort")
    def reverse_proxy_endpoint_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "reverseProxyEndpointPort"))

    @reverse_proxy_endpoint_port.setter
    def reverse_proxy_endpoint_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c4f257e6526b5ccdfafebbf000c88b9d8f8e5155e15854082243eec11131a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reverseProxyEndpointPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterNodeType]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterNodeType]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterNodeType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7769a9c15bbe9d0b7895ac743592daad6b3e05928e38b55c5ad8a8655dbd6ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterReverseProxyCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "thumbprint": "thumbprint",
        "x509_store_name": "x509StoreName",
        "thumbprint_secondary": "thumbprintSecondary",
    },
)
class ServiceFabricClusterReverseProxyCertificate:
    def __init__(
        self,
        *,
        thumbprint: builtins.str,
        x509_store_name: builtins.str,
        thumbprint_secondary: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param thumbprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint ServiceFabricCluster#thumbprint}.
        :param x509_store_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#x509_store_name ServiceFabricCluster#x509_store_name}.
        :param thumbprint_secondary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint_secondary ServiceFabricCluster#thumbprint_secondary}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41dfaa0f2723eb3af6408601b0bf830ef5fbe7e442caf6c73bbf5b19f4ef13a0)
            check_type(argname="argument thumbprint", value=thumbprint, expected_type=type_hints["thumbprint"])
            check_type(argname="argument x509_store_name", value=x509_store_name, expected_type=type_hints["x509_store_name"])
            check_type(argname="argument thumbprint_secondary", value=thumbprint_secondary, expected_type=type_hints["thumbprint_secondary"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "thumbprint": thumbprint,
            "x509_store_name": x509_store_name,
        }
        if thumbprint_secondary is not None:
            self._values["thumbprint_secondary"] = thumbprint_secondary

    @builtins.property
    def thumbprint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint ServiceFabricCluster#thumbprint}.'''
        result = self._values.get("thumbprint")
        assert result is not None, "Required property 'thumbprint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def x509_store_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#x509_store_name ServiceFabricCluster#x509_store_name}.'''
        result = self._values.get("x509_store_name")
        assert result is not None, "Required property 'x509_store_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def thumbprint_secondary(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#thumbprint_secondary ServiceFabricCluster#thumbprint_secondary}.'''
        result = self._values.get("thumbprint_secondary")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterReverseProxyCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterReverseProxyCertificateCommonNames",
    jsii_struct_bases=[],
    name_mapping={"common_names": "commonNames", "x509_store_name": "x509StoreName"},
)
class ServiceFabricClusterReverseProxyCertificateCommonNames:
    def __init__(
        self,
        *,
        common_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames", typing.Dict[builtins.str, typing.Any]]]],
        x509_store_name: builtins.str,
    ) -> None:
        '''
        :param common_names: common_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#common_names ServiceFabricCluster#common_names}
        :param x509_store_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#x509_store_name ServiceFabricCluster#x509_store_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e07c5bd1b27324ee36f32817f73660af094f2f1bf6297bec2f050091b30887)
            check_type(argname="argument common_names", value=common_names, expected_type=type_hints["common_names"])
            check_type(argname="argument x509_store_name", value=x509_store_name, expected_type=type_hints["x509_store_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "common_names": common_names,
            "x509_store_name": x509_store_name,
        }

    @builtins.property
    def common_names(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames"]]:
        '''common_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#common_names ServiceFabricCluster#common_names}
        '''
        result = self._values.get("common_names")
        assert result is not None, "Required property 'common_names' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames"]], result)

    @builtins.property
    def x509_store_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#x509_store_name ServiceFabricCluster#x509_store_name}.'''
        result = self._values.get("x509_store_name")
        assert result is not None, "Required property 'x509_store_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterReverseProxyCertificateCommonNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_common_name": "certificateCommonName",
        "certificate_issuer_thumbprint": "certificateIssuerThumbprint",
    },
)
class ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames:
    def __init__(
        self,
        *,
        certificate_common_name: builtins.str,
        certificate_issuer_thumbprint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param certificate_common_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate_common_name ServiceFabricCluster#certificate_common_name}.
        :param certificate_issuer_thumbprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate_issuer_thumbprint ServiceFabricCluster#certificate_issuer_thumbprint}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc1d28b3191883a1b828e357634502cdda4945888cadfe4731babc75b871b8f)
            check_type(argname="argument certificate_common_name", value=certificate_common_name, expected_type=type_hints["certificate_common_name"])
            check_type(argname="argument certificate_issuer_thumbprint", value=certificate_issuer_thumbprint, expected_type=type_hints["certificate_issuer_thumbprint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_common_name": certificate_common_name,
        }
        if certificate_issuer_thumbprint is not None:
            self._values["certificate_issuer_thumbprint"] = certificate_issuer_thumbprint

    @builtins.property
    def certificate_common_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate_common_name ServiceFabricCluster#certificate_common_name}.'''
        result = self._values.get("certificate_common_name")
        assert result is not None, "Required property 'certificate_common_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_issuer_thumbprint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#certificate_issuer_thumbprint ServiceFabricCluster#certificate_issuer_thumbprint}.'''
        result = self._values.get("certificate_issuer_thumbprint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNamesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNamesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00a1cea47e07ee8be87f78f3f74d11344653be27762d58b9224c5763390591d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNamesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ee1fc0e64c49ef313009d7009b2746959c76f2b51506173d28842127d8c4be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNamesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b35838acabd27adff183855ea8abb3921caee708b11b0ff686cb7b3ef24a83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdad457f98e29cc4eeacb71d796798c11f233262e0f3f068f09b81f8fae0fbaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce4565dbfce5911b61ab932ae1e484f353c52026a498dfab9ae1626693bc25e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66d3351caa1b913211a8d13cfecabb60a8fa4cce8ca00e9fb9aeed59522e6ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e2a97f29c57a568c9f0fd5172c18fc61ff89780fc77f74cbd4c9864d77e3eb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificateIssuerThumbprint")
    def reset_certificate_issuer_thumbprint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateIssuerThumbprint", []))

    @builtins.property
    @jsii.member(jsii_name="certificateCommonNameInput")
    def certificate_common_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateCommonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateIssuerThumbprintInput")
    def certificate_issuer_thumbprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateIssuerThumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateCommonName")
    def certificate_common_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateCommonName"))

    @certificate_common_name.setter
    def certificate_common_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e99e15627ab5edbd1188ecf265812cf4673127e6b84cec09c860a7803ecdb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateCommonName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificateIssuerThumbprint")
    def certificate_issuer_thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateIssuerThumbprint"))

    @certificate_issuer_thumbprint.setter
    def certificate_issuer_thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1666275b2cb8a9483188e57ba0a23e467859fc8143fa462a35bea4657c179baa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateIssuerThumbprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0983ee61d5c74073b356b011bf83df67ec9a386ca33490792c7b1c753e8301c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricClusterReverseProxyCertificateCommonNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterReverseProxyCertificateCommonNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a709323552dea48ee2d18789553cd3e54803b99699c458bbc32acfd4b8e627f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCommonNames")
    def put_common_names(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35b7bb5e5c0a75b1c632382b9dd58f27fd3972f8b5d11864f49b026f7c9acbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCommonNames", [value]))

    @builtins.property
    @jsii.member(jsii_name="commonNames")
    def common_names(
        self,
    ) -> ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNamesList:
        return typing.cast(ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNamesList, jsii.get(self, "commonNames"))

    @builtins.property
    @jsii.member(jsii_name="commonNamesInput")
    def common_names_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames]]], jsii.get(self, "commonNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="x509StoreNameInput")
    def x509_store_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "x509StoreNameInput"))

    @builtins.property
    @jsii.member(jsii_name="x509StoreName")
    def x509_store_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "x509StoreName"))

    @x509_store_name.setter
    def x509_store_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3c01f66df06d1513509751695afc7dabf1e7f442383ffec75562de62c316c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x509StoreName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceFabricClusterReverseProxyCertificateCommonNames]:
        return typing.cast(typing.Optional[ServiceFabricClusterReverseProxyCertificateCommonNames], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFabricClusterReverseProxyCertificateCommonNames],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21895ef77f0faf18ff6634880ddc62c0595be567ebb81e9d9e157c247a8e25a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricClusterReverseProxyCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterReverseProxyCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8973c428f9d41394c6e14dc2480be9fbdeefd1dec358afb4c4cc88fd3ea75bf7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetThumbprintSecondary")
    def reset_thumbprint_secondary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThumbprintSecondary", []))

    @builtins.property
    @jsii.member(jsii_name="thumbprintInput")
    def thumbprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="thumbprintSecondaryInput")
    def thumbprint_secondary_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thumbprintSecondaryInput"))

    @builtins.property
    @jsii.member(jsii_name="x509StoreNameInput")
    def x509_store_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "x509StoreNameInput"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @thumbprint.setter
    def thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__936cbcdd91bd4226ea626d3746a8cd0b4ebbd1c83cfb91153cd446a151ba81b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thumbprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thumbprintSecondary")
    def thumbprint_secondary(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprintSecondary"))

    @thumbprint_secondary.setter
    def thumbprint_secondary(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b73d4c26ddaba0198d9c08a16bcf96e87663f05608b766b2d5e27a7b962fd6da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thumbprintSecondary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="x509StoreName")
    def x509_store_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "x509StoreName"))

    @x509_store_name.setter
    def x509_store_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6f159435a629b953e0e3fae804f5683cfa73a0382e3223c60e32324eddfeca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x509StoreName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceFabricClusterReverseProxyCertificate]:
        return typing.cast(typing.Optional[ServiceFabricClusterReverseProxyCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFabricClusterReverseProxyCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c4306e4cb05c1ae319add3b73d2e5cc1e5ecd076e9c62417af805876e4005a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ServiceFabricClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#create ServiceFabricCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#delete ServiceFabricCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#read ServiceFabricCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#update ServiceFabricCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a184c6e1650b7e3d137760151a6b3ca5e4bae96d2f29085d8c1c3acfcf73e6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#create ServiceFabricCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#delete ServiceFabricCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#read ServiceFabricCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#update ServiceFabricCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0196f337c515f7778aef3abd8b4bbd2cc0fa5bb94440cd0097cf7892362c9b93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65d09a75c1a0475ddf2517a95bceb01739a3906a4644334c60d443b5bf68db7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7eac318fd58cfe30e084c94cf783814f5806afb79c69f4f149dc7e7bad74f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2174a06f327bcf8731aec29cf2f8791b04768d5f8522306f17ea8dd553072734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd0fb8b967c5186e1758977698aab6469609ec0f500761ec5551ef2ed582757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ab7e84bb3fa2dda216647ccfb5e2662be024b5459e5578139f93e9407ff5dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterUpgradePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "delta_health_policy": "deltaHealthPolicy",
        "force_restart_enabled": "forceRestartEnabled",
        "health_check_retry_timeout": "healthCheckRetryTimeout",
        "health_check_stable_duration": "healthCheckStableDuration",
        "health_check_wait_duration": "healthCheckWaitDuration",
        "health_policy": "healthPolicy",
        "upgrade_domain_timeout": "upgradeDomainTimeout",
        "upgrade_replica_set_check_timeout": "upgradeReplicaSetCheckTimeout",
        "upgrade_timeout": "upgradeTimeout",
    },
)
class ServiceFabricClusterUpgradePolicy:
    def __init__(
        self,
        *,
        delta_health_policy: typing.Optional[typing.Union["ServiceFabricClusterUpgradePolicyDeltaHealthPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        force_restart_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        health_check_retry_timeout: typing.Optional[builtins.str] = None,
        health_check_stable_duration: typing.Optional[builtins.str] = None,
        health_check_wait_duration: typing.Optional[builtins.str] = None,
        health_policy: typing.Optional[typing.Union["ServiceFabricClusterUpgradePolicyHealthPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_domain_timeout: typing.Optional[builtins.str] = None,
        upgrade_replica_set_check_timeout: typing.Optional[builtins.str] = None,
        upgrade_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delta_health_policy: delta_health_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#delta_health_policy ServiceFabricCluster#delta_health_policy}
        :param force_restart_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#force_restart_enabled ServiceFabricCluster#force_restart_enabled}.
        :param health_check_retry_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#health_check_retry_timeout ServiceFabricCluster#health_check_retry_timeout}.
        :param health_check_stable_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#health_check_stable_duration ServiceFabricCluster#health_check_stable_duration}.
        :param health_check_wait_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#health_check_wait_duration ServiceFabricCluster#health_check_wait_duration}.
        :param health_policy: health_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#health_policy ServiceFabricCluster#health_policy}
        :param upgrade_domain_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_domain_timeout ServiceFabricCluster#upgrade_domain_timeout}.
        :param upgrade_replica_set_check_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_replica_set_check_timeout ServiceFabricCluster#upgrade_replica_set_check_timeout}.
        :param upgrade_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_timeout ServiceFabricCluster#upgrade_timeout}.
        '''
        if isinstance(delta_health_policy, dict):
            delta_health_policy = ServiceFabricClusterUpgradePolicyDeltaHealthPolicy(**delta_health_policy)
        if isinstance(health_policy, dict):
            health_policy = ServiceFabricClusterUpgradePolicyHealthPolicy(**health_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b220085624c9f48b213d26c4b76de5fcf53d12f134bc6bd4211a4379c1249db)
            check_type(argname="argument delta_health_policy", value=delta_health_policy, expected_type=type_hints["delta_health_policy"])
            check_type(argname="argument force_restart_enabled", value=force_restart_enabled, expected_type=type_hints["force_restart_enabled"])
            check_type(argname="argument health_check_retry_timeout", value=health_check_retry_timeout, expected_type=type_hints["health_check_retry_timeout"])
            check_type(argname="argument health_check_stable_duration", value=health_check_stable_duration, expected_type=type_hints["health_check_stable_duration"])
            check_type(argname="argument health_check_wait_duration", value=health_check_wait_duration, expected_type=type_hints["health_check_wait_duration"])
            check_type(argname="argument health_policy", value=health_policy, expected_type=type_hints["health_policy"])
            check_type(argname="argument upgrade_domain_timeout", value=upgrade_domain_timeout, expected_type=type_hints["upgrade_domain_timeout"])
            check_type(argname="argument upgrade_replica_set_check_timeout", value=upgrade_replica_set_check_timeout, expected_type=type_hints["upgrade_replica_set_check_timeout"])
            check_type(argname="argument upgrade_timeout", value=upgrade_timeout, expected_type=type_hints["upgrade_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delta_health_policy is not None:
            self._values["delta_health_policy"] = delta_health_policy
        if force_restart_enabled is not None:
            self._values["force_restart_enabled"] = force_restart_enabled
        if health_check_retry_timeout is not None:
            self._values["health_check_retry_timeout"] = health_check_retry_timeout
        if health_check_stable_duration is not None:
            self._values["health_check_stable_duration"] = health_check_stable_duration
        if health_check_wait_duration is not None:
            self._values["health_check_wait_duration"] = health_check_wait_duration
        if health_policy is not None:
            self._values["health_policy"] = health_policy
        if upgrade_domain_timeout is not None:
            self._values["upgrade_domain_timeout"] = upgrade_domain_timeout
        if upgrade_replica_set_check_timeout is not None:
            self._values["upgrade_replica_set_check_timeout"] = upgrade_replica_set_check_timeout
        if upgrade_timeout is not None:
            self._values["upgrade_timeout"] = upgrade_timeout

    @builtins.property
    def delta_health_policy(
        self,
    ) -> typing.Optional["ServiceFabricClusterUpgradePolicyDeltaHealthPolicy"]:
        '''delta_health_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#delta_health_policy ServiceFabricCluster#delta_health_policy}
        '''
        result = self._values.get("delta_health_policy")
        return typing.cast(typing.Optional["ServiceFabricClusterUpgradePolicyDeltaHealthPolicy"], result)

    @builtins.property
    def force_restart_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#force_restart_enabled ServiceFabricCluster#force_restart_enabled}.'''
        result = self._values.get("force_restart_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def health_check_retry_timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#health_check_retry_timeout ServiceFabricCluster#health_check_retry_timeout}.'''
        result = self._values.get("health_check_retry_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_stable_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#health_check_stable_duration ServiceFabricCluster#health_check_stable_duration}.'''
        result = self._values.get("health_check_stable_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_wait_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#health_check_wait_duration ServiceFabricCluster#health_check_wait_duration}.'''
        result = self._values.get("health_check_wait_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_policy(
        self,
    ) -> typing.Optional["ServiceFabricClusterUpgradePolicyHealthPolicy"]:
        '''health_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#health_policy ServiceFabricCluster#health_policy}
        '''
        result = self._values.get("health_policy")
        return typing.cast(typing.Optional["ServiceFabricClusterUpgradePolicyHealthPolicy"], result)

    @builtins.property
    def upgrade_domain_timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_domain_timeout ServiceFabricCluster#upgrade_domain_timeout}.'''
        result = self._values.get("upgrade_domain_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upgrade_replica_set_check_timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_replica_set_check_timeout ServiceFabricCluster#upgrade_replica_set_check_timeout}.'''
        result = self._values.get("upgrade_replica_set_check_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upgrade_timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#upgrade_timeout ServiceFabricCluster#upgrade_timeout}.'''
        result = self._values.get("upgrade_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterUpgradePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterUpgradePolicyDeltaHealthPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_delta_unhealthy_applications_percent": "maxDeltaUnhealthyApplicationsPercent",
        "max_delta_unhealthy_nodes_percent": "maxDeltaUnhealthyNodesPercent",
        "max_upgrade_domain_delta_unhealthy_nodes_percent": "maxUpgradeDomainDeltaUnhealthyNodesPercent",
    },
)
class ServiceFabricClusterUpgradePolicyDeltaHealthPolicy:
    def __init__(
        self,
        *,
        max_delta_unhealthy_applications_percent: typing.Optional[jsii.Number] = None,
        max_delta_unhealthy_nodes_percent: typing.Optional[jsii.Number] = None,
        max_upgrade_domain_delta_unhealthy_nodes_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_delta_unhealthy_applications_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_delta_unhealthy_applications_percent ServiceFabricCluster#max_delta_unhealthy_applications_percent}.
        :param max_delta_unhealthy_nodes_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_delta_unhealthy_nodes_percent ServiceFabricCluster#max_delta_unhealthy_nodes_percent}.
        :param max_upgrade_domain_delta_unhealthy_nodes_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_upgrade_domain_delta_unhealthy_nodes_percent ServiceFabricCluster#max_upgrade_domain_delta_unhealthy_nodes_percent}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27408665e7510a4adbab784275ea1a7ec58760d62e0fab1475197b2e55a56ec)
            check_type(argname="argument max_delta_unhealthy_applications_percent", value=max_delta_unhealthy_applications_percent, expected_type=type_hints["max_delta_unhealthy_applications_percent"])
            check_type(argname="argument max_delta_unhealthy_nodes_percent", value=max_delta_unhealthy_nodes_percent, expected_type=type_hints["max_delta_unhealthy_nodes_percent"])
            check_type(argname="argument max_upgrade_domain_delta_unhealthy_nodes_percent", value=max_upgrade_domain_delta_unhealthy_nodes_percent, expected_type=type_hints["max_upgrade_domain_delta_unhealthy_nodes_percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_delta_unhealthy_applications_percent is not None:
            self._values["max_delta_unhealthy_applications_percent"] = max_delta_unhealthy_applications_percent
        if max_delta_unhealthy_nodes_percent is not None:
            self._values["max_delta_unhealthy_nodes_percent"] = max_delta_unhealthy_nodes_percent
        if max_upgrade_domain_delta_unhealthy_nodes_percent is not None:
            self._values["max_upgrade_domain_delta_unhealthy_nodes_percent"] = max_upgrade_domain_delta_unhealthy_nodes_percent

    @builtins.property
    def max_delta_unhealthy_applications_percent(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_delta_unhealthy_applications_percent ServiceFabricCluster#max_delta_unhealthy_applications_percent}.'''
        result = self._values.get("max_delta_unhealthy_applications_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_delta_unhealthy_nodes_percent(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_delta_unhealthy_nodes_percent ServiceFabricCluster#max_delta_unhealthy_nodes_percent}.'''
        result = self._values.get("max_delta_unhealthy_nodes_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_upgrade_domain_delta_unhealthy_nodes_percent(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_upgrade_domain_delta_unhealthy_nodes_percent ServiceFabricCluster#max_upgrade_domain_delta_unhealthy_nodes_percent}.'''
        result = self._values.get("max_upgrade_domain_delta_unhealthy_nodes_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterUpgradePolicyDeltaHealthPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricClusterUpgradePolicyDeltaHealthPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterUpgradePolicyDeltaHealthPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9417ce7d1429db5dd3175e37eb8675b8b2627e2729fb44c6fd8ff34a2918439c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxDeltaUnhealthyApplicationsPercent")
    def reset_max_delta_unhealthy_applications_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDeltaUnhealthyApplicationsPercent", []))

    @jsii.member(jsii_name="resetMaxDeltaUnhealthyNodesPercent")
    def reset_max_delta_unhealthy_nodes_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDeltaUnhealthyNodesPercent", []))

    @jsii.member(jsii_name="resetMaxUpgradeDomainDeltaUnhealthyNodesPercent")
    def reset_max_upgrade_domain_delta_unhealthy_nodes_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUpgradeDomainDeltaUnhealthyNodesPercent", []))

    @builtins.property
    @jsii.member(jsii_name="maxDeltaUnhealthyApplicationsPercentInput")
    def max_delta_unhealthy_applications_percent_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDeltaUnhealthyApplicationsPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDeltaUnhealthyNodesPercentInput")
    def max_delta_unhealthy_nodes_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDeltaUnhealthyNodesPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUpgradeDomainDeltaUnhealthyNodesPercentInput")
    def max_upgrade_domain_delta_unhealthy_nodes_percent_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUpgradeDomainDeltaUnhealthyNodesPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDeltaUnhealthyApplicationsPercent")
    def max_delta_unhealthy_applications_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDeltaUnhealthyApplicationsPercent"))

    @max_delta_unhealthy_applications_percent.setter
    def max_delta_unhealthy_applications_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefbc4929b8e14019f6f6318dc29f77ae1d8677436284781b8dda6fd9d3a3727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDeltaUnhealthyApplicationsPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDeltaUnhealthyNodesPercent")
    def max_delta_unhealthy_nodes_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDeltaUnhealthyNodesPercent"))

    @max_delta_unhealthy_nodes_percent.setter
    def max_delta_unhealthy_nodes_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42cab5d4948146e71ae2be2996619b91d7b1973cbb7b900ea7242d6e1b915666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDeltaUnhealthyNodesPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUpgradeDomainDeltaUnhealthyNodesPercent")
    def max_upgrade_domain_delta_unhealthy_nodes_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUpgradeDomainDeltaUnhealthyNodesPercent"))

    @max_upgrade_domain_delta_unhealthy_nodes_percent.setter
    def max_upgrade_domain_delta_unhealthy_nodes_percent(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fde053317d61d88c3b2df67fd0df199a3191caa19ed0bddfe439a2c45ec6477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUpgradeDomainDeltaUnhealthyNodesPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceFabricClusterUpgradePolicyDeltaHealthPolicy]:
        return typing.cast(typing.Optional[ServiceFabricClusterUpgradePolicyDeltaHealthPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFabricClusterUpgradePolicyDeltaHealthPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f266729e1684933ea1bc74062b65514ea8b86108476efe54d66daedef78b5bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterUpgradePolicyHealthPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_unhealthy_applications_percent": "maxUnhealthyApplicationsPercent",
        "max_unhealthy_nodes_percent": "maxUnhealthyNodesPercent",
    },
)
class ServiceFabricClusterUpgradePolicyHealthPolicy:
    def __init__(
        self,
        *,
        max_unhealthy_applications_percent: typing.Optional[jsii.Number] = None,
        max_unhealthy_nodes_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_unhealthy_applications_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_unhealthy_applications_percent ServiceFabricCluster#max_unhealthy_applications_percent}.
        :param max_unhealthy_nodes_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_unhealthy_nodes_percent ServiceFabricCluster#max_unhealthy_nodes_percent}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c29d2f7bce8ff391566a059d9e0bae72c7b74c8e4620126be6bf268f9954774d)
            check_type(argname="argument max_unhealthy_applications_percent", value=max_unhealthy_applications_percent, expected_type=type_hints["max_unhealthy_applications_percent"])
            check_type(argname="argument max_unhealthy_nodes_percent", value=max_unhealthy_nodes_percent, expected_type=type_hints["max_unhealthy_nodes_percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_unhealthy_applications_percent is not None:
            self._values["max_unhealthy_applications_percent"] = max_unhealthy_applications_percent
        if max_unhealthy_nodes_percent is not None:
            self._values["max_unhealthy_nodes_percent"] = max_unhealthy_nodes_percent

    @builtins.property
    def max_unhealthy_applications_percent(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_unhealthy_applications_percent ServiceFabricCluster#max_unhealthy_applications_percent}.'''
        result = self._values.get("max_unhealthy_applications_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unhealthy_nodes_percent(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_unhealthy_nodes_percent ServiceFabricCluster#max_unhealthy_nodes_percent}.'''
        result = self._values.get("max_unhealthy_nodes_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricClusterUpgradePolicyHealthPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricClusterUpgradePolicyHealthPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterUpgradePolicyHealthPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c607c98d5a78a5e4284dfbd50d9293f3616fb8b3fe3eb67e00cb731097c531b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxUnhealthyApplicationsPercent")
    def reset_max_unhealthy_applications_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUnhealthyApplicationsPercent", []))

    @jsii.member(jsii_name="resetMaxUnhealthyNodesPercent")
    def reset_max_unhealthy_nodes_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUnhealthyNodesPercent", []))

    @builtins.property
    @jsii.member(jsii_name="maxUnhealthyApplicationsPercentInput")
    def max_unhealthy_applications_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnhealthyApplicationsPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnhealthyNodesPercentInput")
    def max_unhealthy_nodes_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnhealthyNodesPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnhealthyApplicationsPercent")
    def max_unhealthy_applications_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnhealthyApplicationsPercent"))

    @max_unhealthy_applications_percent.setter
    def max_unhealthy_applications_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2aaf72f767b24d3413044b1c12294643be5170f573dd5817f237db61c45f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnhealthyApplicationsPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnhealthyNodesPercent")
    def max_unhealthy_nodes_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnhealthyNodesPercent"))

    @max_unhealthy_nodes_percent.setter
    def max_unhealthy_nodes_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a77dc82654bba67e8bee97305869fe119441ea6ad7f83111f0206f1f7587c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnhealthyNodesPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceFabricClusterUpgradePolicyHealthPolicy]:
        return typing.cast(typing.Optional[ServiceFabricClusterUpgradePolicyHealthPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFabricClusterUpgradePolicyHealthPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e79a93c2ea09650e9e6c9ae8d4dc251d26e5fcd9ee9e05e730559ad02d632b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricClusterUpgradePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricCluster.ServiceFabricClusterUpgradePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fea84fd0e24bb70ec34b74c18336d91f1e18d656d8422941533b49271e8b746d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeltaHealthPolicy")
    def put_delta_health_policy(
        self,
        *,
        max_delta_unhealthy_applications_percent: typing.Optional[jsii.Number] = None,
        max_delta_unhealthy_nodes_percent: typing.Optional[jsii.Number] = None,
        max_upgrade_domain_delta_unhealthy_nodes_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_delta_unhealthy_applications_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_delta_unhealthy_applications_percent ServiceFabricCluster#max_delta_unhealthy_applications_percent}.
        :param max_delta_unhealthy_nodes_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_delta_unhealthy_nodes_percent ServiceFabricCluster#max_delta_unhealthy_nodes_percent}.
        :param max_upgrade_domain_delta_unhealthy_nodes_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_upgrade_domain_delta_unhealthy_nodes_percent ServiceFabricCluster#max_upgrade_domain_delta_unhealthy_nodes_percent}.
        '''
        value = ServiceFabricClusterUpgradePolicyDeltaHealthPolicy(
            max_delta_unhealthy_applications_percent=max_delta_unhealthy_applications_percent,
            max_delta_unhealthy_nodes_percent=max_delta_unhealthy_nodes_percent,
            max_upgrade_domain_delta_unhealthy_nodes_percent=max_upgrade_domain_delta_unhealthy_nodes_percent,
        )

        return typing.cast(None, jsii.invoke(self, "putDeltaHealthPolicy", [value]))

    @jsii.member(jsii_name="putHealthPolicy")
    def put_health_policy(
        self,
        *,
        max_unhealthy_applications_percent: typing.Optional[jsii.Number] = None,
        max_unhealthy_nodes_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_unhealthy_applications_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_unhealthy_applications_percent ServiceFabricCluster#max_unhealthy_applications_percent}.
        :param max_unhealthy_nodes_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_cluster#max_unhealthy_nodes_percent ServiceFabricCluster#max_unhealthy_nodes_percent}.
        '''
        value = ServiceFabricClusterUpgradePolicyHealthPolicy(
            max_unhealthy_applications_percent=max_unhealthy_applications_percent,
            max_unhealthy_nodes_percent=max_unhealthy_nodes_percent,
        )

        return typing.cast(None, jsii.invoke(self, "putHealthPolicy", [value]))

    @jsii.member(jsii_name="resetDeltaHealthPolicy")
    def reset_delta_health_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeltaHealthPolicy", []))

    @jsii.member(jsii_name="resetForceRestartEnabled")
    def reset_force_restart_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceRestartEnabled", []))

    @jsii.member(jsii_name="resetHealthCheckRetryTimeout")
    def reset_health_check_retry_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckRetryTimeout", []))

    @jsii.member(jsii_name="resetHealthCheckStableDuration")
    def reset_health_check_stable_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckStableDuration", []))

    @jsii.member(jsii_name="resetHealthCheckWaitDuration")
    def reset_health_check_wait_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckWaitDuration", []))

    @jsii.member(jsii_name="resetHealthPolicy")
    def reset_health_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthPolicy", []))

    @jsii.member(jsii_name="resetUpgradeDomainTimeout")
    def reset_upgrade_domain_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpgradeDomainTimeout", []))

    @jsii.member(jsii_name="resetUpgradeReplicaSetCheckTimeout")
    def reset_upgrade_replica_set_check_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpgradeReplicaSetCheckTimeout", []))

    @jsii.member(jsii_name="resetUpgradeTimeout")
    def reset_upgrade_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpgradeTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="deltaHealthPolicy")
    def delta_health_policy(
        self,
    ) -> ServiceFabricClusterUpgradePolicyDeltaHealthPolicyOutputReference:
        return typing.cast(ServiceFabricClusterUpgradePolicyDeltaHealthPolicyOutputReference, jsii.get(self, "deltaHealthPolicy"))

    @builtins.property
    @jsii.member(jsii_name="healthPolicy")
    def health_policy(
        self,
    ) -> ServiceFabricClusterUpgradePolicyHealthPolicyOutputReference:
        return typing.cast(ServiceFabricClusterUpgradePolicyHealthPolicyOutputReference, jsii.get(self, "healthPolicy"))

    @builtins.property
    @jsii.member(jsii_name="deltaHealthPolicyInput")
    def delta_health_policy_input(
        self,
    ) -> typing.Optional[ServiceFabricClusterUpgradePolicyDeltaHealthPolicy]:
        return typing.cast(typing.Optional[ServiceFabricClusterUpgradePolicyDeltaHealthPolicy], jsii.get(self, "deltaHealthPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="forceRestartEnabledInput")
    def force_restart_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceRestartEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckRetryTimeoutInput")
    def health_check_retry_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckRetryTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckStableDurationInput")
    def health_check_stable_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckStableDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckWaitDurationInput")
    def health_check_wait_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckWaitDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="healthPolicyInput")
    def health_policy_input(
        self,
    ) -> typing.Optional[ServiceFabricClusterUpgradePolicyHealthPolicy]:
        return typing.cast(typing.Optional[ServiceFabricClusterUpgradePolicyHealthPolicy], jsii.get(self, "healthPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeDomainTimeoutInput")
    def upgrade_domain_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "upgradeDomainTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeReplicaSetCheckTimeoutInput")
    def upgrade_replica_set_check_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "upgradeReplicaSetCheckTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeTimeoutInput")
    def upgrade_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "upgradeTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="forceRestartEnabled")
    def force_restart_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceRestartEnabled"))

    @force_restart_enabled.setter
    def force_restart_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9ce1e71c60db731df6426c4f8de91edf81ddf1b2314e8acc44dbeed3fab26e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceRestartEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckRetryTimeout")
    def health_check_retry_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckRetryTimeout"))

    @health_check_retry_timeout.setter
    def health_check_retry_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a760df183e378c44a0fd65e9073de2b82bc8ff5735c92953cce73b5305fc6f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckRetryTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckStableDuration")
    def health_check_stable_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckStableDuration"))

    @health_check_stable_duration.setter
    def health_check_stable_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__910d8ef0c2fb2cb8aab8aa836c42abc12556f6bf65d7ac8e2b376bc5c9fa46e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckStableDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckWaitDuration")
    def health_check_wait_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckWaitDuration"))

    @health_check_wait_duration.setter
    def health_check_wait_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76dec1c9c0af71c8219ab7b226728ec036e66514e8efd2e1e87f96bf858784cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckWaitDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="upgradeDomainTimeout")
    def upgrade_domain_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "upgradeDomainTimeout"))

    @upgrade_domain_timeout.setter
    def upgrade_domain_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f6baa201bdd9df3364b463192840ca2c5897bb47346011cf965c4297b989be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upgradeDomainTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="upgradeReplicaSetCheckTimeout")
    def upgrade_replica_set_check_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "upgradeReplicaSetCheckTimeout"))

    @upgrade_replica_set_check_timeout.setter
    def upgrade_replica_set_check_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9783b3768cf47fd1e30e1bbb7e48dfe9efe2f07203b6ca652c555106b54b1abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upgradeReplicaSetCheckTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="upgradeTimeout")
    def upgrade_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "upgradeTimeout"))

    @upgrade_timeout.setter
    def upgrade_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3276dc08ef0cd63c9386bedfecf2f6e65d32054317c8503be2dc86a0e7d57fad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upgradeTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceFabricClusterUpgradePolicy]:
        return typing.cast(typing.Optional[ServiceFabricClusterUpgradePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFabricClusterUpgradePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a24f282e3128f3c0008129b5dbfe342647a9cc43d6e6533309e1011f12b36c9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ServiceFabricCluster",
    "ServiceFabricClusterAzureActiveDirectory",
    "ServiceFabricClusterAzureActiveDirectoryOutputReference",
    "ServiceFabricClusterCertificate",
    "ServiceFabricClusterCertificateCommonNames",
    "ServiceFabricClusterCertificateCommonNamesCommonNames",
    "ServiceFabricClusterCertificateCommonNamesCommonNamesList",
    "ServiceFabricClusterCertificateCommonNamesCommonNamesOutputReference",
    "ServiceFabricClusterCertificateCommonNamesOutputReference",
    "ServiceFabricClusterCertificateOutputReference",
    "ServiceFabricClusterClientCertificateCommonName",
    "ServiceFabricClusterClientCertificateCommonNameList",
    "ServiceFabricClusterClientCertificateCommonNameOutputReference",
    "ServiceFabricClusterClientCertificateThumbprint",
    "ServiceFabricClusterClientCertificateThumbprintList",
    "ServiceFabricClusterClientCertificateThumbprintOutputReference",
    "ServiceFabricClusterConfig",
    "ServiceFabricClusterDiagnosticsConfig",
    "ServiceFabricClusterDiagnosticsConfigOutputReference",
    "ServiceFabricClusterFabricSettings",
    "ServiceFabricClusterFabricSettingsList",
    "ServiceFabricClusterFabricSettingsOutputReference",
    "ServiceFabricClusterNodeType",
    "ServiceFabricClusterNodeTypeApplicationPorts",
    "ServiceFabricClusterNodeTypeApplicationPortsOutputReference",
    "ServiceFabricClusterNodeTypeEphemeralPorts",
    "ServiceFabricClusterNodeTypeEphemeralPortsOutputReference",
    "ServiceFabricClusterNodeTypeList",
    "ServiceFabricClusterNodeTypeOutputReference",
    "ServiceFabricClusterReverseProxyCertificate",
    "ServiceFabricClusterReverseProxyCertificateCommonNames",
    "ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames",
    "ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNamesList",
    "ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNamesOutputReference",
    "ServiceFabricClusterReverseProxyCertificateCommonNamesOutputReference",
    "ServiceFabricClusterReverseProxyCertificateOutputReference",
    "ServiceFabricClusterTimeouts",
    "ServiceFabricClusterTimeoutsOutputReference",
    "ServiceFabricClusterUpgradePolicy",
    "ServiceFabricClusterUpgradePolicyDeltaHealthPolicy",
    "ServiceFabricClusterUpgradePolicyDeltaHealthPolicyOutputReference",
    "ServiceFabricClusterUpgradePolicyHealthPolicy",
    "ServiceFabricClusterUpgradePolicyHealthPolicyOutputReference",
    "ServiceFabricClusterUpgradePolicyOutputReference",
]

publication.publish()

def _typecheckingstub__4d7b121ce003664e03eedb5db95cc39ba5cdbbbb035e8afc7d32a3bf9d038c4e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    management_endpoint: builtins.str,
    name: builtins.str,
    node_type: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterNodeType, typing.Dict[builtins.str, typing.Any]]]],
    reliability_level: builtins.str,
    resource_group_name: builtins.str,
    upgrade_mode: builtins.str,
    vm_image: builtins.str,
    add_on_features: typing.Optional[typing.Sequence[builtins.str]] = None,
    azure_active_directory: typing.Optional[typing.Union[ServiceFabricClusterAzureActiveDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate: typing.Optional[typing.Union[ServiceFabricClusterCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate_common_names: typing.Optional[typing.Union[ServiceFabricClusterCertificateCommonNames, typing.Dict[builtins.str, typing.Any]]] = None,
    client_certificate_common_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterClientCertificateCommonName, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_certificate_thumbprint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterClientCertificateThumbprint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_code_version: typing.Optional[builtins.str] = None,
    diagnostics_config: typing.Optional[typing.Union[ServiceFabricClusterDiagnosticsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    fabric_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterFabricSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    reverse_proxy_certificate: typing.Optional[typing.Union[ServiceFabricClusterReverseProxyCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    reverse_proxy_certificate_common_names: typing.Optional[typing.Union[ServiceFabricClusterReverseProxyCertificateCommonNames, typing.Dict[builtins.str, typing.Any]]] = None,
    service_fabric_zonal_upgrade_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ServiceFabricClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_policy: typing.Optional[typing.Union[ServiceFabricClusterUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    vmss_zonal_upgrade_mode: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__54a870ff83ebdaed745c9342b5c0ebf5999f1fa171ff4fd12080931e4d6101d8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d85bf78cc986a26cf632940187f7659f905808bbdd362a54abb5e322d50cff7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterClientCertificateCommonName, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd04d9a17209b859b0300cd4ec5c857bfdb0b3e8d09c65b857419ea686312af(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterClientCertificateThumbprint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56730839f30763e4b166aca15a082be917e43f9238bf6f397f460b89321749ef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterFabricSettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddb09be8fe3321754a817bf3fb9de7c7ab8a3d78f84d4f6bb018170ce8076e3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterNodeType, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c261cc5eb215687386ac95141cfdb98cc5010c0833472d767e5641e03714a3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dfcddcfdd11a533720597d0251278f276fc666544a885b8e6c267905e29f787(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94d2d6b39b4163b8565f13c7eb4d32f72b7113c8da05814501327cd1d33b7f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26526a5bd513ee72962cce1921181cee92117fda914155650309dd0b53ca4f97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e553575d19bcecc45bb928727bc30303ea77270ad829232eb9ece580e633bd47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feef05690eed73c617d2bd214517d011d74de9a403c4ee718d92ec5f1c071940(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279c2f025269107bb58d42b32adfdf5b7f91fe531d3ae89fb688d904c61b0a95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7885a9d08114fe4a4355a7858db2fa9a2f5dad5ec4a5bd8a0a8acde5c18d357c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af1a95ec5da1b4758e92ba6b6eba07f6162cb5ce317e516a2339c5d4215fa2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f0c434f84b36f4f4c884b8f91993d735e183d513584a4b83566bca984c6b791(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177fe8743e4d6f38e7887e5217d5a25a32865367786bdcc3707805a733f3a825(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd2b2a4c5844fe4b6940ed47bda7bf1240f6ae20656a6b53f5acff8950063e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36eda299292bd52bed6e09bcca7a547d53e04b7e04976d94fd4ee7a477e41a66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e6fc8b821874f37a38872261fb6fc73fa0d80a0a146c2f1320a4383491a8ec(
    *,
    client_application_id: builtins.str,
    cluster_application_id: builtins.str,
    tenant_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d93c5fc5fe7abca3228197febecc057586d243e15aabc009f25a1c9321729d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91010a8b446ab3d812df19974fa2ee34e65aa64a25e9aa50122c8237750031e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de8de991c0efa0d986219e07dddc3a77fbafd8de22dc5988a40658f92214d5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e021d7ba6a55da2523534030e79ade9d00b98ab75990d5ab67622769a620bf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5a6c5ac7c5c0024005e2d78ba09ed59c358fb78772babe7bc350562c25dd7b(
    value: typing.Optional[ServiceFabricClusterAzureActiveDirectory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de7a34f0cf56d68c4c11f5086ff6755b3420e3896103c188d75d5e0c2cb2e35(
    *,
    thumbprint: builtins.str,
    x509_store_name: builtins.str,
    thumbprint_secondary: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfc4e2dd2319de1931f8df3e3422524c35d82573f13010b8066b9f8fafb230d(
    *,
    common_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterCertificateCommonNamesCommonNames, typing.Dict[builtins.str, typing.Any]]]],
    x509_store_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb63f613634bd5533867ccb791c09b27c8d0bbb07f7502f003e246a2ab55ca7(
    *,
    certificate_common_name: builtins.str,
    certificate_issuer_thumbprint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303bc467940fa49cd801315e9432a53b739cfeec68655d3bbd66132a8c12f8b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e00287ee631050e20d159099d22602402bb40306019bb54df53ebd3a19e22a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfd87615ef01ebb4d81ed97bb75e1649d2818ac32789ea9eb5d3bc59f9fe387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55698c7ee321697a58c75f462508a3b6ba929cecc29854f5ffb43caf1842990(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15bd016e2d6d95d8a0551cb26521102675811e092cf322cc019c3cdb0d24594(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f34886302bb8e11792883ded5c5d01dd267dbd4f7f4103da7e5dabb7ce834e8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterCertificateCommonNamesCommonNames]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d80aa828a10c51217074eebf34a5faa2190d7037f4aa460857e2ad330de0651(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35a8928bd762ebdf7ddab7f9507760a40430e62569d8112c1c4c2e3e043c297(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4817a73d59e1d2fecb764c2987db39c72d7faa99bb913002e19f7a1b25eb54b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb79fe52a53d5c1f4e537327757655979bdbdfedcca7b3d980bcf7a40e93ce6e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterCertificateCommonNamesCommonNames]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ba855629e8679333351e232ef3b5bb7e4393777c7dd7f7e5bdfb51fb527201(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd308b1769c1d35fd7b4705dacc210e68580ef6252787468455250e6a4e768a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterCertificateCommonNamesCommonNames, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39dbaea0797b4405b0119bc827e618d8e09730e6336746fcc717af9bfd6de3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978d456a86a2fbee25d144abfa52d9ffb257f8b41be40ff756ebfafb3bc24142(
    value: typing.Optional[ServiceFabricClusterCertificateCommonNames],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e6e2f94b5bf3dc3b7565e6d5d3a4b22b6d911f8b86eb9b3b234c77869a124b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089e98c85a01e07e24b6fcd12430e8bb4181da23e617f42e4abf979b0ddfea8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b024c5207472463bcd4e03585e8ea1033053b84b9f5646d1ad697b2239e007(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1295ecba720239de0fd3ac31c8ed7ecbabc79480aa039346cad8f6d7f6ff68a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb9f2835e234f77bbc925cd85148f7406624f50ecff182bac660a802912a93b(
    value: typing.Optional[ServiceFabricClusterCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b6ef950df47cbe51d9da1686dbfe8d6e29e27c4a0bef72d4d1ac077c782f5e(
    *,
    common_name: builtins.str,
    is_admin: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    issuer_thumbprint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5e65e1368dbb3302df6382f8dc4faad292a9f823a68f8191f3498be795bcb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8934838d5894ff79524ee7c72feea7fca8739226f3bea4007c7148f87c64e183(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb6ed7ac2da2db20825a3051d820609b73806e4ff20244db84c1d28bea665e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d0357cebcae154980a0da624e6aecc5c3e958373f7d0e121cf4a9174904ad5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1abe4ceaa6b357587bdf9afe7c1dd54790f207bb414d73db8f18c68241fb5a4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3075c1a09f3eab2d1fdfb57098e62c2ec8c193f6ac27287e6debe75180f7db9e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterClientCertificateCommonName]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312c9d8c6f06ba54a206dbb151e8d80852d500237a794cf4f6378a3e81a5a346(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f317878febe2da060e3e943956e6eccbed03aa30ff5e35595a7c7de0db5766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad82646d2fa34c72b04e76bb92202fb763faa64d07ab0e194344e810efa7e2e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528535d52287ec34594b5aba73f128fda9bb8e9c0e662b582d9822caa3a56f98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e19295157ca3253a6baf4140ae4a86e7ce3b17b24fed4e311ef4dc9e5d4bc6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterClientCertificateCommonName]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28feff4373043f5a3c33e88b21b57bf3a6eae2cc80dc0fe5e883afb0fa550969(
    *,
    is_admin: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    thumbprint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05148e07f5d6595c34f3acc45cf2af45e08df215bee17516f7d673702a859904(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6fa372a543448b142a11a9d1af9a6eb320ac820693c28b7c5ca8ec1c5ecda4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff165ac35dc41b124d91f665c1f543ade065014f5e062c22dc5fbab91e44b3ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23ece02aa589b4d92494025820a238329d16c99f5c57f88fe6c51bce259e37a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e48a04d9ae99187b364b43a46d9b734bbb3984b30068f281daa1125b7306156(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758095b0e22e660615ffcb8f6476fcbc3de234b3637d011e8f70604ed949830e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterClientCertificateThumbprint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6284258c7bad9010db0f80e54d7f6a978f86838399c2c964a9d9dffceacf6b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f72cc44fddf0c049bb5c5a05579529700177ba9c12d9bc9923af31573adf2b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c872f81384765a04e541a78abf4c3973ac74bf44ae13a8e9dba2620fc3d223ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5f35f0f5399050a6f2652395daada76499e8062895c73c61b6de4cfc7e248c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterClientCertificateThumbprint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7006e5b8e427f5efcc75f1a9947fe3aad4ac02143bc5bf8264568372f990bd15(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    management_endpoint: builtins.str,
    name: builtins.str,
    node_type: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterNodeType, typing.Dict[builtins.str, typing.Any]]]],
    reliability_level: builtins.str,
    resource_group_name: builtins.str,
    upgrade_mode: builtins.str,
    vm_image: builtins.str,
    add_on_features: typing.Optional[typing.Sequence[builtins.str]] = None,
    azure_active_directory: typing.Optional[typing.Union[ServiceFabricClusterAzureActiveDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate: typing.Optional[typing.Union[ServiceFabricClusterCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate_common_names: typing.Optional[typing.Union[ServiceFabricClusterCertificateCommonNames, typing.Dict[builtins.str, typing.Any]]] = None,
    client_certificate_common_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterClientCertificateCommonName, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_certificate_thumbprint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterClientCertificateThumbprint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_code_version: typing.Optional[builtins.str] = None,
    diagnostics_config: typing.Optional[typing.Union[ServiceFabricClusterDiagnosticsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    fabric_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterFabricSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    reverse_proxy_certificate: typing.Optional[typing.Union[ServiceFabricClusterReverseProxyCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    reverse_proxy_certificate_common_names: typing.Optional[typing.Union[ServiceFabricClusterReverseProxyCertificateCommonNames, typing.Dict[builtins.str, typing.Any]]] = None,
    service_fabric_zonal_upgrade_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ServiceFabricClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_policy: typing.Optional[typing.Union[ServiceFabricClusterUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    vmss_zonal_upgrade_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac01a4f93923d121137459d7e6f1043aec7b793bafe3aa8a3b150e5f707423e(
    *,
    blob_endpoint: builtins.str,
    protected_account_key_name: builtins.str,
    queue_endpoint: builtins.str,
    storage_account_name: builtins.str,
    table_endpoint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c436ab80a33d7026b72df27d70d61971e5f301c7be8bf9771ef33168ab08e73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08dc4d707cecdbc57de7352db8f6bceed4344f282c7f65d5ecf1a5c57dcc7e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b46783b7ef92e6c24f9b2ee187e366f20fd2692798ab94a90288da9319904d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d96b83d4d31c57f9ba462ae050457cf4c960496e7fa02d56c52f25f583d38b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9efb7de991399fc42b454a74bfc3a33804c132e915cc538881078bd8933388f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d458a2208868f41606a70a164ce4e030abe1b8a8c60326522bde06f7d9b87970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0619ef725eb5ee44f4ecd985b0410e3747d8476ca6b7b2adb7c10d6a17453472(
    value: typing.Optional[ServiceFabricClusterDiagnosticsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a4e0c4d2a26bab1fb9749ab177b1fc9c9cd3bc06c678db3a8be82857ce9588(
    *,
    name: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05fd25fc82c7ec493b7c16890cf3c104c74466dcab428522cabb10836b17fe1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44fafd345fd53980fef97429ac867d83681f52ea38713942cb41bcb6d4ddac78(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd67f6922dcc878e0010ab624049a56b52b3d0a4c87ec14b79e1775711d889e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dcfdc52188b8e1555ef90ca9afde9a79923316f06555aa0ecf34253c7605cd0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd0fe75ae7e355d11728c1e3a23d6a08dbe3f4ec2463571e14b2d40886d0242(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430eeabae0fdff766c164c5aca2a45a202db75ebc47dab4cb65d76e6ae91abd9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterFabricSettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a7c79e992c4d4947f329a5a533e5bdb6aea34ed0198e52071fd7cbfea8e9f86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b623b7d71ac978eafdaddebaca26f8c86e18c59b8dd3f9d93dadc9f9f0daaa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1fd28d0f934faa3c9143b72966f324c945cd2cabdf0a97fc360fbc3a029d10(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070ecc837780bbe7c5fcef1422dab635266f9ba4e6f478b8894efe63d87210db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterFabricSettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03cd6fabdc156c3c5422ef24d457cbdedffa683f278f5274911f7a43bba2099d(
    *,
    client_endpoint_port: jsii.Number,
    http_endpoint_port: jsii.Number,
    instance_count: jsii.Number,
    is_primary: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    application_ports: typing.Optional[typing.Union[ServiceFabricClusterNodeTypeApplicationPorts, typing.Dict[builtins.str, typing.Any]]] = None,
    capacities: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    durability_level: typing.Optional[builtins.str] = None,
    ephemeral_ports: typing.Optional[typing.Union[ServiceFabricClusterNodeTypeEphemeralPorts, typing.Dict[builtins.str, typing.Any]]] = None,
    is_stateless: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    multiple_availability_zones: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    placement_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    reverse_proxy_endpoint_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76536b620d87e133397e36cbe5d5a3f38b8ed65e5afe18c5d545ff25aa95599d(
    *,
    end_port: jsii.Number,
    start_port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c6dda839f6852db5f1943c830922326d852c011c839793663bb08392f3fa3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68aee28f93742ebce5cc18ce1de5b95489bb60a0e7fb22c04dc841ebbfe76928(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e460d0a343b97154aeecb814c8e413d95d757e617a669999973db56910c925(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd3faad9702265f4b6a6b794fcfbafa2ddb8c56045c4c97c9754f15b47d10e43(
    value: typing.Optional[ServiceFabricClusterNodeTypeApplicationPorts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33322a04e6f4ed1edfe207e2c4d36601447edc9456118e95ea67fc11b2e3332b(
    *,
    end_port: jsii.Number,
    start_port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f800f82790fd04a1d99f0391cbed4036e667993820c553fd7f1ed2cd4814c64c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f9a52c7347a23570cb53008bd3e50417b2d1e3b026e1bd22a8522a60852c0b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3757fbe66e269a8136764d10661fc9a082f73d96e42a40262837d7cb99ac5a9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a746d333751d319ddac64394290b296df63192402bcc21bcd4a5f166b32868(
    value: typing.Optional[ServiceFabricClusterNodeTypeEphemeralPorts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8dd72eea7ad12ba9881464a0240a59e8badc2c07af65154458e89bffed174c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93ad6b0836271d19e0dc625c13d3d9ec096114b5d9fabea81d8911f2479c821(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e730718464f478eacac7265c68dd2e561250622da188b4be078fd565437e2d07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__254a9de5464429de7cc0adc29904f457aa520bd8b72e7beb541af22d18def1e6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9624e19123ff423c6f0ae2389a9896d41d55bac5e0289843fbc6324a94b0142(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723dd911b53b8a07e9f3545ec68b886afb9f9fd4dee1697a399f3f50d176d659(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterNodeType]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1dbdd0fdf7cd8e632408cc21f78455030411342af45fc5c4f1dc260c95e4ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246e7b6d570c3fa5904e1f19cb444dbda6eb0f2e7cd66e60fa88c62d29dcada3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69010fbc7a3430fd1c7b1d767cd9a7696d7bfb5af7864a8a971b6322e6e5a8ef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c22df8454261bd4ea1fb549a7756f482312bc6cb1f8df5f65e989386f94fd1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd390244df67d8a3235353f64a93ccc65114063415bb3c85e4b27a54d11e7431(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b49f00f1dfda7746267907166dbdd671cbc45c81a8080d2366ab4ccb49467b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831e7c13936585bdfd8a39ddc40a0376e601fcf28ec341aaf478881a6c26aa0c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71f0348c084a54b761a4419ed697904fafafa084b06b8e109dd4381b3c7639f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67a5ed6ef30c6a1d8950a3002ba91d2ce66a32a4dccc92228611c27f6e20da7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1558feab2c96062a36f2489b5def01ce7dcafa596551182cb60c2884ce41d408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4650a49a6d5f236209e5fa0e76460350a0642fd07d693241ad98870077395c97(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c4f257e6526b5ccdfafebbf000c88b9d8f8e5155e15854082243eec11131a7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7769a9c15bbe9d0b7895ac743592daad6b3e05928e38b55c5ad8a8655dbd6ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterNodeType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41dfaa0f2723eb3af6408601b0bf830ef5fbe7e442caf6c73bbf5b19f4ef13a0(
    *,
    thumbprint: builtins.str,
    x509_store_name: builtins.str,
    thumbprint_secondary: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e07c5bd1b27324ee36f32817f73660af094f2f1bf6297bec2f050091b30887(
    *,
    common_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames, typing.Dict[builtins.str, typing.Any]]]],
    x509_store_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc1d28b3191883a1b828e357634502cdda4945888cadfe4731babc75b871b8f(
    *,
    certificate_common_name: builtins.str,
    certificate_issuer_thumbprint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a1cea47e07ee8be87f78f3f74d11344653be27762d58b9224c5763390591d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ee1fc0e64c49ef313009d7009b2746959c76f2b51506173d28842127d8c4be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b35838acabd27adff183855ea8abb3921caee708b11b0ff686cb7b3ef24a83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdad457f98e29cc4eeacb71d796798c11f233262e0f3f068f09b81f8fae0fbaf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4565dbfce5911b61ab932ae1e484f353c52026a498dfab9ae1626693bc25e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66d3351caa1b913211a8d13cfecabb60a8fa4cce8ca00e9fb9aeed59522e6ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2a97f29c57a568c9f0fd5172c18fc61ff89780fc77f74cbd4c9864d77e3eb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e99e15627ab5edbd1188ecf265812cf4673127e6b84cec09c860a7803ecdb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1666275b2cb8a9483188e57ba0a23e467859fc8143fa462a35bea4657c179baa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0983ee61d5c74073b356b011bf83df67ec9a386ca33490792c7b1c753e8301c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a709323552dea48ee2d18789553cd3e54803b99699c458bbc32acfd4b8e627f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35b7bb5e5c0a75b1c632382b9dd58f27fd3972f8b5d11864f49b026f7c9acbe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricClusterReverseProxyCertificateCommonNamesCommonNames, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3c01f66df06d1513509751695afc7dabf1e7f442383ffec75562de62c316c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21895ef77f0faf18ff6634880ddc62c0595be567ebb81e9d9e157c247a8e25a(
    value: typing.Optional[ServiceFabricClusterReverseProxyCertificateCommonNames],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8973c428f9d41394c6e14dc2480be9fbdeefd1dec358afb4c4cc88fd3ea75bf7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936cbcdd91bd4226ea626d3746a8cd0b4ebbd1c83cfb91153cd446a151ba81b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b73d4c26ddaba0198d9c08a16bcf96e87663f05608b766b2d5e27a7b962fd6da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6f159435a629b953e0e3fae804f5683cfa73a0382e3223c60e32324eddfeca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c4306e4cb05c1ae319add3b73d2e5cc1e5ecd076e9c62417af805876e4005a(
    value: typing.Optional[ServiceFabricClusterReverseProxyCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a184c6e1650b7e3d137760151a6b3ca5e4bae96d2f29085d8c1c3acfcf73e6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0196f337c515f7778aef3abd8b4bbd2cc0fa5bb94440cd0097cf7892362c9b93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d09a75c1a0475ddf2517a95bceb01739a3906a4644334c60d443b5bf68db7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7eac318fd58cfe30e084c94cf783814f5806afb79c69f4f149dc7e7bad74f7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2174a06f327bcf8731aec29cf2f8791b04768d5f8522306f17ea8dd553072734(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd0fb8b967c5186e1758977698aab6469609ec0f500761ec5551ef2ed582757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab7e84bb3fa2dda216647ccfb5e2662be024b5459e5578139f93e9407ff5dc2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b220085624c9f48b213d26c4b76de5fcf53d12f134bc6bd4211a4379c1249db(
    *,
    delta_health_policy: typing.Optional[typing.Union[ServiceFabricClusterUpgradePolicyDeltaHealthPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    force_restart_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    health_check_retry_timeout: typing.Optional[builtins.str] = None,
    health_check_stable_duration: typing.Optional[builtins.str] = None,
    health_check_wait_duration: typing.Optional[builtins.str] = None,
    health_policy: typing.Optional[typing.Union[ServiceFabricClusterUpgradePolicyHealthPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_domain_timeout: typing.Optional[builtins.str] = None,
    upgrade_replica_set_check_timeout: typing.Optional[builtins.str] = None,
    upgrade_timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27408665e7510a4adbab784275ea1a7ec58760d62e0fab1475197b2e55a56ec(
    *,
    max_delta_unhealthy_applications_percent: typing.Optional[jsii.Number] = None,
    max_delta_unhealthy_nodes_percent: typing.Optional[jsii.Number] = None,
    max_upgrade_domain_delta_unhealthy_nodes_percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9417ce7d1429db5dd3175e37eb8675b8b2627e2729fb44c6fd8ff34a2918439c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefbc4929b8e14019f6f6318dc29f77ae1d8677436284781b8dda6fd9d3a3727(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42cab5d4948146e71ae2be2996619b91d7b1973cbb7b900ea7242d6e1b915666(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fde053317d61d88c3b2df67fd0df199a3191caa19ed0bddfe439a2c45ec6477(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f266729e1684933ea1bc74062b65514ea8b86108476efe54d66daedef78b5bac(
    value: typing.Optional[ServiceFabricClusterUpgradePolicyDeltaHealthPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29d2f7bce8ff391566a059d9e0bae72c7b74c8e4620126be6bf268f9954774d(
    *,
    max_unhealthy_applications_percent: typing.Optional[jsii.Number] = None,
    max_unhealthy_nodes_percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c607c98d5a78a5e4284dfbd50d9293f3616fb8b3fe3eb67e00cb731097c531b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2aaf72f767b24d3413044b1c12294643be5170f573dd5817f237db61c45f2b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a77dc82654bba67e8bee97305869fe119441ea6ad7f83111f0206f1f7587c8c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e79a93c2ea09650e9e6c9ae8d4dc251d26e5fcd9ee9e05e730559ad02d632b(
    value: typing.Optional[ServiceFabricClusterUpgradePolicyHealthPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea84fd0e24bb70ec34b74c18336d91f1e18d656d8422941533b49271e8b746d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9ce1e71c60db731df6426c4f8de91edf81ddf1b2314e8acc44dbeed3fab26e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a760df183e378c44a0fd65e9073de2b82bc8ff5735c92953cce73b5305fc6f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910d8ef0c2fb2cb8aab8aa836c42abc12556f6bf65d7ac8e2b376bc5c9fa46e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76dec1c9c0af71c8219ab7b226728ec036e66514e8efd2e1e87f96bf858784cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f6baa201bdd9df3364b463192840ca2c5897bb47346011cf965c4297b989be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9783b3768cf47fd1e30e1bbb7e48dfe9efe2f07203b6ca652c555106b54b1abb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3276dc08ef0cd63c9386bedfecf2f6e65d32054317c8503be2dc86a0e7d57fad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24f282e3128f3c0008129b5dbfe342647a9cc43d6e6533309e1011f12b36c9b(
    value: typing.Optional[ServiceFabricClusterUpgradePolicy],
) -> None:
    """Type checking stubs"""
    pass
