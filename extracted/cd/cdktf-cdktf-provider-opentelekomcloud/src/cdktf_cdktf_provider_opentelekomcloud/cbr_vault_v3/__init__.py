r'''
# `opentelekomcloud_cbr_vault_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_cbr_vault_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3).
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


class CbrVaultV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3 opentelekomcloud_cbr_vault_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        billing: typing.Union["CbrVaultV3Billing", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        auto_bind: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_expand: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backup_policy_id: typing.Optional[builtins.str] = None,
        bind_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CbrVaultV3BindRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enterprise_project_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CbrVaultV3Resource", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3 opentelekomcloud_cbr_vault_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param billing: billing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#billing CbrVaultV3#billing}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#name CbrVaultV3#name}.
        :param auto_bind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#auto_bind CbrVaultV3#auto_bind}.
        :param auto_expand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#auto_expand CbrVaultV3#auto_expand}.
        :param backup_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#backup_policy_id CbrVaultV3#backup_policy_id}.
        :param bind_rules: bind_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#bind_rules CbrVaultV3#bind_rules}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#description CbrVaultV3#description}.
        :param enterprise_project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#enterprise_project_id CbrVaultV3#enterprise_project_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#id CbrVaultV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param locked: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#locked CbrVaultV3#locked}.
        :param resource: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#resource CbrVaultV3#resource}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#tags CbrVaultV3#tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c52a02ce2cd36873fdd7fe976ebacf6804c138432d9c378f2ef5484e7c6a9e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CbrVaultV3Config(
            billing=billing,
            name=name,
            auto_bind=auto_bind,
            auto_expand=auto_expand,
            backup_policy_id=backup_policy_id,
            bind_rules=bind_rules,
            description=description,
            enterprise_project_id=enterprise_project_id,
            id=id,
            locked=locked,
            resource=resource,
            tags=tags,
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
        '''Generates CDKTF code for importing a CbrVaultV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CbrVaultV3 to import.
        :param import_from_id: The id of the existing CbrVaultV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CbrVaultV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bec3c691c9701d2808fa1831bcae3be77b7e05a53362bf641668e92dba2b435)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBilling")
    def put_billing(
        self,
        *,
        object_type: builtins.str,
        protect_type: builtins.str,
        size: jsii.Number,
        charging_mode: typing.Optional[builtins.str] = None,
        cloud_type: typing.Optional[builtins.str] = None,
        consistent_level: typing.Optional[builtins.str] = None,
        console_url: typing.Optional[builtins.str] = None,
        extra_info: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_auto_pay: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_auto_renew: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        period_num: typing.Optional[jsii.Number] = None,
        period_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#object_type CbrVaultV3#object_type}.
        :param protect_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#protect_type CbrVaultV3#protect_type}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#size CbrVaultV3#size}.
        :param charging_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#charging_mode CbrVaultV3#charging_mode}.
        :param cloud_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#cloud_type CbrVaultV3#cloud_type}.
        :param consistent_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#consistent_level CbrVaultV3#consistent_level}.
        :param console_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#console_url CbrVaultV3#console_url}.
        :param extra_info: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#extra_info CbrVaultV3#extra_info}.
        :param is_auto_pay: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#is_auto_pay CbrVaultV3#is_auto_pay}.
        :param is_auto_renew: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#is_auto_renew CbrVaultV3#is_auto_renew}.
        :param period_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#period_num CbrVaultV3#period_num}.
        :param period_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#period_type CbrVaultV3#period_type}.
        '''
        value = CbrVaultV3Billing(
            object_type=object_type,
            protect_type=protect_type,
            size=size,
            charging_mode=charging_mode,
            cloud_type=cloud_type,
            consistent_level=consistent_level,
            console_url=console_url,
            extra_info=extra_info,
            is_auto_pay=is_auto_pay,
            is_auto_renew=is_auto_renew,
            period_num=period_num,
            period_type=period_type,
        )

        return typing.cast(None, jsii.invoke(self, "putBilling", [value]))

    @jsii.member(jsii_name="putBindRules")
    def put_bind_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CbrVaultV3BindRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45b8b735c76d971ddd4c4dbfaeba8af7ef6ebc3ff0c435d5958c18873e2b861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBindRules", [value]))

    @jsii.member(jsii_name="putResource")
    def put_resource(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CbrVaultV3Resource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207b808cfc8768b057dee2e90761ef569734c39b4547a99d7efcb7476aac3cbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResource", [value]))

    @jsii.member(jsii_name="resetAutoBind")
    def reset_auto_bind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoBind", []))

    @jsii.member(jsii_name="resetAutoExpand")
    def reset_auto_expand(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoExpand", []))

    @jsii.member(jsii_name="resetBackupPolicyId")
    def reset_backup_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupPolicyId", []))

    @jsii.member(jsii_name="resetBindRules")
    def reset_bind_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBindRules", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnterpriseProjectId")
    def reset_enterprise_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnterpriseProjectId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocked")
    def reset_locked(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocked", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="billing")
    def billing(self) -> "CbrVaultV3BillingOutputReference":
        return typing.cast("CbrVaultV3BillingOutputReference", jsii.get(self, "billing"))

    @builtins.property
    @jsii.member(jsii_name="bindRules")
    def bind_rules(self) -> "CbrVaultV3BindRulesList":
        return typing.cast("CbrVaultV3BindRulesList", jsii.get(self, "bindRules"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="providerId")
    def provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerId"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> "CbrVaultV3ResourceList":
        return typing.cast("CbrVaultV3ResourceList", jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @builtins.property
    @jsii.member(jsii_name="autoBindInput")
    def auto_bind_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoBindInput"))

    @builtins.property
    @jsii.member(jsii_name="autoExpandInput")
    def auto_expand_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoExpandInput"))

    @builtins.property
    @jsii.member(jsii_name="backupPolicyIdInput")
    def backup_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="billingInput")
    def billing_input(self) -> typing.Optional["CbrVaultV3Billing"]:
        return typing.cast(typing.Optional["CbrVaultV3Billing"], jsii.get(self, "billingInput"))

    @builtins.property
    @jsii.member(jsii_name="bindRulesInput")
    def bind_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CbrVaultV3BindRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CbrVaultV3BindRules"]]], jsii.get(self, "bindRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseProjectIdInput")
    def enterprise_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enterpriseProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lockedInput")
    def locked_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lockedInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CbrVaultV3Resource"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CbrVaultV3Resource"]]], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoBind")
    def auto_bind(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoBind"))

    @auto_bind.setter
    def auto_bind(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ac3173c9dc4ae781a3f2999beaa01b13bc8bfd4b5116fcf35676a909f43d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoBind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoExpand")
    def auto_expand(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoExpand"))

    @auto_expand.setter
    def auto_expand(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c7ad7f4b730c67d54f62ed5b865856be40a828a73e668ae4a3dcdbb7e97e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoExpand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupPolicyId")
    def backup_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupPolicyId"))

    @backup_policy_id.setter
    def backup_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6658a4dcebcd79c9f5f0e18c0a66117c4fc41f4b091e396922589f6ab849b4ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5826c8adb45d257b29964be4fc852bfa9d5dca6d3fbe3e51deddef0719d8b534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enterpriseProjectId")
    def enterprise_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enterpriseProjectId"))

    @enterprise_project_id.setter
    def enterprise_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ff61fb3084f817aaa0281a33bfcb079cc7ec98aa82a03ade798b17612b5ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterpriseProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e522456083bb3b30a611946a4102217eb143edf81601794b39f55c76a773e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locked")
    def locked(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "locked"))

    @locked.setter
    def locked(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c3e0285a3b1075e48dc6798e1869e293a70368f1aad3ef44dc7527d5441b0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locked", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97688582bedf91bb028d159526a3e59752f250e1865d38a05a4634c4fb6d6262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c5e737ad846c45356685215de2570e0da79b5c78722e3e8f416e12f9d35a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3Billing",
    jsii_struct_bases=[],
    name_mapping={
        "object_type": "objectType",
        "protect_type": "protectType",
        "size": "size",
        "charging_mode": "chargingMode",
        "cloud_type": "cloudType",
        "consistent_level": "consistentLevel",
        "console_url": "consoleUrl",
        "extra_info": "extraInfo",
        "is_auto_pay": "isAutoPay",
        "is_auto_renew": "isAutoRenew",
        "period_num": "periodNum",
        "period_type": "periodType",
    },
)
class CbrVaultV3Billing:
    def __init__(
        self,
        *,
        object_type: builtins.str,
        protect_type: builtins.str,
        size: jsii.Number,
        charging_mode: typing.Optional[builtins.str] = None,
        cloud_type: typing.Optional[builtins.str] = None,
        consistent_level: typing.Optional[builtins.str] = None,
        console_url: typing.Optional[builtins.str] = None,
        extra_info: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_auto_pay: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_auto_renew: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        period_num: typing.Optional[jsii.Number] = None,
        period_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#object_type CbrVaultV3#object_type}.
        :param protect_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#protect_type CbrVaultV3#protect_type}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#size CbrVaultV3#size}.
        :param charging_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#charging_mode CbrVaultV3#charging_mode}.
        :param cloud_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#cloud_type CbrVaultV3#cloud_type}.
        :param consistent_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#consistent_level CbrVaultV3#consistent_level}.
        :param console_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#console_url CbrVaultV3#console_url}.
        :param extra_info: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#extra_info CbrVaultV3#extra_info}.
        :param is_auto_pay: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#is_auto_pay CbrVaultV3#is_auto_pay}.
        :param is_auto_renew: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#is_auto_renew CbrVaultV3#is_auto_renew}.
        :param period_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#period_num CbrVaultV3#period_num}.
        :param period_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#period_type CbrVaultV3#period_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa15f27a51fb6b7d6704d362243232d647ce278bd1b8064d9a7e088dd02ba52e)
            check_type(argname="argument object_type", value=object_type, expected_type=type_hints["object_type"])
            check_type(argname="argument protect_type", value=protect_type, expected_type=type_hints["protect_type"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument charging_mode", value=charging_mode, expected_type=type_hints["charging_mode"])
            check_type(argname="argument cloud_type", value=cloud_type, expected_type=type_hints["cloud_type"])
            check_type(argname="argument consistent_level", value=consistent_level, expected_type=type_hints["consistent_level"])
            check_type(argname="argument console_url", value=console_url, expected_type=type_hints["console_url"])
            check_type(argname="argument extra_info", value=extra_info, expected_type=type_hints["extra_info"])
            check_type(argname="argument is_auto_pay", value=is_auto_pay, expected_type=type_hints["is_auto_pay"])
            check_type(argname="argument is_auto_renew", value=is_auto_renew, expected_type=type_hints["is_auto_renew"])
            check_type(argname="argument period_num", value=period_num, expected_type=type_hints["period_num"])
            check_type(argname="argument period_type", value=period_type, expected_type=type_hints["period_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_type": object_type,
            "protect_type": protect_type,
            "size": size,
        }
        if charging_mode is not None:
            self._values["charging_mode"] = charging_mode
        if cloud_type is not None:
            self._values["cloud_type"] = cloud_type
        if consistent_level is not None:
            self._values["consistent_level"] = consistent_level
        if console_url is not None:
            self._values["console_url"] = console_url
        if extra_info is not None:
            self._values["extra_info"] = extra_info
        if is_auto_pay is not None:
            self._values["is_auto_pay"] = is_auto_pay
        if is_auto_renew is not None:
            self._values["is_auto_renew"] = is_auto_renew
        if period_num is not None:
            self._values["period_num"] = period_num
        if period_type is not None:
            self._values["period_type"] = period_type

    @builtins.property
    def object_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#object_type CbrVaultV3#object_type}.'''
        result = self._values.get("object_type")
        assert result is not None, "Required property 'object_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protect_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#protect_type CbrVaultV3#protect_type}.'''
        result = self._values.get("protect_type")
        assert result is not None, "Required property 'protect_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#size CbrVaultV3#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def charging_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#charging_mode CbrVaultV3#charging_mode}.'''
        result = self._values.get("charging_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#cloud_type CbrVaultV3#cloud_type}.'''
        result = self._values.get("cloud_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consistent_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#consistent_level CbrVaultV3#consistent_level}.'''
        result = self._values.get("consistent_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def console_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#console_url CbrVaultV3#console_url}.'''
        result = self._values.get("console_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_info(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#extra_info CbrVaultV3#extra_info}.'''
        result = self._values.get("extra_info")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def is_auto_pay(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#is_auto_pay CbrVaultV3#is_auto_pay}.'''
        result = self._values.get("is_auto_pay")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_auto_renew(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#is_auto_renew CbrVaultV3#is_auto_renew}.'''
        result = self._values.get("is_auto_renew")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def period_num(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#period_num CbrVaultV3#period_num}.'''
        result = self._values.get("period_num")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#period_type CbrVaultV3#period_type}.'''
        result = self._values.get("period_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CbrVaultV3Billing(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CbrVaultV3BillingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3BillingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27e883b35fbd9f5d81b6bf7caee3fdfab7fccd01feb2f248cff66028aeb1cc27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetChargingMode")
    def reset_charging_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChargingMode", []))

    @jsii.member(jsii_name="resetCloudType")
    def reset_cloud_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudType", []))

    @jsii.member(jsii_name="resetConsistentLevel")
    def reset_consistent_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsistentLevel", []))

    @jsii.member(jsii_name="resetConsoleUrl")
    def reset_console_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsoleUrl", []))

    @jsii.member(jsii_name="resetExtraInfo")
    def reset_extra_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraInfo", []))

    @jsii.member(jsii_name="resetIsAutoPay")
    def reset_is_auto_pay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsAutoPay", []))

    @jsii.member(jsii_name="resetIsAutoRenew")
    def reset_is_auto_renew(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsAutoRenew", []))

    @jsii.member(jsii_name="resetPeriodNum")
    def reset_period_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodNum", []))

    @jsii.member(jsii_name="resetPeriodType")
    def reset_period_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodType", []))

    @builtins.property
    @jsii.member(jsii_name="allocated")
    def allocated(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocated"))

    @builtins.property
    @jsii.member(jsii_name="frozenScene")
    def frozen_scene(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frozenScene"))

    @builtins.property
    @jsii.member(jsii_name="orderId")
    def order_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orderId"))

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @builtins.property
    @jsii.member(jsii_name="specCode")
    def spec_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "specCode"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="storageUnit")
    def storage_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageUnit"))

    @builtins.property
    @jsii.member(jsii_name="used")
    def used(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "used"))

    @builtins.property
    @jsii.member(jsii_name="chargingModeInput")
    def charging_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chargingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudTypeInput")
    def cloud_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="consistentLevelInput")
    def consistent_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consistentLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="consoleUrlInput")
    def console_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consoleUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="extraInfoInput")
    def extra_info_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extraInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="isAutoPayInput")
    def is_auto_pay_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isAutoPayInput"))

    @builtins.property
    @jsii.member(jsii_name="isAutoRenewInput")
    def is_auto_renew_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isAutoRenewInput"))

    @builtins.property
    @jsii.member(jsii_name="objectTypeInput")
    def object_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="periodNumInput")
    def period_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodNumInput"))

    @builtins.property
    @jsii.member(jsii_name="periodTypeInput")
    def period_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="protectTypeInput")
    def protect_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="chargingMode")
    def charging_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chargingMode"))

    @charging_mode.setter
    def charging_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bcb79cbce684113d9879c7239e71cdcef0a77aedc499f4e638b1afeb4a82ea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chargingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudType")
    def cloud_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudType"))

    @cloud_type.setter
    def cloud_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02bc02ce85cda981abfbe381da5e4e46d83910a6b4d5280d2dec53a3bdd950d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consistentLevel")
    def consistent_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consistentLevel"))

    @consistent_level.setter
    def consistent_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b37c0092663717ea8a74f38f9ba4474beaa116a40ed2135ac86149ec22e36b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consistentLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consoleUrl")
    def console_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consoleUrl"))

    @console_url.setter
    def console_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3956dfa9b1a0aaf4723f7bf3e11dbc4e96038ee9c1822c909775e830ef139675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consoleUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extraInfo")
    def extra_info(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "extraInfo"))

    @extra_info.setter
    def extra_info(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c6f7d25d253711f8e42825a59c0d9b8d65016054a8c8a6c9260428033878a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraInfo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isAutoPay")
    def is_auto_pay(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isAutoPay"))

    @is_auto_pay.setter
    def is_auto_pay(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce53401006d5ef765cb6eea646ab1cd936fd90eb8b71cdd6f04c124da6ba8ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isAutoPay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isAutoRenew")
    def is_auto_renew(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isAutoRenew"))

    @is_auto_renew.setter
    def is_auto_renew(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d6014a497909bab85b41ab32fe21fd17fa2b1db9e1054f1d21a48f36138048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isAutoRenew", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectType")
    def object_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectType"))

    @object_type.setter
    def object_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0451daecd4baa5f737884ee2101364a78973d5ec4e52eaad9d8faec1fb264142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodNum")
    def period_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodNum"))

    @period_num.setter
    def period_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c51b3b350d1bc0aeb7d85d2874e7f26baffbbb43156227e5b4bb7b5705f0d81a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodType")
    def period_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "periodType"))

    @period_type.setter
    def period_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7296e4aa32c9d0da602b12599bed3c80cd681ef6a7baf2bdf7db7aeaf1d5804c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protectType")
    def protect_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectType"))

    @protect_type.setter
    def protect_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40eeec3bf6223bec4408c593c204e539e4990af5aaff37e74b36593aad420d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3ea5a234792d70a8c45765e154c28e5711eac1b210f46d844395346d2fae67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CbrVaultV3Billing]:
        return typing.cast(typing.Optional[CbrVaultV3Billing], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CbrVaultV3Billing]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014ad0aa438aa1132ebec36a22ff4f9ae991584c4b5362aaab96d7d7c29b1611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3BindRules",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class CbrVaultV3BindRules:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#key CbrVaultV3#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#value CbrVaultV3#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f905291637465e15585557c94cad534c404756b750be4e2c562dff54eb4830)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#key CbrVaultV3#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#value CbrVaultV3#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CbrVaultV3BindRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CbrVaultV3BindRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3BindRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db34c9d5a1aff8c2b26d66bef61864477a10871e1c9bbfd064d81fe3f818ad8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CbrVaultV3BindRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f51bea9f78e4af7aeb6b9b08fc123bec1b1b93d48431b46e2b5e79aee1599fce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CbrVaultV3BindRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b50e6043534cb84d24ddf591b3be8bb4fac1b70a242ee49b17613bdfe0db53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0ba8223f7b86a1c7de84b6929d4db07ea42a0b9509c089853d5d75f8a65e149)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ebff16315f590a7ce1f826987044ad2ebd17fd522a08361b8164e4935627006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CbrVaultV3BindRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CbrVaultV3BindRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CbrVaultV3BindRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d44028c10bb490332305ada25a6eb5840e0463a322b3cfbb7aa937911599bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CbrVaultV3BindRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3BindRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4d67922749cbd6bae6fb3e7ea0b733bf004c0bc26e49446aae29e5aa9eafd62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb18e56b2aed1e57dd031968612430b4e9e164b895c80af624ce773b72bc52d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a0b02072482fdcd4f362ce01e62408fada85caa6a70376fdb227c130472b624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CbrVaultV3BindRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CbrVaultV3BindRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CbrVaultV3BindRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49279390e1a4176b205ff0a9796205fe7dc573e797fbc2a93268125f8cb938b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "billing": "billing",
        "name": "name",
        "auto_bind": "autoBind",
        "auto_expand": "autoExpand",
        "backup_policy_id": "backupPolicyId",
        "bind_rules": "bindRules",
        "description": "description",
        "enterprise_project_id": "enterpriseProjectId",
        "id": "id",
        "locked": "locked",
        "resource": "resource",
        "tags": "tags",
    },
)
class CbrVaultV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        billing: typing.Union[CbrVaultV3Billing, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        auto_bind: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_expand: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backup_policy_id: typing.Optional[builtins.str] = None,
        bind_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CbrVaultV3BindRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enterprise_project_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CbrVaultV3Resource", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param billing: billing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#billing CbrVaultV3#billing}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#name CbrVaultV3#name}.
        :param auto_bind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#auto_bind CbrVaultV3#auto_bind}.
        :param auto_expand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#auto_expand CbrVaultV3#auto_expand}.
        :param backup_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#backup_policy_id CbrVaultV3#backup_policy_id}.
        :param bind_rules: bind_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#bind_rules CbrVaultV3#bind_rules}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#description CbrVaultV3#description}.
        :param enterprise_project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#enterprise_project_id CbrVaultV3#enterprise_project_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#id CbrVaultV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param locked: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#locked CbrVaultV3#locked}.
        :param resource: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#resource CbrVaultV3#resource}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#tags CbrVaultV3#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(billing, dict):
            billing = CbrVaultV3Billing(**billing)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d4533ecd4c69ed8c7298cb04ecb7870304cc7e04bb3e8610e5d7d21d592eec2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument billing", value=billing, expected_type=type_hints["billing"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument auto_bind", value=auto_bind, expected_type=type_hints["auto_bind"])
            check_type(argname="argument auto_expand", value=auto_expand, expected_type=type_hints["auto_expand"])
            check_type(argname="argument backup_policy_id", value=backup_policy_id, expected_type=type_hints["backup_policy_id"])
            check_type(argname="argument bind_rules", value=bind_rules, expected_type=type_hints["bind_rules"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enterprise_project_id", value=enterprise_project_id, expected_type=type_hints["enterprise_project_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument locked", value=locked, expected_type=type_hints["locked"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "billing": billing,
            "name": name,
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
        if auto_bind is not None:
            self._values["auto_bind"] = auto_bind
        if auto_expand is not None:
            self._values["auto_expand"] = auto_expand
        if backup_policy_id is not None:
            self._values["backup_policy_id"] = backup_policy_id
        if bind_rules is not None:
            self._values["bind_rules"] = bind_rules
        if description is not None:
            self._values["description"] = description
        if enterprise_project_id is not None:
            self._values["enterprise_project_id"] = enterprise_project_id
        if id is not None:
            self._values["id"] = id
        if locked is not None:
            self._values["locked"] = locked
        if resource is not None:
            self._values["resource"] = resource
        if tags is not None:
            self._values["tags"] = tags

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
    def billing(self) -> CbrVaultV3Billing:
        '''billing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#billing CbrVaultV3#billing}
        '''
        result = self._values.get("billing")
        assert result is not None, "Required property 'billing' is missing"
        return typing.cast(CbrVaultV3Billing, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#name CbrVaultV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_bind(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#auto_bind CbrVaultV3#auto_bind}.'''
        result = self._values.get("auto_bind")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_expand(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#auto_expand CbrVaultV3#auto_expand}.'''
        result = self._values.get("auto_expand")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def backup_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#backup_policy_id CbrVaultV3#backup_policy_id}.'''
        result = self._values.get("backup_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bind_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CbrVaultV3BindRules]]]:
        '''bind_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#bind_rules CbrVaultV3#bind_rules}
        '''
        result = self._values.get("bind_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CbrVaultV3BindRules]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#description CbrVaultV3#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enterprise_project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#enterprise_project_id CbrVaultV3#enterprise_project_id}.'''
        result = self._values.get("enterprise_project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#id CbrVaultV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#locked CbrVaultV3#locked}.'''
        result = self._values.get("locked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def resource(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CbrVaultV3Resource"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#resource CbrVaultV3#resource}.'''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CbrVaultV3Resource"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#tags CbrVaultV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CbrVaultV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3Resource",
    jsii_struct_bases=[],
    name_mapping={
        "backup_count": "backupCount",
        "backup_size": "backupSize",
        "exclude_volumes": "excludeVolumes",
        "id": "id",
        "include_volumes": "includeVolumes",
        "name": "name",
        "protect_status": "protectStatus",
        "size": "size",
        "type": "type",
    },
)
class CbrVaultV3Resource:
    def __init__(
        self,
        *,
        backup_count: typing.Optional[jsii.Number] = None,
        backup_size: typing.Optional[jsii.Number] = None,
        exclude_volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        include_volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        protect_status: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backup_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#backup_count CbrVaultV3#backup_count}.
        :param backup_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#backup_size CbrVaultV3#backup_size}.
        :param exclude_volumes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#exclude_volumes CbrVaultV3#exclude_volumes}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#id CbrVaultV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_volumes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#include_volumes CbrVaultV3#include_volumes}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#name CbrVaultV3#name}.
        :param protect_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#protect_status CbrVaultV3#protect_status}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#size CbrVaultV3#size}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#type CbrVaultV3#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09a4a56e25733e2e525e278d3903e137f620a88526b667b11dee17c220c2148)
            check_type(argname="argument backup_count", value=backup_count, expected_type=type_hints["backup_count"])
            check_type(argname="argument backup_size", value=backup_size, expected_type=type_hints["backup_size"])
            check_type(argname="argument exclude_volumes", value=exclude_volumes, expected_type=type_hints["exclude_volumes"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include_volumes", value=include_volumes, expected_type=type_hints["include_volumes"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protect_status", value=protect_status, expected_type=type_hints["protect_status"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backup_count is not None:
            self._values["backup_count"] = backup_count
        if backup_size is not None:
            self._values["backup_size"] = backup_size
        if exclude_volumes is not None:
            self._values["exclude_volumes"] = exclude_volumes
        if id is not None:
            self._values["id"] = id
        if include_volumes is not None:
            self._values["include_volumes"] = include_volumes
        if name is not None:
            self._values["name"] = name
        if protect_status is not None:
            self._values["protect_status"] = protect_status
        if size is not None:
            self._values["size"] = size
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def backup_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#backup_count CbrVaultV3#backup_count}.'''
        result = self._values.get("backup_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def backup_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#backup_size CbrVaultV3#backup_size}.'''
        result = self._values.get("backup_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def exclude_volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#exclude_volumes CbrVaultV3#exclude_volumes}.'''
        result = self._values.get("exclude_volumes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#id CbrVaultV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#include_volumes CbrVaultV3#include_volumes}.'''
        result = self._values.get("include_volumes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#name CbrVaultV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protect_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#protect_status CbrVaultV3#protect_status}.'''
        result = self._values.get("protect_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#size CbrVaultV3#size}.'''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cbr_vault_v3#type CbrVaultV3#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CbrVaultV3Resource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CbrVaultV3ResourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3ResourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__765018c71ec594edc4b5e5637bcdc513c5d7e932a1ed089abdaf627e8804f5b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CbrVaultV3ResourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0da1bec2fee5b4ef20762a3489ac939f4e6514d57d71a8d3a9ee5ce92421575)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CbrVaultV3ResourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cea1d722758f1c2fcf1a36612d9a4126f99740be43aa076447dfd0e65fb518c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc88f5ae3758eac727f32c0a539c80f69068d27c6415497566233b45a0ec16cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__716b1ec83d2c5ee868a3c3733919c2c81e5441d95588155ba29040304c097af2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CbrVaultV3Resource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CbrVaultV3Resource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CbrVaultV3Resource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777ab83ab6e2da390dd1265774b029fe557f4310efe9639db3928d5872783cb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CbrVaultV3ResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cbrVaultV3.CbrVaultV3ResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcb4f98639e7dda9fce648dcebd33ef5be4b299ea71c431ad4c16e761a16003f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBackupCount")
    def reset_backup_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupCount", []))

    @jsii.member(jsii_name="resetBackupSize")
    def reset_backup_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupSize", []))

    @jsii.member(jsii_name="resetExcludeVolumes")
    def reset_exclude_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeVolumes", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncludeVolumes")
    def reset_include_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeVolumes", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProtectStatus")
    def reset_protect_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectStatus", []))

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="backupCountInput")
    def backup_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupCountInput"))

    @builtins.property
    @jsii.member(jsii_name="backupSizeInput")
    def backup_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeVolumesInput")
    def exclude_volumes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeVolumesInput")
    def include_volumes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protectStatusInput")
    def protect_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protectStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="backupCount")
    def backup_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupCount"))

    @backup_count.setter
    def backup_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4afa51997a8955a9ef1d4f68a8450e71c7aa266dd7d66f351f17a1772409997f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupSize")
    def backup_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupSize"))

    @backup_size.setter
    def backup_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab19e9401fe0429567fb87fe8008b8adc75e03d640bf73cfb193e40aaca4965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeVolumes")
    def exclude_volumes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeVolumes"))

    @exclude_volumes.setter
    def exclude_volumes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5635d77143b4bdb4aeac9a401c8d57df90fc5e089a3624d3970080a629e3c4bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeVolumes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8f8ea2068e8062ae312e6bf23fc33f195ac9e5159568a3623e4c5dd5c61f3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeVolumes")
    def include_volumes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeVolumes"))

    @include_volumes.setter
    def include_volumes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6049d05e7aace13b0c9b2866edd870f87ccceeb317aa6c27b36c6c05499aaafa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeVolumes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06c3fba942c80141cbe452c8a476fcb3505821bb088e2af32c4cb304671ae3a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protectStatus")
    def protect_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectStatus"))

    @protect_status.setter
    def protect_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c601a4a290a6e3c19326444b2d891dfa980e047b9bee686b0f4073d23b78579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6863f82ead8c2dbde2e660f2f07285c5d2dc63c655db3f6204ef090a569a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa1a8ac0d918ff7a504ce985cebac5e4ef206ea61966c40dd717339a4cee536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CbrVaultV3Resource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CbrVaultV3Resource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CbrVaultV3Resource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e4ff3bc461b1b1ccbba3bd6626490e14bcf876c8458e681f4c0b7540b0380e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CbrVaultV3",
    "CbrVaultV3Billing",
    "CbrVaultV3BillingOutputReference",
    "CbrVaultV3BindRules",
    "CbrVaultV3BindRulesList",
    "CbrVaultV3BindRulesOutputReference",
    "CbrVaultV3Config",
    "CbrVaultV3Resource",
    "CbrVaultV3ResourceList",
    "CbrVaultV3ResourceOutputReference",
]

publication.publish()

def _typecheckingstub__71c52a02ce2cd36873fdd7fe976ebacf6804c138432d9c378f2ef5484e7c6a9e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    billing: typing.Union[CbrVaultV3Billing, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    auto_bind: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_expand: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backup_policy_id: typing.Optional[builtins.str] = None,
    bind_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CbrVaultV3BindRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enterprise_project_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    resource: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CbrVaultV3Resource, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__5bec3c691c9701d2808fa1831bcae3be77b7e05a53362bf641668e92dba2b435(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45b8b735c76d971ddd4c4dbfaeba8af7ef6ebc3ff0c435d5958c18873e2b861(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CbrVaultV3BindRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207b808cfc8768b057dee2e90761ef569734c39b4547a99d7efcb7476aac3cbb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CbrVaultV3Resource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ac3173c9dc4ae781a3f2999beaa01b13bc8bfd4b5116fcf35676a909f43d0c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c7ad7f4b730c67d54f62ed5b865856be40a828a73e668ae4a3dcdbb7e97e79(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6658a4dcebcd79c9f5f0e18c0a66117c4fc41f4b091e396922589f6ab849b4ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5826c8adb45d257b29964be4fc852bfa9d5dca6d3fbe3e51deddef0719d8b534(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ff61fb3084f817aaa0281a33bfcb079cc7ec98aa82a03ade798b17612b5ec4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e522456083bb3b30a611946a4102217eb143edf81601794b39f55c76a773e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c3e0285a3b1075e48dc6798e1869e293a70368f1aad3ef44dc7527d5441b0a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97688582bedf91bb028d159526a3e59752f250e1865d38a05a4634c4fb6d6262(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c5e737ad846c45356685215de2570e0da79b5c78722e3e8f416e12f9d35a82(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa15f27a51fb6b7d6704d362243232d647ce278bd1b8064d9a7e088dd02ba52e(
    *,
    object_type: builtins.str,
    protect_type: builtins.str,
    size: jsii.Number,
    charging_mode: typing.Optional[builtins.str] = None,
    cloud_type: typing.Optional[builtins.str] = None,
    consistent_level: typing.Optional[builtins.str] = None,
    console_url: typing.Optional[builtins.str] = None,
    extra_info: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_auto_pay: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_auto_renew: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    period_num: typing.Optional[jsii.Number] = None,
    period_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e883b35fbd9f5d81b6bf7caee3fdfab7fccd01feb2f248cff66028aeb1cc27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bcb79cbce684113d9879c7239e71cdcef0a77aedc499f4e638b1afeb4a82ea3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bc02ce85cda981abfbe381da5e4e46d83910a6b4d5280d2dec53a3bdd950d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b37c0092663717ea8a74f38f9ba4474beaa116a40ed2135ac86149ec22e36b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3956dfa9b1a0aaf4723f7bf3e11dbc4e96038ee9c1822c909775e830ef139675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c6f7d25d253711f8e42825a59c0d9b8d65016054a8c8a6c9260428033878a0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce53401006d5ef765cb6eea646ab1cd936fd90eb8b71cdd6f04c124da6ba8ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d6014a497909bab85b41ab32fe21fd17fa2b1db9e1054f1d21a48f36138048(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0451daecd4baa5f737884ee2101364a78973d5ec4e52eaad9d8faec1fb264142(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51b3b350d1bc0aeb7d85d2874e7f26baffbbb43156227e5b4bb7b5705f0d81a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7296e4aa32c9d0da602b12599bed3c80cd681ef6a7baf2bdf7db7aeaf1d5804c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40eeec3bf6223bec4408c593c204e539e4990af5aaff37e74b36593aad420d4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3ea5a234792d70a8c45765e154c28e5711eac1b210f46d844395346d2fae67(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014ad0aa438aa1132ebec36a22ff4f9ae991584c4b5362aaab96d7d7c29b1611(
    value: typing.Optional[CbrVaultV3Billing],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f905291637465e15585557c94cad534c404756b750be4e2c562dff54eb4830(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db34c9d5a1aff8c2b26d66bef61864477a10871e1c9bbfd064d81fe3f818ad8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51bea9f78e4af7aeb6b9b08fc123bec1b1b93d48431b46e2b5e79aee1599fce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b50e6043534cb84d24ddf591b3be8bb4fac1b70a242ee49b17613bdfe0db53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ba8223f7b86a1c7de84b6929d4db07ea42a0b9509c089853d5d75f8a65e149(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ebff16315f590a7ce1f826987044ad2ebd17fd522a08361b8164e4935627006(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d44028c10bb490332305ada25a6eb5840e0463a322b3cfbb7aa937911599bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CbrVaultV3BindRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d67922749cbd6bae6fb3e7ea0b733bf004c0bc26e49446aae29e5aa9eafd62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb18e56b2aed1e57dd031968612430b4e9e164b895c80af624ce773b72bc52d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0b02072482fdcd4f362ce01e62408fada85caa6a70376fdb227c130472b624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49279390e1a4176b205ff0a9796205fe7dc573e797fbc2a93268125f8cb938b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CbrVaultV3BindRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4533ecd4c69ed8c7298cb04ecb7870304cc7e04bb3e8610e5d7d21d592eec2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    billing: typing.Union[CbrVaultV3Billing, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    auto_bind: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_expand: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backup_policy_id: typing.Optional[builtins.str] = None,
    bind_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CbrVaultV3BindRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enterprise_project_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    resource: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CbrVaultV3Resource, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09a4a56e25733e2e525e278d3903e137f620a88526b667b11dee17c220c2148(
    *,
    backup_count: typing.Optional[jsii.Number] = None,
    backup_size: typing.Optional[jsii.Number] = None,
    exclude_volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    include_volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    protect_status: typing.Optional[builtins.str] = None,
    size: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765018c71ec594edc4b5e5637bcdc513c5d7e932a1ed089abdaf627e8804f5b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0da1bec2fee5b4ef20762a3489ac939f4e6514d57d71a8d3a9ee5ce92421575(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cea1d722758f1c2fcf1a36612d9a4126f99740be43aa076447dfd0e65fb518c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc88f5ae3758eac727f32c0a539c80f69068d27c6415497566233b45a0ec16cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716b1ec83d2c5ee868a3c3733919c2c81e5441d95588155ba29040304c097af2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777ab83ab6e2da390dd1265774b029fe557f4310efe9639db3928d5872783cb9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CbrVaultV3Resource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb4f98639e7dda9fce648dcebd33ef5be4b299ea71c431ad4c16e761a16003f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4afa51997a8955a9ef1d4f68a8450e71c7aa266dd7d66f351f17a1772409997f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab19e9401fe0429567fb87fe8008b8adc75e03d640bf73cfb193e40aaca4965(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5635d77143b4bdb4aeac9a401c8d57df90fc5e089a3624d3970080a629e3c4bd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8f8ea2068e8062ae312e6bf23fc33f195ac9e5159568a3623e4c5dd5c61f3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6049d05e7aace13b0c9b2866edd870f87ccceeb317aa6c27b36c6c05499aaafa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c3fba942c80141cbe452c8a476fcb3505821bb088e2af32c4cb304671ae3a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c601a4a290a6e3c19326444b2d891dfa980e047b9bee686b0f4073d23b78579(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6863f82ead8c2dbde2e660f2f07285c5d2dc63c655db3f6204ef090a569a96(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa1a8ac0d918ff7a504ce985cebac5e4ef206ea61966c40dd717339a4cee536(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4ff3bc461b1b1ccbba3bd6626490e14bcf876c8458e681f4c0b7540b0380e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CbrVaultV3Resource]],
) -> None:
    """Type checking stubs"""
    pass
