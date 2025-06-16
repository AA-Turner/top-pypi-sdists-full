r'''
# `google_recaptcha_enterprise_key`

Refer to the Terraform Registry for docs: [`google_recaptcha_enterprise_key`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key).
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


class GoogleRecaptchaEnterpriseKey(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKey",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key google_recaptcha_enterprise_key}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        android_settings: typing.Optional[typing.Union["GoogleRecaptchaEnterpriseKeyAndroidSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ios_settings: typing.Optional[typing.Union["GoogleRecaptchaEnterpriseKeyIosSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        testing_options: typing.Optional[typing.Union["GoogleRecaptchaEnterpriseKeyTestingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleRecaptchaEnterpriseKeyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        waf_settings: typing.Optional[typing.Union["GoogleRecaptchaEnterpriseKeyWafSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        web_settings: typing.Optional[typing.Union["GoogleRecaptchaEnterpriseKeyWebSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key google_recaptcha_enterprise_key} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Human-readable display name of this key. Modifiable by user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#display_name GoogleRecaptchaEnterpriseKey#display_name}
        :param android_settings: android_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#android_settings GoogleRecaptchaEnterpriseKey#android_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#id GoogleRecaptchaEnterpriseKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ios_settings: ios_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#ios_settings GoogleRecaptchaEnterpriseKey#ios_settings}
        :param labels: See `Creating and managing labels <https://cloud.google.com/recaptcha-enterprise/docs/labels>`_. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#labels GoogleRecaptchaEnterpriseKey#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#project GoogleRecaptchaEnterpriseKey#project}
        :param testing_options: testing_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#testing_options GoogleRecaptchaEnterpriseKey#testing_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#timeouts GoogleRecaptchaEnterpriseKey#timeouts}
        :param waf_settings: waf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#waf_settings GoogleRecaptchaEnterpriseKey#waf_settings}
        :param web_settings: web_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#web_settings GoogleRecaptchaEnterpriseKey#web_settings}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd54fb351ed940d839c6a7820d2ef478eae314af891cbab500e60b83b3b9fd64)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleRecaptchaEnterpriseKeyConfig(
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
        '''Generates CDKTF code for importing a GoogleRecaptchaEnterpriseKey resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleRecaptchaEnterpriseKey to import.
        :param import_from_id: The id of the existing GoogleRecaptchaEnterpriseKey that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleRecaptchaEnterpriseKey to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd05b1a9d5baa0a8f9430182ef9a60d037a535463dda28dc0a891dd13bee00a0)
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
        :param allow_all_package_names: If set to true, it means allowed_package_names will not be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allow_all_package_names GoogleRecaptchaEnterpriseKey#allow_all_package_names}
        :param allowed_package_names: Android package names of apps allowed to use the key. Example: 'com.companyname.appname'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allowed_package_names GoogleRecaptchaEnterpriseKey#allowed_package_names}
        '''
        value = GoogleRecaptchaEnterpriseKeyAndroidSettings(
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
        :param allow_all_bundle_ids: If set to true, it means allowed_bundle_ids will not be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allow_all_bundle_ids GoogleRecaptchaEnterpriseKey#allow_all_bundle_ids}
        :param allowed_bundle_ids: iOS bundle ids of apps allowed to use the key. Example: 'com.companyname.productname.appname'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allowed_bundle_ids GoogleRecaptchaEnterpriseKey#allowed_bundle_ids}
        '''
        value = GoogleRecaptchaEnterpriseKeyIosSettings(
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
        :param testing_challenge: For challenge-based keys only (CHECKBOX, INVISIBLE), all challenge requests for this site will return nocaptcha if NOCAPTCHA, or an unsolvable challenge if UNSOLVABLE_CHALLENGE. Possible values: TESTING_CHALLENGE_UNSPECIFIED, NOCAPTCHA, UNSOLVABLE_CHALLENGE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#testing_challenge GoogleRecaptchaEnterpriseKey#testing_challenge}
        :param testing_score: All assessments for this Key will return this score. Must be between 0 (likely not legitimate) and 1 (likely legitimate) inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#testing_score GoogleRecaptchaEnterpriseKey#testing_score}
        '''
        value = GoogleRecaptchaEnterpriseKeyTestingOptions(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#create GoogleRecaptchaEnterpriseKey#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#delete GoogleRecaptchaEnterpriseKey#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#update GoogleRecaptchaEnterpriseKey#update}.
        '''
        value = GoogleRecaptchaEnterpriseKeyTimeouts(
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
        :param waf_feature: Supported WAF features. For more information, see https://cloud.google.com/recaptcha-enterprise/docs/usecase#comparison_of_features. Possible values: CHALLENGE_PAGE, SESSION_TOKEN, ACTION_TOKEN, EXPRESS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#waf_feature GoogleRecaptchaEnterpriseKey#waf_feature}
        :param waf_service: The WAF service that uses this key. Possible values: CA, FASTLY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#waf_service GoogleRecaptchaEnterpriseKey#waf_service}
        '''
        value = GoogleRecaptchaEnterpriseKeyWafSettings(
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
        :param integration_type: Required. Describes how this key is integrated with the website. Possible values: SCORE, CHECKBOX, INVISIBLE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#integration_type GoogleRecaptchaEnterpriseKey#integration_type}
        :param allow_all_domains: If set to true, it means allowed_domains will not be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allow_all_domains GoogleRecaptchaEnterpriseKey#allow_all_domains}
        :param allow_amp_traffic: If set to true, the key can be used on AMP (Accelerated Mobile Pages) websites. This is supported only for the SCORE integration type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allow_amp_traffic GoogleRecaptchaEnterpriseKey#allow_amp_traffic}
        :param allowed_domains: Domains or subdomains of websites allowed to use the key. All subdomains of an allowed domain are automatically allowed. A valid domain requires a host and must not include any path, port, query or fragment. Examples: 'example.com' or 'subdomain.example.com' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allowed_domains GoogleRecaptchaEnterpriseKey#allowed_domains}
        :param challenge_security_preference: Settings for the frequency and difficulty at which this key triggers captcha challenges. This should only be specified for IntegrationTypes CHECKBOX and INVISIBLE. Possible values: CHALLENGE_SECURITY_PREFERENCE_UNSPECIFIED, USABILITY, BALANCE, SECURITY Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#challenge_security_preference GoogleRecaptchaEnterpriseKey#challenge_security_preference}
        '''
        value = GoogleRecaptchaEnterpriseKeyWebSettings(
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
    ) -> "GoogleRecaptchaEnterpriseKeyAndroidSettingsOutputReference":
        return typing.cast("GoogleRecaptchaEnterpriseKeyAndroidSettingsOutputReference", jsii.get(self, "androidSettings"))

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
    def ios_settings(self) -> "GoogleRecaptchaEnterpriseKeyIosSettingsOutputReference":
        return typing.cast("GoogleRecaptchaEnterpriseKeyIosSettingsOutputReference", jsii.get(self, "iosSettings"))

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
    def testing_options(
        self,
    ) -> "GoogleRecaptchaEnterpriseKeyTestingOptionsOutputReference":
        return typing.cast("GoogleRecaptchaEnterpriseKeyTestingOptionsOutputReference", jsii.get(self, "testingOptions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleRecaptchaEnterpriseKeyTimeoutsOutputReference":
        return typing.cast("GoogleRecaptchaEnterpriseKeyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="wafSettings")
    def waf_settings(self) -> "GoogleRecaptchaEnterpriseKeyWafSettingsOutputReference":
        return typing.cast("GoogleRecaptchaEnterpriseKeyWafSettingsOutputReference", jsii.get(self, "wafSettings"))

    @builtins.property
    @jsii.member(jsii_name="webSettings")
    def web_settings(self) -> "GoogleRecaptchaEnterpriseKeyWebSettingsOutputReference":
        return typing.cast("GoogleRecaptchaEnterpriseKeyWebSettingsOutputReference", jsii.get(self, "webSettings"))

    @builtins.property
    @jsii.member(jsii_name="androidSettingsInput")
    def android_settings_input(
        self,
    ) -> typing.Optional["GoogleRecaptchaEnterpriseKeyAndroidSettings"]:
        return typing.cast(typing.Optional["GoogleRecaptchaEnterpriseKeyAndroidSettings"], jsii.get(self, "androidSettingsInput"))

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
    ) -> typing.Optional["GoogleRecaptchaEnterpriseKeyIosSettings"]:
        return typing.cast(typing.Optional["GoogleRecaptchaEnterpriseKeyIosSettings"], jsii.get(self, "iosSettingsInput"))

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
    ) -> typing.Optional["GoogleRecaptchaEnterpriseKeyTestingOptions"]:
        return typing.cast(typing.Optional["GoogleRecaptchaEnterpriseKeyTestingOptions"], jsii.get(self, "testingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleRecaptchaEnterpriseKeyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleRecaptchaEnterpriseKeyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="wafSettingsInput")
    def waf_settings_input(
        self,
    ) -> typing.Optional["GoogleRecaptchaEnterpriseKeyWafSettings"]:
        return typing.cast(typing.Optional["GoogleRecaptchaEnterpriseKeyWafSettings"], jsii.get(self, "wafSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="webSettingsInput")
    def web_settings_input(
        self,
    ) -> typing.Optional["GoogleRecaptchaEnterpriseKeyWebSettings"]:
        return typing.cast(typing.Optional["GoogleRecaptchaEnterpriseKeyWebSettings"], jsii.get(self, "webSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69caf1781ca6e1789630201006c22a144c1f569f93e33f22bc4f3573013fd481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b42b92d9637cfc0df3eca2e276d9c43eb69b4c99489962af79a77216649707c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73541b981f83cdf78645be957d002eb9b0365b652c17b40fdd6c7f6ae505d551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ebc76ae49c9c88d03c7364bce5f841fbb9aaa47417c45e04498a4f3e03fe95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKeyAndroidSettings",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all_package_names": "allowAllPackageNames",
        "allowed_package_names": "allowedPackageNames",
    },
)
class GoogleRecaptchaEnterpriseKeyAndroidSettings:
    def __init__(
        self,
        *,
        allow_all_package_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_package_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allow_all_package_names: If set to true, it means allowed_package_names will not be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allow_all_package_names GoogleRecaptchaEnterpriseKey#allow_all_package_names}
        :param allowed_package_names: Android package names of apps allowed to use the key. Example: 'com.companyname.appname'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allowed_package_names GoogleRecaptchaEnterpriseKey#allowed_package_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79855b0ff13af718c6db9d267eeafc337744760a55d018665f149f307b2539d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allow_all_package_names GoogleRecaptchaEnterpriseKey#allow_all_package_names}
        '''
        result = self._values.get("allow_all_package_names")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_package_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Android package names of apps allowed to use the key. Example: 'com.companyname.appname'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allowed_package_names GoogleRecaptchaEnterpriseKey#allowed_package_names}
        '''
        result = self._values.get("allowed_package_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRecaptchaEnterpriseKeyAndroidSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRecaptchaEnterpriseKeyAndroidSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKeyAndroidSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27366ba6cf30cda0a01fa7f2987be558641012f39d1fe18be0f15b991eef0c33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2970323bcbb9a6e9b931b95caea35b63918e23a2e0b0542aecdaeafd9c79924a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAllPackageNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedPackageNames")
    def allowed_package_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedPackageNames"))

    @allowed_package_names.setter
    def allowed_package_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd35b8964be8eef333f365284c98636cb4b661461c653b7a29109c806c0dc9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedPackageNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRecaptchaEnterpriseKeyAndroidSettings]:
        return typing.cast(typing.Optional[GoogleRecaptchaEnterpriseKeyAndroidSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRecaptchaEnterpriseKeyAndroidSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d367ddb9beea1e8f8583dc50019801ee45a34d8cd3218ebf8d7851c5a78d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKeyConfig",
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
class GoogleRecaptchaEnterpriseKeyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        android_settings: typing.Optional[typing.Union[GoogleRecaptchaEnterpriseKeyAndroidSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ios_settings: typing.Optional[typing.Union["GoogleRecaptchaEnterpriseKeyIosSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        testing_options: typing.Optional[typing.Union["GoogleRecaptchaEnterpriseKeyTestingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleRecaptchaEnterpriseKeyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        waf_settings: typing.Optional[typing.Union["GoogleRecaptchaEnterpriseKeyWafSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        web_settings: typing.Optional[typing.Union["GoogleRecaptchaEnterpriseKeyWebSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Human-readable display name of this key. Modifiable by user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#display_name GoogleRecaptchaEnterpriseKey#display_name}
        :param android_settings: android_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#android_settings GoogleRecaptchaEnterpriseKey#android_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#id GoogleRecaptchaEnterpriseKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ios_settings: ios_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#ios_settings GoogleRecaptchaEnterpriseKey#ios_settings}
        :param labels: See `Creating and managing labels <https://cloud.google.com/recaptcha-enterprise/docs/labels>`_. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#labels GoogleRecaptchaEnterpriseKey#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#project GoogleRecaptchaEnterpriseKey#project}
        :param testing_options: testing_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#testing_options GoogleRecaptchaEnterpriseKey#testing_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#timeouts GoogleRecaptchaEnterpriseKey#timeouts}
        :param waf_settings: waf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#waf_settings GoogleRecaptchaEnterpriseKey#waf_settings}
        :param web_settings: web_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#web_settings GoogleRecaptchaEnterpriseKey#web_settings}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(android_settings, dict):
            android_settings = GoogleRecaptchaEnterpriseKeyAndroidSettings(**android_settings)
        if isinstance(ios_settings, dict):
            ios_settings = GoogleRecaptchaEnterpriseKeyIosSettings(**ios_settings)
        if isinstance(testing_options, dict):
            testing_options = GoogleRecaptchaEnterpriseKeyTestingOptions(**testing_options)
        if isinstance(timeouts, dict):
            timeouts = GoogleRecaptchaEnterpriseKeyTimeouts(**timeouts)
        if isinstance(waf_settings, dict):
            waf_settings = GoogleRecaptchaEnterpriseKeyWafSettings(**waf_settings)
        if isinstance(web_settings, dict):
            web_settings = GoogleRecaptchaEnterpriseKeyWebSettings(**web_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085dc3073790e7e166da76602cafa0a4e4042e1efb714d93030a4d9745a19b83)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#display_name GoogleRecaptchaEnterpriseKey#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def android_settings(
        self,
    ) -> typing.Optional[GoogleRecaptchaEnterpriseKeyAndroidSettings]:
        '''android_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#android_settings GoogleRecaptchaEnterpriseKey#android_settings}
        '''
        result = self._values.get("android_settings")
        return typing.cast(typing.Optional[GoogleRecaptchaEnterpriseKeyAndroidSettings], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#id GoogleRecaptchaEnterpriseKey#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ios_settings(
        self,
    ) -> typing.Optional["GoogleRecaptchaEnterpriseKeyIosSettings"]:
        '''ios_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#ios_settings GoogleRecaptchaEnterpriseKey#ios_settings}
        '''
        result = self._values.get("ios_settings")
        return typing.cast(typing.Optional["GoogleRecaptchaEnterpriseKeyIosSettings"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''See `Creating and managing labels <https://cloud.google.com/recaptcha-enterprise/docs/labels>`_.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field ``effective_labels`` for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#labels GoogleRecaptchaEnterpriseKey#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#project GoogleRecaptchaEnterpriseKey#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def testing_options(
        self,
    ) -> typing.Optional["GoogleRecaptchaEnterpriseKeyTestingOptions"]:
        '''testing_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#testing_options GoogleRecaptchaEnterpriseKey#testing_options}
        '''
        result = self._values.get("testing_options")
        return typing.cast(typing.Optional["GoogleRecaptchaEnterpriseKeyTestingOptions"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleRecaptchaEnterpriseKeyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#timeouts GoogleRecaptchaEnterpriseKey#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleRecaptchaEnterpriseKeyTimeouts"], result)

    @builtins.property
    def waf_settings(
        self,
    ) -> typing.Optional["GoogleRecaptchaEnterpriseKeyWafSettings"]:
        '''waf_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#waf_settings GoogleRecaptchaEnterpriseKey#waf_settings}
        '''
        result = self._values.get("waf_settings")
        return typing.cast(typing.Optional["GoogleRecaptchaEnterpriseKeyWafSettings"], result)

    @builtins.property
    def web_settings(
        self,
    ) -> typing.Optional["GoogleRecaptchaEnterpriseKeyWebSettings"]:
        '''web_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#web_settings GoogleRecaptchaEnterpriseKey#web_settings}
        '''
        result = self._values.get("web_settings")
        return typing.cast(typing.Optional["GoogleRecaptchaEnterpriseKeyWebSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRecaptchaEnterpriseKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKeyIosSettings",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all_bundle_ids": "allowAllBundleIds",
        "allowed_bundle_ids": "allowedBundleIds",
    },
)
class GoogleRecaptchaEnterpriseKeyIosSettings:
    def __init__(
        self,
        *,
        allow_all_bundle_ids: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_bundle_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allow_all_bundle_ids: If set to true, it means allowed_bundle_ids will not be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allow_all_bundle_ids GoogleRecaptchaEnterpriseKey#allow_all_bundle_ids}
        :param allowed_bundle_ids: iOS bundle ids of apps allowed to use the key. Example: 'com.companyname.productname.appname'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allowed_bundle_ids GoogleRecaptchaEnterpriseKey#allowed_bundle_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd7b040cc59148012158d53076ee1d97d6995f9d1c154375d1560bbcb4b1ff7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allow_all_bundle_ids GoogleRecaptchaEnterpriseKey#allow_all_bundle_ids}
        '''
        result = self._values.get("allow_all_bundle_ids")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_bundle_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''iOS bundle ids of apps allowed to use the key. Example: 'com.companyname.productname.appname'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allowed_bundle_ids GoogleRecaptchaEnterpriseKey#allowed_bundle_ids}
        '''
        result = self._values.get("allowed_bundle_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRecaptchaEnterpriseKeyIosSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRecaptchaEnterpriseKeyIosSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKeyIosSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bec17663fe2f15a4df8e70c4e56d9c2c46a9e4083cf3c36736a7bbec97b293a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c939281e0280f10aa9afecc35ead43989b5e6dc2a43c270e34100990f07bd11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAllBundleIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedBundleIds")
    def allowed_bundle_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedBundleIds"))

    @allowed_bundle_ids.setter
    def allowed_bundle_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2086c293f3fc8d37cffbda8bffcbf44e1b2b5a3cae2507610fc60b50584f871f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedBundleIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRecaptchaEnterpriseKeyIosSettings]:
        return typing.cast(typing.Optional[GoogleRecaptchaEnterpriseKeyIosSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRecaptchaEnterpriseKeyIosSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7edddf3a53fce1ab773e1ed1191bab2a36054d52b157b92f259badf95d1927dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKeyTestingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "testing_challenge": "testingChallenge",
        "testing_score": "testingScore",
    },
)
class GoogleRecaptchaEnterpriseKeyTestingOptions:
    def __init__(
        self,
        *,
        testing_challenge: typing.Optional[builtins.str] = None,
        testing_score: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param testing_challenge: For challenge-based keys only (CHECKBOX, INVISIBLE), all challenge requests for this site will return nocaptcha if NOCAPTCHA, or an unsolvable challenge if UNSOLVABLE_CHALLENGE. Possible values: TESTING_CHALLENGE_UNSPECIFIED, NOCAPTCHA, UNSOLVABLE_CHALLENGE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#testing_challenge GoogleRecaptchaEnterpriseKey#testing_challenge}
        :param testing_score: All assessments for this Key will return this score. Must be between 0 (likely not legitimate) and 1 (likely legitimate) inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#testing_score GoogleRecaptchaEnterpriseKey#testing_score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfac70b74a0b4303ccd18e514fac0716fdea956aba7bdd1eb14b4df848f46659)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#testing_challenge GoogleRecaptchaEnterpriseKey#testing_challenge}
        '''
        result = self._values.get("testing_challenge")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def testing_score(self) -> typing.Optional[jsii.Number]:
        '''All assessments for this Key will return this score.

        Must be between 0 (likely not legitimate) and 1 (likely legitimate) inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#testing_score GoogleRecaptchaEnterpriseKey#testing_score}
        '''
        result = self._values.get("testing_score")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRecaptchaEnterpriseKeyTestingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRecaptchaEnterpriseKeyTestingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKeyTestingOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d526d342b83c3c944e9c1078eb79d347e73adc93bb68590278ee5a07f418a56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c46c3f5f4276b832782f0b3254c0b907ebb19c01b9bb8b59807e8b51ca8f5368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testingChallenge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="testingScore")
    def testing_score(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "testingScore"))

    @testing_score.setter
    def testing_score(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e5894389f886273f95a524e48fdd6a0d2b1ae5d5a90fe1a924a3e6fad7cdfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testingScore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRecaptchaEnterpriseKeyTestingOptions]:
        return typing.cast(typing.Optional[GoogleRecaptchaEnterpriseKeyTestingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRecaptchaEnterpriseKeyTestingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372533c312d267c389f7c1376da32d25727eb4f6a54953da554a44b66803cce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKeyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleRecaptchaEnterpriseKeyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#create GoogleRecaptchaEnterpriseKey#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#delete GoogleRecaptchaEnterpriseKey#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#update GoogleRecaptchaEnterpriseKey#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72e61ec5236ac6bf289c3b977261b505e2d4056ea79bfa6e9494788a640c23b7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#create GoogleRecaptchaEnterpriseKey#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#delete GoogleRecaptchaEnterpriseKey#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#update GoogleRecaptchaEnterpriseKey#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRecaptchaEnterpriseKeyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRecaptchaEnterpriseKeyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKeyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c4fcfed8c72fd314670b7006bed81715446bc08b26af8e8db30b058fbcd4331)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9779819c3d4f46ed448e57a70a6641e1e858e2081c6ff07894aaf24a39250d71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de785e4fcc7be0c3c6cabdd621c4dbe3591a094a517c3f5d8a3e4137df82d8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a3dc269647dcc649c8e46e235da87aa96ac4d8ff4d4850ce946333f70a32245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRecaptchaEnterpriseKeyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRecaptchaEnterpriseKeyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRecaptchaEnterpriseKeyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e463e10b7eb7f974d00eeb23724545a941ee3d97582ba72fe1c84f73c69807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKeyWafSettings",
    jsii_struct_bases=[],
    name_mapping={"waf_feature": "wafFeature", "waf_service": "wafService"},
)
class GoogleRecaptchaEnterpriseKeyWafSettings:
    def __init__(self, *, waf_feature: builtins.str, waf_service: builtins.str) -> None:
        '''
        :param waf_feature: Supported WAF features. For more information, see https://cloud.google.com/recaptcha-enterprise/docs/usecase#comparison_of_features. Possible values: CHALLENGE_PAGE, SESSION_TOKEN, ACTION_TOKEN, EXPRESS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#waf_feature GoogleRecaptchaEnterpriseKey#waf_feature}
        :param waf_service: The WAF service that uses this key. Possible values: CA, FASTLY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#waf_service GoogleRecaptchaEnterpriseKey#waf_service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c7726901f488133a6595ed9423d08a38c63bd4e5e1d3c58e065ccb2aa8d051)
            check_type(argname="argument waf_feature", value=waf_feature, expected_type=type_hints["waf_feature"])
            check_type(argname="argument waf_service", value=waf_service, expected_type=type_hints["waf_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "waf_feature": waf_feature,
            "waf_service": waf_service,
        }

    @builtins.property
    def waf_feature(self) -> builtins.str:
        '''Supported WAF features. For more information, see https://cloud.google.com/recaptcha-enterprise/docs/usecase#comparison_of_features. Possible values: CHALLENGE_PAGE, SESSION_TOKEN, ACTION_TOKEN, EXPRESS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#waf_feature GoogleRecaptchaEnterpriseKey#waf_feature}
        '''
        result = self._values.get("waf_feature")
        assert result is not None, "Required property 'waf_feature' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def waf_service(self) -> builtins.str:
        '''The WAF service that uses this key. Possible values: CA, FASTLY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#waf_service GoogleRecaptchaEnterpriseKey#waf_service}
        '''
        result = self._values.get("waf_service")
        assert result is not None, "Required property 'waf_service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRecaptchaEnterpriseKeyWafSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRecaptchaEnterpriseKeyWafSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKeyWafSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04b43d4a801922ddc298fbd7e13a2f8e602cde0c6b2b3d3c4d17867bba946aab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e2ceec15ba3f66165703d35fb59778eebbb6acb63f7d487e475ae14f22ab670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wafFeature", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wafService")
    def waf_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wafService"))

    @waf_service.setter
    def waf_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d69d854e1077d32c2c1bb51bdbfd33ca751a332052e0e4f57b0ff12a978b134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wafService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRecaptchaEnterpriseKeyWafSettings]:
        return typing.cast(typing.Optional[GoogleRecaptchaEnterpriseKeyWafSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRecaptchaEnterpriseKeyWafSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198ea0e0bfc226d65d99f7ef22707e72ffcd62d8d63634b6a61502bf9dd93f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKeyWebSettings",
    jsii_struct_bases=[],
    name_mapping={
        "integration_type": "integrationType",
        "allow_all_domains": "allowAllDomains",
        "allow_amp_traffic": "allowAmpTraffic",
        "allowed_domains": "allowedDomains",
        "challenge_security_preference": "challengeSecurityPreference",
    },
)
class GoogleRecaptchaEnterpriseKeyWebSettings:
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
        :param integration_type: Required. Describes how this key is integrated with the website. Possible values: SCORE, CHECKBOX, INVISIBLE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#integration_type GoogleRecaptchaEnterpriseKey#integration_type}
        :param allow_all_domains: If set to true, it means allowed_domains will not be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allow_all_domains GoogleRecaptchaEnterpriseKey#allow_all_domains}
        :param allow_amp_traffic: If set to true, the key can be used on AMP (Accelerated Mobile Pages) websites. This is supported only for the SCORE integration type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allow_amp_traffic GoogleRecaptchaEnterpriseKey#allow_amp_traffic}
        :param allowed_domains: Domains or subdomains of websites allowed to use the key. All subdomains of an allowed domain are automatically allowed. A valid domain requires a host and must not include any path, port, query or fragment. Examples: 'example.com' or 'subdomain.example.com' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allowed_domains GoogleRecaptchaEnterpriseKey#allowed_domains}
        :param challenge_security_preference: Settings for the frequency and difficulty at which this key triggers captcha challenges. This should only be specified for IntegrationTypes CHECKBOX and INVISIBLE. Possible values: CHALLENGE_SECURITY_PREFERENCE_UNSPECIFIED, USABILITY, BALANCE, SECURITY Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#challenge_security_preference GoogleRecaptchaEnterpriseKey#challenge_security_preference}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a237194ba33998a2826e6ab793eb794dc9a8e49917d95aa41404255b2c4a2b85)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#integration_type GoogleRecaptchaEnterpriseKey#integration_type}
        '''
        result = self._values.get("integration_type")
        assert result is not None, "Required property 'integration_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_all_domains(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, it means allowed_domains will not be enforced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allow_all_domains GoogleRecaptchaEnterpriseKey#allow_all_domains}
        '''
        result = self._values.get("allow_all_domains")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_amp_traffic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the key can be used on AMP (Accelerated Mobile Pages) websites.

        This is supported only for the SCORE integration type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allow_amp_traffic GoogleRecaptchaEnterpriseKey#allow_amp_traffic}
        '''
        result = self._values.get("allow_amp_traffic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Domains or subdomains of websites allowed to use the key.

        All subdomains of an allowed domain are automatically allowed. A valid domain requires a host and must not include any path, port, query or fragment. Examples: 'example.com' or 'subdomain.example.com'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#allowed_domains GoogleRecaptchaEnterpriseKey#allowed_domains}
        '''
        result = self._values.get("allowed_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def challenge_security_preference(self) -> typing.Optional[builtins.str]:
        '''Settings for the frequency and difficulty at which this key triggers captcha challenges.

        This should only be specified for IntegrationTypes CHECKBOX and INVISIBLE. Possible values: CHALLENGE_SECURITY_PREFERENCE_UNSPECIFIED, USABILITY, BALANCE, SECURITY

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_recaptcha_enterprise_key#challenge_security_preference GoogleRecaptchaEnterpriseKey#challenge_security_preference}
        '''
        result = self._values.get("challenge_security_preference")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRecaptchaEnterpriseKeyWebSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRecaptchaEnterpriseKeyWebSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRecaptchaEnterpriseKey.GoogleRecaptchaEnterpriseKeyWebSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d42738987dab17aa6f6613d0d58f00708d8a81569a5c08bd4e8ef2053c4a1cba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e943e8f7d124f96cbf9b8f6d400e07fd1e5ac3318cddff11945f5abf21606b4e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b271b3b5d1dba03602a0c819d1c7f9402ff56ea24fbe8c976781f2532ee00b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAmpTraffic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedDomains")
    def allowed_domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedDomains"))

    @allowed_domains.setter
    def allowed_domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6424d929875e780466c1c9648703295503bdda5b9f949bbcfb46b467175ff859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedDomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="challengeSecurityPreference")
    def challenge_security_preference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "challengeSecurityPreference"))

    @challenge_security_preference.setter
    def challenge_security_preference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27026b7c4bbb87ec0d2c712be09a9d9c5a5754081e5e32ae9ae2762014eb2472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "challengeSecurityPreference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def integration_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationType"))

    @integration_type.setter
    def integration_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d61d713bca7ed39831e0f38c163a15bce93f975d62ab8b43abe58ac9dd81e73f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRecaptchaEnterpriseKeyWebSettings]:
        return typing.cast(typing.Optional[GoogleRecaptchaEnterpriseKeyWebSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRecaptchaEnterpriseKeyWebSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f3a3bb6414c1045efa0fb532c8db4fe42238daae463bce2c3d883183088d8d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleRecaptchaEnterpriseKey",
    "GoogleRecaptchaEnterpriseKeyAndroidSettings",
    "GoogleRecaptchaEnterpriseKeyAndroidSettingsOutputReference",
    "GoogleRecaptchaEnterpriseKeyConfig",
    "GoogleRecaptchaEnterpriseKeyIosSettings",
    "GoogleRecaptchaEnterpriseKeyIosSettingsOutputReference",
    "GoogleRecaptchaEnterpriseKeyTestingOptions",
    "GoogleRecaptchaEnterpriseKeyTestingOptionsOutputReference",
    "GoogleRecaptchaEnterpriseKeyTimeouts",
    "GoogleRecaptchaEnterpriseKeyTimeoutsOutputReference",
    "GoogleRecaptchaEnterpriseKeyWafSettings",
    "GoogleRecaptchaEnterpriseKeyWafSettingsOutputReference",
    "GoogleRecaptchaEnterpriseKeyWebSettings",
    "GoogleRecaptchaEnterpriseKeyWebSettingsOutputReference",
]

publication.publish()

def _typecheckingstub__cd54fb351ed940d839c6a7820d2ef478eae314af891cbab500e60b83b3b9fd64(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    android_settings: typing.Optional[typing.Union[GoogleRecaptchaEnterpriseKeyAndroidSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ios_settings: typing.Optional[typing.Union[GoogleRecaptchaEnterpriseKeyIosSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    testing_options: typing.Optional[typing.Union[GoogleRecaptchaEnterpriseKeyTestingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleRecaptchaEnterpriseKeyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    waf_settings: typing.Optional[typing.Union[GoogleRecaptchaEnterpriseKeyWafSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    web_settings: typing.Optional[typing.Union[GoogleRecaptchaEnterpriseKeyWebSettings, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__dd05b1a9d5baa0a8f9430182ef9a60d037a535463dda28dc0a891dd13bee00a0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69caf1781ca6e1789630201006c22a144c1f569f93e33f22bc4f3573013fd481(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b42b92d9637cfc0df3eca2e276d9c43eb69b4c99489962af79a77216649707c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73541b981f83cdf78645be957d002eb9b0365b652c17b40fdd6c7f6ae505d551(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ebc76ae49c9c88d03c7364bce5f841fbb9aaa47417c45e04498a4f3e03fe95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79855b0ff13af718c6db9d267eeafc337744760a55d018665f149f307b2539d(
    *,
    allow_all_package_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_package_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27366ba6cf30cda0a01fa7f2987be558641012f39d1fe18be0f15b991eef0c33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2970323bcbb9a6e9b931b95caea35b63918e23a2e0b0542aecdaeafd9c79924a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd35b8964be8eef333f365284c98636cb4b661461c653b7a29109c806c0dc9b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d367ddb9beea1e8f8583dc50019801ee45a34d8cd3218ebf8d7851c5a78d45(
    value: typing.Optional[GoogleRecaptchaEnterpriseKeyAndroidSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085dc3073790e7e166da76602cafa0a4e4042e1efb714d93030a4d9745a19b83(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    android_settings: typing.Optional[typing.Union[GoogleRecaptchaEnterpriseKeyAndroidSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ios_settings: typing.Optional[typing.Union[GoogleRecaptchaEnterpriseKeyIosSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    testing_options: typing.Optional[typing.Union[GoogleRecaptchaEnterpriseKeyTestingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleRecaptchaEnterpriseKeyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    waf_settings: typing.Optional[typing.Union[GoogleRecaptchaEnterpriseKeyWafSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    web_settings: typing.Optional[typing.Union[GoogleRecaptchaEnterpriseKeyWebSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd7b040cc59148012158d53076ee1d97d6995f9d1c154375d1560bbcb4b1ff7(
    *,
    allow_all_bundle_ids: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_bundle_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bec17663fe2f15a4df8e70c4e56d9c2c46a9e4083cf3c36736a7bbec97b293a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c939281e0280f10aa9afecc35ead43989b5e6dc2a43c270e34100990f07bd11(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2086c293f3fc8d37cffbda8bffcbf44e1b2b5a3cae2507610fc60b50584f871f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7edddf3a53fce1ab773e1ed1191bab2a36054d52b157b92f259badf95d1927dc(
    value: typing.Optional[GoogleRecaptchaEnterpriseKeyIosSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfac70b74a0b4303ccd18e514fac0716fdea956aba7bdd1eb14b4df848f46659(
    *,
    testing_challenge: typing.Optional[builtins.str] = None,
    testing_score: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d526d342b83c3c944e9c1078eb79d347e73adc93bb68590278ee5a07f418a56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46c3f5f4276b832782f0b3254c0b907ebb19c01b9bb8b59807e8b51ca8f5368(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e5894389f886273f95a524e48fdd6a0d2b1ae5d5a90fe1a924a3e6fad7cdfe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372533c312d267c389f7c1376da32d25727eb4f6a54953da554a44b66803cce7(
    value: typing.Optional[GoogleRecaptchaEnterpriseKeyTestingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e61ec5236ac6bf289c3b977261b505e2d4056ea79bfa6e9494788a640c23b7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4fcfed8c72fd314670b7006bed81715446bc08b26af8e8db30b058fbcd4331(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9779819c3d4f46ed448e57a70a6641e1e858e2081c6ff07894aaf24a39250d71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de785e4fcc7be0c3c6cabdd621c4dbe3591a094a517c3f5d8a3e4137df82d8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3dc269647dcc649c8e46e235da87aa96ac4d8ff4d4850ce946333f70a32245(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e463e10b7eb7f974d00eeb23724545a941ee3d97582ba72fe1c84f73c69807(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRecaptchaEnterpriseKeyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c7726901f488133a6595ed9423d08a38c63bd4e5e1d3c58e065ccb2aa8d051(
    *,
    waf_feature: builtins.str,
    waf_service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b43d4a801922ddc298fbd7e13a2f8e602cde0c6b2b3d3c4d17867bba946aab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2ceec15ba3f66165703d35fb59778eebbb6acb63f7d487e475ae14f22ab670(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d69d854e1077d32c2c1bb51bdbfd33ca751a332052e0e4f57b0ff12a978b134(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198ea0e0bfc226d65d99f7ef22707e72ffcd62d8d63634b6a61502bf9dd93f7c(
    value: typing.Optional[GoogleRecaptchaEnterpriseKeyWafSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a237194ba33998a2826e6ab793eb794dc9a8e49917d95aa41404255b2c4a2b85(
    *,
    integration_type: builtins.str,
    allow_all_domains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_amp_traffic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    challenge_security_preference: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42738987dab17aa6f6613d0d58f00708d8a81569a5c08bd4e8ef2053c4a1cba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e943e8f7d124f96cbf9b8f6d400e07fd1e5ac3318cddff11945f5abf21606b4e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b271b3b5d1dba03602a0c819d1c7f9402ff56ea24fbe8c976781f2532ee00b6f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6424d929875e780466c1c9648703295503bdda5b9f949bbcfb46b467175ff859(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27026b7c4bbb87ec0d2c712be09a9d9c5a5754081e5e32ae9ae2762014eb2472(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61d713bca7ed39831e0f38c163a15bce93f975d62ab8b43abe58ac9dd81e73f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f3a3bb6414c1045efa0fb532c8db4fe42238daae463bce2c3d883183088d8d3(
    value: typing.Optional[GoogleRecaptchaEnterpriseKeyWebSettings],
) -> None:
    """Type checking stubs"""
    pass
