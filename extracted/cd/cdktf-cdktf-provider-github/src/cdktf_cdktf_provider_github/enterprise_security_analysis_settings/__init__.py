r'''
# `github_enterprise_security_analysis_settings`

Refer to the Terraform Registry for docs: [`github_enterprise_security_analysis_settings`](https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings).
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


class EnterpriseSecurityAnalysisSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.enterpriseSecurityAnalysisSettings.EnterpriseSecurityAnalysisSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings github_enterprise_security_analysis_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enterprise_slug: builtins.str,
        advanced_security_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        secret_scanning_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_scanning_push_protection_custom_link: typing.Optional[builtins.str] = None,
        secret_scanning_push_protection_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_scanning_validity_checks_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings github_enterprise_security_analysis_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enterprise_slug: The slug of the enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#enterprise_slug EnterpriseSecurityAnalysisSettings#enterprise_slug}
        :param advanced_security_enabled_for_new_repositories: Whether GitHub Advanced Security is automatically enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#advanced_security_enabled_for_new_repositories EnterpriseSecurityAnalysisSettings#advanced_security_enabled_for_new_repositories}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#id EnterpriseSecurityAnalysisSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param secret_scanning_enabled_for_new_repositories: Whether secret scanning is automatically enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#secret_scanning_enabled_for_new_repositories EnterpriseSecurityAnalysisSettings#secret_scanning_enabled_for_new_repositories}
        :param secret_scanning_push_protection_custom_link: Custom URL for secret scanning push protection bypass instructions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#secret_scanning_push_protection_custom_link EnterpriseSecurityAnalysisSettings#secret_scanning_push_protection_custom_link}
        :param secret_scanning_push_protection_enabled_for_new_repositories: Whether secret scanning push protection is automatically enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#secret_scanning_push_protection_enabled_for_new_repositories EnterpriseSecurityAnalysisSettings#secret_scanning_push_protection_enabled_for_new_repositories}
        :param secret_scanning_validity_checks_enabled: Whether secret scanning validity checks are enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#secret_scanning_validity_checks_enabled EnterpriseSecurityAnalysisSettings#secret_scanning_validity_checks_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c2cb4d18eaa27214728dc860233cb6950b745cf92f1e02ac6889c65ee9d4a9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EnterpriseSecurityAnalysisSettingsConfig(
            enterprise_slug=enterprise_slug,
            advanced_security_enabled_for_new_repositories=advanced_security_enabled_for_new_repositories,
            id=id,
            secret_scanning_enabled_for_new_repositories=secret_scanning_enabled_for_new_repositories,
            secret_scanning_push_protection_custom_link=secret_scanning_push_protection_custom_link,
            secret_scanning_push_protection_enabled_for_new_repositories=secret_scanning_push_protection_enabled_for_new_repositories,
            secret_scanning_validity_checks_enabled=secret_scanning_validity_checks_enabled,
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
        '''Generates CDKTF code for importing a EnterpriseSecurityAnalysisSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EnterpriseSecurityAnalysisSettings to import.
        :param import_from_id: The id of the existing EnterpriseSecurityAnalysisSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EnterpriseSecurityAnalysisSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f46812d1999aadeed1c6a3708bf6afd091275b05048b41c024e43ed2627d2d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAdvancedSecurityEnabledForNewRepositories")
    def reset_advanced_security_enabled_for_new_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedSecurityEnabledForNewRepositories", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSecretScanningEnabledForNewRepositories")
    def reset_secret_scanning_enabled_for_new_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretScanningEnabledForNewRepositories", []))

    @jsii.member(jsii_name="resetSecretScanningPushProtectionCustomLink")
    def reset_secret_scanning_push_protection_custom_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretScanningPushProtectionCustomLink", []))

    @jsii.member(jsii_name="resetSecretScanningPushProtectionEnabledForNewRepositories")
    def reset_secret_scanning_push_protection_enabled_for_new_repositories(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretScanningPushProtectionEnabledForNewRepositories", []))

    @jsii.member(jsii_name="resetSecretScanningValidityChecksEnabled")
    def reset_secret_scanning_validity_checks_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretScanningValidityChecksEnabled", []))

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
    @jsii.member(jsii_name="advancedSecurityEnabledForNewRepositoriesInput")
    def advanced_security_enabled_for_new_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "advancedSecurityEnabledForNewRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseSlugInput")
    def enterprise_slug_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enterpriseSlugInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="secretScanningEnabledForNewRepositoriesInput")
    def secret_scanning_enabled_for_new_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secretScanningEnabledForNewRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretScanningPushProtectionCustomLinkInput")
    def secret_scanning_push_protection_custom_link_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretScanningPushProtectionCustomLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="secretScanningPushProtectionEnabledForNewRepositoriesInput")
    def secret_scanning_push_protection_enabled_for_new_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secretScanningPushProtectionEnabledForNewRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretScanningValidityChecksEnabledInput")
    def secret_scanning_validity_checks_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secretScanningValidityChecksEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedSecurityEnabledForNewRepositories")
    def advanced_security_enabled_for_new_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "advancedSecurityEnabledForNewRepositories"))

    @advanced_security_enabled_for_new_repositories.setter
    def advanced_security_enabled_for_new_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6690d2598440af174a30572f5bc8706b23ab65217649e3b57aff246207c6fbbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedSecurityEnabledForNewRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enterpriseSlug")
    def enterprise_slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enterpriseSlug"))

    @enterprise_slug.setter
    def enterprise_slug(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fc7955af467a9c47881252d29b4e19d37513a73585ae2b739a4aae6e87703b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterpriseSlug", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9243fdd47bb19188b1ef292e8128bafeb418450f226180bc4a4445be87905c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretScanningEnabledForNewRepositories")
    def secret_scanning_enabled_for_new_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secretScanningEnabledForNewRepositories"))

    @secret_scanning_enabled_for_new_repositories.setter
    def secret_scanning_enabled_for_new_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c134033e9615a369b346f42f7a0ce27c75caf77e95835adfd6f5e80287cc1d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretScanningEnabledForNewRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretScanningPushProtectionCustomLink")
    def secret_scanning_push_protection_custom_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretScanningPushProtectionCustomLink"))

    @secret_scanning_push_protection_custom_link.setter
    def secret_scanning_push_protection_custom_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433dde9b3adadfea56597e573d276c6737cfca02a7115e3b90fccd2d98d3a947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretScanningPushProtectionCustomLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretScanningPushProtectionEnabledForNewRepositories")
    def secret_scanning_push_protection_enabled_for_new_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secretScanningPushProtectionEnabledForNewRepositories"))

    @secret_scanning_push_protection_enabled_for_new_repositories.setter
    def secret_scanning_push_protection_enabled_for_new_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3e118576c73bc01dea0d7207142b7ec8a4346ff648f4992678388787d0afe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretScanningPushProtectionEnabledForNewRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretScanningValidityChecksEnabled")
    def secret_scanning_validity_checks_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secretScanningValidityChecksEnabled"))

    @secret_scanning_validity_checks_enabled.setter
    def secret_scanning_validity_checks_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ba2976c4b88140c9ade5e38e23471dfc011d32b09bbf2186b982310336b453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretScanningValidityChecksEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.enterpriseSecurityAnalysisSettings.EnterpriseSecurityAnalysisSettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "enterprise_slug": "enterpriseSlug",
        "advanced_security_enabled_for_new_repositories": "advancedSecurityEnabledForNewRepositories",
        "id": "id",
        "secret_scanning_enabled_for_new_repositories": "secretScanningEnabledForNewRepositories",
        "secret_scanning_push_protection_custom_link": "secretScanningPushProtectionCustomLink",
        "secret_scanning_push_protection_enabled_for_new_repositories": "secretScanningPushProtectionEnabledForNewRepositories",
        "secret_scanning_validity_checks_enabled": "secretScanningValidityChecksEnabled",
    },
)
class EnterpriseSecurityAnalysisSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        enterprise_slug: builtins.str,
        advanced_security_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        secret_scanning_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_scanning_push_protection_custom_link: typing.Optional[builtins.str] = None,
        secret_scanning_push_protection_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_scanning_validity_checks_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enterprise_slug: The slug of the enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#enterprise_slug EnterpriseSecurityAnalysisSettings#enterprise_slug}
        :param advanced_security_enabled_for_new_repositories: Whether GitHub Advanced Security is automatically enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#advanced_security_enabled_for_new_repositories EnterpriseSecurityAnalysisSettings#advanced_security_enabled_for_new_repositories}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#id EnterpriseSecurityAnalysisSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param secret_scanning_enabled_for_new_repositories: Whether secret scanning is automatically enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#secret_scanning_enabled_for_new_repositories EnterpriseSecurityAnalysisSettings#secret_scanning_enabled_for_new_repositories}
        :param secret_scanning_push_protection_custom_link: Custom URL for secret scanning push protection bypass instructions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#secret_scanning_push_protection_custom_link EnterpriseSecurityAnalysisSettings#secret_scanning_push_protection_custom_link}
        :param secret_scanning_push_protection_enabled_for_new_repositories: Whether secret scanning push protection is automatically enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#secret_scanning_push_protection_enabled_for_new_repositories EnterpriseSecurityAnalysisSettings#secret_scanning_push_protection_enabled_for_new_repositories}
        :param secret_scanning_validity_checks_enabled: Whether secret scanning validity checks are enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#secret_scanning_validity_checks_enabled EnterpriseSecurityAnalysisSettings#secret_scanning_validity_checks_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db18699ada4cb7633bc39134fd32e786a0cb4dad51a0426197bf9e11c5fd7542)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enterprise_slug", value=enterprise_slug, expected_type=type_hints["enterprise_slug"])
            check_type(argname="argument advanced_security_enabled_for_new_repositories", value=advanced_security_enabled_for_new_repositories, expected_type=type_hints["advanced_security_enabled_for_new_repositories"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument secret_scanning_enabled_for_new_repositories", value=secret_scanning_enabled_for_new_repositories, expected_type=type_hints["secret_scanning_enabled_for_new_repositories"])
            check_type(argname="argument secret_scanning_push_protection_custom_link", value=secret_scanning_push_protection_custom_link, expected_type=type_hints["secret_scanning_push_protection_custom_link"])
            check_type(argname="argument secret_scanning_push_protection_enabled_for_new_repositories", value=secret_scanning_push_protection_enabled_for_new_repositories, expected_type=type_hints["secret_scanning_push_protection_enabled_for_new_repositories"])
            check_type(argname="argument secret_scanning_validity_checks_enabled", value=secret_scanning_validity_checks_enabled, expected_type=type_hints["secret_scanning_validity_checks_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enterprise_slug": enterprise_slug,
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
        if advanced_security_enabled_for_new_repositories is not None:
            self._values["advanced_security_enabled_for_new_repositories"] = advanced_security_enabled_for_new_repositories
        if id is not None:
            self._values["id"] = id
        if secret_scanning_enabled_for_new_repositories is not None:
            self._values["secret_scanning_enabled_for_new_repositories"] = secret_scanning_enabled_for_new_repositories
        if secret_scanning_push_protection_custom_link is not None:
            self._values["secret_scanning_push_protection_custom_link"] = secret_scanning_push_protection_custom_link
        if secret_scanning_push_protection_enabled_for_new_repositories is not None:
            self._values["secret_scanning_push_protection_enabled_for_new_repositories"] = secret_scanning_push_protection_enabled_for_new_repositories
        if secret_scanning_validity_checks_enabled is not None:
            self._values["secret_scanning_validity_checks_enabled"] = secret_scanning_validity_checks_enabled

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
    def enterprise_slug(self) -> builtins.str:
        '''The slug of the enterprise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#enterprise_slug EnterpriseSecurityAnalysisSettings#enterprise_slug}
        '''
        result = self._values.get("enterprise_slug")
        assert result is not None, "Required property 'enterprise_slug' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_security_enabled_for_new_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether GitHub Advanced Security is automatically enabled for new repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#advanced_security_enabled_for_new_repositories EnterpriseSecurityAnalysisSettings#advanced_security_enabled_for_new_repositories}
        '''
        result = self._values.get("advanced_security_enabled_for_new_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#id EnterpriseSecurityAnalysisSettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_scanning_enabled_for_new_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether secret scanning is automatically enabled for new repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#secret_scanning_enabled_for_new_repositories EnterpriseSecurityAnalysisSettings#secret_scanning_enabled_for_new_repositories}
        '''
        result = self._values.get("secret_scanning_enabled_for_new_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret_scanning_push_protection_custom_link(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Custom URL for secret scanning push protection bypass instructions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#secret_scanning_push_protection_custom_link EnterpriseSecurityAnalysisSettings#secret_scanning_push_protection_custom_link}
        '''
        result = self._values.get("secret_scanning_push_protection_custom_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_scanning_push_protection_enabled_for_new_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether secret scanning push protection is automatically enabled for new repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#secret_scanning_push_protection_enabled_for_new_repositories EnterpriseSecurityAnalysisSettings#secret_scanning_push_protection_enabled_for_new_repositories}
        '''
        result = self._values.get("secret_scanning_push_protection_enabled_for_new_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret_scanning_validity_checks_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether secret scanning validity checks are enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/enterprise_security_analysis_settings#secret_scanning_validity_checks_enabled EnterpriseSecurityAnalysisSettings#secret_scanning_validity_checks_enabled}
        '''
        result = self._values.get("secret_scanning_validity_checks_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseSecurityAnalysisSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EnterpriseSecurityAnalysisSettings",
    "EnterpriseSecurityAnalysisSettingsConfig",
]

publication.publish()

def _typecheckingstub__23c2cb4d18eaa27214728dc860233cb6950b745cf92f1e02ac6889c65ee9d4a9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enterprise_slug: builtins.str,
    advanced_security_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    secret_scanning_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_scanning_push_protection_custom_link: typing.Optional[builtins.str] = None,
    secret_scanning_push_protection_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_scanning_validity_checks_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__61f46812d1999aadeed1c6a3708bf6afd091275b05048b41c024e43ed2627d2d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6690d2598440af174a30572f5bc8706b23ab65217649e3b57aff246207c6fbbf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fc7955af467a9c47881252d29b4e19d37513a73585ae2b739a4aae6e87703b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9243fdd47bb19188b1ef292e8128bafeb418450f226180bc4a4445be87905c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c134033e9615a369b346f42f7a0ce27c75caf77e95835adfd6f5e80287cc1d03(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433dde9b3adadfea56597e573d276c6737cfca02a7115e3b90fccd2d98d3a947(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3e118576c73bc01dea0d7207142b7ec8a4346ff648f4992678388787d0afe4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ba2976c4b88140c9ade5e38e23471dfc011d32b09bbf2186b982310336b453(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db18699ada4cb7633bc39134fd32e786a0cb4dad51a0426197bf9e11c5fd7542(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enterprise_slug: builtins.str,
    advanced_security_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    secret_scanning_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_scanning_push_protection_custom_link: typing.Optional[builtins.str] = None,
    secret_scanning_push_protection_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_scanning_validity_checks_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
