r'''
# `azurerm_arc_kubernetes_flux_configuration`

Refer to the Terraform Registry for docs: [`azurerm_arc_kubernetes_flux_configuration`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration).
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


class ArcKubernetesFluxConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration azurerm_arc_kubernetes_flux_configuration}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_id: builtins.str,
        kustomizations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ArcKubernetesFluxConfigurationKustomizations", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        namespace: builtins.str,
        blob_storage: typing.Optional[typing.Union["ArcKubernetesFluxConfigurationBlobStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        bucket: typing.Optional[typing.Union["ArcKubernetesFluxConfigurationBucket", typing.Dict[builtins.str, typing.Any]]] = None,
        continuous_reconciliation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        git_repository: typing.Optional[typing.Union["ArcKubernetesFluxConfigurationGitRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ArcKubernetesFluxConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration azurerm_arc_kubernetes_flux_configuration} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#cluster_id ArcKubernetesFluxConfiguration#cluster_id}.
        :param kustomizations: kustomizations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#kustomizations ArcKubernetesFluxConfiguration#kustomizations}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#name ArcKubernetesFluxConfiguration#name}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#namespace ArcKubernetesFluxConfiguration#namespace}.
        :param blob_storage: blob_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#blob_storage ArcKubernetesFluxConfiguration#blob_storage}
        :param bucket: bucket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#bucket ArcKubernetesFluxConfiguration#bucket}
        :param continuous_reconciliation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#continuous_reconciliation_enabled ArcKubernetesFluxConfiguration#continuous_reconciliation_enabled}.
        :param git_repository: git_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#git_repository ArcKubernetesFluxConfiguration#git_repository}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#id ArcKubernetesFluxConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#scope ArcKubernetesFluxConfiguration#scope}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeouts ArcKubernetesFluxConfiguration#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f40ad803ca2310ccfa2052d3374abc2b0094a45c0cdfe0cb76b99671bc9bac)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ArcKubernetesFluxConfigurationConfig(
            cluster_id=cluster_id,
            kustomizations=kustomizations,
            name=name,
            namespace=namespace,
            blob_storage=blob_storage,
            bucket=bucket,
            continuous_reconciliation_enabled=continuous_reconciliation_enabled,
            git_repository=git_repository,
            id=id,
            scope=scope,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope_, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ArcKubernetesFluxConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ArcKubernetesFluxConfiguration to import.
        :param import_from_id: The id of the existing ArcKubernetesFluxConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ArcKubernetesFluxConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11ecfc8b035dcd6f9bfe98d66bb3e4b9157cd01a2f6c1656c8acfffe4758847)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBlobStorage")
    def put_blob_storage(
        self,
        *,
        container_id: builtins.str,
        account_key: typing.Optional[builtins.str] = None,
        local_auth_reference: typing.Optional[builtins.str] = None,
        sas_token: typing.Optional[builtins.str] = None,
        service_principal: typing.Optional[typing.Union["ArcKubernetesFluxConfigurationBlobStorageServicePrincipal", typing.Dict[builtins.str, typing.Any]]] = None,
        sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param container_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#container_id ArcKubernetesFluxConfiguration#container_id}.
        :param account_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#account_key ArcKubernetesFluxConfiguration#account_key}.
        :param local_auth_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#local_auth_reference ArcKubernetesFluxConfiguration#local_auth_reference}.
        :param sas_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sas_token ArcKubernetesFluxConfiguration#sas_token}.
        :param service_principal: service_principal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#service_principal ArcKubernetesFluxConfiguration#service_principal}
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sync_interval_in_seconds ArcKubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeout_in_seconds ArcKubernetesFluxConfiguration#timeout_in_seconds}.
        '''
        value = ArcKubernetesFluxConfigurationBlobStorage(
            container_id=container_id,
            account_key=account_key,
            local_auth_reference=local_auth_reference,
            sas_token=sas_token,
            service_principal=service_principal,
            sync_interval_in_seconds=sync_interval_in_seconds,
            timeout_in_seconds=timeout_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putBlobStorage", [value]))

    @jsii.member(jsii_name="putBucket")
    def put_bucket(
        self,
        *,
        bucket_name: builtins.str,
        url: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        local_auth_reference: typing.Optional[builtins.str] = None,
        secret_key_base64: typing.Optional[builtins.str] = None,
        sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
        tls_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#bucket_name ArcKubernetesFluxConfiguration#bucket_name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#url ArcKubernetesFluxConfiguration#url}.
        :param access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#access_key ArcKubernetesFluxConfiguration#access_key}.
        :param local_auth_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#local_auth_reference ArcKubernetesFluxConfiguration#local_auth_reference}.
        :param secret_key_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#secret_key_base64 ArcKubernetesFluxConfiguration#secret_key_base64}.
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sync_interval_in_seconds ArcKubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeout_in_seconds ArcKubernetesFluxConfiguration#timeout_in_seconds}.
        :param tls_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#tls_enabled ArcKubernetesFluxConfiguration#tls_enabled}.
        '''
        value = ArcKubernetesFluxConfigurationBucket(
            bucket_name=bucket_name,
            url=url,
            access_key=access_key,
            local_auth_reference=local_auth_reference,
            secret_key_base64=secret_key_base64,
            sync_interval_in_seconds=sync_interval_in_seconds,
            timeout_in_seconds=timeout_in_seconds,
            tls_enabled=tls_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putBucket", [value]))

    @jsii.member(jsii_name="putGitRepository")
    def put_git_repository(
        self,
        *,
        reference_type: builtins.str,
        reference_value: builtins.str,
        url: builtins.str,
        https_ca_cert_base64: typing.Optional[builtins.str] = None,
        https_key_base64: typing.Optional[builtins.str] = None,
        https_user: typing.Optional[builtins.str] = None,
        local_auth_reference: typing.Optional[builtins.str] = None,
        ssh_known_hosts_base64: typing.Optional[builtins.str] = None,
        ssh_private_key_base64: typing.Optional[builtins.str] = None,
        sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param reference_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#reference_type ArcKubernetesFluxConfiguration#reference_type}.
        :param reference_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#reference_value ArcKubernetesFluxConfiguration#reference_value}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#url ArcKubernetesFluxConfiguration#url}.
        :param https_ca_cert_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#https_ca_cert_base64 ArcKubernetesFluxConfiguration#https_ca_cert_base64}.
        :param https_key_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#https_key_base64 ArcKubernetesFluxConfiguration#https_key_base64}.
        :param https_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#https_user ArcKubernetesFluxConfiguration#https_user}.
        :param local_auth_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#local_auth_reference ArcKubernetesFluxConfiguration#local_auth_reference}.
        :param ssh_known_hosts_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#ssh_known_hosts_base64 ArcKubernetesFluxConfiguration#ssh_known_hosts_base64}.
        :param ssh_private_key_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#ssh_private_key_base64 ArcKubernetesFluxConfiguration#ssh_private_key_base64}.
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sync_interval_in_seconds ArcKubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeout_in_seconds ArcKubernetesFluxConfiguration#timeout_in_seconds}.
        '''
        value = ArcKubernetesFluxConfigurationGitRepository(
            reference_type=reference_type,
            reference_value=reference_value,
            url=url,
            https_ca_cert_base64=https_ca_cert_base64,
            https_key_base64=https_key_base64,
            https_user=https_user,
            local_auth_reference=local_auth_reference,
            ssh_known_hosts_base64=ssh_known_hosts_base64,
            ssh_private_key_base64=ssh_private_key_base64,
            sync_interval_in_seconds=sync_interval_in_seconds,
            timeout_in_seconds=timeout_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putGitRepository", [value]))

    @jsii.member(jsii_name="putKustomizations")
    def put_kustomizations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ArcKubernetesFluxConfigurationKustomizations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e17cafbadee6713c1510b49e0860aed1af9bedef1a8ceec6b14e99b16f9f4060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKustomizations", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#create ArcKubernetesFluxConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#delete ArcKubernetesFluxConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#read ArcKubernetesFluxConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#update ArcKubernetesFluxConfiguration#update}.
        '''
        value = ArcKubernetesFluxConfigurationTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBlobStorage")
    def reset_blob_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlobStorage", []))

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetContinuousReconciliationEnabled")
    def reset_continuous_reconciliation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContinuousReconciliationEnabled", []))

    @jsii.member(jsii_name="resetGitRepository")
    def reset_git_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitRepository", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="blobStorage")
    def blob_storage(
        self,
    ) -> "ArcKubernetesFluxConfigurationBlobStorageOutputReference":
        return typing.cast("ArcKubernetesFluxConfigurationBlobStorageOutputReference", jsii.get(self, "blobStorage"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> "ArcKubernetesFluxConfigurationBucketOutputReference":
        return typing.cast("ArcKubernetesFluxConfigurationBucketOutputReference", jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="gitRepository")
    def git_repository(
        self,
    ) -> "ArcKubernetesFluxConfigurationGitRepositoryOutputReference":
        return typing.cast("ArcKubernetesFluxConfigurationGitRepositoryOutputReference", jsii.get(self, "gitRepository"))

    @builtins.property
    @jsii.member(jsii_name="kustomizations")
    def kustomizations(self) -> "ArcKubernetesFluxConfigurationKustomizationsList":
        return typing.cast("ArcKubernetesFluxConfigurationKustomizationsList", jsii.get(self, "kustomizations"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ArcKubernetesFluxConfigurationTimeoutsOutputReference":
        return typing.cast("ArcKubernetesFluxConfigurationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="blobStorageInput")
    def blob_storage_input(
        self,
    ) -> typing.Optional["ArcKubernetesFluxConfigurationBlobStorage"]:
        return typing.cast(typing.Optional["ArcKubernetesFluxConfigurationBlobStorage"], jsii.get(self, "blobStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional["ArcKubernetesFluxConfigurationBucket"]:
        return typing.cast(typing.Optional["ArcKubernetesFluxConfigurationBucket"], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="continuousReconciliationEnabledInput")
    def continuous_reconciliation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "continuousReconciliationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="gitRepositoryInput")
    def git_repository_input(
        self,
    ) -> typing.Optional["ArcKubernetesFluxConfigurationGitRepository"]:
        return typing.cast(typing.Optional["ArcKubernetesFluxConfigurationGitRepository"], jsii.get(self, "gitRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kustomizationsInput")
    def kustomizations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArcKubernetesFluxConfigurationKustomizations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArcKubernetesFluxConfigurationKustomizations"]]], jsii.get(self, "kustomizationsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ArcKubernetesFluxConfigurationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ArcKubernetesFluxConfigurationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d193a5efcd7ae3d22046943f5171a26f4f67ffd2e199375581eca3e1e36cd504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="continuousReconciliationEnabled")
    def continuous_reconciliation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "continuousReconciliationEnabled"))

    @continuous_reconciliation_enabled.setter
    def continuous_reconciliation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208fd24d7f2fe9c986be93a6f4bd33b5e1c846adb989d9c498b99416f7cfdd33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "continuousReconciliationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaef9bee33c544b31ff7358c7c7e3877552af61556411b472403c486fee421c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e9bbbeca0e2da852780add610dc9a576ba67b4479432cc1a8e3f0dad0047daa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811faf671e4a5bcbdae244f3d44876a68bb3acc6fc3129f8aa6d3d0294512abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f41739bcb6a0004f1537ddf06bb0f9f5acf527ab8feb2d978d92e3fe188c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationBlobStorage",
    jsii_struct_bases=[],
    name_mapping={
        "container_id": "containerId",
        "account_key": "accountKey",
        "local_auth_reference": "localAuthReference",
        "sas_token": "sasToken",
        "service_principal": "servicePrincipal",
        "sync_interval_in_seconds": "syncIntervalInSeconds",
        "timeout_in_seconds": "timeoutInSeconds",
    },
)
class ArcKubernetesFluxConfigurationBlobStorage:
    def __init__(
        self,
        *,
        container_id: builtins.str,
        account_key: typing.Optional[builtins.str] = None,
        local_auth_reference: typing.Optional[builtins.str] = None,
        sas_token: typing.Optional[builtins.str] = None,
        service_principal: typing.Optional[typing.Union["ArcKubernetesFluxConfigurationBlobStorageServicePrincipal", typing.Dict[builtins.str, typing.Any]]] = None,
        sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param container_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#container_id ArcKubernetesFluxConfiguration#container_id}.
        :param account_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#account_key ArcKubernetesFluxConfiguration#account_key}.
        :param local_auth_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#local_auth_reference ArcKubernetesFluxConfiguration#local_auth_reference}.
        :param sas_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sas_token ArcKubernetesFluxConfiguration#sas_token}.
        :param service_principal: service_principal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#service_principal ArcKubernetesFluxConfiguration#service_principal}
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sync_interval_in_seconds ArcKubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeout_in_seconds ArcKubernetesFluxConfiguration#timeout_in_seconds}.
        '''
        if isinstance(service_principal, dict):
            service_principal = ArcKubernetesFluxConfigurationBlobStorageServicePrincipal(**service_principal)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1306f56fed9aa80dc5362b98ea92fe037c6b46370f299b34fdce4e09db147188)
            check_type(argname="argument container_id", value=container_id, expected_type=type_hints["container_id"])
            check_type(argname="argument account_key", value=account_key, expected_type=type_hints["account_key"])
            check_type(argname="argument local_auth_reference", value=local_auth_reference, expected_type=type_hints["local_auth_reference"])
            check_type(argname="argument sas_token", value=sas_token, expected_type=type_hints["sas_token"])
            check_type(argname="argument service_principal", value=service_principal, expected_type=type_hints["service_principal"])
            check_type(argname="argument sync_interval_in_seconds", value=sync_interval_in_seconds, expected_type=type_hints["sync_interval_in_seconds"])
            check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_id": container_id,
        }
        if account_key is not None:
            self._values["account_key"] = account_key
        if local_auth_reference is not None:
            self._values["local_auth_reference"] = local_auth_reference
        if sas_token is not None:
            self._values["sas_token"] = sas_token
        if service_principal is not None:
            self._values["service_principal"] = service_principal
        if sync_interval_in_seconds is not None:
            self._values["sync_interval_in_seconds"] = sync_interval_in_seconds
        if timeout_in_seconds is not None:
            self._values["timeout_in_seconds"] = timeout_in_seconds

    @builtins.property
    def container_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#container_id ArcKubernetesFluxConfiguration#container_id}.'''
        result = self._values.get("container_id")
        assert result is not None, "Required property 'container_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#account_key ArcKubernetesFluxConfiguration#account_key}.'''
        result = self._values.get("account_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_auth_reference(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#local_auth_reference ArcKubernetesFluxConfiguration#local_auth_reference}.'''
        result = self._values.get("local_auth_reference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sas_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sas_token ArcKubernetesFluxConfiguration#sas_token}.'''
        result = self._values.get("sas_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_principal(
        self,
    ) -> typing.Optional["ArcKubernetesFluxConfigurationBlobStorageServicePrincipal"]:
        '''service_principal block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#service_principal ArcKubernetesFluxConfiguration#service_principal}
        '''
        result = self._values.get("service_principal")
        return typing.cast(typing.Optional["ArcKubernetesFluxConfigurationBlobStorageServicePrincipal"], result)

    @builtins.property
    def sync_interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sync_interval_in_seconds ArcKubernetesFluxConfiguration#sync_interval_in_seconds}.'''
        result = self._values.get("sync_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeout_in_seconds ArcKubernetesFluxConfiguration#timeout_in_seconds}.'''
        result = self._values.get("timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArcKubernetesFluxConfigurationBlobStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArcKubernetesFluxConfigurationBlobStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationBlobStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5f8753f1926c03e0e28061cab3a787ddadf5cb3d46317b94937eebaa741f4fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putServicePrincipal")
    def put_service_principal(
        self,
        *,
        client_id: builtins.str,
        tenant_id: builtins.str,
        client_certificate_base64: typing.Optional[builtins.str] = None,
        client_certificate_password: typing.Optional[builtins.str] = None,
        client_certificate_send_chain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_id ArcKubernetesFluxConfiguration#client_id}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#tenant_id ArcKubernetesFluxConfiguration#tenant_id}.
        :param client_certificate_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_certificate_base64 ArcKubernetesFluxConfiguration#client_certificate_base64}.
        :param client_certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_certificate_password ArcKubernetesFluxConfiguration#client_certificate_password}.
        :param client_certificate_send_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_certificate_send_chain ArcKubernetesFluxConfiguration#client_certificate_send_chain}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_secret ArcKubernetesFluxConfiguration#client_secret}.
        '''
        value = ArcKubernetesFluxConfigurationBlobStorageServicePrincipal(
            client_id=client_id,
            tenant_id=tenant_id,
            client_certificate_base64=client_certificate_base64,
            client_certificate_password=client_certificate_password,
            client_certificate_send_chain=client_certificate_send_chain,
            client_secret=client_secret,
        )

        return typing.cast(None, jsii.invoke(self, "putServicePrincipal", [value]))

    @jsii.member(jsii_name="resetAccountKey")
    def reset_account_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountKey", []))

    @jsii.member(jsii_name="resetLocalAuthReference")
    def reset_local_auth_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalAuthReference", []))

    @jsii.member(jsii_name="resetSasToken")
    def reset_sas_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSasToken", []))

    @jsii.member(jsii_name="resetServicePrincipal")
    def reset_service_principal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicePrincipal", []))

    @jsii.member(jsii_name="resetSyncIntervalInSeconds")
    def reset_sync_interval_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncIntervalInSeconds", []))

    @jsii.member(jsii_name="resetTimeoutInSeconds")
    def reset_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipal")
    def service_principal(
        self,
    ) -> "ArcKubernetesFluxConfigurationBlobStorageServicePrincipalOutputReference":
        return typing.cast("ArcKubernetesFluxConfigurationBlobStorageServicePrincipalOutputReference", jsii.get(self, "servicePrincipal"))

    @builtins.property
    @jsii.member(jsii_name="accountKeyInput")
    def account_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="containerIdInput")
    def container_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="localAuthReferenceInput")
    def local_auth_reference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localAuthReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="sasTokenInput")
    def sas_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sasTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalInput")
    def service_principal_input(
        self,
    ) -> typing.Optional["ArcKubernetesFluxConfigurationBlobStorageServicePrincipal"]:
        return typing.cast(typing.Optional["ArcKubernetesFluxConfigurationBlobStorageServicePrincipal"], jsii.get(self, "servicePrincipalInput"))

    @builtins.property
    @jsii.member(jsii_name="syncIntervalInSecondsInput")
    def sync_interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "syncIntervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInSecondsInput")
    def timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountKey")
    def account_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountKey"))

    @account_key.setter
    def account_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967aa655dd5e2e8f87aa116b35845b04a047f024a7257e5ee3fb3453ea7b51a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerId")
    def container_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerId"))

    @container_id.setter
    def container_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3365b87fdc9ca76782fe01ca9d94a578e8b07a6c9d96bbda4e7bc58725342ab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localAuthReference")
    def local_auth_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localAuthReference"))

    @local_auth_reference.setter
    def local_auth_reference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24751dd34d17fcb0d2b33e80010a32b274da9b012bbcb77aa3f914956c4bd9fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localAuthReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sasToken")
    def sas_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sasToken"))

    @sas_token.setter
    def sas_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e28701d76db41543ed3f3770b2e29c43246c221a750618318c5e9ae5ff1b89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sasToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "syncIntervalInSeconds"))

    @sync_interval_in_seconds.setter
    def sync_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ba3e1ede370194bd8864bdbe992e971f4092d51fd7a6cc913c329192badbba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutInSeconds")
    def timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutInSeconds"))

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d1bbc61127027dbc2fe1933eae770bf8c8e6f0d8da6ce6ebfe492a66793449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArcKubernetesFluxConfigurationBlobStorage]:
        return typing.cast(typing.Optional[ArcKubernetesFluxConfigurationBlobStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArcKubernetesFluxConfigurationBlobStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31b87daaf9a39f0fb7d9ab9dbf87bbbdb55951f2f14b5e8d88d10fe6dee9d12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationBlobStorageServicePrincipal",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "tenant_id": "tenantId",
        "client_certificate_base64": "clientCertificateBase64",
        "client_certificate_password": "clientCertificatePassword",
        "client_certificate_send_chain": "clientCertificateSendChain",
        "client_secret": "clientSecret",
    },
)
class ArcKubernetesFluxConfigurationBlobStorageServicePrincipal:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        tenant_id: builtins.str,
        client_certificate_base64: typing.Optional[builtins.str] = None,
        client_certificate_password: typing.Optional[builtins.str] = None,
        client_certificate_send_chain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_id ArcKubernetesFluxConfiguration#client_id}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#tenant_id ArcKubernetesFluxConfiguration#tenant_id}.
        :param client_certificate_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_certificate_base64 ArcKubernetesFluxConfiguration#client_certificate_base64}.
        :param client_certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_certificate_password ArcKubernetesFluxConfiguration#client_certificate_password}.
        :param client_certificate_send_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_certificate_send_chain ArcKubernetesFluxConfiguration#client_certificate_send_chain}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_secret ArcKubernetesFluxConfiguration#client_secret}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3fd5ac1f8a4f2eaba85a811daf4cdf75016d2f541c30b010c904590a54ced4)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument client_certificate_base64", value=client_certificate_base64, expected_type=type_hints["client_certificate_base64"])
            check_type(argname="argument client_certificate_password", value=client_certificate_password, expected_type=type_hints["client_certificate_password"])
            check_type(argname="argument client_certificate_send_chain", value=client_certificate_send_chain, expected_type=type_hints["client_certificate_send_chain"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "tenant_id": tenant_id,
        }
        if client_certificate_base64 is not None:
            self._values["client_certificate_base64"] = client_certificate_base64
        if client_certificate_password is not None:
            self._values["client_certificate_password"] = client_certificate_password
        if client_certificate_send_chain is not None:
            self._values["client_certificate_send_chain"] = client_certificate_send_chain
        if client_secret is not None:
            self._values["client_secret"] = client_secret

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_id ArcKubernetesFluxConfiguration#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#tenant_id ArcKubernetesFluxConfiguration#tenant_id}.'''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_certificate_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_certificate_base64 ArcKubernetesFluxConfiguration#client_certificate_base64}.'''
        result = self._values.get("client_certificate_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_certificate_password ArcKubernetesFluxConfiguration#client_certificate_password}.'''
        result = self._values.get("client_certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_send_chain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_certificate_send_chain ArcKubernetesFluxConfiguration#client_certificate_send_chain}.'''
        result = self._values.get("client_certificate_send_chain")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#client_secret ArcKubernetesFluxConfiguration#client_secret}.'''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArcKubernetesFluxConfigurationBlobStorageServicePrincipal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArcKubernetesFluxConfigurationBlobStorageServicePrincipalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationBlobStorageServicePrincipalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebc9dd92c8c334c11e056392eafd11642669029080913feb8e7dedd56c633cac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientCertificateBase64")
    def reset_client_certificate_base64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateBase64", []))

    @jsii.member(jsii_name="resetClientCertificatePassword")
    def reset_client_certificate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificatePassword", []))

    @jsii.member(jsii_name="resetClientCertificateSendChain")
    def reset_client_certificate_send_chain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateSendChain", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateBase64Input")
    def client_certificate_base64_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificatePasswordInput")
    def client_certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateSendChainInput")
    def client_certificate_send_chain_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientCertificateSendChainInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateBase64")
    def client_certificate_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateBase64"))

    @client_certificate_base64.setter
    def client_certificate_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2c067a8dacecd28d41995d3f2c3e1298afba2e0d5bd4d83977ae54e8518fa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificatePassword")
    def client_certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificatePassword"))

    @client_certificate_password.setter
    def client_certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__495dc1b391c5a2565748a9f19d04d93c0dab05896ec6a1524ec9b87e4074433e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificateSendChain")
    def client_certificate_send_chain(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientCertificateSendChain"))

    @client_certificate_send_chain.setter
    def client_certificate_send_chain(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f71b2060f90fabe7310e3397c00e886fe2295ed91fe2f19a5c754b3d2c4c5b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateSendChain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9733f0d1d04460787e10f14448eb4be344b3d521a6456013f3bfc604ba846462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12d40df0bf42bb85b15f5dd47ea0bd0a0d0ab9ef63de89dab5a512170a78cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be07a5bf4d86f2a93f6ff146e35732811f98384b8f4e1d56e8731df9989cd4aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArcKubernetesFluxConfigurationBlobStorageServicePrincipal]:
        return typing.cast(typing.Optional[ArcKubernetesFluxConfigurationBlobStorageServicePrincipal], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArcKubernetesFluxConfigurationBlobStorageServicePrincipal],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eb1db0c91dc9bcf5d05540af23dbc376b1cf4cddc6343ff2f3555b8e14c7671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationBucket",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "url": "url",
        "access_key": "accessKey",
        "local_auth_reference": "localAuthReference",
        "secret_key_base64": "secretKeyBase64",
        "sync_interval_in_seconds": "syncIntervalInSeconds",
        "timeout_in_seconds": "timeoutInSeconds",
        "tls_enabled": "tlsEnabled",
    },
)
class ArcKubernetesFluxConfigurationBucket:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        url: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        local_auth_reference: typing.Optional[builtins.str] = None,
        secret_key_base64: typing.Optional[builtins.str] = None,
        sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
        tls_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#bucket_name ArcKubernetesFluxConfiguration#bucket_name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#url ArcKubernetesFluxConfiguration#url}.
        :param access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#access_key ArcKubernetesFluxConfiguration#access_key}.
        :param local_auth_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#local_auth_reference ArcKubernetesFluxConfiguration#local_auth_reference}.
        :param secret_key_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#secret_key_base64 ArcKubernetesFluxConfiguration#secret_key_base64}.
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sync_interval_in_seconds ArcKubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeout_in_seconds ArcKubernetesFluxConfiguration#timeout_in_seconds}.
        :param tls_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#tls_enabled ArcKubernetesFluxConfiguration#tls_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd134588be5f6899c227463e4cbf07ea391e0410a58e176c5930352b56ff10f3)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument local_auth_reference", value=local_auth_reference, expected_type=type_hints["local_auth_reference"])
            check_type(argname="argument secret_key_base64", value=secret_key_base64, expected_type=type_hints["secret_key_base64"])
            check_type(argname="argument sync_interval_in_seconds", value=sync_interval_in_seconds, expected_type=type_hints["sync_interval_in_seconds"])
            check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            check_type(argname="argument tls_enabled", value=tls_enabled, expected_type=type_hints["tls_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "url": url,
        }
        if access_key is not None:
            self._values["access_key"] = access_key
        if local_auth_reference is not None:
            self._values["local_auth_reference"] = local_auth_reference
        if secret_key_base64 is not None:
            self._values["secret_key_base64"] = secret_key_base64
        if sync_interval_in_seconds is not None:
            self._values["sync_interval_in_seconds"] = sync_interval_in_seconds
        if timeout_in_seconds is not None:
            self._values["timeout_in_seconds"] = timeout_in_seconds
        if tls_enabled is not None:
            self._values["tls_enabled"] = tls_enabled

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#bucket_name ArcKubernetesFluxConfiguration#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#url ArcKubernetesFluxConfiguration#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#access_key ArcKubernetesFluxConfiguration#access_key}.'''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_auth_reference(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#local_auth_reference ArcKubernetesFluxConfiguration#local_auth_reference}.'''
        result = self._values.get("local_auth_reference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#secret_key_base64 ArcKubernetesFluxConfiguration#secret_key_base64}.'''
        result = self._values.get("secret_key_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sync_interval_in_seconds ArcKubernetesFluxConfiguration#sync_interval_in_seconds}.'''
        result = self._values.get("sync_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeout_in_seconds ArcKubernetesFluxConfiguration#timeout_in_seconds}.'''
        result = self._values.get("timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#tls_enabled ArcKubernetesFluxConfiguration#tls_enabled}.'''
        result = self._values.get("tls_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArcKubernetesFluxConfigurationBucket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArcKubernetesFluxConfigurationBucketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationBucketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8b82f1852d68ad5bdbcae510d7e625326b781ca65b4473f6f397a4b89a77079)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessKey")
    def reset_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKey", []))

    @jsii.member(jsii_name="resetLocalAuthReference")
    def reset_local_auth_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalAuthReference", []))

    @jsii.member(jsii_name="resetSecretKeyBase64")
    def reset_secret_key_base64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretKeyBase64", []))

    @jsii.member(jsii_name="resetSyncIntervalInSeconds")
    def reset_sync_interval_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncIntervalInSeconds", []))

    @jsii.member(jsii_name="resetTimeoutInSeconds")
    def reset_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetTlsEnabled")
    def reset_tls_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="accessKeyInput")
    def access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="localAuthReferenceInput")
    def local_auth_reference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localAuthReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyBase64Input")
    def secret_key_base64_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKeyBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="syncIntervalInSecondsInput")
    def sync_interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "syncIntervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInSecondsInput")
    def timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsEnabledInput")
    def tls_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01afd95bdfa6cbe1d44f0a61d14fef156406859621b5088714f32a901bcb2a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28774c63a460abbc220a21a8c8ab5b8abb892e97fdb1c4185ef1cb9f913b56ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localAuthReference")
    def local_auth_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localAuthReference"))

    @local_auth_reference.setter
    def local_auth_reference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be820534b68f8045c620e9c37d656e88565afa0f56880d2e160ff547dae6d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localAuthReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretKeyBase64")
    def secret_key_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretKeyBase64"))

    @secret_key_base64.setter
    def secret_key_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f7d9fc240afdd12932d86578b60e178003f7eb69d94114b29effabd62d690d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKeyBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "syncIntervalInSeconds"))

    @sync_interval_in_seconds.setter
    def sync_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfcd052288c149cfde7e27b699843ae69479474f584b7825d6c43cc61a6354b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutInSeconds")
    def timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutInSeconds"))

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__365e4f6b8b4c17deeaea52885aefd68a36daf8028eee6659eb608e17e34d2e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsEnabled")
    def tls_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsEnabled"))

    @tls_enabled.setter
    def tls_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e5ee7879f9b40da5df0797f4a1403bf634c3380228880c74652cbe3d88f8f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14db6b0b5207d898461437c159859dcb35c02085b841dfcdaac805769da1a718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ArcKubernetesFluxConfigurationBucket]:
        return typing.cast(typing.Optional[ArcKubernetesFluxConfigurationBucket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArcKubernetesFluxConfigurationBucket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfabd02bdae27085369132fea4b46929802ab18a3f14396d537becd0526e6c5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_id": "clusterId",
        "kustomizations": "kustomizations",
        "name": "name",
        "namespace": "namespace",
        "blob_storage": "blobStorage",
        "bucket": "bucket",
        "continuous_reconciliation_enabled": "continuousReconciliationEnabled",
        "git_repository": "gitRepository",
        "id": "id",
        "scope": "scope",
        "timeouts": "timeouts",
    },
)
class ArcKubernetesFluxConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_id: builtins.str,
        kustomizations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ArcKubernetesFluxConfigurationKustomizations", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        namespace: builtins.str,
        blob_storage: typing.Optional[typing.Union[ArcKubernetesFluxConfigurationBlobStorage, typing.Dict[builtins.str, typing.Any]]] = None,
        bucket: typing.Optional[typing.Union[ArcKubernetesFluxConfigurationBucket, typing.Dict[builtins.str, typing.Any]]] = None,
        continuous_reconciliation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        git_repository: typing.Optional[typing.Union["ArcKubernetesFluxConfigurationGitRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ArcKubernetesFluxConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#cluster_id ArcKubernetesFluxConfiguration#cluster_id}.
        :param kustomizations: kustomizations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#kustomizations ArcKubernetesFluxConfiguration#kustomizations}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#name ArcKubernetesFluxConfiguration#name}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#namespace ArcKubernetesFluxConfiguration#namespace}.
        :param blob_storage: blob_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#blob_storage ArcKubernetesFluxConfiguration#blob_storage}
        :param bucket: bucket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#bucket ArcKubernetesFluxConfiguration#bucket}
        :param continuous_reconciliation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#continuous_reconciliation_enabled ArcKubernetesFluxConfiguration#continuous_reconciliation_enabled}.
        :param git_repository: git_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#git_repository ArcKubernetesFluxConfiguration#git_repository}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#id ArcKubernetesFluxConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#scope ArcKubernetesFluxConfiguration#scope}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeouts ArcKubernetesFluxConfiguration#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(blob_storage, dict):
            blob_storage = ArcKubernetesFluxConfigurationBlobStorage(**blob_storage)
        if isinstance(bucket, dict):
            bucket = ArcKubernetesFluxConfigurationBucket(**bucket)
        if isinstance(git_repository, dict):
            git_repository = ArcKubernetesFluxConfigurationGitRepository(**git_repository)
        if isinstance(timeouts, dict):
            timeouts = ArcKubernetesFluxConfigurationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26dc42ee83a7fcffc6e7261921fba7c3a2cfc9b00a15568e7b854f6b873714dc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument kustomizations", value=kustomizations, expected_type=type_hints["kustomizations"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument blob_storage", value=blob_storage, expected_type=type_hints["blob_storage"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument continuous_reconciliation_enabled", value=continuous_reconciliation_enabled, expected_type=type_hints["continuous_reconciliation_enabled"])
            check_type(argname="argument git_repository", value=git_repository, expected_type=type_hints["git_repository"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_id": cluster_id,
            "kustomizations": kustomizations,
            "name": name,
            "namespace": namespace,
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
        if blob_storage is not None:
            self._values["blob_storage"] = blob_storage
        if bucket is not None:
            self._values["bucket"] = bucket
        if continuous_reconciliation_enabled is not None:
            self._values["continuous_reconciliation_enabled"] = continuous_reconciliation_enabled
        if git_repository is not None:
            self._values["git_repository"] = git_repository
        if id is not None:
            self._values["id"] = id
        if scope is not None:
            self._values["scope"] = scope
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def cluster_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#cluster_id ArcKubernetesFluxConfiguration#cluster_id}.'''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kustomizations(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArcKubernetesFluxConfigurationKustomizations"]]:
        '''kustomizations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#kustomizations ArcKubernetesFluxConfiguration#kustomizations}
        '''
        result = self._values.get("kustomizations")
        assert result is not None, "Required property 'kustomizations' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArcKubernetesFluxConfigurationKustomizations"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#name ArcKubernetesFluxConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#namespace ArcKubernetesFluxConfiguration#namespace}.'''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def blob_storage(
        self,
    ) -> typing.Optional[ArcKubernetesFluxConfigurationBlobStorage]:
        '''blob_storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#blob_storage ArcKubernetesFluxConfiguration#blob_storage}
        '''
        result = self._values.get("blob_storage")
        return typing.cast(typing.Optional[ArcKubernetesFluxConfigurationBlobStorage], result)

    @builtins.property
    def bucket(self) -> typing.Optional[ArcKubernetesFluxConfigurationBucket]:
        '''bucket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#bucket ArcKubernetesFluxConfiguration#bucket}
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[ArcKubernetesFluxConfigurationBucket], result)

    @builtins.property
    def continuous_reconciliation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#continuous_reconciliation_enabled ArcKubernetesFluxConfiguration#continuous_reconciliation_enabled}.'''
        result = self._values.get("continuous_reconciliation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def git_repository(
        self,
    ) -> typing.Optional["ArcKubernetesFluxConfigurationGitRepository"]:
        '''git_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#git_repository ArcKubernetesFluxConfiguration#git_repository}
        '''
        result = self._values.get("git_repository")
        return typing.cast(typing.Optional["ArcKubernetesFluxConfigurationGitRepository"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#id ArcKubernetesFluxConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#scope ArcKubernetesFluxConfiguration#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ArcKubernetesFluxConfigurationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeouts ArcKubernetesFluxConfiguration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ArcKubernetesFluxConfigurationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArcKubernetesFluxConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationGitRepository",
    jsii_struct_bases=[],
    name_mapping={
        "reference_type": "referenceType",
        "reference_value": "referenceValue",
        "url": "url",
        "https_ca_cert_base64": "httpsCaCertBase64",
        "https_key_base64": "httpsKeyBase64",
        "https_user": "httpsUser",
        "local_auth_reference": "localAuthReference",
        "ssh_known_hosts_base64": "sshKnownHostsBase64",
        "ssh_private_key_base64": "sshPrivateKeyBase64",
        "sync_interval_in_seconds": "syncIntervalInSeconds",
        "timeout_in_seconds": "timeoutInSeconds",
    },
)
class ArcKubernetesFluxConfigurationGitRepository:
    def __init__(
        self,
        *,
        reference_type: builtins.str,
        reference_value: builtins.str,
        url: builtins.str,
        https_ca_cert_base64: typing.Optional[builtins.str] = None,
        https_key_base64: typing.Optional[builtins.str] = None,
        https_user: typing.Optional[builtins.str] = None,
        local_auth_reference: typing.Optional[builtins.str] = None,
        ssh_known_hosts_base64: typing.Optional[builtins.str] = None,
        ssh_private_key_base64: typing.Optional[builtins.str] = None,
        sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param reference_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#reference_type ArcKubernetesFluxConfiguration#reference_type}.
        :param reference_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#reference_value ArcKubernetesFluxConfiguration#reference_value}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#url ArcKubernetesFluxConfiguration#url}.
        :param https_ca_cert_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#https_ca_cert_base64 ArcKubernetesFluxConfiguration#https_ca_cert_base64}.
        :param https_key_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#https_key_base64 ArcKubernetesFluxConfiguration#https_key_base64}.
        :param https_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#https_user ArcKubernetesFluxConfiguration#https_user}.
        :param local_auth_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#local_auth_reference ArcKubernetesFluxConfiguration#local_auth_reference}.
        :param ssh_known_hosts_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#ssh_known_hosts_base64 ArcKubernetesFluxConfiguration#ssh_known_hosts_base64}.
        :param ssh_private_key_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#ssh_private_key_base64 ArcKubernetesFluxConfiguration#ssh_private_key_base64}.
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sync_interval_in_seconds ArcKubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeout_in_seconds ArcKubernetesFluxConfiguration#timeout_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e751481fe272ab5f592c0aa6cbe4f4c5e59ed174ebadd0d6a705b9b96d8e01ea)
            check_type(argname="argument reference_type", value=reference_type, expected_type=type_hints["reference_type"])
            check_type(argname="argument reference_value", value=reference_value, expected_type=type_hints["reference_value"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument https_ca_cert_base64", value=https_ca_cert_base64, expected_type=type_hints["https_ca_cert_base64"])
            check_type(argname="argument https_key_base64", value=https_key_base64, expected_type=type_hints["https_key_base64"])
            check_type(argname="argument https_user", value=https_user, expected_type=type_hints["https_user"])
            check_type(argname="argument local_auth_reference", value=local_auth_reference, expected_type=type_hints["local_auth_reference"])
            check_type(argname="argument ssh_known_hosts_base64", value=ssh_known_hosts_base64, expected_type=type_hints["ssh_known_hosts_base64"])
            check_type(argname="argument ssh_private_key_base64", value=ssh_private_key_base64, expected_type=type_hints["ssh_private_key_base64"])
            check_type(argname="argument sync_interval_in_seconds", value=sync_interval_in_seconds, expected_type=type_hints["sync_interval_in_seconds"])
            check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "reference_type": reference_type,
            "reference_value": reference_value,
            "url": url,
        }
        if https_ca_cert_base64 is not None:
            self._values["https_ca_cert_base64"] = https_ca_cert_base64
        if https_key_base64 is not None:
            self._values["https_key_base64"] = https_key_base64
        if https_user is not None:
            self._values["https_user"] = https_user
        if local_auth_reference is not None:
            self._values["local_auth_reference"] = local_auth_reference
        if ssh_known_hosts_base64 is not None:
            self._values["ssh_known_hosts_base64"] = ssh_known_hosts_base64
        if ssh_private_key_base64 is not None:
            self._values["ssh_private_key_base64"] = ssh_private_key_base64
        if sync_interval_in_seconds is not None:
            self._values["sync_interval_in_seconds"] = sync_interval_in_seconds
        if timeout_in_seconds is not None:
            self._values["timeout_in_seconds"] = timeout_in_seconds

    @builtins.property
    def reference_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#reference_type ArcKubernetesFluxConfiguration#reference_type}.'''
        result = self._values.get("reference_type")
        assert result is not None, "Required property 'reference_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reference_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#reference_value ArcKubernetesFluxConfiguration#reference_value}.'''
        result = self._values.get("reference_value")
        assert result is not None, "Required property 'reference_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#url ArcKubernetesFluxConfiguration#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def https_ca_cert_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#https_ca_cert_base64 ArcKubernetesFluxConfiguration#https_ca_cert_base64}.'''
        result = self._values.get("https_ca_cert_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_key_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#https_key_base64 ArcKubernetesFluxConfiguration#https_key_base64}.'''
        result = self._values.get("https_key_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#https_user ArcKubernetesFluxConfiguration#https_user}.'''
        result = self._values.get("https_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_auth_reference(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#local_auth_reference ArcKubernetesFluxConfiguration#local_auth_reference}.'''
        result = self._values.get("local_auth_reference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_known_hosts_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#ssh_known_hosts_base64 ArcKubernetesFluxConfiguration#ssh_known_hosts_base64}.'''
        result = self._values.get("ssh_known_hosts_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_private_key_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#ssh_private_key_base64 ArcKubernetesFluxConfiguration#ssh_private_key_base64}.'''
        result = self._values.get("ssh_private_key_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sync_interval_in_seconds ArcKubernetesFluxConfiguration#sync_interval_in_seconds}.'''
        result = self._values.get("sync_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeout_in_seconds ArcKubernetesFluxConfiguration#timeout_in_seconds}.'''
        result = self._values.get("timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArcKubernetesFluxConfigurationGitRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArcKubernetesFluxConfigurationGitRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationGitRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8352569697c67ebec163ff53a3965d2fed23cec883a38a0706207bab3f38ff3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHttpsCaCertBase64")
    def reset_https_ca_cert_base64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsCaCertBase64", []))

    @jsii.member(jsii_name="resetHttpsKeyBase64")
    def reset_https_key_base64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsKeyBase64", []))

    @jsii.member(jsii_name="resetHttpsUser")
    def reset_https_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsUser", []))

    @jsii.member(jsii_name="resetLocalAuthReference")
    def reset_local_auth_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalAuthReference", []))

    @jsii.member(jsii_name="resetSshKnownHostsBase64")
    def reset_ssh_known_hosts_base64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshKnownHostsBase64", []))

    @jsii.member(jsii_name="resetSshPrivateKeyBase64")
    def reset_ssh_private_key_base64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshPrivateKeyBase64", []))

    @jsii.member(jsii_name="resetSyncIntervalInSeconds")
    def reset_sync_interval_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncIntervalInSeconds", []))

    @jsii.member(jsii_name="resetTimeoutInSeconds")
    def reset_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="httpsCaCertBase64Input")
    def https_ca_cert_base64_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsCaCertBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="httpsKeyBase64Input")
    def https_key_base64_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsKeyBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="httpsUserInput")
    def https_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsUserInput"))

    @builtins.property
    @jsii.member(jsii_name="localAuthReferenceInput")
    def local_auth_reference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localAuthReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceTypeInput")
    def reference_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "referenceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceValueInput")
    def reference_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "referenceValueInput"))

    @builtins.property
    @jsii.member(jsii_name="sshKnownHostsBase64Input")
    def ssh_known_hosts_base64_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshKnownHostsBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKeyBase64Input")
    def ssh_private_key_base64_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshPrivateKeyBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="syncIntervalInSecondsInput")
    def sync_interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "syncIntervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInSecondsInput")
    def timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsCaCertBase64")
    def https_ca_cert_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsCaCertBase64"))

    @https_ca_cert_base64.setter
    def https_ca_cert_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad8c714bcc40470dd38ebc337bb90ebdd43a1345389aab4c66a00cfe8c3d83c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsCaCertBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsKeyBase64")
    def https_key_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsKeyBase64"))

    @https_key_base64.setter
    def https_key_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9e0db5a362c2cec95ed660327bb7f221a7a42571eb2ae0efbf8be33635601d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsKeyBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsUser")
    def https_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsUser"))

    @https_user.setter
    def https_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627e314372abef834c943588dde105a87d2c5ba30ea24021cb854d2008d7c7b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localAuthReference")
    def local_auth_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localAuthReference"))

    @local_auth_reference.setter
    def local_auth_reference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ae48438247922c938d419e27d10096763acbefaf9129a7ddf4a3b925a2bc49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localAuthReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="referenceType")
    def reference_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referenceType"))

    @reference_type.setter
    def reference_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828ceabaceb3eee044e6a920d75ab48f64963a0f48edcd5d0c4f0d08c4bc9a7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referenceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="referenceValue")
    def reference_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referenceValue"))

    @reference_value.setter
    def reference_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__617f1fb1c81dd1f620737af796be1ce0b515b1fdc69daa8ffa34855cb61da6d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referenceValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKnownHostsBase64")
    def ssh_known_hosts_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshKnownHostsBase64"))

    @ssh_known_hosts_base64.setter
    def ssh_known_hosts_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4707a223246636b87f81b86b93db8e84ad0c14523d6868671114caf3f44f5ace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKnownHostsBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKeyBase64")
    def ssh_private_key_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPrivateKeyBase64"))

    @ssh_private_key_base64.setter
    def ssh_private_key_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9225376c90e9a390d2f34270e4b0a5a1288e226784425be697587ac3256bb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPrivateKeyBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "syncIntervalInSeconds"))

    @sync_interval_in_seconds.setter
    def sync_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__549803e920df2207dc718614a63b46142429e013526b6ed67caf592f1da5ddce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutInSeconds")
    def timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutInSeconds"))

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f9f5cd5696cf14300602993ef7e8d66f4f8229744191f9fb7e86c4a93f0577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72749de3e4f1463bc8df528006e23f62036c26eea788395badf1c60f4560c5b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArcKubernetesFluxConfigurationGitRepository]:
        return typing.cast(typing.Optional[ArcKubernetesFluxConfigurationGitRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArcKubernetesFluxConfigurationGitRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dbc1fb1be378c5cad8d8252113f12427c017325d2cb89ffe4b8104b2b3d3305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationKustomizations",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "depends_on": "dependsOn",
        "garbage_collection_enabled": "garbageCollectionEnabled",
        "path": "path",
        "recreating_enabled": "recreatingEnabled",
        "retry_interval_in_seconds": "retryIntervalInSeconds",
        "sync_interval_in_seconds": "syncIntervalInSeconds",
        "timeout_in_seconds": "timeoutInSeconds",
    },
)
class ArcKubernetesFluxConfigurationKustomizations:
    def __init__(
        self,
        *,
        name: builtins.str,
        depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        garbage_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
        recreating_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_interval_in_seconds: typing.Optional[jsii.Number] = None,
        sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#name ArcKubernetesFluxConfiguration#name}.
        :param depends_on: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#depends_on ArcKubernetesFluxConfiguration#depends_on}.
        :param garbage_collection_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#garbage_collection_enabled ArcKubernetesFluxConfiguration#garbage_collection_enabled}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#path ArcKubernetesFluxConfiguration#path}.
        :param recreating_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#recreating_enabled ArcKubernetesFluxConfiguration#recreating_enabled}.
        :param retry_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#retry_interval_in_seconds ArcKubernetesFluxConfiguration#retry_interval_in_seconds}.
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sync_interval_in_seconds ArcKubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeout_in_seconds ArcKubernetesFluxConfiguration#timeout_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171c708654f7b0c089ccdec74792e2f8027e16bfdd91c61348a835f8f7100ee1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument garbage_collection_enabled", value=garbage_collection_enabled, expected_type=type_hints["garbage_collection_enabled"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument recreating_enabled", value=recreating_enabled, expected_type=type_hints["recreating_enabled"])
            check_type(argname="argument retry_interval_in_seconds", value=retry_interval_in_seconds, expected_type=type_hints["retry_interval_in_seconds"])
            check_type(argname="argument sync_interval_in_seconds", value=sync_interval_in_seconds, expected_type=type_hints["sync_interval_in_seconds"])
            check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if garbage_collection_enabled is not None:
            self._values["garbage_collection_enabled"] = garbage_collection_enabled
        if path is not None:
            self._values["path"] = path
        if recreating_enabled is not None:
            self._values["recreating_enabled"] = recreating_enabled
        if retry_interval_in_seconds is not None:
            self._values["retry_interval_in_seconds"] = retry_interval_in_seconds
        if sync_interval_in_seconds is not None:
            self._values["sync_interval_in_seconds"] = sync_interval_in_seconds
        if timeout_in_seconds is not None:
            self._values["timeout_in_seconds"] = timeout_in_seconds

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#name ArcKubernetesFluxConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#depends_on ArcKubernetesFluxConfiguration#depends_on}.'''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def garbage_collection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#garbage_collection_enabled ArcKubernetesFluxConfiguration#garbage_collection_enabled}.'''
        result = self._values.get("garbage_collection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#path ArcKubernetesFluxConfiguration#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recreating_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#recreating_enabled ArcKubernetesFluxConfiguration#recreating_enabled}.'''
        result = self._values.get("recreating_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retry_interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#retry_interval_in_seconds ArcKubernetesFluxConfiguration#retry_interval_in_seconds}.'''
        result = self._values.get("retry_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sync_interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#sync_interval_in_seconds ArcKubernetesFluxConfiguration#sync_interval_in_seconds}.'''
        result = self._values.get("sync_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#timeout_in_seconds ArcKubernetesFluxConfiguration#timeout_in_seconds}.'''
        result = self._values.get("timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArcKubernetesFluxConfigurationKustomizations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArcKubernetesFluxConfigurationKustomizationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationKustomizationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df1a3638be6498e54e6d25c9832f1d05805abf83d3b4029892aca5c7f68f4b06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ArcKubernetesFluxConfigurationKustomizationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510b2cbb20e04e8210d158367dea88c9d8f6d20456e7c5a52aaa20f573bee24d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ArcKubernetesFluxConfigurationKustomizationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67996be485dcfed53fb6dea81e73c83ac9bad8d3910173ef7527645c62efa524)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd9369338e15271b482e894b555fe79eab15cb10cb718650d2c5bd80b2ba0188)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08d2eae0ab6d9f8a79374bcc27facc123dd07a7891799ea79755a97375f35785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArcKubernetesFluxConfigurationKustomizations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArcKubernetesFluxConfigurationKustomizations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArcKubernetesFluxConfigurationKustomizations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a865bf8f30b6386eabc80b93363d476789b5652b32701f766333d6ba407e06f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ArcKubernetesFluxConfigurationKustomizationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationKustomizationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ac68a6d453de04399d6fab67506ab66b4c3e263bbfed00c2666aa45fab04d25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDependsOn")
    def reset_depends_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependsOn", []))

    @jsii.member(jsii_name="resetGarbageCollectionEnabled")
    def reset_garbage_collection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGarbageCollectionEnabled", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetRecreatingEnabled")
    def reset_recreating_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecreatingEnabled", []))

    @jsii.member(jsii_name="resetRetryIntervalInSeconds")
    def reset_retry_interval_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryIntervalInSeconds", []))

    @jsii.member(jsii_name="resetSyncIntervalInSeconds")
    def reset_sync_interval_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncIntervalInSeconds", []))

    @jsii.member(jsii_name="resetTimeoutInSeconds")
    def reset_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="dependsOnInput")
    def depends_on_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependsOnInput"))

    @builtins.property
    @jsii.member(jsii_name="garbageCollectionEnabledInput")
    def garbage_collection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "garbageCollectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="recreatingEnabledInput")
    def recreating_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "recreatingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="retryIntervalInSecondsInput")
    def retry_interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryIntervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="syncIntervalInSecondsInput")
    def sync_interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "syncIntervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInSecondsInput")
    def timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dependsOn"))

    @depends_on.setter
    def depends_on(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa8a02a99d6fbef6ac2c9cf0e9c7c8a785b6b634823b22bb7e745ebf429d008e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependsOn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="garbageCollectionEnabled")
    def garbage_collection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "garbageCollectionEnabled"))

    @garbage_collection_enabled.setter
    def garbage_collection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49279dfc41b925f996b766d19edf4fdbd9680626943c57f82e252b0ac415236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "garbageCollectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c67025912574026f7df33c27fe453ddc8f7b998b7b11931ab3b8bcf8df56c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573d93c223651ab1b3353e5156c1c161939bfcf15bdc67f17e672e9365810543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recreatingEnabled")
    def recreating_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "recreatingEnabled"))

    @recreating_enabled.setter
    def recreating_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2e5aa6f06520be47243f53e37a3c84888f0759055a9dc3961f62c28aedd9a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recreatingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryIntervalInSeconds")
    def retry_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryIntervalInSeconds"))

    @retry_interval_in_seconds.setter
    def retry_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c2a75fbf173079674d686dbcb29b2cc1fb3ddb4fc41312cf5ea3b556ed6922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "syncIntervalInSeconds"))

    @sync_interval_in_seconds.setter
    def sync_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30629906200bf5dbf1b515637e6b7487b079bc51cb0a64bbe4c3af084b97ade0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutInSeconds")
    def timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutInSeconds"))

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde8190e707d29a84ce8b209ad1d55e47279279c27c2e0aee180de3a0484976a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArcKubernetesFluxConfigurationKustomizations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArcKubernetesFluxConfigurationKustomizations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArcKubernetesFluxConfigurationKustomizations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9422971b301d1244c98c36fc4e117da3ba14c05c31d0a5fcd9a03540206c710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ArcKubernetesFluxConfigurationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#create ArcKubernetesFluxConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#delete ArcKubernetesFluxConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#read ArcKubernetesFluxConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#update ArcKubernetesFluxConfiguration#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf35586fdfcc8ee0bb7919c4b5026b890d73644d588018386d9cb4f3cefea11)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#create ArcKubernetesFluxConfiguration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#delete ArcKubernetesFluxConfiguration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#read ArcKubernetesFluxConfiguration#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_flux_configuration#update ArcKubernetesFluxConfiguration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArcKubernetesFluxConfigurationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArcKubernetesFluxConfigurationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.arcKubernetesFluxConfiguration.ArcKubernetesFluxConfigurationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59c1b86696e883b40218e95068421b8273016f2fc63efdb5f31a448211fedf28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81589a0a1c06ffc7bea87d5c82c6af6adca6ef7824807ecc4b2abc6099956433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d13a90ee1bd7319c14dada97a53d0f43260fc1c009a361d492f0eddba46478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c311862ff80cf14ac8d5338259deba06bae55ac7adcb5abd2509c09fc71e19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9bc3c48572b33943e0c23512a87b378daa107051a487d7e8ecf9c9e2a196f12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArcKubernetesFluxConfigurationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArcKubernetesFluxConfigurationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArcKubernetesFluxConfigurationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c25a96090b972a32a6650478206840e506d1da3290df4e0770d3d3c8cb349706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ArcKubernetesFluxConfiguration",
    "ArcKubernetesFluxConfigurationBlobStorage",
    "ArcKubernetesFluxConfigurationBlobStorageOutputReference",
    "ArcKubernetesFluxConfigurationBlobStorageServicePrincipal",
    "ArcKubernetesFluxConfigurationBlobStorageServicePrincipalOutputReference",
    "ArcKubernetesFluxConfigurationBucket",
    "ArcKubernetesFluxConfigurationBucketOutputReference",
    "ArcKubernetesFluxConfigurationConfig",
    "ArcKubernetesFluxConfigurationGitRepository",
    "ArcKubernetesFluxConfigurationGitRepositoryOutputReference",
    "ArcKubernetesFluxConfigurationKustomizations",
    "ArcKubernetesFluxConfigurationKustomizationsList",
    "ArcKubernetesFluxConfigurationKustomizationsOutputReference",
    "ArcKubernetesFluxConfigurationTimeouts",
    "ArcKubernetesFluxConfigurationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b8f40ad803ca2310ccfa2052d3374abc2b0094a45c0cdfe0cb76b99671bc9bac(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_id: builtins.str,
    kustomizations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ArcKubernetesFluxConfigurationKustomizations, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    namespace: builtins.str,
    blob_storage: typing.Optional[typing.Union[ArcKubernetesFluxConfigurationBlobStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    bucket: typing.Optional[typing.Union[ArcKubernetesFluxConfigurationBucket, typing.Dict[builtins.str, typing.Any]]] = None,
    continuous_reconciliation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    git_repository: typing.Optional[typing.Union[ArcKubernetesFluxConfigurationGitRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ArcKubernetesFluxConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e11ecfc8b035dcd6f9bfe98d66bb3e4b9157cd01a2f6c1656c8acfffe4758847(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17cafbadee6713c1510b49e0860aed1af9bedef1a8ceec6b14e99b16f9f4060(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ArcKubernetesFluxConfigurationKustomizations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d193a5efcd7ae3d22046943f5171a26f4f67ffd2e199375581eca3e1e36cd504(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208fd24d7f2fe9c986be93a6f4bd33b5e1c846adb989d9c498b99416f7cfdd33(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaef9bee33c544b31ff7358c7c7e3877552af61556411b472403c486fee421c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9bbbeca0e2da852780add610dc9a576ba67b4479432cc1a8e3f0dad0047daa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811faf671e4a5bcbdae244f3d44876a68bb3acc6fc3129f8aa6d3d0294512abf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f41739bcb6a0004f1537ddf06bb0f9f5acf527ab8feb2d978d92e3fe188c3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1306f56fed9aa80dc5362b98ea92fe037c6b46370f299b34fdce4e09db147188(
    *,
    container_id: builtins.str,
    account_key: typing.Optional[builtins.str] = None,
    local_auth_reference: typing.Optional[builtins.str] = None,
    sas_token: typing.Optional[builtins.str] = None,
    service_principal: typing.Optional[typing.Union[ArcKubernetesFluxConfigurationBlobStorageServicePrincipal, typing.Dict[builtins.str, typing.Any]]] = None,
    sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f8753f1926c03e0e28061cab3a787ddadf5cb3d46317b94937eebaa741f4fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967aa655dd5e2e8f87aa116b35845b04a047f024a7257e5ee3fb3453ea7b51a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3365b87fdc9ca76782fe01ca9d94a578e8b07a6c9d96bbda4e7bc58725342ab3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24751dd34d17fcb0d2b33e80010a32b274da9b012bbcb77aa3f914956c4bd9fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e28701d76db41543ed3f3770b2e29c43246c221a750618318c5e9ae5ff1b89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ba3e1ede370194bd8864bdbe992e971f4092d51fd7a6cc913c329192badbba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d1bbc61127027dbc2fe1933eae770bf8c8e6f0d8da6ce6ebfe492a66793449(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31b87daaf9a39f0fb7d9ab9dbf87bbbdb55951f2f14b5e8d88d10fe6dee9d12(
    value: typing.Optional[ArcKubernetesFluxConfigurationBlobStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3fd5ac1f8a4f2eaba85a811daf4cdf75016d2f541c30b010c904590a54ced4(
    *,
    client_id: builtins.str,
    tenant_id: builtins.str,
    client_certificate_base64: typing.Optional[builtins.str] = None,
    client_certificate_password: typing.Optional[builtins.str] = None,
    client_certificate_send_chain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc9dd92c8c334c11e056392eafd11642669029080913feb8e7dedd56c633cac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2c067a8dacecd28d41995d3f2c3e1298afba2e0d5bd4d83977ae54e8518fa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495dc1b391c5a2565748a9f19d04d93c0dab05896ec6a1524ec9b87e4074433e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f71b2060f90fabe7310e3397c00e886fe2295ed91fe2f19a5c754b3d2c4c5b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9733f0d1d04460787e10f14448eb4be344b3d521a6456013f3bfc604ba846462(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12d40df0bf42bb85b15f5dd47ea0bd0a0d0ab9ef63de89dab5a512170a78cf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be07a5bf4d86f2a93f6ff146e35732811f98384b8f4e1d56e8731df9989cd4aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb1db0c91dc9bcf5d05540af23dbc376b1cf4cddc6343ff2f3555b8e14c7671(
    value: typing.Optional[ArcKubernetesFluxConfigurationBlobStorageServicePrincipal],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd134588be5f6899c227463e4cbf07ea391e0410a58e176c5930352b56ff10f3(
    *,
    bucket_name: builtins.str,
    url: builtins.str,
    access_key: typing.Optional[builtins.str] = None,
    local_auth_reference: typing.Optional[builtins.str] = None,
    secret_key_base64: typing.Optional[builtins.str] = None,
    sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
    tls_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b82f1852d68ad5bdbcae510d7e625326b781ca65b4473f6f397a4b89a77079(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01afd95bdfa6cbe1d44f0a61d14fef156406859621b5088714f32a901bcb2a14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28774c63a460abbc220a21a8c8ab5b8abb892e97fdb1c4185ef1cb9f913b56ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be820534b68f8045c620e9c37d656e88565afa0f56880d2e160ff547dae6d20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f7d9fc240afdd12932d86578b60e178003f7eb69d94114b29effabd62d690d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfcd052288c149cfde7e27b699843ae69479474f584b7825d6c43cc61a6354b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365e4f6b8b4c17deeaea52885aefd68a36daf8028eee6659eb608e17e34d2e0b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e5ee7879f9b40da5df0797f4a1403bf634c3380228880c74652cbe3d88f8f9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14db6b0b5207d898461437c159859dcb35c02085b841dfcdaac805769da1a718(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfabd02bdae27085369132fea4b46929802ab18a3f14396d537becd0526e6c5b(
    value: typing.Optional[ArcKubernetesFluxConfigurationBucket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26dc42ee83a7fcffc6e7261921fba7c3a2cfc9b00a15568e7b854f6b873714dc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_id: builtins.str,
    kustomizations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ArcKubernetesFluxConfigurationKustomizations, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    namespace: builtins.str,
    blob_storage: typing.Optional[typing.Union[ArcKubernetesFluxConfigurationBlobStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    bucket: typing.Optional[typing.Union[ArcKubernetesFluxConfigurationBucket, typing.Dict[builtins.str, typing.Any]]] = None,
    continuous_reconciliation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    git_repository: typing.Optional[typing.Union[ArcKubernetesFluxConfigurationGitRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ArcKubernetesFluxConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e751481fe272ab5f592c0aa6cbe4f4c5e59ed174ebadd0d6a705b9b96d8e01ea(
    *,
    reference_type: builtins.str,
    reference_value: builtins.str,
    url: builtins.str,
    https_ca_cert_base64: typing.Optional[builtins.str] = None,
    https_key_base64: typing.Optional[builtins.str] = None,
    https_user: typing.Optional[builtins.str] = None,
    local_auth_reference: typing.Optional[builtins.str] = None,
    ssh_known_hosts_base64: typing.Optional[builtins.str] = None,
    ssh_private_key_base64: typing.Optional[builtins.str] = None,
    sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8352569697c67ebec163ff53a3965d2fed23cec883a38a0706207bab3f38ff3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad8c714bcc40470dd38ebc337bb90ebdd43a1345389aab4c66a00cfe8c3d83c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9e0db5a362c2cec95ed660327bb7f221a7a42571eb2ae0efbf8be33635601d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627e314372abef834c943588dde105a87d2c5ba30ea24021cb854d2008d7c7b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ae48438247922c938d419e27d10096763acbefaf9129a7ddf4a3b925a2bc49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828ceabaceb3eee044e6a920d75ab48f64963a0f48edcd5d0c4f0d08c4bc9a7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__617f1fb1c81dd1f620737af796be1ce0b515b1fdc69daa8ffa34855cb61da6d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4707a223246636b87f81b86b93db8e84ad0c14523d6868671114caf3f44f5ace(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9225376c90e9a390d2f34270e4b0a5a1288e226784425be697587ac3256bb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549803e920df2207dc718614a63b46142429e013526b6ed67caf592f1da5ddce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f9f5cd5696cf14300602993ef7e8d66f4f8229744191f9fb7e86c4a93f0577(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72749de3e4f1463bc8df528006e23f62036c26eea788395badf1c60f4560c5b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbc1fb1be378c5cad8d8252113f12427c017325d2cb89ffe4b8104b2b3d3305(
    value: typing.Optional[ArcKubernetesFluxConfigurationGitRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171c708654f7b0c089ccdec74792e2f8027e16bfdd91c61348a835f8f7100ee1(
    *,
    name: builtins.str,
    depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    garbage_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path: typing.Optional[builtins.str] = None,
    recreating_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retry_interval_in_seconds: typing.Optional[jsii.Number] = None,
    sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1a3638be6498e54e6d25c9832f1d05805abf83d3b4029892aca5c7f68f4b06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510b2cbb20e04e8210d158367dea88c9d8f6d20456e7c5a52aaa20f573bee24d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67996be485dcfed53fb6dea81e73c83ac9bad8d3910173ef7527645c62efa524(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd9369338e15271b482e894b555fe79eab15cb10cb718650d2c5bd80b2ba0188(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d2eae0ab6d9f8a79374bcc27facc123dd07a7891799ea79755a97375f35785(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a865bf8f30b6386eabc80b93363d476789b5652b32701f766333d6ba407e06f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArcKubernetesFluxConfigurationKustomizations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac68a6d453de04399d6fab67506ab66b4c3e263bbfed00c2666aa45fab04d25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8a02a99d6fbef6ac2c9cf0e9c7c8a785b6b634823b22bb7e745ebf429d008e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49279dfc41b925f996b766d19edf4fdbd9680626943c57f82e252b0ac415236(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c67025912574026f7df33c27fe453ddc8f7b998b7b11931ab3b8bcf8df56c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573d93c223651ab1b3353e5156c1c161939bfcf15bdc67f17e672e9365810543(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2e5aa6f06520be47243f53e37a3c84888f0759055a9dc3961f62c28aedd9a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c2a75fbf173079674d686dbcb29b2cc1fb3ddb4fc41312cf5ea3b556ed6922(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30629906200bf5dbf1b515637e6b7487b079bc51cb0a64bbe4c3af084b97ade0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde8190e707d29a84ce8b209ad1d55e47279279c27c2e0aee180de3a0484976a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9422971b301d1244c98c36fc4e117da3ba14c05c31d0a5fcd9a03540206c710(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArcKubernetesFluxConfigurationKustomizations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf35586fdfcc8ee0bb7919c4b5026b890d73644d588018386d9cb4f3cefea11(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c1b86696e883b40218e95068421b8273016f2fc63efdb5f31a448211fedf28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81589a0a1c06ffc7bea87d5c82c6af6adca6ef7824807ecc4b2abc6099956433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d13a90ee1bd7319c14dada97a53d0f43260fc1c009a361d492f0eddba46478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c311862ff80cf14ac8d5338259deba06bae55ac7adcb5abd2509c09fc71e19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9bc3c48572b33943e0c23512a87b378daa107051a487d7e8ecf9c9e2a196f12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c25a96090b972a32a6650478206840e506d1da3290df4e0770d3d3c8cb349706(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArcKubernetesFluxConfigurationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
