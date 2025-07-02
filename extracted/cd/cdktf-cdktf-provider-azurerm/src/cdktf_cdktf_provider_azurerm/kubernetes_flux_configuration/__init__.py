r'''
# `azurerm_kubernetes_flux_configuration`

Refer to the Terraform Registry for docs: [`azurerm_kubernetes_flux_configuration`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration).
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


class KubernetesFluxConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration azurerm_kubernetes_flux_configuration}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_id: builtins.str,
        kustomizations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesFluxConfigurationKustomizations", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        namespace: builtins.str,
        blob_storage: typing.Optional[typing.Union["KubernetesFluxConfigurationBlobStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        bucket: typing.Optional[typing.Union["KubernetesFluxConfigurationBucket", typing.Dict[builtins.str, typing.Any]]] = None,
        continuous_reconciliation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        git_repository: typing.Optional[typing.Union["KubernetesFluxConfigurationGitRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KubernetesFluxConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration azurerm_kubernetes_flux_configuration} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#cluster_id KubernetesFluxConfiguration#cluster_id}.
        :param kustomizations: kustomizations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#kustomizations KubernetesFluxConfiguration#kustomizations}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#name KubernetesFluxConfiguration#name}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#namespace KubernetesFluxConfiguration#namespace}.
        :param blob_storage: blob_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#blob_storage KubernetesFluxConfiguration#blob_storage}
        :param bucket: bucket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#bucket KubernetesFluxConfiguration#bucket}
        :param continuous_reconciliation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#continuous_reconciliation_enabled KubernetesFluxConfiguration#continuous_reconciliation_enabled}.
        :param git_repository: git_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#git_repository KubernetesFluxConfiguration#git_repository}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#id KubernetesFluxConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#scope KubernetesFluxConfiguration#scope}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeouts KubernetesFluxConfiguration#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81903c4c16ea34abc735c25d6e81f6fa2cd3d2e37e54b0c24807166a864f4526)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KubernetesFluxConfigurationConfig(
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
        '''Generates CDKTF code for importing a KubernetesFluxConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KubernetesFluxConfiguration to import.
        :param import_from_id: The id of the existing KubernetesFluxConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KubernetesFluxConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b793270e8fa4c5981433febc35b81208007b2837ea68fd042be6aaf8a5bc717)
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
        managed_identity: typing.Optional[typing.Union["KubernetesFluxConfigurationBlobStorageManagedIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        sas_token: typing.Optional[builtins.str] = None,
        service_principal: typing.Optional[typing.Union["KubernetesFluxConfigurationBlobStorageServicePrincipal", typing.Dict[builtins.str, typing.Any]]] = None,
        sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param container_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#container_id KubernetesFluxConfiguration#container_id}.
        :param account_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#account_key KubernetesFluxConfiguration#account_key}.
        :param local_auth_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#local_auth_reference KubernetesFluxConfiguration#local_auth_reference}.
        :param managed_identity: managed_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#managed_identity KubernetesFluxConfiguration#managed_identity}
        :param sas_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sas_token KubernetesFluxConfiguration#sas_token}.
        :param service_principal: service_principal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#service_principal KubernetesFluxConfiguration#service_principal}
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sync_interval_in_seconds KubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeout_in_seconds KubernetesFluxConfiguration#timeout_in_seconds}.
        '''
        value = KubernetesFluxConfigurationBlobStorage(
            container_id=container_id,
            account_key=account_key,
            local_auth_reference=local_auth_reference,
            managed_identity=managed_identity,
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
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#bucket_name KubernetesFluxConfiguration#bucket_name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#url KubernetesFluxConfiguration#url}.
        :param access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#access_key KubernetesFluxConfiguration#access_key}.
        :param local_auth_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#local_auth_reference KubernetesFluxConfiguration#local_auth_reference}.
        :param secret_key_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#secret_key_base64 KubernetesFluxConfiguration#secret_key_base64}.
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sync_interval_in_seconds KubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeout_in_seconds KubernetesFluxConfiguration#timeout_in_seconds}.
        :param tls_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#tls_enabled KubernetesFluxConfiguration#tls_enabled}.
        '''
        value = KubernetesFluxConfigurationBucket(
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
        :param reference_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#reference_type KubernetesFluxConfiguration#reference_type}.
        :param reference_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#reference_value KubernetesFluxConfiguration#reference_value}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#url KubernetesFluxConfiguration#url}.
        :param https_ca_cert_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#https_ca_cert_base64 KubernetesFluxConfiguration#https_ca_cert_base64}.
        :param https_key_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#https_key_base64 KubernetesFluxConfiguration#https_key_base64}.
        :param https_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#https_user KubernetesFluxConfiguration#https_user}.
        :param local_auth_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#local_auth_reference KubernetesFluxConfiguration#local_auth_reference}.
        :param ssh_known_hosts_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#ssh_known_hosts_base64 KubernetesFluxConfiguration#ssh_known_hosts_base64}.
        :param ssh_private_key_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#ssh_private_key_base64 KubernetesFluxConfiguration#ssh_private_key_base64}.
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sync_interval_in_seconds KubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeout_in_seconds KubernetesFluxConfiguration#timeout_in_seconds}.
        '''
        value = KubernetesFluxConfigurationGitRepository(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesFluxConfigurationKustomizations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2a6d600e6c1c97bcdda8551f189126e319eb428de84c54acaae27123f8b832)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#create KubernetesFluxConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#delete KubernetesFluxConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#read KubernetesFluxConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#update KubernetesFluxConfiguration#update}.
        '''
        value = KubernetesFluxConfigurationTimeouts(
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
    def blob_storage(self) -> "KubernetesFluxConfigurationBlobStorageOutputReference":
        return typing.cast("KubernetesFluxConfigurationBlobStorageOutputReference", jsii.get(self, "blobStorage"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> "KubernetesFluxConfigurationBucketOutputReference":
        return typing.cast("KubernetesFluxConfigurationBucketOutputReference", jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="gitRepository")
    def git_repository(
        self,
    ) -> "KubernetesFluxConfigurationGitRepositoryOutputReference":
        return typing.cast("KubernetesFluxConfigurationGitRepositoryOutputReference", jsii.get(self, "gitRepository"))

    @builtins.property
    @jsii.member(jsii_name="kustomizations")
    def kustomizations(self) -> "KubernetesFluxConfigurationKustomizationsList":
        return typing.cast("KubernetesFluxConfigurationKustomizationsList", jsii.get(self, "kustomizations"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KubernetesFluxConfigurationTimeoutsOutputReference":
        return typing.cast("KubernetesFluxConfigurationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="blobStorageInput")
    def blob_storage_input(
        self,
    ) -> typing.Optional["KubernetesFluxConfigurationBlobStorage"]:
        return typing.cast(typing.Optional["KubernetesFluxConfigurationBlobStorage"], jsii.get(self, "blobStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional["KubernetesFluxConfigurationBucket"]:
        return typing.cast(typing.Optional["KubernetesFluxConfigurationBucket"], jsii.get(self, "bucketInput"))

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
    ) -> typing.Optional["KubernetesFluxConfigurationGitRepository"]:
        return typing.cast(typing.Optional["KubernetesFluxConfigurationGitRepository"], jsii.get(self, "gitRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kustomizationsInput")
    def kustomizations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFluxConfigurationKustomizations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFluxConfigurationKustomizations"]]], jsii.get(self, "kustomizationsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KubernetesFluxConfigurationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KubernetesFluxConfigurationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f1ef95dff92ba5dbdf3c59ba98eca07e6057e76c937a3c12524a32960266b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad8901716c83f9f981d08e919751a7c8b8d972672241eeff27408f9a8cd94667)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "continuousReconciliationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba883caf686830f6eebd6b71b3d43c4c885fffe173a526ef834da8e691ce53e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907f0086a852f41ddd00e9f29749c597cea6a8f4f0c4f3d158cc3c0fb1a7939d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0c9a80087c16759677c02c878d4e62c2a9fe890c00f86c3b984b936f331037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6056662f30b2aa4b74c1b89e1ccea4165a4b45135ac2a5ff7997bdabdb077695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationBlobStorage",
    jsii_struct_bases=[],
    name_mapping={
        "container_id": "containerId",
        "account_key": "accountKey",
        "local_auth_reference": "localAuthReference",
        "managed_identity": "managedIdentity",
        "sas_token": "sasToken",
        "service_principal": "servicePrincipal",
        "sync_interval_in_seconds": "syncIntervalInSeconds",
        "timeout_in_seconds": "timeoutInSeconds",
    },
)
class KubernetesFluxConfigurationBlobStorage:
    def __init__(
        self,
        *,
        container_id: builtins.str,
        account_key: typing.Optional[builtins.str] = None,
        local_auth_reference: typing.Optional[builtins.str] = None,
        managed_identity: typing.Optional[typing.Union["KubernetesFluxConfigurationBlobStorageManagedIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        sas_token: typing.Optional[builtins.str] = None,
        service_principal: typing.Optional[typing.Union["KubernetesFluxConfigurationBlobStorageServicePrincipal", typing.Dict[builtins.str, typing.Any]]] = None,
        sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param container_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#container_id KubernetesFluxConfiguration#container_id}.
        :param account_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#account_key KubernetesFluxConfiguration#account_key}.
        :param local_auth_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#local_auth_reference KubernetesFluxConfiguration#local_auth_reference}.
        :param managed_identity: managed_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#managed_identity KubernetesFluxConfiguration#managed_identity}
        :param sas_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sas_token KubernetesFluxConfiguration#sas_token}.
        :param service_principal: service_principal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#service_principal KubernetesFluxConfiguration#service_principal}
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sync_interval_in_seconds KubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeout_in_seconds KubernetesFluxConfiguration#timeout_in_seconds}.
        '''
        if isinstance(managed_identity, dict):
            managed_identity = KubernetesFluxConfigurationBlobStorageManagedIdentity(**managed_identity)
        if isinstance(service_principal, dict):
            service_principal = KubernetesFluxConfigurationBlobStorageServicePrincipal(**service_principal)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23835d0d1afea627bfb6d96fcc4f5099e8d30ce4f3320ae619d9aba6d40d569a)
            check_type(argname="argument container_id", value=container_id, expected_type=type_hints["container_id"])
            check_type(argname="argument account_key", value=account_key, expected_type=type_hints["account_key"])
            check_type(argname="argument local_auth_reference", value=local_auth_reference, expected_type=type_hints["local_auth_reference"])
            check_type(argname="argument managed_identity", value=managed_identity, expected_type=type_hints["managed_identity"])
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
        if managed_identity is not None:
            self._values["managed_identity"] = managed_identity
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#container_id KubernetesFluxConfiguration#container_id}.'''
        result = self._values.get("container_id")
        assert result is not None, "Required property 'container_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#account_key KubernetesFluxConfiguration#account_key}.'''
        result = self._values.get("account_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_auth_reference(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#local_auth_reference KubernetesFluxConfiguration#local_auth_reference}.'''
        result = self._values.get("local_auth_reference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_identity(
        self,
    ) -> typing.Optional["KubernetesFluxConfigurationBlobStorageManagedIdentity"]:
        '''managed_identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#managed_identity KubernetesFluxConfiguration#managed_identity}
        '''
        result = self._values.get("managed_identity")
        return typing.cast(typing.Optional["KubernetesFluxConfigurationBlobStorageManagedIdentity"], result)

    @builtins.property
    def sas_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sas_token KubernetesFluxConfiguration#sas_token}.'''
        result = self._values.get("sas_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_principal(
        self,
    ) -> typing.Optional["KubernetesFluxConfigurationBlobStorageServicePrincipal"]:
        '''service_principal block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#service_principal KubernetesFluxConfiguration#service_principal}
        '''
        result = self._values.get("service_principal")
        return typing.cast(typing.Optional["KubernetesFluxConfigurationBlobStorageServicePrincipal"], result)

    @builtins.property
    def sync_interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sync_interval_in_seconds KubernetesFluxConfiguration#sync_interval_in_seconds}.'''
        result = self._values.get("sync_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeout_in_seconds KubernetesFluxConfiguration#timeout_in_seconds}.'''
        result = self._values.get("timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFluxConfigurationBlobStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationBlobStorageManagedIdentity",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId"},
)
class KubernetesFluxConfigurationBlobStorageManagedIdentity:
    def __init__(self, *, client_id: builtins.str) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_id KubernetesFluxConfiguration#client_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f79e32daf1f82ab4a28b98ef68a52b886bd82c6bffeff2e1703260e714fa67)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_id KubernetesFluxConfiguration#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFluxConfigurationBlobStorageManagedIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesFluxConfigurationBlobStorageManagedIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationBlobStorageManagedIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b8f0b244e987a8686cee7e664539f0d17c31782721d38ec3506ef5fdb0ad290)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f432951e6ab15413be333612c4161b372bda583744bd4b83ba40a7825d3e56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesFluxConfigurationBlobStorageManagedIdentity]:
        return typing.cast(typing.Optional[KubernetesFluxConfigurationBlobStorageManagedIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesFluxConfigurationBlobStorageManagedIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__429e25e976e63eedee0bc449ea8eb17760b6bf34b8fa76e9a518556b2a3e0aaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KubernetesFluxConfigurationBlobStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationBlobStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05bba9ca84ccdbf5d531b0fc047b78f98f0a9a10bb549f27609346a98c3ffcbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putManagedIdentity")
    def put_managed_identity(self, *, client_id: builtins.str) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_id KubernetesFluxConfiguration#client_id}.
        '''
        value = KubernetesFluxConfigurationBlobStorageManagedIdentity(
            client_id=client_id
        )

        return typing.cast(None, jsii.invoke(self, "putManagedIdentity", [value]))

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
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_id KubernetesFluxConfiguration#client_id}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#tenant_id KubernetesFluxConfiguration#tenant_id}.
        :param client_certificate_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_certificate_base64 KubernetesFluxConfiguration#client_certificate_base64}.
        :param client_certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_certificate_password KubernetesFluxConfiguration#client_certificate_password}.
        :param client_certificate_send_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_certificate_send_chain KubernetesFluxConfiguration#client_certificate_send_chain}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_secret KubernetesFluxConfiguration#client_secret}.
        '''
        value = KubernetesFluxConfigurationBlobStorageServicePrincipal(
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

    @jsii.member(jsii_name="resetManagedIdentity")
    def reset_managed_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedIdentity", []))

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
    @jsii.member(jsii_name="managedIdentity")
    def managed_identity(
        self,
    ) -> KubernetesFluxConfigurationBlobStorageManagedIdentityOutputReference:
        return typing.cast(KubernetesFluxConfigurationBlobStorageManagedIdentityOutputReference, jsii.get(self, "managedIdentity"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipal")
    def service_principal(
        self,
    ) -> "KubernetesFluxConfigurationBlobStorageServicePrincipalOutputReference":
        return typing.cast("KubernetesFluxConfigurationBlobStorageServicePrincipalOutputReference", jsii.get(self, "servicePrincipal"))

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
    @jsii.member(jsii_name="managedIdentityInput")
    def managed_identity_input(
        self,
    ) -> typing.Optional[KubernetesFluxConfigurationBlobStorageManagedIdentity]:
        return typing.cast(typing.Optional[KubernetesFluxConfigurationBlobStorageManagedIdentity], jsii.get(self, "managedIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="sasTokenInput")
    def sas_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sasTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalInput")
    def service_principal_input(
        self,
    ) -> typing.Optional["KubernetesFluxConfigurationBlobStorageServicePrincipal"]:
        return typing.cast(typing.Optional["KubernetesFluxConfigurationBlobStorageServicePrincipal"], jsii.get(self, "servicePrincipalInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5574dea1f62ef37ecaa32827abb70e6af3066f4ec2817a10a134e58e218e93f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerId")
    def container_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerId"))

    @container_id.setter
    def container_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e211d7e4cd812785380826c316c288965b964665684fb7c7939d9448bcd9950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localAuthReference")
    def local_auth_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localAuthReference"))

    @local_auth_reference.setter
    def local_auth_reference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7955653a8d81af424d0641e5659002a7d8589f9f7b453f9fceca3934ba9ccd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localAuthReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sasToken")
    def sas_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sasToken"))

    @sas_token.setter
    def sas_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99df4f8ff0292a12dd6dd288f4a3e6adaaf465d4015e0ed6c81bfa9b4e181cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sasToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "syncIntervalInSeconds"))

    @sync_interval_in_seconds.setter
    def sync_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daca5b3069cec96ffecbfea6af900f327d57451bdf3921549d7db7e8f783f6c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutInSeconds")
    def timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutInSeconds"))

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded5218c90ffda094ab81412d1686c3f49bddc8f46c5629b611ac84b13039ba2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesFluxConfigurationBlobStorage]:
        return typing.cast(typing.Optional[KubernetesFluxConfigurationBlobStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesFluxConfigurationBlobStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__476bb085624bd7a2805aab2f4236349d5f9a6169c85369c2257f21a898a94eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationBlobStorageServicePrincipal",
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
class KubernetesFluxConfigurationBlobStorageServicePrincipal:
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
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_id KubernetesFluxConfiguration#client_id}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#tenant_id KubernetesFluxConfiguration#tenant_id}.
        :param client_certificate_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_certificate_base64 KubernetesFluxConfiguration#client_certificate_base64}.
        :param client_certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_certificate_password KubernetesFluxConfiguration#client_certificate_password}.
        :param client_certificate_send_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_certificate_send_chain KubernetesFluxConfiguration#client_certificate_send_chain}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_secret KubernetesFluxConfiguration#client_secret}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f1df621a89ac00485cfd0c0a691aa3817238c33f3f67e6437e13b5c0f5666e3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_id KubernetesFluxConfiguration#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#tenant_id KubernetesFluxConfiguration#tenant_id}.'''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_certificate_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_certificate_base64 KubernetesFluxConfiguration#client_certificate_base64}.'''
        result = self._values.get("client_certificate_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_certificate_password KubernetesFluxConfiguration#client_certificate_password}.'''
        result = self._values.get("client_certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_send_chain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_certificate_send_chain KubernetesFluxConfiguration#client_certificate_send_chain}.'''
        result = self._values.get("client_certificate_send_chain")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#client_secret KubernetesFluxConfiguration#client_secret}.'''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFluxConfigurationBlobStorageServicePrincipal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesFluxConfigurationBlobStorageServicePrincipalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationBlobStorageServicePrincipalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6866d578c9d8294a0ef0a5d904df425bd5fd856be0770e6c60149130fe21ace3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f56589636dd41fea19c7cc3e0d6ab5640465fd8cd6b063d624535fe667e354e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificatePassword")
    def client_certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificatePassword"))

    @client_certificate_password.setter
    def client_certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7237a3a9f8e88b864db5e232474f3a06bd7dd243f420f6c50a0e47436eee01bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da81b5c192204aa5f265796112cdf7a5dbfa6cdcb3820708cfffd484db6d8135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateSendChain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97b383d71f13862e7ab9b731ce8dbacc7fe2a56024bb68e704aa27300b596104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed14140fdf0d0f0db24755b917afd2dbe46d5fa6a7b8141eb1832b9e82154bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b4d94e704fab4125ec9c9e166b4d20d09c6c1eebbfdcf23c4dd202c95cd24eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesFluxConfigurationBlobStorageServicePrincipal]:
        return typing.cast(typing.Optional[KubernetesFluxConfigurationBlobStorageServicePrincipal], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesFluxConfigurationBlobStorageServicePrincipal],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e92419f8012b50dceda58e16ae88ebf6d38f642be62dfa501120747f9a370c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationBucket",
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
class KubernetesFluxConfigurationBucket:
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
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#bucket_name KubernetesFluxConfiguration#bucket_name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#url KubernetesFluxConfiguration#url}.
        :param access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#access_key KubernetesFluxConfiguration#access_key}.
        :param local_auth_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#local_auth_reference KubernetesFluxConfiguration#local_auth_reference}.
        :param secret_key_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#secret_key_base64 KubernetesFluxConfiguration#secret_key_base64}.
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sync_interval_in_seconds KubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeout_in_seconds KubernetesFluxConfiguration#timeout_in_seconds}.
        :param tls_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#tls_enabled KubernetesFluxConfiguration#tls_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4333914c7d146202580e3d9dee0115556983fea5c72c7b7d49eef7ed23bc0c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#bucket_name KubernetesFluxConfiguration#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#url KubernetesFluxConfiguration#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#access_key KubernetesFluxConfiguration#access_key}.'''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_auth_reference(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#local_auth_reference KubernetesFluxConfiguration#local_auth_reference}.'''
        result = self._values.get("local_auth_reference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#secret_key_base64 KubernetesFluxConfiguration#secret_key_base64}.'''
        result = self._values.get("secret_key_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sync_interval_in_seconds KubernetesFluxConfiguration#sync_interval_in_seconds}.'''
        result = self._values.get("sync_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeout_in_seconds KubernetesFluxConfiguration#timeout_in_seconds}.'''
        result = self._values.get("timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#tls_enabled KubernetesFluxConfiguration#tls_enabled}.'''
        result = self._values.get("tls_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFluxConfigurationBucket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesFluxConfigurationBucketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationBucketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b617737cea9c75c92741edb400fadbd4ab716439eb5a96fb750568c010658c49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec92911964c9ba9c989d9f4c3ccdba9a89802565e94f9eb9a2124517ddd6e5ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c406b92844b9d6693008d3d9665671bb6d87555716bffacf1a805717e8fe80c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localAuthReference")
    def local_auth_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localAuthReference"))

    @local_auth_reference.setter
    def local_auth_reference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba61dd7a0983d857e4b8b20eabea9fdafecd9d192889dd391983cb0555821e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localAuthReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretKeyBase64")
    def secret_key_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretKeyBase64"))

    @secret_key_base64.setter
    def secret_key_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7143f074fc5665ddb8090134facbce83d109b6f9e24a08e4101e4a18196a5473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKeyBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "syncIntervalInSeconds"))

    @sync_interval_in_seconds.setter
    def sync_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cbfcf3ec470c609c3f7798ffa500726a9d64757aa8870b589959577240311aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutInSeconds")
    def timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutInSeconds"))

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd5776a92338fc0848a2987106c5383164a9a35cdd987c669cf107562cd950b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0be3b361f29cb744123000d61ae47093ef51eda76cb40b0b9a3fd4e869bb7561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e202e231229714fa49eae93c0f446ba50bf2dd9f28336e9862bc6038ba8fc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesFluxConfigurationBucket]:
        return typing.cast(typing.Optional[KubernetesFluxConfigurationBucket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesFluxConfigurationBucket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93293ed3a4d8949e4caaf0f0ccff20529f9ffb9ca199213e8b3c620fda734fb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationConfig",
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
class KubernetesFluxConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        kustomizations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesFluxConfigurationKustomizations", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        namespace: builtins.str,
        blob_storage: typing.Optional[typing.Union[KubernetesFluxConfigurationBlobStorage, typing.Dict[builtins.str, typing.Any]]] = None,
        bucket: typing.Optional[typing.Union[KubernetesFluxConfigurationBucket, typing.Dict[builtins.str, typing.Any]]] = None,
        continuous_reconciliation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        git_repository: typing.Optional[typing.Union["KubernetesFluxConfigurationGitRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KubernetesFluxConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#cluster_id KubernetesFluxConfiguration#cluster_id}.
        :param kustomizations: kustomizations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#kustomizations KubernetesFluxConfiguration#kustomizations}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#name KubernetesFluxConfiguration#name}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#namespace KubernetesFluxConfiguration#namespace}.
        :param blob_storage: blob_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#blob_storage KubernetesFluxConfiguration#blob_storage}
        :param bucket: bucket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#bucket KubernetesFluxConfiguration#bucket}
        :param continuous_reconciliation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#continuous_reconciliation_enabled KubernetesFluxConfiguration#continuous_reconciliation_enabled}.
        :param git_repository: git_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#git_repository KubernetesFluxConfiguration#git_repository}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#id KubernetesFluxConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#scope KubernetesFluxConfiguration#scope}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeouts KubernetesFluxConfiguration#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(blob_storage, dict):
            blob_storage = KubernetesFluxConfigurationBlobStorage(**blob_storage)
        if isinstance(bucket, dict):
            bucket = KubernetesFluxConfigurationBucket(**bucket)
        if isinstance(git_repository, dict):
            git_repository = KubernetesFluxConfigurationGitRepository(**git_repository)
        if isinstance(timeouts, dict):
            timeouts = KubernetesFluxConfigurationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8febffc46389bc07e34a62ccafa4a8b1f43f7773ab0da3ea92834c4a810052d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#cluster_id KubernetesFluxConfiguration#cluster_id}.'''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kustomizations(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFluxConfigurationKustomizations"]]:
        '''kustomizations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#kustomizations KubernetesFluxConfiguration#kustomizations}
        '''
        result = self._values.get("kustomizations")
        assert result is not None, "Required property 'kustomizations' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFluxConfigurationKustomizations"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#name KubernetesFluxConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#namespace KubernetesFluxConfiguration#namespace}.'''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def blob_storage(self) -> typing.Optional[KubernetesFluxConfigurationBlobStorage]:
        '''blob_storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#blob_storage KubernetesFluxConfiguration#blob_storage}
        '''
        result = self._values.get("blob_storage")
        return typing.cast(typing.Optional[KubernetesFluxConfigurationBlobStorage], result)

    @builtins.property
    def bucket(self) -> typing.Optional[KubernetesFluxConfigurationBucket]:
        '''bucket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#bucket KubernetesFluxConfiguration#bucket}
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[KubernetesFluxConfigurationBucket], result)

    @builtins.property
    def continuous_reconciliation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#continuous_reconciliation_enabled KubernetesFluxConfiguration#continuous_reconciliation_enabled}.'''
        result = self._values.get("continuous_reconciliation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def git_repository(
        self,
    ) -> typing.Optional["KubernetesFluxConfigurationGitRepository"]:
        '''git_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#git_repository KubernetesFluxConfiguration#git_repository}
        '''
        result = self._values.get("git_repository")
        return typing.cast(typing.Optional["KubernetesFluxConfigurationGitRepository"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#id KubernetesFluxConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#scope KubernetesFluxConfiguration#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KubernetesFluxConfigurationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeouts KubernetesFluxConfiguration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KubernetesFluxConfigurationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFluxConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationGitRepository",
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
class KubernetesFluxConfigurationGitRepository:
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
        :param reference_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#reference_type KubernetesFluxConfiguration#reference_type}.
        :param reference_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#reference_value KubernetesFluxConfiguration#reference_value}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#url KubernetesFluxConfiguration#url}.
        :param https_ca_cert_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#https_ca_cert_base64 KubernetesFluxConfiguration#https_ca_cert_base64}.
        :param https_key_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#https_key_base64 KubernetesFluxConfiguration#https_key_base64}.
        :param https_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#https_user KubernetesFluxConfiguration#https_user}.
        :param local_auth_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#local_auth_reference KubernetesFluxConfiguration#local_auth_reference}.
        :param ssh_known_hosts_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#ssh_known_hosts_base64 KubernetesFluxConfiguration#ssh_known_hosts_base64}.
        :param ssh_private_key_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#ssh_private_key_base64 KubernetesFluxConfiguration#ssh_private_key_base64}.
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sync_interval_in_seconds KubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeout_in_seconds KubernetesFluxConfiguration#timeout_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34f61c6ff5f2cf91768333ff783d0563f0acbaaedc57ef866f0cc1784293ee3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#reference_type KubernetesFluxConfiguration#reference_type}.'''
        result = self._values.get("reference_type")
        assert result is not None, "Required property 'reference_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reference_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#reference_value KubernetesFluxConfiguration#reference_value}.'''
        result = self._values.get("reference_value")
        assert result is not None, "Required property 'reference_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#url KubernetesFluxConfiguration#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def https_ca_cert_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#https_ca_cert_base64 KubernetesFluxConfiguration#https_ca_cert_base64}.'''
        result = self._values.get("https_ca_cert_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_key_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#https_key_base64 KubernetesFluxConfiguration#https_key_base64}.'''
        result = self._values.get("https_key_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#https_user KubernetesFluxConfiguration#https_user}.'''
        result = self._values.get("https_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_auth_reference(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#local_auth_reference KubernetesFluxConfiguration#local_auth_reference}.'''
        result = self._values.get("local_auth_reference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_known_hosts_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#ssh_known_hosts_base64 KubernetesFluxConfiguration#ssh_known_hosts_base64}.'''
        result = self._values.get("ssh_known_hosts_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_private_key_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#ssh_private_key_base64 KubernetesFluxConfiguration#ssh_private_key_base64}.'''
        result = self._values.get("ssh_private_key_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sync_interval_in_seconds KubernetesFluxConfiguration#sync_interval_in_seconds}.'''
        result = self._values.get("sync_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeout_in_seconds KubernetesFluxConfiguration#timeout_in_seconds}.'''
        result = self._values.get("timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFluxConfigurationGitRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesFluxConfigurationGitRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationGitRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e565fabcc0c1608da907e89b6368660732d33602c12ee25a5985358cf77623b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b8765cdec22317c8f1af088781b74c925d29036a78e64356b97507836f4f194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsCaCertBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsKeyBase64")
    def https_key_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsKeyBase64"))

    @https_key_base64.setter
    def https_key_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdb9600b443b59e793236b1d10470ba013f0bbe197189e5e162158947d5baf4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsKeyBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsUser")
    def https_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsUser"))

    @https_user.setter
    def https_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e49ca9a2afa3e6cc51a50d2bcb434ee958af2f93797308277bbfc60d1978a660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localAuthReference")
    def local_auth_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localAuthReference"))

    @local_auth_reference.setter
    def local_auth_reference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a440c32229a5eef8b695db6833333b3eff64d29925aeb04efc94c123e5626cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localAuthReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="referenceType")
    def reference_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referenceType"))

    @reference_type.setter
    def reference_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__711013224260d1fa4a7b46bed3e7747051971c02682020a075d00130ff2ab432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referenceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="referenceValue")
    def reference_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referenceValue"))

    @reference_value.setter
    def reference_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90875211b1265fc816aa362d1baab558950a76e749f5492fce05f5e5fbea4d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referenceValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKnownHostsBase64")
    def ssh_known_hosts_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshKnownHostsBase64"))

    @ssh_known_hosts_base64.setter
    def ssh_known_hosts_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846d78b987a131470c025c055c27e9e2e85d4f62be86d28b80f52dae9bf8faed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKnownHostsBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKeyBase64")
    def ssh_private_key_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPrivateKeyBase64"))

    @ssh_private_key_base64.setter
    def ssh_private_key_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5842e9c5078a61c48d5f49519d4a62519a282897dcffe8b6575462645c87fc28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPrivateKeyBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "syncIntervalInSeconds"))

    @sync_interval_in_seconds.setter
    def sync_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f5599956102601c7ba373912bd67fe694c68002a3ed2f18a2ab7af638a36a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutInSeconds")
    def timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutInSeconds"))

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03c1b295b32185a12fe14b30cd00b9c1daba5b8f511bd2f3f25433e9145fbbe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6127f7cfcc5c76dd0ac7e31248b1c1dba5bc1c6a9df470645857b71aca2c5bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesFluxConfigurationGitRepository]:
        return typing.cast(typing.Optional[KubernetesFluxConfigurationGitRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesFluxConfigurationGitRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f0572b0cc518af4f1733a467813e0ddcf259c6405c75e64472a52e7f63339aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationKustomizations",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "depends_on": "dependsOn",
        "garbage_collection_enabled": "garbageCollectionEnabled",
        "path": "path",
        "post_build": "postBuild",
        "recreating_enabled": "recreatingEnabled",
        "retry_interval_in_seconds": "retryIntervalInSeconds",
        "sync_interval_in_seconds": "syncIntervalInSeconds",
        "timeout_in_seconds": "timeoutInSeconds",
        "wait": "wait",
    },
)
class KubernetesFluxConfigurationKustomizations:
    def __init__(
        self,
        *,
        name: builtins.str,
        depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        garbage_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
        post_build: typing.Optional[typing.Union["KubernetesFluxConfigurationKustomizationsPostBuild", typing.Dict[builtins.str, typing.Any]]] = None,
        recreating_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_interval_in_seconds: typing.Optional[jsii.Number] = None,
        sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
        wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#name KubernetesFluxConfiguration#name}.
        :param depends_on: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#depends_on KubernetesFluxConfiguration#depends_on}.
        :param garbage_collection_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#garbage_collection_enabled KubernetesFluxConfiguration#garbage_collection_enabled}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#path KubernetesFluxConfiguration#path}.
        :param post_build: post_build block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#post_build KubernetesFluxConfiguration#post_build}
        :param recreating_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#recreating_enabled KubernetesFluxConfiguration#recreating_enabled}.
        :param retry_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#retry_interval_in_seconds KubernetesFluxConfiguration#retry_interval_in_seconds}.
        :param sync_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sync_interval_in_seconds KubernetesFluxConfiguration#sync_interval_in_seconds}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeout_in_seconds KubernetesFluxConfiguration#timeout_in_seconds}.
        :param wait: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#wait KubernetesFluxConfiguration#wait}.
        '''
        if isinstance(post_build, dict):
            post_build = KubernetesFluxConfigurationKustomizationsPostBuild(**post_build)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47e462f777d1fb3e9148464395b21f371d58c3032c4162dc0475ca7d6a7d4f8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument garbage_collection_enabled", value=garbage_collection_enabled, expected_type=type_hints["garbage_collection_enabled"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument post_build", value=post_build, expected_type=type_hints["post_build"])
            check_type(argname="argument recreating_enabled", value=recreating_enabled, expected_type=type_hints["recreating_enabled"])
            check_type(argname="argument retry_interval_in_seconds", value=retry_interval_in_seconds, expected_type=type_hints["retry_interval_in_seconds"])
            check_type(argname="argument sync_interval_in_seconds", value=sync_interval_in_seconds, expected_type=type_hints["sync_interval_in_seconds"])
            check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            check_type(argname="argument wait", value=wait, expected_type=type_hints["wait"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if garbage_collection_enabled is not None:
            self._values["garbage_collection_enabled"] = garbage_collection_enabled
        if path is not None:
            self._values["path"] = path
        if post_build is not None:
            self._values["post_build"] = post_build
        if recreating_enabled is not None:
            self._values["recreating_enabled"] = recreating_enabled
        if retry_interval_in_seconds is not None:
            self._values["retry_interval_in_seconds"] = retry_interval_in_seconds
        if sync_interval_in_seconds is not None:
            self._values["sync_interval_in_seconds"] = sync_interval_in_seconds
        if timeout_in_seconds is not None:
            self._values["timeout_in_seconds"] = timeout_in_seconds
        if wait is not None:
            self._values["wait"] = wait

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#name KubernetesFluxConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#depends_on KubernetesFluxConfiguration#depends_on}.'''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def garbage_collection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#garbage_collection_enabled KubernetesFluxConfiguration#garbage_collection_enabled}.'''
        result = self._values.get("garbage_collection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#path KubernetesFluxConfiguration#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_build(
        self,
    ) -> typing.Optional["KubernetesFluxConfigurationKustomizationsPostBuild"]:
        '''post_build block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#post_build KubernetesFluxConfiguration#post_build}
        '''
        result = self._values.get("post_build")
        return typing.cast(typing.Optional["KubernetesFluxConfigurationKustomizationsPostBuild"], result)

    @builtins.property
    def recreating_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#recreating_enabled KubernetesFluxConfiguration#recreating_enabled}.'''
        result = self._values.get("recreating_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retry_interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#retry_interval_in_seconds KubernetesFluxConfiguration#retry_interval_in_seconds}.'''
        result = self._values.get("retry_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sync_interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#sync_interval_in_seconds KubernetesFluxConfiguration#sync_interval_in_seconds}.'''
        result = self._values.get("sync_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#timeout_in_seconds KubernetesFluxConfiguration#timeout_in_seconds}.'''
        result = self._values.get("timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def wait(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#wait KubernetesFluxConfiguration#wait}.'''
        result = self._values.get("wait")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFluxConfigurationKustomizations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesFluxConfigurationKustomizationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationKustomizationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a51877bd5c17bf6f4ea07ece1da593e0f56ca8c145b551f5a37c446d9630226)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KubernetesFluxConfigurationKustomizationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d07f20f0cb01ff6e5d087e01576ac4e85dd6fa6061770fdbd593e89a1a1fe974)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KubernetesFluxConfigurationKustomizationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a88889c175cc114081d0b5725ceeceaa01777ab43f9454e0436de22bc6e407d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47567ac8a7e206f53d711a2bd17316695280fc50b8dfab20fb26efa783b57977)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2627344da8bd298454188b20505741aaa38f97c0492276287408e71c361d7829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFluxConfigurationKustomizations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFluxConfigurationKustomizations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFluxConfigurationKustomizations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d90edb243daa4d036688532849ca3154e9ab88f963bb4efb90a5f94e11c187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KubernetesFluxConfigurationKustomizationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationKustomizationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bfdbf65eb65d150d0003ce5fe4a5f7306ea9e90af1d4407bdd2c1317b05dc02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPostBuild")
    def put_post_build(
        self,
        *,
        substitute: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        substitute_from: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param substitute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#substitute KubernetesFluxConfiguration#substitute}.
        :param substitute_from: substitute_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#substitute_from KubernetesFluxConfiguration#substitute_from}
        '''
        value = KubernetesFluxConfigurationKustomizationsPostBuild(
            substitute=substitute, substitute_from=substitute_from
        )

        return typing.cast(None, jsii.invoke(self, "putPostBuild", [value]))

    @jsii.member(jsii_name="resetDependsOn")
    def reset_depends_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependsOn", []))

    @jsii.member(jsii_name="resetGarbageCollectionEnabled")
    def reset_garbage_collection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGarbageCollectionEnabled", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPostBuild")
    def reset_post_build(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostBuild", []))

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

    @jsii.member(jsii_name="resetWait")
    def reset_wait(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWait", []))

    @builtins.property
    @jsii.member(jsii_name="postBuild")
    def post_build(
        self,
    ) -> "KubernetesFluxConfigurationKustomizationsPostBuildOutputReference":
        return typing.cast("KubernetesFluxConfigurationKustomizationsPostBuildOutputReference", jsii.get(self, "postBuild"))

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
    @jsii.member(jsii_name="postBuildInput")
    def post_build_input(
        self,
    ) -> typing.Optional["KubernetesFluxConfigurationKustomizationsPostBuild"]:
        return typing.cast(typing.Optional["KubernetesFluxConfigurationKustomizationsPostBuild"], jsii.get(self, "postBuildInput"))

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
    @jsii.member(jsii_name="waitInput")
    def wait_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitInput"))

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dependsOn"))

    @depends_on.setter
    def depends_on(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b193342fe7ed40fb197094defdc098050d091f5ee5f756080733390eb52365ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8abe967986b20bc4539fa5c2cf7e5a1bd5c42f54eab85e75f7ec269adf8ce051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "garbageCollectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078f946cbdbed9af3f17ee9c743f4e13413f9a637c531deb5bb266df8c3da0a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5431c0a17184eaf642a1b21e2608cc2f3921c24198820babb26cacac05b9b20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a5a4d86ef5a2fddcdedc3c85546fdd6d5fbe3ca2a5608a35a6e02e3aa65068a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recreatingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryIntervalInSeconds")
    def retry_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryIntervalInSeconds"))

    @retry_interval_in_seconds.setter
    def retry_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fd4a9458f588ec909fa8afca77f301b5c521fadecd0262f592a64337e14cbc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "syncIntervalInSeconds"))

    @sync_interval_in_seconds.setter
    def sync_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85f488ca8c98dd70ee69180edbcd7008f3ab3578fd85019db001b7694e047aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutInSeconds")
    def timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutInSeconds"))

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c30fbcdba2910d35bf088c7ff247f17bc839e0fb82b01017da3aa8f3606b52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wait")
    def wait(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "wait"))

    @wait.setter
    def wait(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ce0b1e6766ef5f804e56f88558c7769df458a5cb97bf6d238da9be2e8ee8f70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wait", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFluxConfigurationKustomizations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFluxConfigurationKustomizations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFluxConfigurationKustomizations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ea0f8c38f7a62ed87e1de465f65fdbedfef7fb4283c85e32cdc0b0452a7168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationKustomizationsPostBuild",
    jsii_struct_bases=[],
    name_mapping={"substitute": "substitute", "substitute_from": "substituteFrom"},
)
class KubernetesFluxConfigurationKustomizationsPostBuild:
    def __init__(
        self,
        *,
        substitute: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        substitute_from: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param substitute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#substitute KubernetesFluxConfiguration#substitute}.
        :param substitute_from: substitute_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#substitute_from KubernetesFluxConfiguration#substitute_from}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b61fa3a5016a1712370a7253c7f183799b0fa2711c7d345d7e08ee4207fdffe)
            check_type(argname="argument substitute", value=substitute, expected_type=type_hints["substitute"])
            check_type(argname="argument substitute_from", value=substitute_from, expected_type=type_hints["substitute_from"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if substitute is not None:
            self._values["substitute"] = substitute
        if substitute_from is not None:
            self._values["substitute_from"] = substitute_from

    @builtins.property
    def substitute(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#substitute KubernetesFluxConfiguration#substitute}.'''
        result = self._values.get("substitute")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def substitute_from(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom"]]]:
        '''substitute_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#substitute_from KubernetesFluxConfiguration#substitute_from}
        '''
        result = self._values.get("substitute_from")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFluxConfigurationKustomizationsPostBuild(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesFluxConfigurationKustomizationsPostBuildOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationKustomizationsPostBuildOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f94ba695d9bcc8ee2a7c3b7273dd809c6e1988006cb9067af9b09bcf2cdb8de8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSubstituteFrom")
    def put_substitute_from(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d31e419fad87c5c2a6581a18291cc6efc3d2ba904a0f16e47eff9db5732cb8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubstituteFrom", [value]))

    @jsii.member(jsii_name="resetSubstitute")
    def reset_substitute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubstitute", []))

    @jsii.member(jsii_name="resetSubstituteFrom")
    def reset_substitute_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubstituteFrom", []))

    @builtins.property
    @jsii.member(jsii_name="substituteFrom")
    def substitute_from(
        self,
    ) -> "KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFromList":
        return typing.cast("KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFromList", jsii.get(self, "substituteFrom"))

    @builtins.property
    @jsii.member(jsii_name="substituteFromInput")
    def substitute_from_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom"]]], jsii.get(self, "substituteFromInput"))

    @builtins.property
    @jsii.member(jsii_name="substituteInput")
    def substitute_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "substituteInput"))

    @builtins.property
    @jsii.member(jsii_name="substitute")
    def substitute(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "substitute"))

    @substitute.setter
    def substitute(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17d89fba08e2736bcb2ec946298c17799a138dcb77d5a84460ef99a433d9803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "substitute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesFluxConfigurationKustomizationsPostBuild]:
        return typing.cast(typing.Optional[KubernetesFluxConfigurationKustomizationsPostBuild], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesFluxConfigurationKustomizationsPostBuild],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5612ca6053388ea08b023a3674573a735f75f1b1877a5491bd18386df98438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom",
    jsii_struct_bases=[],
    name_mapping={"kind": "kind", "name": "name", "optional": "optional"},
)
class KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom:
    def __init__(
        self,
        *,
        kind: builtins.str,
        name: builtins.str,
        optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#kind KubernetesFluxConfiguration#kind}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#name KubernetesFluxConfiguration#name}.
        :param optional: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#optional KubernetesFluxConfiguration#optional}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f693dd5c93902e6d37784307e8fb540b447892a823b04d2e2a00a0e8f8b9f43)
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kind": kind,
            "name": name,
        }
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def kind(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#kind KubernetesFluxConfiguration#kind}.'''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#name KubernetesFluxConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def optional(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#optional KubernetesFluxConfiguration#optional}.'''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFromList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFromList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__384cea9e7e31fd55b3db0e415c214216dfd0cb36ce63df0e23fcc29c9c152519)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFromOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e70e7118a9c70ffbe14e3807e8619d3951c9f0a009a461ce025baef691b1ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFromOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1dfb28fc961d0672140a2035ddea167c54f2f5a6db26c8e744b9a84ee83098c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__031823655298d147b3ea231406459bf2994aee5eb0382c3361e20f81ab50bfd3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e28f482afcf28ac41bd400ab4c71311a3908b61f647a5406d6ab5147444f0307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e4f1e6a0bbd1d8445660d37112435c182fe78d9eecb263d1d58ac7a20cb0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fadf7ab9e5a07f0a012208fdeaf917e94ae9f357f885a5825ab2b010cc75d538)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOptional")
    def reset_optional(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptional", []))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalInput")
    def optional_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optionalInput"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc3c671f4605d9fc695fe1ca5bc3830aa36c28a109756f51d7807b70934896e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61aca05d0b36bb4a8a0feca3826885a1229c0439e176184af08dbe256d7f7985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optional")
    def optional(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optional"))

    @optional.setter
    def optional(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0c0c1d6225ddda73c3c7e0cfd3d0fabd963dfd38e432b8032a5c6c93c960bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optional", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45e4c000cd298f5058bcfa2cc546bde5424b8a135926d5736be92dada50baaf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class KubernetesFluxConfigurationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#create KubernetesFluxConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#delete KubernetesFluxConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#read KubernetesFluxConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#update KubernetesFluxConfiguration#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c32003f86f2b834bae39850d942b01b852d2ede10dfc9013fd8acfccebef30b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#create KubernetesFluxConfiguration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#delete KubernetesFluxConfiguration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#read KubernetesFluxConfiguration#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_flux_configuration#update KubernetesFluxConfiguration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFluxConfigurationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesFluxConfigurationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFluxConfiguration.KubernetesFluxConfigurationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d59eae77638f83b452b8fc92230b9c00530d14871431f7a8cfb623235c28d23f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47da1fae04375b68466df12fccf8ae226b0d94ee496861abe3d550a28488e851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__896c0d9722ca8469008accb0cfa7e551f1a6f402bb22ec393f1243cf28e95ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff7883c7043a5b99ef96900eaecbe00f9a28d87bd3f65e6dc936549aa0af503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2b590014a083dd43a72cda0f0a87dde24f3f343d64e6e7a4dcdc79cbd95dbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFluxConfigurationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFluxConfigurationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFluxConfigurationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__750c975af402fca8ba2cca50312bbee48d584d6b394a3172d590aa09c8cc9ed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KubernetesFluxConfiguration",
    "KubernetesFluxConfigurationBlobStorage",
    "KubernetesFluxConfigurationBlobStorageManagedIdentity",
    "KubernetesFluxConfigurationBlobStorageManagedIdentityOutputReference",
    "KubernetesFluxConfigurationBlobStorageOutputReference",
    "KubernetesFluxConfigurationBlobStorageServicePrincipal",
    "KubernetesFluxConfigurationBlobStorageServicePrincipalOutputReference",
    "KubernetesFluxConfigurationBucket",
    "KubernetesFluxConfigurationBucketOutputReference",
    "KubernetesFluxConfigurationConfig",
    "KubernetesFluxConfigurationGitRepository",
    "KubernetesFluxConfigurationGitRepositoryOutputReference",
    "KubernetesFluxConfigurationKustomizations",
    "KubernetesFluxConfigurationKustomizationsList",
    "KubernetesFluxConfigurationKustomizationsOutputReference",
    "KubernetesFluxConfigurationKustomizationsPostBuild",
    "KubernetesFluxConfigurationKustomizationsPostBuildOutputReference",
    "KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom",
    "KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFromList",
    "KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFromOutputReference",
    "KubernetesFluxConfigurationTimeouts",
    "KubernetesFluxConfigurationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__81903c4c16ea34abc735c25d6e81f6fa2cd3d2e37e54b0c24807166a864f4526(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_id: builtins.str,
    kustomizations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesFluxConfigurationKustomizations, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    namespace: builtins.str,
    blob_storage: typing.Optional[typing.Union[KubernetesFluxConfigurationBlobStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    bucket: typing.Optional[typing.Union[KubernetesFluxConfigurationBucket, typing.Dict[builtins.str, typing.Any]]] = None,
    continuous_reconciliation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    git_repository: typing.Optional[typing.Union[KubernetesFluxConfigurationGitRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KubernetesFluxConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9b793270e8fa4c5981433febc35b81208007b2837ea68fd042be6aaf8a5bc717(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2a6d600e6c1c97bcdda8551f189126e319eb428de84c54acaae27123f8b832(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesFluxConfigurationKustomizations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f1ef95dff92ba5dbdf3c59ba98eca07e6057e76c937a3c12524a32960266b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8901716c83f9f981d08e919751a7c8b8d972672241eeff27408f9a8cd94667(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba883caf686830f6eebd6b71b3d43c4c885fffe173a526ef834da8e691ce53e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907f0086a852f41ddd00e9f29749c597cea6a8f4f0c4f3d158cc3c0fb1a7939d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0c9a80087c16759677c02c878d4e62c2a9fe890c00f86c3b984b936f331037(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6056662f30b2aa4b74c1b89e1ccea4165a4b45135ac2a5ff7997bdabdb077695(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23835d0d1afea627bfb6d96fcc4f5099e8d30ce4f3320ae619d9aba6d40d569a(
    *,
    container_id: builtins.str,
    account_key: typing.Optional[builtins.str] = None,
    local_auth_reference: typing.Optional[builtins.str] = None,
    managed_identity: typing.Optional[typing.Union[KubernetesFluxConfigurationBlobStorageManagedIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    sas_token: typing.Optional[builtins.str] = None,
    service_principal: typing.Optional[typing.Union[KubernetesFluxConfigurationBlobStorageServicePrincipal, typing.Dict[builtins.str, typing.Any]]] = None,
    sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f79e32daf1f82ab4a28b98ef68a52b886bd82c6bffeff2e1703260e714fa67(
    *,
    client_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8f0b244e987a8686cee7e664539f0d17c31782721d38ec3506ef5fdb0ad290(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f432951e6ab15413be333612c4161b372bda583744bd4b83ba40a7825d3e56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429e25e976e63eedee0bc449ea8eb17760b6bf34b8fa76e9a518556b2a3e0aaa(
    value: typing.Optional[KubernetesFluxConfigurationBlobStorageManagedIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05bba9ca84ccdbf5d531b0fc047b78f98f0a9a10bb549f27609346a98c3ffcbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5574dea1f62ef37ecaa32827abb70e6af3066f4ec2817a10a134e58e218e93f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e211d7e4cd812785380826c316c288965b964665684fb7c7939d9448bcd9950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7955653a8d81af424d0641e5659002a7d8589f9f7b453f9fceca3934ba9ccd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99df4f8ff0292a12dd6dd288f4a3e6adaaf465d4015e0ed6c81bfa9b4e181cac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daca5b3069cec96ffecbfea6af900f327d57451bdf3921549d7db7e8f783f6c5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded5218c90ffda094ab81412d1686c3f49bddc8f46c5629b611ac84b13039ba2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__476bb085624bd7a2805aab2f4236349d5f9a6169c85369c2257f21a898a94eaa(
    value: typing.Optional[KubernetesFluxConfigurationBlobStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1df621a89ac00485cfd0c0a691aa3817238c33f3f67e6437e13b5c0f5666e3(
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

def _typecheckingstub__6866d578c9d8294a0ef0a5d904df425bd5fd856be0770e6c60149130fe21ace3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f56589636dd41fea19c7cc3e0d6ab5640465fd8cd6b063d624535fe667e354e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7237a3a9f8e88b864db5e232474f3a06bd7dd243f420f6c50a0e47436eee01bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da81b5c192204aa5f265796112cdf7a5dbfa6cdcb3820708cfffd484db6d8135(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97b383d71f13862e7ab9b731ce8dbacc7fe2a56024bb68e704aa27300b596104(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed14140fdf0d0f0db24755b917afd2dbe46d5fa6a7b8141eb1832b9e82154bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4d94e704fab4125ec9c9e166b4d20d09c6c1eebbfdcf23c4dd202c95cd24eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e92419f8012b50dceda58e16ae88ebf6d38f642be62dfa501120747f9a370c8(
    value: typing.Optional[KubernetesFluxConfigurationBlobStorageServicePrincipal],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4333914c7d146202580e3d9dee0115556983fea5c72c7b7d49eef7ed23bc0c(
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

def _typecheckingstub__b617737cea9c75c92741edb400fadbd4ab716439eb5a96fb750568c010658c49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec92911964c9ba9c989d9f4c3ccdba9a89802565e94f9eb9a2124517ddd6e5ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c406b92844b9d6693008d3d9665671bb6d87555716bffacf1a805717e8fe80c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba61dd7a0983d857e4b8b20eabea9fdafecd9d192889dd391983cb0555821e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7143f074fc5665ddb8090134facbce83d109b6f9e24a08e4101e4a18196a5473(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cbfcf3ec470c609c3f7798ffa500726a9d64757aa8870b589959577240311aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd5776a92338fc0848a2987106c5383164a9a35cdd987c669cf107562cd950b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be3b361f29cb744123000d61ae47093ef51eda76cb40b0b9a3fd4e869bb7561(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e202e231229714fa49eae93c0f446ba50bf2dd9f28336e9862bc6038ba8fc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93293ed3a4d8949e4caaf0f0ccff20529f9ffb9ca199213e8b3c620fda734fb1(
    value: typing.Optional[KubernetesFluxConfigurationBucket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8febffc46389bc07e34a62ccafa4a8b1f43f7773ab0da3ea92834c4a810052d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_id: builtins.str,
    kustomizations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesFluxConfigurationKustomizations, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    namespace: builtins.str,
    blob_storage: typing.Optional[typing.Union[KubernetesFluxConfigurationBlobStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    bucket: typing.Optional[typing.Union[KubernetesFluxConfigurationBucket, typing.Dict[builtins.str, typing.Any]]] = None,
    continuous_reconciliation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    git_repository: typing.Optional[typing.Union[KubernetesFluxConfigurationGitRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KubernetesFluxConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34f61c6ff5f2cf91768333ff783d0563f0acbaaedc57ef866f0cc1784293ee3(
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

def _typecheckingstub__e565fabcc0c1608da907e89b6368660732d33602c12ee25a5985358cf77623b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b8765cdec22317c8f1af088781b74c925d29036a78e64356b97507836f4f194(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb9600b443b59e793236b1d10470ba013f0bbe197189e5e162158947d5baf4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e49ca9a2afa3e6cc51a50d2bcb434ee958af2f93797308277bbfc60d1978a660(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a440c32229a5eef8b695db6833333b3eff64d29925aeb04efc94c123e5626cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711013224260d1fa4a7b46bed3e7747051971c02682020a075d00130ff2ab432(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90875211b1265fc816aa362d1baab558950a76e749f5492fce05f5e5fbea4d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846d78b987a131470c025c055c27e9e2e85d4f62be86d28b80f52dae9bf8faed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5842e9c5078a61c48d5f49519d4a62519a282897dcffe8b6575462645c87fc28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f5599956102601c7ba373912bd67fe694c68002a3ed2f18a2ab7af638a36a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c1b295b32185a12fe14b30cd00b9c1daba5b8f511bd2f3f25433e9145fbbe0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6127f7cfcc5c76dd0ac7e31248b1c1dba5bc1c6a9df470645857b71aca2c5bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f0572b0cc518af4f1733a467813e0ddcf259c6405c75e64472a52e7f63339aa(
    value: typing.Optional[KubernetesFluxConfigurationGitRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47e462f777d1fb3e9148464395b21f371d58c3032c4162dc0475ca7d6a7d4f8(
    *,
    name: builtins.str,
    depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    garbage_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path: typing.Optional[builtins.str] = None,
    post_build: typing.Optional[typing.Union[KubernetesFluxConfigurationKustomizationsPostBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    recreating_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retry_interval_in_seconds: typing.Optional[jsii.Number] = None,
    sync_interval_in_seconds: typing.Optional[jsii.Number] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
    wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a51877bd5c17bf6f4ea07ece1da593e0f56ca8c145b551f5a37c446d9630226(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07f20f0cb01ff6e5d087e01576ac4e85dd6fa6061770fdbd593e89a1a1fe974(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a88889c175cc114081d0b5725ceeceaa01777ab43f9454e0436de22bc6e407d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47567ac8a7e206f53d711a2bd17316695280fc50b8dfab20fb26efa783b57977(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2627344da8bd298454188b20505741aaa38f97c0492276287408e71c361d7829(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d90edb243daa4d036688532849ca3154e9ab88f963bb4efb90a5f94e11c187(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFluxConfigurationKustomizations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bfdbf65eb65d150d0003ce5fe4a5f7306ea9e90af1d4407bdd2c1317b05dc02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b193342fe7ed40fb197094defdc098050d091f5ee5f756080733390eb52365ab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abe967986b20bc4539fa5c2cf7e5a1bd5c42f54eab85e75f7ec269adf8ce051(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078f946cbdbed9af3f17ee9c743f4e13413f9a637c531deb5bb266df8c3da0a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5431c0a17184eaf642a1b21e2608cc2f3921c24198820babb26cacac05b9b20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5a4d86ef5a2fddcdedc3c85546fdd6d5fbe3ca2a5608a35a6e02e3aa65068a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd4a9458f588ec909fa8afca77f301b5c521fadecd0262f592a64337e14cbc0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f488ca8c98dd70ee69180edbcd7008f3ab3578fd85019db001b7694e047aac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c30fbcdba2910d35bf088c7ff247f17bc839e0fb82b01017da3aa8f3606b52(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce0b1e6766ef5f804e56f88558c7769df458a5cb97bf6d238da9be2e8ee8f70(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ea0f8c38f7a62ed87e1de465f65fdbedfef7fb4283c85e32cdc0b0452a7168(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFluxConfigurationKustomizations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b61fa3a5016a1712370a7253c7f183799b0fa2711c7d345d7e08ee4207fdffe(
    *,
    substitute: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    substitute_from: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94ba695d9bcc8ee2a7c3b7273dd809c6e1988006cb9067af9b09bcf2cdb8de8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d31e419fad87c5c2a6581a18291cc6efc3d2ba904a0f16e47eff9db5732cb8b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17d89fba08e2736bcb2ec946298c17799a138dcb77d5a84460ef99a433d9803(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5612ca6053388ea08b023a3674573a735f75f1b1877a5491bd18386df98438(
    value: typing.Optional[KubernetesFluxConfigurationKustomizationsPostBuild],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f693dd5c93902e6d37784307e8fb540b447892a823b04d2e2a00a0e8f8b9f43(
    *,
    kind: builtins.str,
    name: builtins.str,
    optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__384cea9e7e31fd55b3db0e415c214216dfd0cb36ce63df0e23fcc29c9c152519(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e70e7118a9c70ffbe14e3807e8619d3951c9f0a009a461ce025baef691b1ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1dfb28fc961d0672140a2035ddea167c54f2f5a6db26c8e744b9a84ee83098c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031823655298d147b3ea231406459bf2994aee5eb0382c3361e20f81ab50bfd3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e28f482afcf28ac41bd400ab4c71311a3908b61f647a5406d6ab5147444f0307(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e4f1e6a0bbd1d8445660d37112435c182fe78d9eecb263d1d58ac7a20cb0ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fadf7ab9e5a07f0a012208fdeaf917e94ae9f357f885a5825ab2b010cc75d538(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc3c671f4605d9fc695fe1ca5bc3830aa36c28a109756f51d7807b70934896e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61aca05d0b36bb4a8a0feca3826885a1229c0439e176184af08dbe256d7f7985(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0c0c1d6225ddda73c3c7e0cfd3d0fabd963dfd38e432b8032a5c6c93c960bf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e4c000cd298f5058bcfa2cc546bde5424b8a135926d5736be92dada50baaf3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFluxConfigurationKustomizationsPostBuildSubstituteFrom]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c32003f86f2b834bae39850d942b01b852d2ede10dfc9013fd8acfccebef30b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59eae77638f83b452b8fc92230b9c00530d14871431f7a8cfb623235c28d23f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47da1fae04375b68466df12fccf8ae226b0d94ee496861abe3d550a28488e851(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896c0d9722ca8469008accb0cfa7e551f1a6f402bb22ec393f1243cf28e95ce7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff7883c7043a5b99ef96900eaecbe00f9a28d87bd3f65e6dc936549aa0af503(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2b590014a083dd43a72cda0f0a87dde24f3f343d64e6e7a4dcdc79cbd95dbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750c975af402fca8ba2cca50312bbee48d584d6b394a3172d590aa09c8cc9ed3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFluxConfigurationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
