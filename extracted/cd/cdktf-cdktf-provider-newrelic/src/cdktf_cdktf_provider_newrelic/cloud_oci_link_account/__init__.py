r'''
# `newrelic_cloud_oci_link_account`

Refer to the Terraform Registry for docs: [`newrelic_cloud_oci_link_account`](https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account).
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


class CloudOciLinkAccount(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudOciLinkAccount.CloudOciLinkAccount",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account newrelic_cloud_oci_link_account}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        compartment_ocid: builtins.str,
        name: builtins.str,
        oci_client_id: builtins.str,
        oci_client_secret: builtins.str,
        oci_domain_url: builtins.str,
        oci_home_region: builtins.str,
        tenant_id: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ingest_vault_ocid: typing.Optional[builtins.str] = None,
        instrumentation_type: typing.Optional[builtins.str] = None,
        logging_stack_ocid: typing.Optional[builtins.str] = None,
        metric_stack_ocid: typing.Optional[builtins.str] = None,
        oci_region: typing.Optional[builtins.str] = None,
        user_vault_ocid: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account newrelic_cloud_oci_link_account} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param compartment_ocid: The New Relic compartment OCID in OCI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#compartment_ocid CloudOciLinkAccount#compartment_ocid}
        :param name: The linked account name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#name CloudOciLinkAccount#name}
        :param oci_client_id: The client ID for OCI WIF. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_client_id CloudOciLinkAccount#oci_client_id}
        :param oci_client_secret: The client secret for OCI WIF. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_client_secret CloudOciLinkAccount#oci_client_secret}
        :param oci_domain_url: The OCI domain URL for WIF. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_domain_url CloudOciLinkAccount#oci_domain_url}
        :param oci_home_region: The home region of the tenancy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_home_region CloudOciLinkAccount#oci_home_region}
        :param tenant_id: The OCI tenant identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#tenant_id CloudOciLinkAccount#tenant_id}
        :param account_id: The New Relic account ID where you want to link the OCI account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#account_id CloudOciLinkAccount#account_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#id CloudOciLinkAccount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingest_vault_ocid: The OCI ingest secret OCID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#ingest_vault_ocid CloudOciLinkAccount#ingest_vault_ocid}
        :param instrumentation_type: Specifies the type of integration, such as metrics, logs, or a combination of logs and metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#instrumentation_type CloudOciLinkAccount#instrumentation_type}
        :param logging_stack_ocid: The Logging stack identifier for the OCI account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#logging_stack_ocid CloudOciLinkAccount#logging_stack_ocid}
        :param metric_stack_ocid: The metric stack identifier for the OCI account. This field is only used for updates, not during initial creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#metric_stack_ocid CloudOciLinkAccount#metric_stack_ocid}
        :param oci_region: The OCI region for the account. This field is only used for updates, not during initial creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_region CloudOciLinkAccount#oci_region}
        :param user_vault_ocid: The user secret OCID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#user_vault_ocid CloudOciLinkAccount#user_vault_ocid}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35045cf23b7bc410068a73a618526a21dbabc5cf504c4ac087ec53c80fe2645)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudOciLinkAccountConfig(
            compartment_ocid=compartment_ocid,
            name=name,
            oci_client_id=oci_client_id,
            oci_client_secret=oci_client_secret,
            oci_domain_url=oci_domain_url,
            oci_home_region=oci_home_region,
            tenant_id=tenant_id,
            account_id=account_id,
            id=id,
            ingest_vault_ocid=ingest_vault_ocid,
            instrumentation_type=instrumentation_type,
            logging_stack_ocid=logging_stack_ocid,
            metric_stack_ocid=metric_stack_ocid,
            oci_region=oci_region,
            user_vault_ocid=user_vault_ocid,
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
        '''Generates CDKTF code for importing a CloudOciLinkAccount resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudOciLinkAccount to import.
        :param import_from_id: The id of the existing CloudOciLinkAccount that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudOciLinkAccount to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34c1de95baf7e6a99967fca6a34b4f9b5e6ce7d402e7f03514722640d98b9e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIngestVaultOcid")
    def reset_ingest_vault_ocid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngestVaultOcid", []))

    @jsii.member(jsii_name="resetInstrumentationType")
    def reset_instrumentation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstrumentationType", []))

    @jsii.member(jsii_name="resetLoggingStackOcid")
    def reset_logging_stack_ocid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingStackOcid", []))

    @jsii.member(jsii_name="resetMetricStackOcid")
    def reset_metric_stack_ocid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricStackOcid", []))

    @jsii.member(jsii_name="resetOciRegion")
    def reset_oci_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOciRegion", []))

    @jsii.member(jsii_name="resetUserVaultOcid")
    def reset_user_vault_ocid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserVaultOcid", []))

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
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="compartmentOcidInput")
    def compartment_ocid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compartmentOcidInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ingestVaultOcidInput")
    def ingest_vault_ocid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ingestVaultOcidInput"))

    @builtins.property
    @jsii.member(jsii_name="instrumentationTypeInput")
    def instrumentation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instrumentationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingStackOcidInput")
    def logging_stack_ocid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingStackOcidInput"))

    @builtins.property
    @jsii.member(jsii_name="metricStackOcidInput")
    def metric_stack_ocid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricStackOcidInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ociClientIdInput")
    def oci_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ociClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ociClientSecretInput")
    def oci_client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ociClientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="ociDomainUrlInput")
    def oci_domain_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ociDomainUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="ociHomeRegionInput")
    def oci_home_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ociHomeRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="ociRegionInput")
    def oci_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ociRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userVaultOcidInput")
    def user_vault_ocid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userVaultOcidInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1839c4a1b8f26c213bca79827b33c1050297749c8fbd5f717e704d85a7edca99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="compartmentOcid")
    def compartment_ocid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compartmentOcid"))

    @compartment_ocid.setter
    def compartment_ocid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee1f0f19bb7f8e4ef6103fa51fca7b2714a65aa1c1262e58490f42cd4f8d639)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compartmentOcid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3586ecbad78f822bd51e9eb1e589dc5b4a2e97c71597dfda0930c6ba25c6e6b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingestVaultOcid")
    def ingest_vault_ocid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingestVaultOcid"))

    @ingest_vault_ocid.setter
    def ingest_vault_ocid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557a6cdcee825238db0efe6fc2f7fd2225b792c8297ac64c2ba85cc8b8427de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingestVaultOcid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instrumentationType")
    def instrumentation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instrumentationType"))

    @instrumentation_type.setter
    def instrumentation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec11c63d650d32e5a9d3c644ae0f0f229ab0b91a14b6d612cbedb85ff3c012aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instrumentationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loggingStackOcid")
    def logging_stack_ocid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loggingStackOcid"))

    @logging_stack_ocid.setter
    def logging_stack_ocid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50ffcf645c9fd4d7aa5b770b5d050cd2791bd2eb8375b90456aac154f398f58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingStackOcid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricStackOcid")
    def metric_stack_ocid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricStackOcid"))

    @metric_stack_ocid.setter
    def metric_stack_ocid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45db1b82cbbdd8166737ae12e3c07a5dca69b89e224b175f32fb100b768848cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricStackOcid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8fc8ffa1a2db18118204a9717269ea974d23b4ae1a0f4083a1cd651220815be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ociClientId")
    def oci_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociClientId"))

    @oci_client_id.setter
    def oci_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b357d0c8b50d226155715a46fda0130224902dfd191c05bd5f98c776310ba52b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ociClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ociClientSecret")
    def oci_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociClientSecret"))

    @oci_client_secret.setter
    def oci_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee4b21f9bf2ed23011acfc67c2657489c6198c83147f1f58fef2334666da625c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ociClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ociDomainUrl")
    def oci_domain_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociDomainUrl"))

    @oci_domain_url.setter
    def oci_domain_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d86cca073669f63b2cf131675dca3792b155f0921dd4b3a92a7dde564b062c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ociDomainUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ociHomeRegion")
    def oci_home_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociHomeRegion"))

    @oci_home_region.setter
    def oci_home_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f883428d0bdcd38e42661af6eebd9180b898a320983a3b45cb69a5b7ce33c19f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ociHomeRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ociRegion")
    def oci_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociRegion"))

    @oci_region.setter
    def oci_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e892b2be64713231d86eb61de38317cbfdc0da00439254dc4770267f2d7754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ociRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d726e6eba63f0fd3946437b4b6cb60e06ad86b83fcce08136e9f800cf58c8be6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userVaultOcid")
    def user_vault_ocid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userVaultOcid"))

    @user_vault_ocid.setter
    def user_vault_ocid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddee461f588a842a205a04c0871a669b4546f350cdad0fdec410a2935a09c23e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userVaultOcid", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudOciLinkAccount.CloudOciLinkAccountConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "compartment_ocid": "compartmentOcid",
        "name": "name",
        "oci_client_id": "ociClientId",
        "oci_client_secret": "ociClientSecret",
        "oci_domain_url": "ociDomainUrl",
        "oci_home_region": "ociHomeRegion",
        "tenant_id": "tenantId",
        "account_id": "accountId",
        "id": "id",
        "ingest_vault_ocid": "ingestVaultOcid",
        "instrumentation_type": "instrumentationType",
        "logging_stack_ocid": "loggingStackOcid",
        "metric_stack_ocid": "metricStackOcid",
        "oci_region": "ociRegion",
        "user_vault_ocid": "userVaultOcid",
    },
)
class CloudOciLinkAccountConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        compartment_ocid: builtins.str,
        name: builtins.str,
        oci_client_id: builtins.str,
        oci_client_secret: builtins.str,
        oci_domain_url: builtins.str,
        oci_home_region: builtins.str,
        tenant_id: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ingest_vault_ocid: typing.Optional[builtins.str] = None,
        instrumentation_type: typing.Optional[builtins.str] = None,
        logging_stack_ocid: typing.Optional[builtins.str] = None,
        metric_stack_ocid: typing.Optional[builtins.str] = None,
        oci_region: typing.Optional[builtins.str] = None,
        user_vault_ocid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param compartment_ocid: The New Relic compartment OCID in OCI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#compartment_ocid CloudOciLinkAccount#compartment_ocid}
        :param name: The linked account name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#name CloudOciLinkAccount#name}
        :param oci_client_id: The client ID for OCI WIF. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_client_id CloudOciLinkAccount#oci_client_id}
        :param oci_client_secret: The client secret for OCI WIF. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_client_secret CloudOciLinkAccount#oci_client_secret}
        :param oci_domain_url: The OCI domain URL for WIF. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_domain_url CloudOciLinkAccount#oci_domain_url}
        :param oci_home_region: The home region of the tenancy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_home_region CloudOciLinkAccount#oci_home_region}
        :param tenant_id: The OCI tenant identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#tenant_id CloudOciLinkAccount#tenant_id}
        :param account_id: The New Relic account ID where you want to link the OCI account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#account_id CloudOciLinkAccount#account_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#id CloudOciLinkAccount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingest_vault_ocid: The OCI ingest secret OCID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#ingest_vault_ocid CloudOciLinkAccount#ingest_vault_ocid}
        :param instrumentation_type: Specifies the type of integration, such as metrics, logs, or a combination of logs and metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#instrumentation_type CloudOciLinkAccount#instrumentation_type}
        :param logging_stack_ocid: The Logging stack identifier for the OCI account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#logging_stack_ocid CloudOciLinkAccount#logging_stack_ocid}
        :param metric_stack_ocid: The metric stack identifier for the OCI account. This field is only used for updates, not during initial creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#metric_stack_ocid CloudOciLinkAccount#metric_stack_ocid}
        :param oci_region: The OCI region for the account. This field is only used for updates, not during initial creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_region CloudOciLinkAccount#oci_region}
        :param user_vault_ocid: The user secret OCID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#user_vault_ocid CloudOciLinkAccount#user_vault_ocid}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2ec87092f841d6c041a8248d99192e1f8460862273d896eb89bdd1286bb7365)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument compartment_ocid", value=compartment_ocid, expected_type=type_hints["compartment_ocid"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument oci_client_id", value=oci_client_id, expected_type=type_hints["oci_client_id"])
            check_type(argname="argument oci_client_secret", value=oci_client_secret, expected_type=type_hints["oci_client_secret"])
            check_type(argname="argument oci_domain_url", value=oci_domain_url, expected_type=type_hints["oci_domain_url"])
            check_type(argname="argument oci_home_region", value=oci_home_region, expected_type=type_hints["oci_home_region"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ingest_vault_ocid", value=ingest_vault_ocid, expected_type=type_hints["ingest_vault_ocid"])
            check_type(argname="argument instrumentation_type", value=instrumentation_type, expected_type=type_hints["instrumentation_type"])
            check_type(argname="argument logging_stack_ocid", value=logging_stack_ocid, expected_type=type_hints["logging_stack_ocid"])
            check_type(argname="argument metric_stack_ocid", value=metric_stack_ocid, expected_type=type_hints["metric_stack_ocid"])
            check_type(argname="argument oci_region", value=oci_region, expected_type=type_hints["oci_region"])
            check_type(argname="argument user_vault_ocid", value=user_vault_ocid, expected_type=type_hints["user_vault_ocid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compartment_ocid": compartment_ocid,
            "name": name,
            "oci_client_id": oci_client_id,
            "oci_client_secret": oci_client_secret,
            "oci_domain_url": oci_domain_url,
            "oci_home_region": oci_home_region,
            "tenant_id": tenant_id,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if id is not None:
            self._values["id"] = id
        if ingest_vault_ocid is not None:
            self._values["ingest_vault_ocid"] = ingest_vault_ocid
        if instrumentation_type is not None:
            self._values["instrumentation_type"] = instrumentation_type
        if logging_stack_ocid is not None:
            self._values["logging_stack_ocid"] = logging_stack_ocid
        if metric_stack_ocid is not None:
            self._values["metric_stack_ocid"] = metric_stack_ocid
        if oci_region is not None:
            self._values["oci_region"] = oci_region
        if user_vault_ocid is not None:
            self._values["user_vault_ocid"] = user_vault_ocid

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
    def compartment_ocid(self) -> builtins.str:
        '''The New Relic compartment OCID in OCI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#compartment_ocid CloudOciLinkAccount#compartment_ocid}
        '''
        result = self._values.get("compartment_ocid")
        assert result is not None, "Required property 'compartment_ocid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The linked account name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#name CloudOciLinkAccount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oci_client_id(self) -> builtins.str:
        '''The client ID for OCI WIF.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_client_id CloudOciLinkAccount#oci_client_id}
        '''
        result = self._values.get("oci_client_id")
        assert result is not None, "Required property 'oci_client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oci_client_secret(self) -> builtins.str:
        '''The client secret for OCI WIF.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_client_secret CloudOciLinkAccount#oci_client_secret}
        '''
        result = self._values.get("oci_client_secret")
        assert result is not None, "Required property 'oci_client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oci_domain_url(self) -> builtins.str:
        '''The OCI domain URL for WIF.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_domain_url CloudOciLinkAccount#oci_domain_url}
        '''
        result = self._values.get("oci_domain_url")
        assert result is not None, "Required property 'oci_domain_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oci_home_region(self) -> builtins.str:
        '''The home region of the tenancy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_home_region CloudOciLinkAccount#oci_home_region}
        '''
        result = self._values.get("oci_home_region")
        assert result is not None, "Required property 'oci_home_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''The OCI tenant identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#tenant_id CloudOciLinkAccount#tenant_id}
        '''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The New Relic account ID where you want to link the OCI account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#account_id CloudOciLinkAccount#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#id CloudOciLinkAccount#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingest_vault_ocid(self) -> typing.Optional[builtins.str]:
        '''The OCI ingest secret OCID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#ingest_vault_ocid CloudOciLinkAccount#ingest_vault_ocid}
        '''
        result = self._values.get("ingest_vault_ocid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instrumentation_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of integration, such as metrics, logs, or a combination of logs and metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#instrumentation_type CloudOciLinkAccount#instrumentation_type}
        '''
        result = self._values.get("instrumentation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_stack_ocid(self) -> typing.Optional[builtins.str]:
        '''The Logging stack identifier for the OCI account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#logging_stack_ocid CloudOciLinkAccount#logging_stack_ocid}
        '''
        result = self._values.get("logging_stack_ocid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_stack_ocid(self) -> typing.Optional[builtins.str]:
        '''The metric stack identifier for the OCI account. This field is only used for updates, not during initial creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#metric_stack_ocid CloudOciLinkAccount#metric_stack_ocid}
        '''
        result = self._values.get("metric_stack_ocid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oci_region(self) -> typing.Optional[builtins.str]:
        '''The OCI region for the account. This field is only used for updates, not during initial creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#oci_region CloudOciLinkAccount#oci_region}
        '''
        result = self._values.get("oci_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_vault_ocid(self) -> typing.Optional[builtins.str]:
        '''The user secret OCID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.76.3/docs/resources/cloud_oci_link_account#user_vault_ocid CloudOciLinkAccount#user_vault_ocid}
        '''
        result = self._values.get("user_vault_ocid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudOciLinkAccountConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudOciLinkAccount",
    "CloudOciLinkAccountConfig",
]

publication.publish()

def _typecheckingstub__e35045cf23b7bc410068a73a618526a21dbabc5cf504c4ac087ec53c80fe2645(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    compartment_ocid: builtins.str,
    name: builtins.str,
    oci_client_id: builtins.str,
    oci_client_secret: builtins.str,
    oci_domain_url: builtins.str,
    oci_home_region: builtins.str,
    tenant_id: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    ingest_vault_ocid: typing.Optional[builtins.str] = None,
    instrumentation_type: typing.Optional[builtins.str] = None,
    logging_stack_ocid: typing.Optional[builtins.str] = None,
    metric_stack_ocid: typing.Optional[builtins.str] = None,
    oci_region: typing.Optional[builtins.str] = None,
    user_vault_ocid: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d34c1de95baf7e6a99967fca6a34b4f9b5e6ce7d402e7f03514722640d98b9e8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1839c4a1b8f26c213bca79827b33c1050297749c8fbd5f717e704d85a7edca99(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee1f0f19bb7f8e4ef6103fa51fca7b2714a65aa1c1262e58490f42cd4f8d639(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3586ecbad78f822bd51e9eb1e589dc5b4a2e97c71597dfda0930c6ba25c6e6b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557a6cdcee825238db0efe6fc2f7fd2225b792c8297ac64c2ba85cc8b8427de6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec11c63d650d32e5a9d3c644ae0f0f229ab0b91a14b6d612cbedb85ff3c012aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50ffcf645c9fd4d7aa5b770b5d050cd2791bd2eb8375b90456aac154f398f58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45db1b82cbbdd8166737ae12e3c07a5dca69b89e224b175f32fb100b768848cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fc8ffa1a2db18118204a9717269ea974d23b4ae1a0f4083a1cd651220815be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b357d0c8b50d226155715a46fda0130224902dfd191c05bd5f98c776310ba52b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4b21f9bf2ed23011acfc67c2657489c6198c83147f1f58fef2334666da625c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d86cca073669f63b2cf131675dca3792b155f0921dd4b3a92a7dde564b062c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f883428d0bdcd38e42661af6eebd9180b898a320983a3b45cb69a5b7ce33c19f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e892b2be64713231d86eb61de38317cbfdc0da00439254dc4770267f2d7754(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d726e6eba63f0fd3946437b4b6cb60e06ad86b83fcce08136e9f800cf58c8be6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddee461f588a842a205a04c0871a669b4546f350cdad0fdec410a2935a09c23e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ec87092f841d6c041a8248d99192e1f8460862273d896eb89bdd1286bb7365(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    compartment_ocid: builtins.str,
    name: builtins.str,
    oci_client_id: builtins.str,
    oci_client_secret: builtins.str,
    oci_domain_url: builtins.str,
    oci_home_region: builtins.str,
    tenant_id: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    ingest_vault_ocid: typing.Optional[builtins.str] = None,
    instrumentation_type: typing.Optional[builtins.str] = None,
    logging_stack_ocid: typing.Optional[builtins.str] = None,
    metric_stack_ocid: typing.Optional[builtins.str] = None,
    oci_region: typing.Optional[builtins.str] = None,
    user_vault_ocid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
