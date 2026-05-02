r'''
# `datadog_aws_cur_config`

Refer to the Terraform Registry for docs: [`datadog_aws_cur_config`](https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config).
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


class AwsCurConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.awsCurConfig.AwsCurConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config datadog_aws_cur_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account_id: builtins.str,
        bucket_name: builtins.str,
        report_name: builtins.str,
        report_prefix: builtins.str,
        account_filters: typing.Optional[typing.Union["AwsCurConfigAccountFilters", typing.Dict[builtins.str, typing.Any]]] = None,
        bucket_region: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config datadog_aws_cur_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The AWS account ID of your billing/payer account. For AWS Organizations, this is typically the management account ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#account_id AwsCurConfig#account_id}
        :param bucket_name: The S3 bucket name where your AWS Cost and Usage Report files are stored. This bucket must have appropriate IAM permissions for Datadog access and should be in the same AWS account as the CUR report. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#bucket_name AwsCurConfig#bucket_name}
        :param report_name: The exact name of your AWS Cost and Usage Report as configured in AWS Billing preferences. This must match the report name exactly as it appears in your AWS billing settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#report_name AwsCurConfig#report_name}
        :param report_prefix: The S3 key prefix where your Cost and Usage Report files are stored within the bucket (e.g., 'cur-reports/', 'billing/cur/'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#report_prefix AwsCurConfig#report_prefix}
        :param account_filters: account_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#account_filters AwsCurConfig#account_filters}
        :param bucket_region: The AWS region where the S3 bucket containing your Cost and Usage Report is located (e.g., us-east-1, eu-west-1). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#bucket_region AwsCurConfig#bucket_region}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45086d9d5c0ae639eedf87c22bf7f5d4bc6dd4f26e193a1aeedaac5b8c50f8e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = AwsCurConfigConfig(
            account_id=account_id,
            bucket_name=bucket_name,
            report_name=report_name,
            report_prefix=report_prefix,
            account_filters=account_filters,
            bucket_region=bucket_region,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
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
        '''Generates CDKTF code for importing a AwsCurConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AwsCurConfig to import.
        :param import_from_id: The id of the existing AwsCurConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AwsCurConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0988e83f824b1b313a040df5e84cde26ed49f45065a27b5c38d4a98f47a55838)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccountFilters")
    def put_account_filters(
        self,
        *,
        excluded_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_new_accounts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param excluded_accounts: List of AWS account IDs to exclude from cost analysis. Only used when ``include_new_accounts`` is ``true``. Cannot be used together with ``included_accounts``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#excluded_accounts AwsCurConfig#excluded_accounts}
        :param included_accounts: List of AWS account IDs to include in cost analysis. Only used when ``include_new_accounts`` is ``false``. Cannot be used together with ``excluded_accounts``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#included_accounts AwsCurConfig#included_accounts}
        :param include_new_accounts: Whether to automatically include new member accounts in your cost analysis. When ``true``, use ``excluded_accounts`` to specify accounts to exclude. When ``false``, use ``included_accounts`` to specify only the accounts to include. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#include_new_accounts AwsCurConfig#include_new_accounts}
        '''
        value = AwsCurConfigAccountFilters(
            excluded_accounts=excluded_accounts,
            included_accounts=included_accounts,
            include_new_accounts=include_new_accounts,
        )

        return typing.cast(None, jsii.invoke(self, "putAccountFilters", [value]))

    @jsii.member(jsii_name="resetAccountFilters")
    def reset_account_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountFilters", []))

    @jsii.member(jsii_name="resetBucketRegion")
    def reset_bucket_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketRegion", []))

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
    @jsii.member(jsii_name="accountFilters")
    def account_filters(self) -> "AwsCurConfigAccountFiltersOutputReference":
        return typing.cast("AwsCurConfigAccountFiltersOutputReference", jsii.get(self, "accountFilters"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="errorMessages")
    def error_messages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "errorMessages"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="statusUpdatedAt")
    def status_updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="accountFiltersInput")
    def account_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AwsCurConfigAccountFilters"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AwsCurConfigAccountFilters"]], jsii.get(self, "accountFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketRegionInput")
    def bucket_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="reportNameInput")
    def report_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reportNameInput"))

    @builtins.property
    @jsii.member(jsii_name="reportPrefixInput")
    def report_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reportPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0838726ee11c886a4edd9cafb39de10551de479e383a08f579b0484ec144c807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e58e0c44000e797aa148bc614a275ca669c0c015f3ac93c821a764cf28773c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketRegion")
    def bucket_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketRegion"))

    @bucket_region.setter
    def bucket_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267086de28e50211549b56a5c2975fc4b5f8880fa9e0307f586f56d826199b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reportName")
    def report_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reportName"))

    @report_name.setter
    def report_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e19c3516987d60d2ce715594e76d841d1ba1a8a667a29071c2d8268d7b4e32d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reportPrefix")
    def report_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reportPrefix"))

    @report_prefix.setter
    def report_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be21558b030585cd8d6eb1e2438f533d32c5cdb60677ca21e59336638a1befd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportPrefix", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.awsCurConfig.AwsCurConfigAccountFilters",
    jsii_struct_bases=[],
    name_mapping={
        "excluded_accounts": "excludedAccounts",
        "included_accounts": "includedAccounts",
        "include_new_accounts": "includeNewAccounts",
    },
)
class AwsCurConfigAccountFilters:
    def __init__(
        self,
        *,
        excluded_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_new_accounts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param excluded_accounts: List of AWS account IDs to exclude from cost analysis. Only used when ``include_new_accounts`` is ``true``. Cannot be used together with ``included_accounts``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#excluded_accounts AwsCurConfig#excluded_accounts}
        :param included_accounts: List of AWS account IDs to include in cost analysis. Only used when ``include_new_accounts`` is ``false``. Cannot be used together with ``excluded_accounts``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#included_accounts AwsCurConfig#included_accounts}
        :param include_new_accounts: Whether to automatically include new member accounts in your cost analysis. When ``true``, use ``excluded_accounts`` to specify accounts to exclude. When ``false``, use ``included_accounts`` to specify only the accounts to include. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#include_new_accounts AwsCurConfig#include_new_accounts}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce89b0ac032dc9f8f29cc678d230f95892f2c7ea9b3e69ab23ba3364fc0d5c6)
            check_type(argname="argument excluded_accounts", value=excluded_accounts, expected_type=type_hints["excluded_accounts"])
            check_type(argname="argument included_accounts", value=included_accounts, expected_type=type_hints["included_accounts"])
            check_type(argname="argument include_new_accounts", value=include_new_accounts, expected_type=type_hints["include_new_accounts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excluded_accounts is not None:
            self._values["excluded_accounts"] = excluded_accounts
        if included_accounts is not None:
            self._values["included_accounts"] = included_accounts
        if include_new_accounts is not None:
            self._values["include_new_accounts"] = include_new_accounts

    @builtins.property
    def excluded_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of AWS account IDs to exclude from cost analysis.

        Only used when ``include_new_accounts`` is ``true``. Cannot be used together with ``included_accounts``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#excluded_accounts AwsCurConfig#excluded_accounts}
        '''
        result = self._values.get("excluded_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of AWS account IDs to include in cost analysis.

        Only used when ``include_new_accounts`` is ``false``. Cannot be used together with ``excluded_accounts``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#included_accounts AwsCurConfig#included_accounts}
        '''
        result = self._values.get("included_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_new_accounts(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to automatically include new member accounts in your cost analysis.

        When ``true``, use ``excluded_accounts`` to specify accounts to exclude. When ``false``, use ``included_accounts`` to specify only the accounts to include.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#include_new_accounts AwsCurConfig#include_new_accounts}
        '''
        result = self._values.get("include_new_accounts")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCurConfigAccountFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsCurConfigAccountFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.awsCurConfig.AwsCurConfigAccountFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c2799b8fc64207e3b1b2c216ff18e1c34d6c00c24a69005630999d07d1fa32d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludedAccounts")
    def reset_excluded_accounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedAccounts", []))

    @jsii.member(jsii_name="resetIncludedAccounts")
    def reset_included_accounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedAccounts", []))

    @jsii.member(jsii_name="resetIncludeNewAccounts")
    def reset_include_new_accounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeNewAccounts", []))

    @builtins.property
    @jsii.member(jsii_name="excludedAccountsInput")
    def excluded_accounts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedAccountsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedAccountsInput")
    def included_accounts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedAccountsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeNewAccountsInput")
    def include_new_accounts_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeNewAccountsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedAccounts")
    def excluded_accounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedAccounts"))

    @excluded_accounts.setter
    def excluded_accounts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef0a4afb717f3994914b4661f3c482b1064f7e9339286f6ac888fc86d6e0b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedAccounts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedAccounts")
    def included_accounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedAccounts"))

    @included_accounts.setter
    def included_accounts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a20a5eca50fbcc252105bf8005aed265080b972856e9dbbb66b9c9e1146bf83f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedAccounts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeNewAccounts")
    def include_new_accounts(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeNewAccounts"))

    @include_new_accounts.setter
    def include_new_accounts(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ea3a1ef1224fc94631b52c57fa8aee47a3b11ef52fa702dd37dea1d7640d87a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeNewAccounts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AwsCurConfigAccountFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AwsCurConfigAccountFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AwsCurConfigAccountFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce72d62ad2b84e0e3c0b121ccd97f4b0f7ec907861f98dbc1f84da0ab4b8d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.awsCurConfig.AwsCurConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_id": "accountId",
        "bucket_name": "bucketName",
        "report_name": "reportName",
        "report_prefix": "reportPrefix",
        "account_filters": "accountFilters",
        "bucket_region": "bucketRegion",
    },
)
class AwsCurConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_id: builtins.str,
        bucket_name: builtins.str,
        report_name: builtins.str,
        report_prefix: builtins.str,
        account_filters: typing.Optional[typing.Union[AwsCurConfigAccountFilters, typing.Dict[builtins.str, typing.Any]]] = None,
        bucket_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The AWS account ID of your billing/payer account. For AWS Organizations, this is typically the management account ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#account_id AwsCurConfig#account_id}
        :param bucket_name: The S3 bucket name where your AWS Cost and Usage Report files are stored. This bucket must have appropriate IAM permissions for Datadog access and should be in the same AWS account as the CUR report. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#bucket_name AwsCurConfig#bucket_name}
        :param report_name: The exact name of your AWS Cost and Usage Report as configured in AWS Billing preferences. This must match the report name exactly as it appears in your AWS billing settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#report_name AwsCurConfig#report_name}
        :param report_prefix: The S3 key prefix where your Cost and Usage Report files are stored within the bucket (e.g., 'cur-reports/', 'billing/cur/'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#report_prefix AwsCurConfig#report_prefix}
        :param account_filters: account_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#account_filters AwsCurConfig#account_filters}
        :param bucket_region: The AWS region where the S3 bucket containing your Cost and Usage Report is located (e.g., us-east-1, eu-west-1). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#bucket_region AwsCurConfig#bucket_region}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(account_filters, dict):
            account_filters = AwsCurConfigAccountFilters(**account_filters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a316c9c455b669886b1a92b2fa31dddf3ef40455e2b94b69f324166db72fadc3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument report_name", value=report_name, expected_type=type_hints["report_name"])
            check_type(argname="argument report_prefix", value=report_prefix, expected_type=type_hints["report_prefix"])
            check_type(argname="argument account_filters", value=account_filters, expected_type=type_hints["account_filters"])
            check_type(argname="argument bucket_region", value=bucket_region, expected_type=type_hints["bucket_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "bucket_name": bucket_name,
            "report_name": report_name,
            "report_prefix": report_prefix,
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
        if account_filters is not None:
            self._values["account_filters"] = account_filters
        if bucket_region is not None:
            self._values["bucket_region"] = bucket_region

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
    def account_id(self) -> builtins.str:
        '''The AWS account ID of your billing/payer account. For AWS Organizations, this is typically the management account ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#account_id AwsCurConfig#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''The S3 bucket name where your AWS Cost and Usage Report files are stored.

        This bucket must have appropriate IAM permissions for Datadog access and should be in the same AWS account as the CUR report.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#bucket_name AwsCurConfig#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def report_name(self) -> builtins.str:
        '''The exact name of your AWS Cost and Usage Report as configured in AWS Billing preferences.

        This must match the report name exactly as it appears in your AWS billing settings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#report_name AwsCurConfig#report_name}
        '''
        result = self._values.get("report_name")
        assert result is not None, "Required property 'report_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def report_prefix(self) -> builtins.str:
        '''The S3 key prefix where your Cost and Usage Report files are stored within the bucket (e.g., 'cur-reports/', 'billing/cur/').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#report_prefix AwsCurConfig#report_prefix}
        '''
        result = self._values.get("report_prefix")
        assert result is not None, "Required property 'report_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_filters(self) -> typing.Optional[AwsCurConfigAccountFilters]:
        '''account_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#account_filters AwsCurConfig#account_filters}
        '''
        result = self._values.get("account_filters")
        return typing.cast(typing.Optional[AwsCurConfigAccountFilters], result)

    @builtins.property
    def bucket_region(self) -> typing.Optional[builtins.str]:
        '''The AWS region where the S3 bucket containing your Cost and Usage Report is located (e.g., us-east-1, eu-west-1).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/aws_cur_config#bucket_region AwsCurConfig#bucket_region}
        '''
        result = self._values.get("bucket_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCurConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsCurConfig",
    "AwsCurConfigAccountFilters",
    "AwsCurConfigAccountFiltersOutputReference",
    "AwsCurConfigConfig",
]

publication.publish()

def _typecheckingstub__45086d9d5c0ae639eedf87c22bf7f5d4bc6dd4f26e193a1aeedaac5b8c50f8e9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account_id: builtins.str,
    bucket_name: builtins.str,
    report_name: builtins.str,
    report_prefix: builtins.str,
    account_filters: typing.Optional[typing.Union[AwsCurConfigAccountFilters, typing.Dict[builtins.str, typing.Any]]] = None,
    bucket_region: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__0988e83f824b1b313a040df5e84cde26ed49f45065a27b5c38d4a98f47a55838(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0838726ee11c886a4edd9cafb39de10551de479e383a08f579b0484ec144c807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e58e0c44000e797aa148bc614a275ca669c0c015f3ac93c821a764cf28773c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267086de28e50211549b56a5c2975fc4b5f8880fa9e0307f586f56d826199b19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19c3516987d60d2ce715594e76d841d1ba1a8a667a29071c2d8268d7b4e32d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be21558b030585cd8d6eb1e2438f533d32c5cdb60677ca21e59336638a1befd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce89b0ac032dc9f8f29cc678d230f95892f2c7ea9b3e69ab23ba3364fc0d5c6(
    *,
    excluded_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_new_accounts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2799b8fc64207e3b1b2c216ff18e1c34d6c00c24a69005630999d07d1fa32d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef0a4afb717f3994914b4661f3c482b1064f7e9339286f6ac888fc86d6e0b2b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20a5eca50fbcc252105bf8005aed265080b972856e9dbbb66b9c9e1146bf83f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea3a1ef1224fc94631b52c57fa8aee47a3b11ef52fa702dd37dea1d7640d87a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce72d62ad2b84e0e3c0b121ccd97f4b0f7ec907861f98dbc1f84da0ab4b8d96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AwsCurConfigAccountFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a316c9c455b669886b1a92b2fa31dddf3ef40455e2b94b69f324166db72fadc3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    bucket_name: builtins.str,
    report_name: builtins.str,
    report_prefix: builtins.str,
    account_filters: typing.Optional[typing.Union[AwsCurConfigAccountFilters, typing.Dict[builtins.str, typing.Any]]] = None,
    bucket_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
