r'''
# `google_recaptcha_enterprise_key`

Refer to the Terraform Registry for docs: [`google_recaptcha_enterprise_key`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key).
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


class RecaptchaEnterpriseKey(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKey",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key google_recaptcha_enterprise_key}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        android_settings: typing.Optional[typing.Union["RecaptchaEnterpriseKeyAndroidSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ios_settings: typing.Optional[typing.Union["RecaptchaEnterpriseKeyIosSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        testing_options: typing.Optional[typing.Union["RecaptchaEnterpriseKeyTestingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["RecaptchaEnterpriseKeyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        waf_settings: typing.Optional[typing.Union["RecaptchaEnterpriseKeyWafSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        web_settings: typing.Optional[typing.Union["RecaptchaEnterpriseKeyWebSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key google_recaptcha_enterprise_key} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Human-readable display name of this key. Modifiable by user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#display_name RecaptchaEnterpriseKey#display_name}
        :param android_settings: android_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#android_settings RecaptchaEnterpriseKey#android_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#id RecaptchaEnterpriseKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ios_settings: ios_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#ios_settings RecaptchaEnterpriseKey#ios_settings}
        :param labels: See `Creating and managing labels <https://cloud.google.com/recaptcha-enterprise/docs/labels>`_. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#labels RecaptchaEnterpriseKey#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#project RecaptchaEnterpriseKey#project}
        :param testing_options: testing_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#testing_options RecaptchaEnterpriseKey#testing_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#timeouts RecaptchaEnterpriseKey#timeouts}
        :param waf_settings: waf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#waf_settings RecaptchaEnterpriseKey#waf_settings}
        :param web_settings: web_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#web_settings RecaptchaEnterpriseKey#web_settings}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f13f297bf3284053793b26a6d43e0d96f91b5d4db7fe71e47f010ea5dd2a64)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RecaptchaEnterpriseKeyConfig(
            display_name=display_name,
            android_settings=android_settings,
            id=id,
            ios_settings=ios_settings,
            labels=labels,
            project=project,
            testing_options=testing_options,
            timeouts=timeouts,
            waf_settings=waf_settings,
            web_settings=web_settings,
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
        '''Generates CDKTF code for importing a RecaptchaEnterpriseKey resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RecaptchaEnterpriseKey to import.
        :param import_from_id: The id of the existing RecaptchaEnterpriseKey that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RecaptchaEnterpriseKey to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa743c036f81fb8287b1c4dd3d54f429caf19b74befc39113b3e41ca76f232c2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAndroidSettings")
    def put_android_settings(
        self,
        *,
        allow_all_package_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_package_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allow_all_package_names: If set to true, it means allowed_package_names will not be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allow_all_package_names RecaptchaEnterpriseKey#allow_all_package_names}
        :param allowed_package_names: Android package names of apps allowed to use the key. Example: 'com.companyname.appname'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allowed_package_names RecaptchaEnterpriseKey#allowed_package_names}
        '''
        value = RecaptchaEnterpriseKeyAndroidSettings(
            allow_all_package_names=allow_all_package_names,
            allowed_package_names=allowed_package_names,
        )

        return typing.cast(None, jsii.invoke(self, "putAndroidSettings", [value]))

    @jsii.member(jsii_name="putIosSettings")
    def put_ios_settings(
        self,
        *,
        allow_all_bundle_ids: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_bundle_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allow_all_bundle_ids: If set to true, it means allowed_bundle_ids will not be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allow_all_bundle_ids RecaptchaEnterpriseKey#allow_all_bundle_ids}
        :param allowed_bundle_ids: iOS bundle ids of apps allowed to use the key. Example: 'com.companyname.productname.appname'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allowed_bundle_ids RecaptchaEnterpriseKey#allowed_bundle_ids}
        '''
        value = RecaptchaEnterpriseKeyIosSettings(
            allow_all_bundle_ids=allow_all_bundle_ids,
            allowed_bundle_ids=allowed_bundle_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putIosSettings", [value]))

    @jsii.member(jsii_name="putTestingOptions")
    def put_testing_options(
        self,
        *,
        testing_challenge: typing.Optional[builtins.str] = None,
        testing_score: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param testing_challenge: For challenge-based keys only (CHECKBOX, INVISIBLE), all challenge requests for this site will return nocaptcha if NOCAPTCHA, or an unsolvable challenge if UNSOLVABLE_CHALLENGE. Possible values: TESTING_CHALLENGE_UNSPECIFIED, NOCAPTCHA, UNSOLVABLE_CHALLENGE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#testing_challenge RecaptchaEnterpriseKey#testing_challenge}
        :param testing_score: All assessments for this Key will return this score. Must be between 0 (likely not legitimate) and 1 (likely legitimate) inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#testing_score RecaptchaEnterpriseKey#testing_score}
        '''
        value = RecaptchaEnterpriseKeyTestingOptions(
            testing_challenge=testing_challenge, testing_score=testing_score
        )

        return typing.cast(None, jsii.invoke(self, "putTestingOptions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#create RecaptchaEnterpriseKey#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#delete RecaptchaEnterpriseKey#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#update RecaptchaEnterpriseKey#update}.
        '''
        value = RecaptchaEnterpriseKeyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWafSettings")
    def put_waf_settings(
        self,
        *,
        waf_feature: builtins.str,
        waf_service: builtins.str,
    ) -> None:
        '''
        :param waf_feature: Supported WAF features. For more information, see https://cloud.google.com/recaptcha-enterprise/docs/usecase#comparison_of_features. Possible values: CHALLENGE_PAGE, SESSION_TOKEN, ACTION_TOKEN, EXPRESS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#waf_feature RecaptchaEnterpriseKey#waf_feature}
        :param waf_service: The WAF service that uses this key. Possible values: CA, FASTLY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#waf_service RecaptchaEnterpriseKey#waf_service}
        '''
        value = RecaptchaEnterpriseKeyWafSettings(
            waf_feature=waf_feature, waf_service=waf_service
        )

        return typing.cast(None, jsii.invoke(self, "putWafSettings", [value]))

    @jsii.member(jsii_name="putWebSettings")
    def put_web_settings(
        self,
        *,
        integration_type: builtins.str,
        allow_all_domains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_amp_traffic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        challenge_security_preference: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param integration_type: Required. Describes how this key is integrated with the website. Possible values: SCORE, CHECKBOX, INVISIBLE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#integration_type RecaptchaEnterpriseKey#integration_type}
        :param allow_all_domains: If set to true, it means allowed_domains will not be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allow_all_domains RecaptchaEnterpriseKey#allow_all_domains}
        :param allow_amp_traffic: If set to true, the key can be used on AMP (Accelerated Mobile Pages) websites. This is supported only for the SCORE integration type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allow_amp_traffic RecaptchaEnterpriseKey#allow_amp_traffic}
        :param allowed_domains: Domains or subdomains of websites allowed to use the key. All subdomains of an allowed domain are automatically allowed. A valid domain requires a host and must not include any path, port, query or fragment. Examples: 'example.com' or 'subdomain.example.com' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allowed_domains RecaptchaEnterpriseKey#allowed_domains}
        :param challenge_security_preference: Settings for the frequency and difficulty at which this key triggers captcha challenges. This should only be specified for IntegrationTypes CHECKBOX and INVISIBLE. Possible values: CHALLENGE_SECURITY_PREFERENCE_UNSPECIFIED, USABILITY, BALANCE, SECURITY Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#challenge_security_preference RecaptchaEnterpriseKey#challenge_security_preference}
        '''
        value = RecaptchaEnterpriseKeyWebSettings(
            integration_type=integration_type,
            allow_all_domains=allow_all_domains,
            allow_amp_traffic=allow_amp_traffic,
            allowed_domains=allowed_domains,
            challenge_security_preference=challenge_security_preference,
        )

        return typing.cast(None, jsii.invoke(self, "putWebSettings", [value]))

    @jsii.member(jsii_name="resetAndroidSettings")
    def reset_android_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAndroidSettings", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIosSettings")
    def reset_ios_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIosSettings", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTestingOptions")
    def reset_testing_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestingOptions", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWafSettings")
    def reset_waf_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWafSettings", []))

    @jsii.member(jsii_name="resetWebSettings")
    def reset_web_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebSettings", []))

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
    @jsii.member(jsii_name="androidSettings")
    def android_settings(
        self,
    ) -> "RecaptchaEnterpriseKeyAndroidSettingsOutputReference":
        return typing.cast("RecaptchaEnterpriseKeyAndroidSettingsOutputReference", jsii.get(self, "androidSettings"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="iosSettings")
    def ios_settings(self) -> "RecaptchaEnterpriseKeyIosSettingsOutputReference":
        return typing.cast("RecaptchaEnterpriseKeyIosSettingsOutputReference", jsii.get(self, "iosSettings"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="testingOptions")
    def testing_options(self) -> "RecaptchaEnterpriseKeyTestingOptionsOutputReference":
        return typing.cast("RecaptchaEnterpriseKeyTestingOptionsOutputReference", jsii.get(self, "testingOptions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RecaptchaEnterpriseKeyTimeoutsOutputReference":
        return typing.cast("RecaptchaEnterpriseKeyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="wafSettings")
    def waf_settings(self) -> "RecaptchaEnterpriseKeyWafSettingsOutputReference":
        return typing.cast("RecaptchaEnterpriseKeyWafSettingsOutputReference", jsii.get(self, "wafSettings"))

    @builtins.property
    @jsii.member(jsii_name="webSettings")
    def web_settings(self) -> "RecaptchaEnterpriseKeyWebSettingsOutputReference":
        return typing.cast("RecaptchaEnterpriseKeyWebSettingsOutputReference", jsii.get(self, "webSettings"))

    @builtins.property
    @jsii.member(jsii_name="androidSettingsInput")
    def android_settings_input(
        self,
    ) -> typing.Optional["RecaptchaEnterpriseKeyAndroidSettings"]:
        return typing.cast(typing.Optional["RecaptchaEnterpriseKeyAndroidSettings"], jsii.get(self, "androidSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="iosSettingsInput")
    def ios_settings_input(
        self,
    ) -> typing.Optional["RecaptchaEnterpriseKeyIosSettings"]:
        return typing.cast(typing.Optional["RecaptchaEnterpriseKeyIosSettings"], jsii.get(self, "iosSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="testingOptionsInput")
    def testing_options_input(
        self,
    ) -> typing.Optional["RecaptchaEnterpriseKeyTestingOptions"]:
        return typing.cast(typing.Optional["RecaptchaEnterpriseKeyTestingOptions"], jsii.get(self, "testingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RecaptchaEnterpriseKeyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RecaptchaEnterpriseKeyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="wafSettingsInput")
    def waf_settings_input(
        self,
    ) -> typing.Optional["RecaptchaEnterpriseKeyWafSettings"]:
        return typing.cast(typing.Optional["RecaptchaEnterpriseKeyWafSettings"], jsii.get(self, "wafSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="webSettingsInput")
    def web_settings_input(
        self,
    ) -> typing.Optional["RecaptchaEnterpriseKeyWebSettings"]:
        return typing.cast(typing.Optional["RecaptchaEnterpriseKeyWebSettings"], jsii.get(self, "webSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1164c41731106258ccde0037dcc92d696bccb1b3277b99a9da83f289288ee69e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed74543a0677a0ac4e112dd6a727fc8a4f7c44f10f05104f184f0a24f485c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545418e133c90cd201d9d677eebb09df40777a830be2e9d724b9b8e28b3e8ace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1be5b209b270d929053ecc7d3f1b22c7929423d4d523d9bc8d9e361c1372b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKeyAndroidSettings",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all_package_names": "allowAllPackageNames",
        "allowed_package_names": "allowedPackageNames",
    },
)
class RecaptchaEnterpriseKeyAndroidSettings:
    def __init__(
        self,
        *,
        allow_all_package_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_package_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allow_all_package_names: If set to true, it means allowed_package_names will not be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allow_all_package_names RecaptchaEnterpriseKey#allow_all_package_names}
        :param allowed_package_names: Android package names of apps allowed to use the key. Example: 'com.companyname.appname'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allowed_package_names RecaptchaEnterpriseKey#allowed_package_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c482240e855ef4e798d9c94acfc9080c70f08bfb5d8b36d5924579788fcd485)
            check_type(argname="argument allow_all_package_names", value=allow_all_package_names, expected_type=type_hints["allow_all_package_names"])
            check_type(argname="argument allowed_package_names", value=allowed_package_names, expected_type=type_hints["allowed_package_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_all_package_names is not None:
            self._values["allow_all_package_names"] = allow_all_package_names
        if allowed_package_names is not None:
            self._values["allowed_package_names"] = allowed_package_names

    @builtins.property
    def allow_all_package_names(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, it means allowed_package_names will not be enforced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allow_all_package_names RecaptchaEnterpriseKey#allow_all_package_names}
        '''
        result = self._values.get("allow_all_package_names")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_package_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Android package names of apps allowed to use the key. Example: 'com.companyname.appname'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allowed_package_names RecaptchaEnterpriseKey#allowed_package_names}
        '''
        result = self._values.get("allowed_package_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RecaptchaEnterpriseKeyAndroidSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RecaptchaEnterpriseKeyAndroidSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKeyAndroidSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4786e8c6a8480f8737c7f3cd2195c1391b1ed408fd50725ed448c5b87f756086)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowAllPackageNames")
    def reset_allow_all_package_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAllPackageNames", []))

    @jsii.member(jsii_name="resetAllowedPackageNames")
    def reset_allowed_package_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedPackageNames", []))

    @builtins.property
    @jsii.member(jsii_name="allowAllPackageNamesInput")
    def allow_all_package_names_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllPackageNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedPackageNamesInput")
    def allowed_package_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedPackageNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAllPackageNames")
    def allow_all_package_names(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAllPackageNames"))

    @allow_all_package_names.setter
    def allow_all_package_names(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e8d95eac66ad17e6e6a6dec3d9561c291bda8548c2e332a44c73c0114eb3bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAllPackageNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedPackageNames")
    def allowed_package_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedPackageNames"))

    @allowed_package_names.setter
    def allowed_package_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676190f25d17a94bee95d6b4c3ece723121ed34e05b7e219007c996254e2394d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedPackageNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RecaptchaEnterpriseKeyAndroidSettings]:
        return typing.cast(typing.Optional[RecaptchaEnterpriseKeyAndroidSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RecaptchaEnterpriseKeyAndroidSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a0a82dc13a9d21758a124d57a6178eac52eca251fb78bbb8e69ef5a23e19d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKeyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "android_settings": "androidSettings",
        "id": "id",
        "ios_settings": "iosSettings",
        "labels": "labels",
        "project": "project",
        "testing_options": "testingOptions",
        "timeouts": "timeouts",
        "waf_settings": "wafSettings",
        "web_settings": "webSettings",
    },
)
class RecaptchaEnterpriseKeyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        android_settings: typing.Optional[typing.Union[RecaptchaEnterpriseKeyAndroidSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ios_settings: typing.Optional[typing.Union["RecaptchaEnterpriseKeyIosSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        testing_options: typing.Optional[typing.Union["RecaptchaEnterpriseKeyTestingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["RecaptchaEnterpriseKeyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        waf_settings: typing.Optional[typing.Union["RecaptchaEnterpriseKeyWafSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        web_settings: typing.Optional[typing.Union["RecaptchaEnterpriseKeyWebSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Human-readable display name of this key. Modifiable by user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#display_name RecaptchaEnterpriseKey#display_name}
        :param android_settings: android_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#android_settings RecaptchaEnterpriseKey#android_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#id RecaptchaEnterpriseKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ios_settings: ios_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#ios_settings RecaptchaEnterpriseKey#ios_settings}
        :param labels: See `Creating and managing labels <https://cloud.google.com/recaptcha-enterprise/docs/labels>`_. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#labels RecaptchaEnterpriseKey#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#project RecaptchaEnterpriseKey#project}
        :param testing_options: testing_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#testing_options RecaptchaEnterpriseKey#testing_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#timeouts RecaptchaEnterpriseKey#timeouts}
        :param waf_settings: waf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#waf_settings RecaptchaEnterpriseKey#waf_settings}
        :param web_settings: web_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#web_settings RecaptchaEnterpriseKey#web_settings}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(android_settings, dict):
            android_settings = RecaptchaEnterpriseKeyAndroidSettings(**android_settings)
        if isinstance(ios_settings, dict):
            ios_settings = RecaptchaEnterpriseKeyIosSettings(**ios_settings)
        if isinstance(testing_options, dict):
            testing_options = RecaptchaEnterpriseKeyTestingOptions(**testing_options)
        if isinstance(timeouts, dict):
            timeouts = RecaptchaEnterpriseKeyTimeouts(**timeouts)
        if isinstance(waf_settings, dict):
            waf_settings = RecaptchaEnterpriseKeyWafSettings(**waf_settings)
        if isinstance(web_settings, dict):
            web_settings = RecaptchaEnterpriseKeyWebSettings(**web_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3142d313cf6f6a955948dba1623881bab431735a181718d0b7ae590b9855dafc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument android_settings", value=android_settings, expected_type=type_hints["android_settings"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ios_settings", value=ios_settings, expected_type=type_hints["ios_settings"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument testing_options", value=testing_options, expected_type=type_hints["testing_options"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument waf_settings", value=waf_settings, expected_type=type_hints["waf_settings"])
            check_type(argname="argument web_settings", value=web_settings, expected_type=type_hints["web_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
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
        if android_settings is not None:
            self._values["android_settings"] = android_settings
        if id is not None:
            self._values["id"] = id
        if ios_settings is not None:
            self._values["ios_settings"] = ios_settings
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if testing_options is not None:
            self._values["testing_options"] = testing_options
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if waf_settings is not None:
            self._values["waf_settings"] = waf_settings
        if web_settings is not None:
            self._values["web_settings"] = web_settings

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
    def display_name(self) -> builtins.str:
        '''Human-readable display name of this key. Modifiable by user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#display_name RecaptchaEnterpriseKey#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def android_settings(
        self,
    ) -> typing.Optional[RecaptchaEnterpriseKeyAndroidSettings]:
        '''android_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#android_settings RecaptchaEnterpriseKey#android_settings}
        '''
        result = self._values.get("android_settings")
        return typing.cast(typing.Optional[RecaptchaEnterpriseKeyAndroidSettings], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#id RecaptchaEnterpriseKey#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ios_settings(self) -> typing.Optional["RecaptchaEnterpriseKeyIosSettings"]:
        '''ios_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#ios_settings RecaptchaEnterpriseKey#ios_settings}
        '''
        result = self._values.get("ios_settings")
        return typing.cast(typing.Optional["RecaptchaEnterpriseKeyIosSettings"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''See `Creating and managing labels <https://cloud.google.com/recaptcha-enterprise/docs/labels>`_.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field ``effective_labels`` for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#labels RecaptchaEnterpriseKey#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#project RecaptchaEnterpriseKey#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def testing_options(
        self,
    ) -> typing.Optional["RecaptchaEnterpriseKeyTestingOptions"]:
        '''testing_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#testing_options RecaptchaEnterpriseKey#testing_options}
        '''
        result = self._values.get("testing_options")
        return typing.cast(typing.Optional["RecaptchaEnterpriseKeyTestingOptions"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RecaptchaEnterpriseKeyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#timeouts RecaptchaEnterpriseKey#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RecaptchaEnterpriseKeyTimeouts"], result)

    @builtins.property
    def waf_settings(self) -> typing.Optional["RecaptchaEnterpriseKeyWafSettings"]:
        '''waf_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#waf_settings RecaptchaEnterpriseKey#waf_settings}
        '''
        result = self._values.get("waf_settings")
        return typing.cast(typing.Optional["RecaptchaEnterpriseKeyWafSettings"], result)

    @builtins.property
    def web_settings(self) -> typing.Optional["RecaptchaEnterpriseKeyWebSettings"]:
        '''web_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#web_settings RecaptchaEnterpriseKey#web_settings}
        '''
        result = self._values.get("web_settings")
        return typing.cast(typing.Optional["RecaptchaEnterpriseKeyWebSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RecaptchaEnterpriseKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKeyIosSettings",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all_bundle_ids": "allowAllBundleIds",
        "allowed_bundle_ids": "allowedBundleIds",
    },
)
class RecaptchaEnterpriseKeyIosSettings:
    def __init__(
        self,
        *,
        allow_all_bundle_ids: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_bundle_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allow_all_bundle_ids: If set to true, it means allowed_bundle_ids will not be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allow_all_bundle_ids RecaptchaEnterpriseKey#allow_all_bundle_ids}
        :param allowed_bundle_ids: iOS bundle ids of apps allowed to use the key. Example: 'com.companyname.productname.appname'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allowed_bundle_ids RecaptchaEnterpriseKey#allowed_bundle_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f7469d8da85d7896e8650b771caa4fb2dd7cd924b16fbcd14eb65f7fed7faf)
            check_type(argname="argument allow_all_bundle_ids", value=allow_all_bundle_ids, expected_type=type_hints["allow_all_bundle_ids"])
            check_type(argname="argument allowed_bundle_ids", value=allowed_bundle_ids, expected_type=type_hints["allowed_bundle_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_all_bundle_ids is not None:
            self._values["allow_all_bundle_ids"] = allow_all_bundle_ids
        if allowed_bundle_ids is not None:
            self._values["allowed_bundle_ids"] = allowed_bundle_ids

    @builtins.property
    def allow_all_bundle_ids(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, it means allowed_bundle_ids will not be enforced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allow_all_bundle_ids RecaptchaEnterpriseKey#allow_all_bundle_ids}
        '''
        result = self._values.get("allow_all_bundle_ids")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_bundle_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''iOS bundle ids of apps allowed to use the key. Example: 'com.companyname.productname.appname'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allowed_bundle_ids RecaptchaEnterpriseKey#allowed_bundle_ids}
        '''
        result = self._values.get("allowed_bundle_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RecaptchaEnterpriseKeyIosSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RecaptchaEnterpriseKeyIosSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKeyIosSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b1c564d7d10fdbcab8a2632efca10d357ed48e94085ad96139f5b032be36645)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowAllBundleIds")
    def reset_allow_all_bundle_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAllBundleIds", []))

    @jsii.member(jsii_name="resetAllowedBundleIds")
    def reset_allowed_bundle_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedBundleIds", []))

    @builtins.property
    @jsii.member(jsii_name="allowAllBundleIdsInput")
    def allow_all_bundle_ids_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllBundleIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedBundleIdsInput")
    def allowed_bundle_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedBundleIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAllBundleIds")
    def allow_all_bundle_ids(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAllBundleIds"))

    @allow_all_bundle_ids.setter
    def allow_all_bundle_ids(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c59d011e57498bb6fd4e463c9d20fb9ce8180c4c60c53358d473b21b4e77ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAllBundleIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedBundleIds")
    def allowed_bundle_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedBundleIds"))

    @allowed_bundle_ids.setter
    def allowed_bundle_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__842f6760fdae1302954cfa3a3b0c30e8c161f44448a00f8626cbb25714dbeb84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedBundleIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RecaptchaEnterpriseKeyIosSettings]:
        return typing.cast(typing.Optional[RecaptchaEnterpriseKeyIosSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RecaptchaEnterpriseKeyIosSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f463d048cdf02c09a8574d750ab96d6deae6418171ca08c27873029376c3713c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKeyTestingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "testing_challenge": "testingChallenge",
        "testing_score": "testingScore",
    },
)
class RecaptchaEnterpriseKeyTestingOptions:
    def __init__(
        self,
        *,
        testing_challenge: typing.Optional[builtins.str] = None,
        testing_score: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param testing_challenge: For challenge-based keys only (CHECKBOX, INVISIBLE), all challenge requests for this site will return nocaptcha if NOCAPTCHA, or an unsolvable challenge if UNSOLVABLE_CHALLENGE. Possible values: TESTING_CHALLENGE_UNSPECIFIED, NOCAPTCHA, UNSOLVABLE_CHALLENGE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#testing_challenge RecaptchaEnterpriseKey#testing_challenge}
        :param testing_score: All assessments for this Key will return this score. Must be between 0 (likely not legitimate) and 1 (likely legitimate) inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#testing_score RecaptchaEnterpriseKey#testing_score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b64d199c825b4b6430c9377a027e02bcd5e9e0353620eaeba739b704b185cf5)
            check_type(argname="argument testing_challenge", value=testing_challenge, expected_type=type_hints["testing_challenge"])
            check_type(argname="argument testing_score", value=testing_score, expected_type=type_hints["testing_score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if testing_challenge is not None:
            self._values["testing_challenge"] = testing_challenge
        if testing_score is not None:
            self._values["testing_score"] = testing_score

    @builtins.property
    def testing_challenge(self) -> typing.Optional[builtins.str]:
        '''For challenge-based keys only (CHECKBOX, INVISIBLE), all challenge requests for this site will return nocaptcha if NOCAPTCHA, or an unsolvable challenge if UNSOLVABLE_CHALLENGE.

        Possible values: TESTING_CHALLENGE_UNSPECIFIED, NOCAPTCHA, UNSOLVABLE_CHALLENGE

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#testing_challenge RecaptchaEnterpriseKey#testing_challenge}
        '''
        result = self._values.get("testing_challenge")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def testing_score(self) -> typing.Optional[jsii.Number]:
        '''All assessments for this Key will return this score.

        Must be between 0 (likely not legitimate) and 1 (likely legitimate) inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#testing_score RecaptchaEnterpriseKey#testing_score}
        '''
        result = self._values.get("testing_score")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RecaptchaEnterpriseKeyTestingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RecaptchaEnterpriseKeyTestingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKeyTestingOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00eba8d3dfcbd7ca7ab86e61055982630cc59e6be59db847a54541a6d0967db5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTestingChallenge")
    def reset_testing_challenge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestingChallenge", []))

    @jsii.member(jsii_name="resetTestingScore")
    def reset_testing_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestingScore", []))

    @builtins.property
    @jsii.member(jsii_name="testingChallengeInput")
    def testing_challenge_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "testingChallengeInput"))

    @builtins.property
    @jsii.member(jsii_name="testingScoreInput")
    def testing_score_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "testingScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="testingChallenge")
    def testing_challenge(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "testingChallenge"))

    @testing_challenge.setter
    def testing_challenge(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8d4ddf483dc193ac9af7bdd2ee6acc8ac952164805f5082751961a9c0d74de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testingChallenge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="testingScore")
    def testing_score(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "testingScore"))

    @testing_score.setter
    def testing_score(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f58c132cd2af2cdd3f63c11b29fef559ff611f99c056fcdf769c4d0e1f14871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testingScore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RecaptchaEnterpriseKeyTestingOptions]:
        return typing.cast(typing.Optional[RecaptchaEnterpriseKeyTestingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RecaptchaEnterpriseKeyTestingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1956fb7e29bf7444b7bbfaab0caa7b4debcc93a758abd43233c4ba21cf232914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKeyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class RecaptchaEnterpriseKeyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#create RecaptchaEnterpriseKey#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#delete RecaptchaEnterpriseKey#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#update RecaptchaEnterpriseKey#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cddf0258dc5aa6688ae260464e55bfe39807ac8f1b02fa4d18d382c929465a00)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#create RecaptchaEnterpriseKey#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#delete RecaptchaEnterpriseKey#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#update RecaptchaEnterpriseKey#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RecaptchaEnterpriseKeyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RecaptchaEnterpriseKeyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKeyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__171589ec1079ba7cff4f80561ef8b4f4732b0e35ef47046c1f796ade68798473)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fe88bc857be38e47b741ffd319111e66f2fe582340f632f9dbe0e2df90c99fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab89695a5195e4c651d7d7e132b4d36ef1389f1ef4d7ca2284dab644793b7d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c6494a2c4ea3898d5b635d7774d7228ad9cdcefedbfd5e0870d0a489c42336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RecaptchaEnterpriseKeyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RecaptchaEnterpriseKeyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RecaptchaEnterpriseKeyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce36a122188907a3045199e98d157620da4162e6ba718f21777f84e0e1f8dbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKeyWafSettings",
    jsii_struct_bases=[],
    name_mapping={"waf_feature": "wafFeature", "waf_service": "wafService"},
)
class RecaptchaEnterpriseKeyWafSettings:
    def __init__(self, *, waf_feature: builtins.str, waf_service: builtins.str) -> None:
        '''
        :param waf_feature: Supported WAF features. For more information, see https://cloud.google.com/recaptcha-enterprise/docs/usecase#comparison_of_features. Possible values: CHALLENGE_PAGE, SESSION_TOKEN, ACTION_TOKEN, EXPRESS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#waf_feature RecaptchaEnterpriseKey#waf_feature}
        :param waf_service: The WAF service that uses this key. Possible values: CA, FASTLY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#waf_service RecaptchaEnterpriseKey#waf_service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d68bde468629f07e996ef8189b074930fff076d74f67c1cfdfb70455971245)
            check_type(argname="argument waf_feature", value=waf_feature, expected_type=type_hints["waf_feature"])
            check_type(argname="argument waf_service", value=waf_service, expected_type=type_hints["waf_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "waf_feature": waf_feature,
            "waf_service": waf_service,
        }

    @builtins.property
    def waf_feature(self) -> builtins.str:
        '''Supported WAF features. For more information, see https://cloud.google.com/recaptcha-enterprise/docs/usecase#comparison_of_features. Possible values: CHALLENGE_PAGE, SESSION_TOKEN, ACTION_TOKEN, EXPRESS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#waf_feature RecaptchaEnterpriseKey#waf_feature}
        '''
        result = self._values.get("waf_feature")
        assert result is not None, "Required property 'waf_feature' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def waf_service(self) -> builtins.str:
        '''The WAF service that uses this key. Possible values: CA, FASTLY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#waf_service RecaptchaEnterpriseKey#waf_service}
        '''
        result = self._values.get("waf_service")
        assert result is not None, "Required property 'waf_service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RecaptchaEnterpriseKeyWafSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RecaptchaEnterpriseKeyWafSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKeyWafSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30075dc608ddf6d826e3f0596fd6f236ef3a201a5129e4572dfbfd0e07c92d2f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="wafFeatureInput")
    def waf_feature_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "wafFeatureInput"))

    @builtins.property
    @jsii.member(jsii_name="wafServiceInput")
    def waf_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "wafServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="wafFeature")
    def waf_feature(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wafFeature"))

    @waf_feature.setter
    def waf_feature(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf25cb810272963943e3acf393d3753c389f08b6debd0b98fffb8f6b0b473994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wafFeature", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wafService")
    def waf_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wafService"))

    @waf_service.setter
    def waf_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e82aae8c6205c72a7476751b67e8386c5b2da50b07781e34d83fbe79b5ab615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wafService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RecaptchaEnterpriseKeyWafSettings]:
        return typing.cast(typing.Optional[RecaptchaEnterpriseKeyWafSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RecaptchaEnterpriseKeyWafSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b08862f32a1be2defa2d94ba2732bca6af3c1dea2a480687da2db3f590c424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKeyWebSettings",
    jsii_struct_bases=[],
    name_mapping={
        "integration_type": "integrationType",
        "allow_all_domains": "allowAllDomains",
        "allow_amp_traffic": "allowAmpTraffic",
        "allowed_domains": "allowedDomains",
        "challenge_security_preference": "challengeSecurityPreference",
    },
)
class RecaptchaEnterpriseKeyWebSettings:
    def __init__(
        self,
        *,
        integration_type: builtins.str,
        allow_all_domains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_amp_traffic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        challenge_security_preference: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param integration_type: Required. Describes how this key is integrated with the website. Possible values: SCORE, CHECKBOX, INVISIBLE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#integration_type RecaptchaEnterpriseKey#integration_type}
        :param allow_all_domains: If set to true, it means allowed_domains will not be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allow_all_domains RecaptchaEnterpriseKey#allow_all_domains}
        :param allow_amp_traffic: If set to true, the key can be used on AMP (Accelerated Mobile Pages) websites. This is supported only for the SCORE integration type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allow_amp_traffic RecaptchaEnterpriseKey#allow_amp_traffic}
        :param allowed_domains: Domains or subdomains of websites allowed to use the key. All subdomains of an allowed domain are automatically allowed. A valid domain requires a host and must not include any path, port, query or fragment. Examples: 'example.com' or 'subdomain.example.com' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allowed_domains RecaptchaEnterpriseKey#allowed_domains}
        :param challenge_security_preference: Settings for the frequency and difficulty at which this key triggers captcha challenges. This should only be specified for IntegrationTypes CHECKBOX and INVISIBLE. Possible values: CHALLENGE_SECURITY_PREFERENCE_UNSPECIFIED, USABILITY, BALANCE, SECURITY Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#challenge_security_preference RecaptchaEnterpriseKey#challenge_security_preference}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb862d097b7d174429ab7236fe7fa2d41c53fff5dc900d4ebdd2ea192257aaf)
            check_type(argname="argument integration_type", value=integration_type, expected_type=type_hints["integration_type"])
            check_type(argname="argument allow_all_domains", value=allow_all_domains, expected_type=type_hints["allow_all_domains"])
            check_type(argname="argument allow_amp_traffic", value=allow_amp_traffic, expected_type=type_hints["allow_amp_traffic"])
            check_type(argname="argument allowed_domains", value=allowed_domains, expected_type=type_hints["allowed_domains"])
            check_type(argname="argument challenge_security_preference", value=challenge_security_preference, expected_type=type_hints["challenge_security_preference"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "integration_type": integration_type,
        }
        if allow_all_domains is not None:
            self._values["allow_all_domains"] = allow_all_domains
        if allow_amp_traffic is not None:
            self._values["allow_amp_traffic"] = allow_amp_traffic
        if allowed_domains is not None:
            self._values["allowed_domains"] = allowed_domains
        if challenge_security_preference is not None:
            self._values["challenge_security_preference"] = challenge_security_preference

    @builtins.property
    def integration_type(self) -> builtins.str:
        '''Required. Describes how this key is integrated with the website. Possible values: SCORE, CHECKBOX, INVISIBLE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#integration_type RecaptchaEnterpriseKey#integration_type}
        '''
        result = self._values.get("integration_type")
        assert result is not None, "Required property 'integration_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_all_domains(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, it means allowed_domains will not be enforced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allow_all_domains RecaptchaEnterpriseKey#allow_all_domains}
        '''
        result = self._values.get("allow_all_domains")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_amp_traffic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the key can be used on AMP (Accelerated Mobile Pages) websites.

        This is supported only for the SCORE integration type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allow_amp_traffic RecaptchaEnterpriseKey#allow_amp_traffic}
        '''
        result = self._values.get("allow_amp_traffic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Domains or subdomains of websites allowed to use the key.

        All subdomains of an allowed domain are automatically allowed. A valid domain requires a host and must not include any path, port, query or fragment. Examples: 'example.com' or 'subdomain.example.com'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#allowed_domains RecaptchaEnterpriseKey#allowed_domains}
        '''
        result = self._values.get("allowed_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def challenge_security_preference(self) -> typing.Optional[builtins.str]:
        '''Settings for the frequency and difficulty at which this key triggers captcha challenges.

        This should only be specified for IntegrationTypes CHECKBOX and INVISIBLE. Possible values: CHALLENGE_SECURITY_PREFERENCE_UNSPECIFIED, USABILITY, BALANCE, SECURITY

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/recaptcha_enterprise_key#challenge_security_preference RecaptchaEnterpriseKey#challenge_security_preference}
        '''
        result = self._values.get("challenge_security_preference")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RecaptchaEnterpriseKeyWebSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RecaptchaEnterpriseKeyWebSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.recaptchaEnterpriseKey.RecaptchaEnterpriseKeyWebSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2aeff8a5addf3d21b125e8d848f59c9e37bb26c1c1da89ea058ac709dc88ba9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowAllDomains")
    def reset_allow_all_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAllDomains", []))

    @jsii.member(jsii_name="resetAllowAmpTraffic")
    def reset_allow_amp_traffic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAmpTraffic", []))

    @jsii.member(jsii_name="resetAllowedDomains")
    def reset_allowed_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedDomains", []))

    @jsii.member(jsii_name="resetChallengeSecurityPreference")
    def reset_challenge_security_preference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChallengeSecurityPreference", []))

    @builtins.property
    @jsii.member(jsii_name="allowAllDomainsInput")
    def allow_all_domains_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllDomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAmpTrafficInput")
    def allow_amp_traffic_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAmpTrafficInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedDomainsInput")
    def allowed_domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedDomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="challengeSecurityPreferenceInput")
    def challenge_security_preference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "challengeSecurityPreferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationTypeInput")
    def integration_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAllDomains")
    def allow_all_domains(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAllDomains"))

    @allow_all_domains.setter
    def allow_all_domains(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b80952e17066d10334c5b4b9d670bef2b734310823dcf7407da29a6769aeb647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAllDomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowAmpTraffic")
    def allow_amp_traffic(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAmpTraffic"))

    @allow_amp_traffic.setter
    def allow_amp_traffic(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6ab57f74474e93381cb99fe1972c634d53f1b79b85f55ba057217946b528fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAmpTraffic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedDomains")
    def allowed_domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedDomains"))

    @allowed_domains.setter
    def allowed_domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3fd084a2aa0e8e138ea43c6e79b4a9afe6663de262fa6a5e0210a3d015f081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedDomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="challengeSecurityPreference")
    def challenge_security_preference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "challengeSecurityPreference"))

    @challenge_security_preference.setter
    def challenge_security_preference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93170615a14eb13b6db8fcd7b4275091c919bd4dc0d8f4ecd4da1a92690c6867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "challengeSecurityPreference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def integration_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationType"))

    @integration_type.setter
    def integration_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c807b5700d6ed8752d539479ded969d661b3b5f799b7a07bb56ce4f0a04bc334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RecaptchaEnterpriseKeyWebSettings]:
        return typing.cast(typing.Optional[RecaptchaEnterpriseKeyWebSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RecaptchaEnterpriseKeyWebSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c09ec9c0183ddcf589d05ddfdd2ddd0cc608d770498e80fccc65c4ec32185d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RecaptchaEnterpriseKey",
    "RecaptchaEnterpriseKeyAndroidSettings",
    "RecaptchaEnterpriseKeyAndroidSettingsOutputReference",
    "RecaptchaEnterpriseKeyConfig",
    "RecaptchaEnterpriseKeyIosSettings",
    "RecaptchaEnterpriseKeyIosSettingsOutputReference",
    "RecaptchaEnterpriseKeyTestingOptions",
    "RecaptchaEnterpriseKeyTestingOptionsOutputReference",
    "RecaptchaEnterpriseKeyTimeouts",
    "RecaptchaEnterpriseKeyTimeoutsOutputReference",
    "RecaptchaEnterpriseKeyWafSettings",
    "RecaptchaEnterpriseKeyWafSettingsOutputReference",
    "RecaptchaEnterpriseKeyWebSettings",
    "RecaptchaEnterpriseKeyWebSettingsOutputReference",
]

publication.publish()

def _typecheckingstub__87f13f297bf3284053793b26a6d43e0d96f91b5d4db7fe71e47f010ea5dd2a64(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    android_settings: typing.Optional[typing.Union[RecaptchaEnterpriseKeyAndroidSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ios_settings: typing.Optional[typing.Union[RecaptchaEnterpriseKeyIosSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    testing_options: typing.Optional[typing.Union[RecaptchaEnterpriseKeyTestingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[RecaptchaEnterpriseKeyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    waf_settings: typing.Optional[typing.Union[RecaptchaEnterpriseKeyWafSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    web_settings: typing.Optional[typing.Union[RecaptchaEnterpriseKeyWebSettings, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__fa743c036f81fb8287b1c4dd3d54f429caf19b74befc39113b3e41ca76f232c2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1164c41731106258ccde0037dcc92d696bccb1b3277b99a9da83f289288ee69e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed74543a0677a0ac4e112dd6a727fc8a4f7c44f10f05104f184f0a24f485c3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545418e133c90cd201d9d677eebb09df40777a830be2e9d724b9b8e28b3e8ace(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1be5b209b270d929053ecc7d3f1b22c7929423d4d523d9bc8d9e361c1372b5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c482240e855ef4e798d9c94acfc9080c70f08bfb5d8b36d5924579788fcd485(
    *,
    allow_all_package_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_package_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4786e8c6a8480f8737c7f3cd2195c1391b1ed408fd50725ed448c5b87f756086(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e8d95eac66ad17e6e6a6dec3d9561c291bda8548c2e332a44c73c0114eb3bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676190f25d17a94bee95d6b4c3ece723121ed34e05b7e219007c996254e2394d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a0a82dc13a9d21758a124d57a6178eac52eca251fb78bbb8e69ef5a23e19d4(
    value: typing.Optional[RecaptchaEnterpriseKeyAndroidSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3142d313cf6f6a955948dba1623881bab431735a181718d0b7ae590b9855dafc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    android_settings: typing.Optional[typing.Union[RecaptchaEnterpriseKeyAndroidSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ios_settings: typing.Optional[typing.Union[RecaptchaEnterpriseKeyIosSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    testing_options: typing.Optional[typing.Union[RecaptchaEnterpriseKeyTestingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[RecaptchaEnterpriseKeyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    waf_settings: typing.Optional[typing.Union[RecaptchaEnterpriseKeyWafSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    web_settings: typing.Optional[typing.Union[RecaptchaEnterpriseKeyWebSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f7469d8da85d7896e8650b771caa4fb2dd7cd924b16fbcd14eb65f7fed7faf(
    *,
    allow_all_bundle_ids: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_bundle_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1c564d7d10fdbcab8a2632efca10d357ed48e94085ad96139f5b032be36645(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c59d011e57498bb6fd4e463c9d20fb9ce8180c4c60c53358d473b21b4e77ab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842f6760fdae1302954cfa3a3b0c30e8c161f44448a00f8626cbb25714dbeb84(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f463d048cdf02c09a8574d750ab96d6deae6418171ca08c27873029376c3713c(
    value: typing.Optional[RecaptchaEnterpriseKeyIosSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b64d199c825b4b6430c9377a027e02bcd5e9e0353620eaeba739b704b185cf5(
    *,
    testing_challenge: typing.Optional[builtins.str] = None,
    testing_score: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00eba8d3dfcbd7ca7ab86e61055982630cc59e6be59db847a54541a6d0967db5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8d4ddf483dc193ac9af7bdd2ee6acc8ac952164805f5082751961a9c0d74de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f58c132cd2af2cdd3f63c11b29fef559ff611f99c056fcdf769c4d0e1f14871(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1956fb7e29bf7444b7bbfaab0caa7b4debcc93a758abd43233c4ba21cf232914(
    value: typing.Optional[RecaptchaEnterpriseKeyTestingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cddf0258dc5aa6688ae260464e55bfe39807ac8f1b02fa4d18d382c929465a00(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171589ec1079ba7cff4f80561ef8b4f4732b0e35ef47046c1f796ade68798473(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe88bc857be38e47b741ffd319111e66f2fe582340f632f9dbe0e2df90c99fca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab89695a5195e4c651d7d7e132b4d36ef1389f1ef4d7ca2284dab644793b7d52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c6494a2c4ea3898d5b635d7774d7228ad9cdcefedbfd5e0870d0a489c42336(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce36a122188907a3045199e98d157620da4162e6ba718f21777f84e0e1f8dbd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RecaptchaEnterpriseKeyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d68bde468629f07e996ef8189b074930fff076d74f67c1cfdfb70455971245(
    *,
    waf_feature: builtins.str,
    waf_service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30075dc608ddf6d826e3f0596fd6f236ef3a201a5129e4572dfbfd0e07c92d2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf25cb810272963943e3acf393d3753c389f08b6debd0b98fffb8f6b0b473994(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e82aae8c6205c72a7476751b67e8386c5b2da50b07781e34d83fbe79b5ab615(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b08862f32a1be2defa2d94ba2732bca6af3c1dea2a480687da2db3f590c424(
    value: typing.Optional[RecaptchaEnterpriseKeyWafSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb862d097b7d174429ab7236fe7fa2d41c53fff5dc900d4ebdd2ea192257aaf(
    *,
    integration_type: builtins.str,
    allow_all_domains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_amp_traffic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    challenge_security_preference: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aeff8a5addf3d21b125e8d848f59c9e37bb26c1c1da89ea058ac709dc88ba9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80952e17066d10334c5b4b9d670bef2b734310823dcf7407da29a6769aeb647(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6ab57f74474e93381cb99fe1972c634d53f1b79b85f55ba057217946b528fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3fd084a2aa0e8e138ea43c6e79b4a9afe6663de262fa6a5e0210a3d015f081(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93170615a14eb13b6db8fcd7b4275091c919bd4dc0d8f4ecd4da1a92690c6867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c807b5700d6ed8752d539479ded969d661b3b5f799b7a07bb56ce4f0a04bc334(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09ec9c0183ddcf589d05ddfdd2ddd0cc608d770498e80fccc65c4ec32185d0b(
    value: typing.Optional[RecaptchaEnterpriseKeyWebSettings],
) -> None:
    """Type checking stubs"""
    pass
