r'''
# `provider`

Refer to the Terraform Registry for docs: [`newrelic`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs).
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


class NewrelicProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.provider.NewrelicProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs newrelic}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account_id: jsii.Number,
        api_key: builtins.str,
        admin_api_key: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        api_url: typing.Optional[builtins.str] = None,
        cacert_file: typing.Optional[builtins.str] = None,
        infrastructure_api_url: typing.Optional[builtins.str] = None,
        insecure_skip_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        insights_insert_key: typing.Optional[builtins.str] = None,
        insights_insert_url: typing.Optional[builtins.str] = None,
        insights_query_url: typing.Optional[builtins.str] = None,
        nerdgraph_api_url: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        synthetics_api_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs newrelic} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#account_id NewrelicProvider#account_id}.
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#api_key NewrelicProvider#api_key}.
        :param admin_api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#admin_api_key NewrelicProvider#admin_api_key}.
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#alias NewrelicProvider#alias}
        :param api_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#api_url NewrelicProvider#api_url}.
        :param cacert_file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#cacert_file NewrelicProvider#cacert_file}.
        :param infrastructure_api_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#infrastructure_api_url NewrelicProvider#infrastructure_api_url}.
        :param insecure_skip_verify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#insecure_skip_verify NewrelicProvider#insecure_skip_verify}.
        :param insights_insert_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#insights_insert_key NewrelicProvider#insights_insert_key}.
        :param insights_insert_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#insights_insert_url NewrelicProvider#insights_insert_url}.
        :param insights_query_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#insights_query_url NewrelicProvider#insights_query_url}.
        :param nerdgraph_api_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#nerdgraph_api_url NewrelicProvider#nerdgraph_api_url}.
        :param region: The data center for which your New Relic account is configured. Only one region per provider block is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#region NewrelicProvider#region}
        :param synthetics_api_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#synthetics_api_url NewrelicProvider#synthetics_api_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afa037631c2b6bae79191bb584dd1a23c1c2764f77ff94450c3708f8ed37e50)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = NewrelicProviderConfig(
            account_id=account_id,
            api_key=api_key,
            admin_api_key=admin_api_key,
            alias=alias,
            api_url=api_url,
            cacert_file=cacert_file,
            infrastructure_api_url=infrastructure_api_url,
            insecure_skip_verify=insecure_skip_verify,
            insights_insert_key=insights_insert_key,
            insights_insert_url=insights_insert_url,
            insights_query_url=insights_query_url,
            nerdgraph_api_url=nerdgraph_api_url,
            region=region,
            synthetics_api_url=synthetics_api_url,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a NewrelicProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NewrelicProvider to import.
        :param import_from_id: The id of the existing NewrelicProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NewrelicProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__122b13451c31fda4c1a14628cc32b6148317d3868f10170cf9305570c14afe13)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAdminApiKey")
    def reset_admin_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminApiKey", []))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetApiUrl")
    def reset_api_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiUrl", []))

    @jsii.member(jsii_name="resetCacertFile")
    def reset_cacert_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacertFile", []))

    @jsii.member(jsii_name="resetInfrastructureApiUrl")
    def reset_infrastructure_api_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfrastructureApiUrl", []))

    @jsii.member(jsii_name="resetInsecureSkipVerify")
    def reset_insecure_skip_verify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureSkipVerify", []))

    @jsii.member(jsii_name="resetInsightsInsertKey")
    def reset_insights_insert_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsightsInsertKey", []))

    @jsii.member(jsii_name="resetInsightsInsertUrl")
    def reset_insights_insert_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsightsInsertUrl", []))

    @jsii.member(jsii_name="resetInsightsQueryUrl")
    def reset_insights_query_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsightsQueryUrl", []))

    @jsii.member(jsii_name="resetNerdgraphApiUrl")
    def reset_nerdgraph_api_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNerdgraphApiUrl", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSyntheticsApiUrl")
    def reset_synthetics_api_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyntheticsApiUrl", []))

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
    @jsii.member(jsii_name="adminApiKeyInput")
    def admin_api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminApiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiUrlInput")
    def api_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="cacertFileInput")
    def cacert_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacertFileInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureApiUrlInput")
    def infrastructure_api_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "infrastructureApiUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureSkipVerifyInput")
    def insecure_skip_verify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureSkipVerifyInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsInsertKeyInput")
    def insights_insert_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsInsertKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsInsertUrlInput")
    def insights_insert_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsInsertUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsQueryUrlInput")
    def insights_query_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsQueryUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="nerdgraphApiUrlInput")
    def nerdgraph_api_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nerdgraphApiUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="syntheticsApiUrlInput")
    def synthetics_api_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syntheticsApiUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62cb5978e0543abed7330325717f572461c599332c9ed701a7fbe760490e19f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adminApiKey")
    def admin_api_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminApiKey"))

    @admin_api_key.setter
    def admin_api_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b686e270285be0fa40547ce9ded7c2bf2d9c7e6dadbcb2225db4762f0e3d4016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminApiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99365525565c5bbe6ec41320090e30534e9558b5a5ae27145e8811bf55414d95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4abcab955f695128a2c2b12147d863693d8146cab3677ac1e5f7ca611b00ffaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiUrl")
    def api_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiUrl"))

    @api_url.setter
    def api_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b011ab59ab84f9f182eafc3774840a5c488f4c3148a409628505c3e22a0ab1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacertFile")
    def cacert_file(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacertFile"))

    @cacert_file.setter
    def cacert_file(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e72e80e951be1e02a7737066031868a74dabedc29215208604dc81b3b067c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacertFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="infrastructureApiUrl")
    def infrastructure_api_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "infrastructureApiUrl"))

    @infrastructure_api_url.setter
    def infrastructure_api_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2dd5ce79512644b1fa0298541ee0b31d35578b8de8ed763c6fab1dfc35d259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructureApiUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insecureSkipVerify")
    def insecure_skip_verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureSkipVerify"))

    @insecure_skip_verify.setter
    def insecure_skip_verify(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31d49d1a491430f922ad084db858857aa783fbfe01e3a87e3b92b81f9ca62db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureSkipVerify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insightsInsertKey")
    def insights_insert_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsInsertKey"))

    @insights_insert_key.setter
    def insights_insert_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37de1118beaf4cc9793f0e35229c34a5271b9e4bebb5ea8ed5cd27dc308795a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsInsertKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insightsInsertUrl")
    def insights_insert_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsInsertUrl"))

    @insights_insert_url.setter
    def insights_insert_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c953e466cf4f971f6f55be103084cee82d61d23657cf6335a5d14a663fef676a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsInsertUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insightsQueryUrl")
    def insights_query_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsQueryUrl"))

    @insights_query_url.setter
    def insights_query_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70915b052de37eb8489ddedaf7ead739e943f24a785951ca155ca4ee04158154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsQueryUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nerdgraphApiUrl")
    def nerdgraph_api_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nerdgraphApiUrl"))

    @nerdgraph_api_url.setter
    def nerdgraph_api_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06bf2f30a937cfc1b3fac8a69ff79814dea87fbab8299081f1cb16abe33b423c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nerdgraphApiUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @region.setter
    def region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b8bcf327142567870ea9c941b96dce268c5e559499a929521f289f4aadc853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syntheticsApiUrl")
    def synthetics_api_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syntheticsApiUrl"))

    @synthetics_api_url.setter
    def synthetics_api_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2b93c6caf4e405cc9496486ed1546654c04036680ab1504392d708b461e7b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syntheticsApiUrl", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.provider.NewrelicProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "api_key": "apiKey",
        "admin_api_key": "adminApiKey",
        "alias": "alias",
        "api_url": "apiUrl",
        "cacert_file": "cacertFile",
        "infrastructure_api_url": "infrastructureApiUrl",
        "insecure_skip_verify": "insecureSkipVerify",
        "insights_insert_key": "insightsInsertKey",
        "insights_insert_url": "insightsInsertUrl",
        "insights_query_url": "insightsQueryUrl",
        "nerdgraph_api_url": "nerdgraphApiUrl",
        "region": "region",
        "synthetics_api_url": "syntheticsApiUrl",
    },
)
class NewrelicProviderConfig:
    def __init__(
        self,
        *,
        account_id: jsii.Number,
        api_key: builtins.str,
        admin_api_key: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        api_url: typing.Optional[builtins.str] = None,
        cacert_file: typing.Optional[builtins.str] = None,
        infrastructure_api_url: typing.Optional[builtins.str] = None,
        insecure_skip_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        insights_insert_key: typing.Optional[builtins.str] = None,
        insights_insert_url: typing.Optional[builtins.str] = None,
        insights_query_url: typing.Optional[builtins.str] = None,
        nerdgraph_api_url: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        synthetics_api_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#account_id NewrelicProvider#account_id}.
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#api_key NewrelicProvider#api_key}.
        :param admin_api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#admin_api_key NewrelicProvider#admin_api_key}.
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#alias NewrelicProvider#alias}
        :param api_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#api_url NewrelicProvider#api_url}.
        :param cacert_file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#cacert_file NewrelicProvider#cacert_file}.
        :param infrastructure_api_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#infrastructure_api_url NewrelicProvider#infrastructure_api_url}.
        :param insecure_skip_verify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#insecure_skip_verify NewrelicProvider#insecure_skip_verify}.
        :param insights_insert_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#insights_insert_key NewrelicProvider#insights_insert_key}.
        :param insights_insert_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#insights_insert_url NewrelicProvider#insights_insert_url}.
        :param insights_query_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#insights_query_url NewrelicProvider#insights_query_url}.
        :param nerdgraph_api_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#nerdgraph_api_url NewrelicProvider#nerdgraph_api_url}.
        :param region: The data center for which your New Relic account is configured. Only one region per provider block is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#region NewrelicProvider#region}
        :param synthetics_api_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#synthetics_api_url NewrelicProvider#synthetics_api_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a75853fe83269a9b7f75343771859bada06ccf5431d89b2f4e22ae38d4508b9)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument admin_api_key", value=admin_api_key, expected_type=type_hints["admin_api_key"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument api_url", value=api_url, expected_type=type_hints["api_url"])
            check_type(argname="argument cacert_file", value=cacert_file, expected_type=type_hints["cacert_file"])
            check_type(argname="argument infrastructure_api_url", value=infrastructure_api_url, expected_type=type_hints["infrastructure_api_url"])
            check_type(argname="argument insecure_skip_verify", value=insecure_skip_verify, expected_type=type_hints["insecure_skip_verify"])
            check_type(argname="argument insights_insert_key", value=insights_insert_key, expected_type=type_hints["insights_insert_key"])
            check_type(argname="argument insights_insert_url", value=insights_insert_url, expected_type=type_hints["insights_insert_url"])
            check_type(argname="argument insights_query_url", value=insights_query_url, expected_type=type_hints["insights_query_url"])
            check_type(argname="argument nerdgraph_api_url", value=nerdgraph_api_url, expected_type=type_hints["nerdgraph_api_url"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument synthetics_api_url", value=synthetics_api_url, expected_type=type_hints["synthetics_api_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "api_key": api_key,
        }
        if admin_api_key is not None:
            self._values["admin_api_key"] = admin_api_key
        if alias is not None:
            self._values["alias"] = alias
        if api_url is not None:
            self._values["api_url"] = api_url
        if cacert_file is not None:
            self._values["cacert_file"] = cacert_file
        if infrastructure_api_url is not None:
            self._values["infrastructure_api_url"] = infrastructure_api_url
        if insecure_skip_verify is not None:
            self._values["insecure_skip_verify"] = insecure_skip_verify
        if insights_insert_key is not None:
            self._values["insights_insert_key"] = insights_insert_key
        if insights_insert_url is not None:
            self._values["insights_insert_url"] = insights_insert_url
        if insights_query_url is not None:
            self._values["insights_query_url"] = insights_query_url
        if nerdgraph_api_url is not None:
            self._values["nerdgraph_api_url"] = nerdgraph_api_url
        if region is not None:
            self._values["region"] = region
        if synthetics_api_url is not None:
            self._values["synthetics_api_url"] = synthetics_api_url

    @builtins.property
    def account_id(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#account_id NewrelicProvider#account_id}.'''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def api_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#api_key NewrelicProvider#api_key}.'''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_api_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#admin_api_key NewrelicProvider#admin_api_key}.'''
        result = self._values.get("admin_api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#alias NewrelicProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#api_url NewrelicProvider#api_url}.'''
        result = self._values.get("api_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cacert_file(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#cacert_file NewrelicProvider#cacert_file}.'''
        result = self._values.get("cacert_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def infrastructure_api_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#infrastructure_api_url NewrelicProvider#infrastructure_api_url}.'''
        result = self._values.get("infrastructure_api_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure_skip_verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#insecure_skip_verify NewrelicProvider#insecure_skip_verify}.'''
        result = self._values.get("insecure_skip_verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def insights_insert_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#insights_insert_key NewrelicProvider#insights_insert_key}.'''
        result = self._values.get("insights_insert_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insights_insert_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#insights_insert_url NewrelicProvider#insights_insert_url}.'''
        result = self._values.get("insights_insert_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insights_query_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#insights_query_url NewrelicProvider#insights_query_url}.'''
        result = self._values.get("insights_query_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nerdgraph_api_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#nerdgraph_api_url NewrelicProvider#nerdgraph_api_url}.'''
        result = self._values.get("nerdgraph_api_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The data center for which your New Relic account is configured. Only one region per provider block is permitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#region NewrelicProvider#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthetics_api_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs#synthetics_api_url NewrelicProvider#synthetics_api_url}.'''
        result = self._values.get("synthetics_api_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NewrelicProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NewrelicProvider",
    "NewrelicProviderConfig",
]

publication.publish()

def _typecheckingstub__2afa037631c2b6bae79191bb584dd1a23c1c2764f77ff94450c3708f8ed37e50(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account_id: jsii.Number,
    api_key: builtins.str,
    admin_api_key: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    api_url: typing.Optional[builtins.str] = None,
    cacert_file: typing.Optional[builtins.str] = None,
    infrastructure_api_url: typing.Optional[builtins.str] = None,
    insecure_skip_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    insights_insert_key: typing.Optional[builtins.str] = None,
    insights_insert_url: typing.Optional[builtins.str] = None,
    insights_query_url: typing.Optional[builtins.str] = None,
    nerdgraph_api_url: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    synthetics_api_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122b13451c31fda4c1a14628cc32b6148317d3868f10170cf9305570c14afe13(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62cb5978e0543abed7330325717f572461c599332c9ed701a7fbe760490e19f3(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b686e270285be0fa40547ce9ded7c2bf2d9c7e6dadbcb2225db4762f0e3d4016(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99365525565c5bbe6ec41320090e30534e9558b5a5ae27145e8811bf55414d95(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abcab955f695128a2c2b12147d863693d8146cab3677ac1e5f7ca611b00ffaa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b011ab59ab84f9f182eafc3774840a5c488f4c3148a409628505c3e22a0ab1e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e72e80e951be1e02a7737066031868a74dabedc29215208604dc81b3b067c2f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2dd5ce79512644b1fa0298541ee0b31d35578b8de8ed763c6fab1dfc35d259(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d49d1a491430f922ad084db858857aa783fbfe01e3a87e3b92b81f9ca62db6(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37de1118beaf4cc9793f0e35229c34a5271b9e4bebb5ea8ed5cd27dc308795a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c953e466cf4f971f6f55be103084cee82d61d23657cf6335a5d14a663fef676a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70915b052de37eb8489ddedaf7ead739e943f24a785951ca155ca4ee04158154(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06bf2f30a937cfc1b3fac8a69ff79814dea87fbab8299081f1cb16abe33b423c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b8bcf327142567870ea9c941b96dce268c5e559499a929521f289f4aadc853(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2b93c6caf4e405cc9496486ed1546654c04036680ab1504392d708b461e7b8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a75853fe83269a9b7f75343771859bada06ccf5431d89b2f4e22ae38d4508b9(
    *,
    account_id: jsii.Number,
    api_key: builtins.str,
    admin_api_key: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    api_url: typing.Optional[builtins.str] = None,
    cacert_file: typing.Optional[builtins.str] = None,
    infrastructure_api_url: typing.Optional[builtins.str] = None,
    insecure_skip_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    insights_insert_key: typing.Optional[builtins.str] = None,
    insights_insert_url: typing.Optional[builtins.str] = None,
    insights_query_url: typing.Optional[builtins.str] = None,
    nerdgraph_api_url: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    synthetics_api_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
