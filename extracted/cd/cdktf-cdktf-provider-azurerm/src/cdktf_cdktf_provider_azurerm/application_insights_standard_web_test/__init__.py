r'''
# `azurerm_application_insights_standard_web_test`

Refer to the Terraform Registry for docs: [`azurerm_application_insights_standard_web_test`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test).
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


class ApplicationInsightsStandardWebTest(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationInsightsStandardWebTest.ApplicationInsightsStandardWebTest",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test azurerm_application_insights_standard_web_test}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        application_insights_id: builtins.str,
        geo_locations: typing.Sequence[builtins.str],
        location: builtins.str,
        name: builtins.str,
        request: typing.Union["ApplicationInsightsStandardWebTestRequest", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        frequency: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        retry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ApplicationInsightsStandardWebTestTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        validation_rules: typing.Optional[typing.Union["ApplicationInsightsStandardWebTestValidationRules", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test azurerm_application_insights_standard_web_test} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param application_insights_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#application_insights_id ApplicationInsightsStandardWebTest#application_insights_id}.
        :param geo_locations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#geo_locations ApplicationInsightsStandardWebTest#geo_locations}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#location ApplicationInsightsStandardWebTest#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#name ApplicationInsightsStandardWebTest#name}.
        :param request: request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#request ApplicationInsightsStandardWebTest#request}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#resource_group_name ApplicationInsightsStandardWebTest#resource_group_name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#description ApplicationInsightsStandardWebTest#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#enabled ApplicationInsightsStandardWebTest#enabled}.
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#frequency ApplicationInsightsStandardWebTest#frequency}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#id ApplicationInsightsStandardWebTest#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param retry_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#retry_enabled ApplicationInsightsStandardWebTest#retry_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#tags ApplicationInsightsStandardWebTest#tags}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#timeout ApplicationInsightsStandardWebTest#timeout}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#timeouts ApplicationInsightsStandardWebTest#timeouts}
        :param validation_rules: validation_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#validation_rules ApplicationInsightsStandardWebTest#validation_rules}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a54a8aa6db3ba14875bd1c8f7473e40c7ca4e64ec83a42e9cd7c5ef49be954c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApplicationInsightsStandardWebTestConfig(
            application_insights_id=application_insights_id,
            geo_locations=geo_locations,
            location=location,
            name=name,
            request=request,
            resource_group_name=resource_group_name,
            description=description,
            enabled=enabled,
            frequency=frequency,
            id=id,
            retry_enabled=retry_enabled,
            tags=tags,
            timeout=timeout,
            timeouts=timeouts,
            validation_rules=validation_rules,
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
        '''Generates CDKTF code for importing a ApplicationInsightsStandardWebTest resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApplicationInsightsStandardWebTest to import.
        :param import_from_id: The id of the existing ApplicationInsightsStandardWebTest that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApplicationInsightsStandardWebTest to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97acea876af8fc96e5b2ffafab26037f97b56a030d9da9c57fcbd4cdfb0aa7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRequest")
    def put_request(
        self,
        *,
        url: builtins.str,
        body: typing.Optional[builtins.str] = None,
        follow_redirects_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationInsightsStandardWebTestRequestHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_verb: typing.Optional[builtins.str] = None,
        parse_dependent_requests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#url ApplicationInsightsStandardWebTest#url}.
        :param body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#body ApplicationInsightsStandardWebTest#body}.
        :param follow_redirects_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#follow_redirects_enabled ApplicationInsightsStandardWebTest#follow_redirects_enabled}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#header ApplicationInsightsStandardWebTest#header}
        :param http_verb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#http_verb ApplicationInsightsStandardWebTest#http_verb}.
        :param parse_dependent_requests_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#parse_dependent_requests_enabled ApplicationInsightsStandardWebTest#parse_dependent_requests_enabled}.
        '''
        value = ApplicationInsightsStandardWebTestRequest(
            url=url,
            body=body,
            follow_redirects_enabled=follow_redirects_enabled,
            header=header,
            http_verb=http_verb,
            parse_dependent_requests_enabled=parse_dependent_requests_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putRequest", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#create ApplicationInsightsStandardWebTest#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#delete ApplicationInsightsStandardWebTest#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#read ApplicationInsightsStandardWebTest#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#update ApplicationInsightsStandardWebTest#update}.
        '''
        value = ApplicationInsightsStandardWebTestTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putValidationRules")
    def put_validation_rules(
        self,
        *,
        content: typing.Optional[typing.Union["ApplicationInsightsStandardWebTestValidationRulesContent", typing.Dict[builtins.str, typing.Any]]] = None,
        expected_status_code: typing.Optional[jsii.Number] = None,
        ssl_cert_remaining_lifetime: typing.Optional[jsii.Number] = None,
        ssl_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param content: content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#content ApplicationInsightsStandardWebTest#content}
        :param expected_status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#expected_status_code ApplicationInsightsStandardWebTest#expected_status_code}.
        :param ssl_cert_remaining_lifetime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#ssl_cert_remaining_lifetime ApplicationInsightsStandardWebTest#ssl_cert_remaining_lifetime}.
        :param ssl_check_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#ssl_check_enabled ApplicationInsightsStandardWebTest#ssl_check_enabled}.
        '''
        value = ApplicationInsightsStandardWebTestValidationRules(
            content=content,
            expected_status_code=expected_status_code,
            ssl_cert_remaining_lifetime=ssl_cert_remaining_lifetime,
            ssl_check_enabled=ssl_check_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putValidationRules", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetFrequency")
    def reset_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequency", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRetryEnabled")
    def reset_retry_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryEnabled", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetValidationRules")
    def reset_validation_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidationRules", []))

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
    @jsii.member(jsii_name="request")
    def request(self) -> "ApplicationInsightsStandardWebTestRequestOutputReference":
        return typing.cast("ApplicationInsightsStandardWebTestRequestOutputReference", jsii.get(self, "request"))

    @builtins.property
    @jsii.member(jsii_name="syntheticMonitorId")
    def synthetic_monitor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syntheticMonitorId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApplicationInsightsStandardWebTestTimeoutsOutputReference":
        return typing.cast("ApplicationInsightsStandardWebTestTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="validationRules")
    def validation_rules(
        self,
    ) -> "ApplicationInsightsStandardWebTestValidationRulesOutputReference":
        return typing.cast("ApplicationInsightsStandardWebTestValidationRulesOutputReference", jsii.get(self, "validationRules"))

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsIdInput")
    def application_insights_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationInsightsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="geoLocationsInput")
    def geo_locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "geoLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="requestInput")
    def request_input(
        self,
    ) -> typing.Optional["ApplicationInsightsStandardWebTestRequest"]:
        return typing.cast(typing.Optional["ApplicationInsightsStandardWebTestRequest"], jsii.get(self, "requestInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="retryEnabledInput")
    def retry_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "retryEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApplicationInsightsStandardWebTestTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApplicationInsightsStandardWebTestTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="validationRulesInput")
    def validation_rules_input(
        self,
    ) -> typing.Optional["ApplicationInsightsStandardWebTestValidationRules"]:
        return typing.cast(typing.Optional["ApplicationInsightsStandardWebTestValidationRules"], jsii.get(self, "validationRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsId")
    def application_insights_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationInsightsId"))

    @application_insights_id.setter
    def application_insights_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e7edf63678c5ca672630686c302e9991dff1bb4c1b90bfb645f39ef8ebfb5c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationInsightsId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b18afce20b915e67262ad0dc6b9308d3c475fea0f52b338b00a76f13ce2451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0788e7a052d21a3a48d204889aee93d4214f2dec256101bf0bb9fd84b145387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf5dcb1ae67d4e35cba88e6d17ba540370509e09f16eb3e8dd73b6b2a2a41e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geoLocations")
    def geo_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "geoLocations"))

    @geo_locations.setter
    def geo_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a165b28473ba13d48c27d09d78a8baa536bfcfea047ee00ab3e7278c0638626c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geoLocations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f07ed79bad671a10aa2c2e37e23bf98ef1ff6c4c78555cff87fb7e397c6189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f41069af4e7f5fa0ab836f9f759f264a3a5cc2c19e1e85ea99927374cd8f49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df10fe585c5042aa34689b92585e4528f4c38bed13cb49b883eba7302453410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4757cc32fca349a1df26bc29d7598eecd7f6e2fd2ced85cb192f3eca0c691331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryEnabled")
    def retry_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "retryEnabled"))

    @retry_enabled.setter
    def retry_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eaa4f58b4eb1d13f28aad0d64493f4e89e06c8f063d05690eb08269685661e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deea776d81656abb722c587cefdd56b5b873fd871cc6dc03cf1b15bf499bc3cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c6d58a41291f4bc9a1488255543e231051f0fcfb41ceec2286b1f7d0dfd999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationInsightsStandardWebTest.ApplicationInsightsStandardWebTestConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "application_insights_id": "applicationInsightsId",
        "geo_locations": "geoLocations",
        "location": "location",
        "name": "name",
        "request": "request",
        "resource_group_name": "resourceGroupName",
        "description": "description",
        "enabled": "enabled",
        "frequency": "frequency",
        "id": "id",
        "retry_enabled": "retryEnabled",
        "tags": "tags",
        "timeout": "timeout",
        "timeouts": "timeouts",
        "validation_rules": "validationRules",
    },
)
class ApplicationInsightsStandardWebTestConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        application_insights_id: builtins.str,
        geo_locations: typing.Sequence[builtins.str],
        location: builtins.str,
        name: builtins.str,
        request: typing.Union["ApplicationInsightsStandardWebTestRequest", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        frequency: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        retry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ApplicationInsightsStandardWebTestTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        validation_rules: typing.Optional[typing.Union["ApplicationInsightsStandardWebTestValidationRules", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param application_insights_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#application_insights_id ApplicationInsightsStandardWebTest#application_insights_id}.
        :param geo_locations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#geo_locations ApplicationInsightsStandardWebTest#geo_locations}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#location ApplicationInsightsStandardWebTest#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#name ApplicationInsightsStandardWebTest#name}.
        :param request: request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#request ApplicationInsightsStandardWebTest#request}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#resource_group_name ApplicationInsightsStandardWebTest#resource_group_name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#description ApplicationInsightsStandardWebTest#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#enabled ApplicationInsightsStandardWebTest#enabled}.
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#frequency ApplicationInsightsStandardWebTest#frequency}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#id ApplicationInsightsStandardWebTest#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param retry_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#retry_enabled ApplicationInsightsStandardWebTest#retry_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#tags ApplicationInsightsStandardWebTest#tags}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#timeout ApplicationInsightsStandardWebTest#timeout}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#timeouts ApplicationInsightsStandardWebTest#timeouts}
        :param validation_rules: validation_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#validation_rules ApplicationInsightsStandardWebTest#validation_rules}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(request, dict):
            request = ApplicationInsightsStandardWebTestRequest(**request)
        if isinstance(timeouts, dict):
            timeouts = ApplicationInsightsStandardWebTestTimeouts(**timeouts)
        if isinstance(validation_rules, dict):
            validation_rules = ApplicationInsightsStandardWebTestValidationRules(**validation_rules)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8a92eff3cd5abf73b40f1af5a9c4ed833e8a7326798426d5315241149f1345)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument application_insights_id", value=application_insights_id, expected_type=type_hints["application_insights_id"])
            check_type(argname="argument geo_locations", value=geo_locations, expected_type=type_hints["geo_locations"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument request", value=request, expected_type=type_hints["request"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument retry_enabled", value=retry_enabled, expected_type=type_hints["retry_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument validation_rules", value=validation_rules, expected_type=type_hints["validation_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_insights_id": application_insights_id,
            "geo_locations": geo_locations,
            "location": location,
            "name": name,
            "request": request,
            "resource_group_name": resource_group_name,
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
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if frequency is not None:
            self._values["frequency"] = frequency
        if id is not None:
            self._values["id"] = id
        if retry_enabled is not None:
            self._values["retry_enabled"] = retry_enabled
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if validation_rules is not None:
            self._values["validation_rules"] = validation_rules

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
    def application_insights_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#application_insights_id ApplicationInsightsStandardWebTest#application_insights_id}.'''
        result = self._values.get("application_insights_id")
        assert result is not None, "Required property 'application_insights_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def geo_locations(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#geo_locations ApplicationInsightsStandardWebTest#geo_locations}.'''
        result = self._values.get("geo_locations")
        assert result is not None, "Required property 'geo_locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#location ApplicationInsightsStandardWebTest#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#name ApplicationInsightsStandardWebTest#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request(self) -> "ApplicationInsightsStandardWebTestRequest":
        '''request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#request ApplicationInsightsStandardWebTest#request}
        '''
        result = self._values.get("request")
        assert result is not None, "Required property 'request' is missing"
        return typing.cast("ApplicationInsightsStandardWebTestRequest", result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#resource_group_name ApplicationInsightsStandardWebTest#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#description ApplicationInsightsStandardWebTest#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#enabled ApplicationInsightsStandardWebTest#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def frequency(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#frequency ApplicationInsightsStandardWebTest#frequency}.'''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#id ApplicationInsightsStandardWebTest#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#retry_enabled ApplicationInsightsStandardWebTest#retry_enabled}.'''
        result = self._values.get("retry_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#tags ApplicationInsightsStandardWebTest#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#timeout ApplicationInsightsStandardWebTest#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApplicationInsightsStandardWebTestTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#timeouts ApplicationInsightsStandardWebTest#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApplicationInsightsStandardWebTestTimeouts"], result)

    @builtins.property
    def validation_rules(
        self,
    ) -> typing.Optional["ApplicationInsightsStandardWebTestValidationRules"]:
        '''validation_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#validation_rules ApplicationInsightsStandardWebTest#validation_rules}
        '''
        result = self._values.get("validation_rules")
        return typing.cast(typing.Optional["ApplicationInsightsStandardWebTestValidationRules"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationInsightsStandardWebTestConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationInsightsStandardWebTest.ApplicationInsightsStandardWebTestRequest",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "body": "body",
        "follow_redirects_enabled": "followRedirectsEnabled",
        "header": "header",
        "http_verb": "httpVerb",
        "parse_dependent_requests_enabled": "parseDependentRequestsEnabled",
    },
)
class ApplicationInsightsStandardWebTestRequest:
    def __init__(
        self,
        *,
        url: builtins.str,
        body: typing.Optional[builtins.str] = None,
        follow_redirects_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationInsightsStandardWebTestRequestHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_verb: typing.Optional[builtins.str] = None,
        parse_dependent_requests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#url ApplicationInsightsStandardWebTest#url}.
        :param body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#body ApplicationInsightsStandardWebTest#body}.
        :param follow_redirects_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#follow_redirects_enabled ApplicationInsightsStandardWebTest#follow_redirects_enabled}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#header ApplicationInsightsStandardWebTest#header}
        :param http_verb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#http_verb ApplicationInsightsStandardWebTest#http_verb}.
        :param parse_dependent_requests_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#parse_dependent_requests_enabled ApplicationInsightsStandardWebTest#parse_dependent_requests_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dbbf50c5ee756793e8be1e6fbeaa5430ba17f2435404a8af74e11699d17df64)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument follow_redirects_enabled", value=follow_redirects_enabled, expected_type=type_hints["follow_redirects_enabled"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument http_verb", value=http_verb, expected_type=type_hints["http_verb"])
            check_type(argname="argument parse_dependent_requests_enabled", value=parse_dependent_requests_enabled, expected_type=type_hints["parse_dependent_requests_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if body is not None:
            self._values["body"] = body
        if follow_redirects_enabled is not None:
            self._values["follow_redirects_enabled"] = follow_redirects_enabled
        if header is not None:
            self._values["header"] = header
        if http_verb is not None:
            self._values["http_verb"] = http_verb
        if parse_dependent_requests_enabled is not None:
            self._values["parse_dependent_requests_enabled"] = parse_dependent_requests_enabled

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#url ApplicationInsightsStandardWebTest#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def body(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#body ApplicationInsightsStandardWebTest#body}.'''
        result = self._values.get("body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def follow_redirects_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#follow_redirects_enabled ApplicationInsightsStandardWebTest#follow_redirects_enabled}.'''
        result = self._values.get("follow_redirects_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationInsightsStandardWebTestRequestHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#header ApplicationInsightsStandardWebTest#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationInsightsStandardWebTestRequestHeader"]]], result)

    @builtins.property
    def http_verb(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#http_verb ApplicationInsightsStandardWebTest#http_verb}.'''
        result = self._values.get("http_verb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parse_dependent_requests_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#parse_dependent_requests_enabled ApplicationInsightsStandardWebTest#parse_dependent_requests_enabled}.'''
        result = self._values.get("parse_dependent_requests_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationInsightsStandardWebTestRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationInsightsStandardWebTest.ApplicationInsightsStandardWebTestRequestHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ApplicationInsightsStandardWebTestRequestHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#name ApplicationInsightsStandardWebTest#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#value ApplicationInsightsStandardWebTest#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f05bbdd5e4d7479bafbd0aa8e1e79e018627cb7d997d715eebe763dda776ad47)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#name ApplicationInsightsStandardWebTest#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#value ApplicationInsightsStandardWebTest#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationInsightsStandardWebTestRequestHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationInsightsStandardWebTestRequestHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationInsightsStandardWebTest.ApplicationInsightsStandardWebTestRequestHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abd26d44ddd78ca9e5f5fa7e223cc46aed2bd49c9caa58cc55523de7c88d559a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationInsightsStandardWebTestRequestHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba06cf462a00590ffa886c6d3da4e1495a64cd8d42e313ec94cb5ef3d4601364)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationInsightsStandardWebTestRequestHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d98590398f1f83fecae556386ae6d06b10a07bb5fdbde372a0f1d977c4ccbe9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0841ec752c0a9a81dea1cd0c0b885b862702b4136972bf76309816f1bf4214a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23dc2306ef08b46704ee2d54dd3c5ef7bc593f8dc3e74cc93b2a06e9d4441631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationInsightsStandardWebTestRequestHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationInsightsStandardWebTestRequestHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationInsightsStandardWebTestRequestHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e89558f34b213507b8cbe35a1e8be235b8b1723bd06aa5d15537376a9097f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationInsightsStandardWebTestRequestHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationInsightsStandardWebTest.ApplicationInsightsStandardWebTestRequestHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ef1f0481bc2469f2a12ea3d4690809f7738c17933692b88c0e2f6c307fdedd7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd722b5d635f05644ac3ed508fa432fccebc2d5241434ed3b3fa36132da7fd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f54c50ec31b441b2db58f1e60f87b9cfe8305a9e9f9540fe4a2f62850d7d4b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationInsightsStandardWebTestRequestHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationInsightsStandardWebTestRequestHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationInsightsStandardWebTestRequestHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41aa8a61d5bb9aec3f01fbd5cb14a85ef6af7c06ce9b508bd6c3801430aa8d65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationInsightsStandardWebTestRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationInsightsStandardWebTest.ApplicationInsightsStandardWebTestRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4a252a5c07b7d3bc7e48f7ed71329c3868b06b63cdc619c1245c22ae3d4e243)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationInsightsStandardWebTestRequestHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8516dde87cea8b4a33174e98197863e093dcddf7846f95cfa8268b47d218e4d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @jsii.member(jsii_name="resetFollowRedirectsEnabled")
    def reset_follow_redirects_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFollowRedirectsEnabled", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetHttpVerb")
    def reset_http_verb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpVerb", []))

    @jsii.member(jsii_name="resetParseDependentRequestsEnabled")
    def reset_parse_dependent_requests_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseDependentRequestsEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> ApplicationInsightsStandardWebTestRequestHeaderList:
        return typing.cast(ApplicationInsightsStandardWebTestRequestHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="followRedirectsEnabledInput")
    def follow_redirects_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "followRedirectsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationInsightsStandardWebTestRequestHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationInsightsStandardWebTestRequestHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="httpVerbInput")
    def http_verb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpVerbInput"))

    @builtins.property
    @jsii.member(jsii_name="parseDependentRequestsEnabledInput")
    def parse_dependent_requests_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "parseDependentRequestsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @body.setter
    def body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09db51bcf295938aea60ea85dc0050e1bce751dda3378bb62fdcbab0785106c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="followRedirectsEnabled")
    def follow_redirects_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "followRedirectsEnabled"))

    @follow_redirects_enabled.setter
    def follow_redirects_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bcb0afadf15a2284e3e4c128ccc87d81960430cc38e42f6eb8206976821f4a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "followRedirectsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpVerb")
    def http_verb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpVerb"))

    @http_verb.setter
    def http_verb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d98b08475f231d5ff334bdb894401fe78b79ecbaaed5f63d784092ef2b474a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpVerb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parseDependentRequestsEnabled")
    def parse_dependent_requests_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "parseDependentRequestsEnabled"))

    @parse_dependent_requests_enabled.setter
    def parse_dependent_requests_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de0e967821691c891281dd071817822d60628bf03fb33d1fa94dad7853a0fa61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parseDependentRequestsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b29dac5368131ca4942554adfd06e4b2864f37613a5919e1a276ea707f22fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApplicationInsightsStandardWebTestRequest]:
        return typing.cast(typing.Optional[ApplicationInsightsStandardWebTestRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationInsightsStandardWebTestRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb6a68622e190a92c0b8d946b57325a33d206cfe4e6c772b3cff39fbe99a0a3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationInsightsStandardWebTest.ApplicationInsightsStandardWebTestTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ApplicationInsightsStandardWebTestTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#create ApplicationInsightsStandardWebTest#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#delete ApplicationInsightsStandardWebTest#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#read ApplicationInsightsStandardWebTest#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#update ApplicationInsightsStandardWebTest#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff4dc7dc7fc761aa1a09ad0aae9624936d29c0ed49cfe4fe5b04eae0135329f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#create ApplicationInsightsStandardWebTest#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#delete ApplicationInsightsStandardWebTest#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#read ApplicationInsightsStandardWebTest#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#update ApplicationInsightsStandardWebTest#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationInsightsStandardWebTestTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationInsightsStandardWebTestTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationInsightsStandardWebTest.ApplicationInsightsStandardWebTestTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__881295f13580ecb506210571640014d1036489579c70fe32a4fbdd514c61f0e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__672fa182823e165dbaa766569532121c22bcd31a79106681a38b4871185bd29a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8de847ecaa37fb077e35984b658636631b6648bfb3f979a56905874ec64031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56b75f83fa278dd7a09a9a0bb4de91e0d62c3160a61e5d81f295e1b6db62cbdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ae09e6000d96764c9b09c95fedeefb19d8fe8cb28709c0f1ae490fce355b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationInsightsStandardWebTestTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationInsightsStandardWebTestTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationInsightsStandardWebTestTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50f7ec9764de1c3948f51a6e9920f2b84533cd730af1847410c057b05a5cf6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationInsightsStandardWebTest.ApplicationInsightsStandardWebTestValidationRules",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "expected_status_code": "expectedStatusCode",
        "ssl_cert_remaining_lifetime": "sslCertRemainingLifetime",
        "ssl_check_enabled": "sslCheckEnabled",
    },
)
class ApplicationInsightsStandardWebTestValidationRules:
    def __init__(
        self,
        *,
        content: typing.Optional[typing.Union["ApplicationInsightsStandardWebTestValidationRulesContent", typing.Dict[builtins.str, typing.Any]]] = None,
        expected_status_code: typing.Optional[jsii.Number] = None,
        ssl_cert_remaining_lifetime: typing.Optional[jsii.Number] = None,
        ssl_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param content: content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#content ApplicationInsightsStandardWebTest#content}
        :param expected_status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#expected_status_code ApplicationInsightsStandardWebTest#expected_status_code}.
        :param ssl_cert_remaining_lifetime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#ssl_cert_remaining_lifetime ApplicationInsightsStandardWebTest#ssl_cert_remaining_lifetime}.
        :param ssl_check_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#ssl_check_enabled ApplicationInsightsStandardWebTest#ssl_check_enabled}.
        '''
        if isinstance(content, dict):
            content = ApplicationInsightsStandardWebTestValidationRulesContent(**content)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859962fc82ef008ee34ce18531e84aaa742000948d26d25c8d80a99dbb3da554)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument expected_status_code", value=expected_status_code, expected_type=type_hints["expected_status_code"])
            check_type(argname="argument ssl_cert_remaining_lifetime", value=ssl_cert_remaining_lifetime, expected_type=type_hints["ssl_cert_remaining_lifetime"])
            check_type(argname="argument ssl_check_enabled", value=ssl_check_enabled, expected_type=type_hints["ssl_check_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content is not None:
            self._values["content"] = content
        if expected_status_code is not None:
            self._values["expected_status_code"] = expected_status_code
        if ssl_cert_remaining_lifetime is not None:
            self._values["ssl_cert_remaining_lifetime"] = ssl_cert_remaining_lifetime
        if ssl_check_enabled is not None:
            self._values["ssl_check_enabled"] = ssl_check_enabled

    @builtins.property
    def content(
        self,
    ) -> typing.Optional["ApplicationInsightsStandardWebTestValidationRulesContent"]:
        '''content block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#content ApplicationInsightsStandardWebTest#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional["ApplicationInsightsStandardWebTestValidationRulesContent"], result)

    @builtins.property
    def expected_status_code(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#expected_status_code ApplicationInsightsStandardWebTest#expected_status_code}.'''
        result = self._values.get("expected_status_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ssl_cert_remaining_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#ssl_cert_remaining_lifetime ApplicationInsightsStandardWebTest#ssl_cert_remaining_lifetime}.'''
        result = self._values.get("ssl_cert_remaining_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ssl_check_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#ssl_check_enabled ApplicationInsightsStandardWebTest#ssl_check_enabled}.'''
        result = self._values.get("ssl_check_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationInsightsStandardWebTestValidationRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationInsightsStandardWebTest.ApplicationInsightsStandardWebTestValidationRulesContent",
    jsii_struct_bases=[],
    name_mapping={
        "content_match": "contentMatch",
        "ignore_case": "ignoreCase",
        "pass_if_text_found": "passIfTextFound",
    },
)
class ApplicationInsightsStandardWebTestValidationRulesContent:
    def __init__(
        self,
        *,
        content_match: builtins.str,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pass_if_text_found: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param content_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#content_match ApplicationInsightsStandardWebTest#content_match}.
        :param ignore_case: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#ignore_case ApplicationInsightsStandardWebTest#ignore_case}.
        :param pass_if_text_found: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#pass_if_text_found ApplicationInsightsStandardWebTest#pass_if_text_found}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5515d134aa1d8618374f77c6570b45c420d2656b73ba31a32deaaebaa3fe66e1)
            check_type(argname="argument content_match", value=content_match, expected_type=type_hints["content_match"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument pass_if_text_found", value=pass_if_text_found, expected_type=type_hints["pass_if_text_found"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_match": content_match,
        }
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if pass_if_text_found is not None:
            self._values["pass_if_text_found"] = pass_if_text_found

    @builtins.property
    def content_match(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#content_match ApplicationInsightsStandardWebTest#content_match}.'''
        result = self._values.get("content_match")
        assert result is not None, "Required property 'content_match' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#ignore_case ApplicationInsightsStandardWebTest#ignore_case}.'''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pass_if_text_found(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#pass_if_text_found ApplicationInsightsStandardWebTest#pass_if_text_found}.'''
        result = self._values.get("pass_if_text_found")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationInsightsStandardWebTestValidationRulesContent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationInsightsStandardWebTestValidationRulesContentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationInsightsStandardWebTest.ApplicationInsightsStandardWebTestValidationRulesContentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37ff58b3e4c69e82c8e9617b3e7464fcb708b4945aeddae4be7870b64d9b5e3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetPassIfTextFound")
    def reset_pass_if_text_found(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassIfTextFound", []))

    @builtins.property
    @jsii.member(jsii_name="contentMatchInput")
    def content_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="passIfTextFoundInput")
    def pass_if_text_found_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passIfTextFoundInput"))

    @builtins.property
    @jsii.member(jsii_name="contentMatch")
    def content_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentMatch"))

    @content_match.setter
    def content_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bc10b666b73112a4749ff4474cbe6df7478b38462904d40ed5da3d6888cfec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ea08164f5887881904bfcb613683e91a483458c99bbf0f6bcaefa8b2be0d34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passIfTextFound")
    def pass_if_text_found(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passIfTextFound"))

    @pass_if_text_found.setter
    def pass_if_text_found(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360250c506e060b643381307eb9c3e59412899d10d8ed3466026245c5124e9e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passIfTextFound", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApplicationInsightsStandardWebTestValidationRulesContent]:
        return typing.cast(typing.Optional[ApplicationInsightsStandardWebTestValidationRulesContent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationInsightsStandardWebTestValidationRulesContent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ff9a4a5ca28bf9581b2ed5f3338362b465069c67da9847da436603c25f5950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationInsightsStandardWebTestValidationRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationInsightsStandardWebTest.ApplicationInsightsStandardWebTestValidationRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abc2c2f34bed282d62b5241ce5b2f935ef10f5b09a93f412388f62cc7802d96b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContent")
    def put_content(
        self,
        *,
        content_match: builtins.str,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pass_if_text_found: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param content_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#content_match ApplicationInsightsStandardWebTest#content_match}.
        :param ignore_case: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#ignore_case ApplicationInsightsStandardWebTest#ignore_case}.
        :param pass_if_text_found: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_insights_standard_web_test#pass_if_text_found ApplicationInsightsStandardWebTest#pass_if_text_found}.
        '''
        value = ApplicationInsightsStandardWebTestValidationRulesContent(
            content_match=content_match,
            ignore_case=ignore_case,
            pass_if_text_found=pass_if_text_found,
        )

        return typing.cast(None, jsii.invoke(self, "putContent", [value]))

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetExpectedStatusCode")
    def reset_expected_status_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpectedStatusCode", []))

    @jsii.member(jsii_name="resetSslCertRemainingLifetime")
    def reset_ssl_cert_remaining_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCertRemainingLifetime", []))

    @jsii.member(jsii_name="resetSslCheckEnabled")
    def reset_ssl_check_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCheckEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(
        self,
    ) -> ApplicationInsightsStandardWebTestValidationRulesContentOutputReference:
        return typing.cast(ApplicationInsightsStandardWebTestValidationRulesContentOutputReference, jsii.get(self, "content"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(
        self,
    ) -> typing.Optional[ApplicationInsightsStandardWebTestValidationRulesContent]:
        return typing.cast(typing.Optional[ApplicationInsightsStandardWebTestValidationRulesContent], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="expectedStatusCodeInput")
    def expected_status_code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expectedStatusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCertRemainingLifetimeInput")
    def ssl_cert_remaining_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sslCertRemainingLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCheckEnabledInput")
    def ssl_check_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sslCheckEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="expectedStatusCode")
    def expected_status_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expectedStatusCode"))

    @expected_status_code.setter
    def expected_status_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7587adcfca5c91baef0875203a09102ce9639ba07f601cc37ea4148d97d92652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expectedStatusCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCertRemainingLifetime")
    def ssl_cert_remaining_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sslCertRemainingLifetime"))

    @ssl_cert_remaining_lifetime.setter
    def ssl_cert_remaining_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19198babe63034cd0f35a9e7c4b09cd6461ea1480c1998bc7831ee002329ae09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCertRemainingLifetime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCheckEnabled")
    def ssl_check_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sslCheckEnabled"))

    @ssl_check_enabled.setter
    def ssl_check_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2a2dda19d8bc1fecad0247be1ae20e84fcf128d0bdfbc205c98ec0b15506f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCheckEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApplicationInsightsStandardWebTestValidationRules]:
        return typing.cast(typing.Optional[ApplicationInsightsStandardWebTestValidationRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationInsightsStandardWebTestValidationRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b875afa0c1fa662c2ea4cebdc27560d6f45d00ffc9c86d810a54facfabfee1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApplicationInsightsStandardWebTest",
    "ApplicationInsightsStandardWebTestConfig",
    "ApplicationInsightsStandardWebTestRequest",
    "ApplicationInsightsStandardWebTestRequestHeader",
    "ApplicationInsightsStandardWebTestRequestHeaderList",
    "ApplicationInsightsStandardWebTestRequestHeaderOutputReference",
    "ApplicationInsightsStandardWebTestRequestOutputReference",
    "ApplicationInsightsStandardWebTestTimeouts",
    "ApplicationInsightsStandardWebTestTimeoutsOutputReference",
    "ApplicationInsightsStandardWebTestValidationRules",
    "ApplicationInsightsStandardWebTestValidationRulesContent",
    "ApplicationInsightsStandardWebTestValidationRulesContentOutputReference",
    "ApplicationInsightsStandardWebTestValidationRulesOutputReference",
]

publication.publish()

def _typecheckingstub__7a54a8aa6db3ba14875bd1c8f7473e40c7ca4e64ec83a42e9cd7c5ef49be954c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    application_insights_id: builtins.str,
    geo_locations: typing.Sequence[builtins.str],
    location: builtins.str,
    name: builtins.str,
    request: typing.Union[ApplicationInsightsStandardWebTestRequest, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    frequency: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    retry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ApplicationInsightsStandardWebTestTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    validation_rules: typing.Optional[typing.Union[ApplicationInsightsStandardWebTestValidationRules, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e97acea876af8fc96e5b2ffafab26037f97b56a030d9da9c57fcbd4cdfb0aa7f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7edf63678c5ca672630686c302e9991dff1bb4c1b90bfb645f39ef8ebfb5c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b18afce20b915e67262ad0dc6b9308d3c475fea0f52b338b00a76f13ce2451(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0788e7a052d21a3a48d204889aee93d4214f2dec256101bf0bb9fd84b145387(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf5dcb1ae67d4e35cba88e6d17ba540370509e09f16eb3e8dd73b6b2a2a41e6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a165b28473ba13d48c27d09d78a8baa536bfcfea047ee00ab3e7278c0638626c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f07ed79bad671a10aa2c2e37e23bf98ef1ff6c4c78555cff87fb7e397c6189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f41069af4e7f5fa0ab836f9f759f264a3a5cc2c19e1e85ea99927374cd8f49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df10fe585c5042aa34689b92585e4528f4c38bed13cb49b883eba7302453410(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4757cc32fca349a1df26bc29d7598eecd7f6e2fd2ced85cb192f3eca0c691331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eaa4f58b4eb1d13f28aad0d64493f4e89e06c8f063d05690eb08269685661e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deea776d81656abb722c587cefdd56b5b873fd871cc6dc03cf1b15bf499bc3cd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c6d58a41291f4bc9a1488255543e231051f0fcfb41ceec2286b1f7d0dfd999(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8a92eff3cd5abf73b40f1af5a9c4ed833e8a7326798426d5315241149f1345(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    application_insights_id: builtins.str,
    geo_locations: typing.Sequence[builtins.str],
    location: builtins.str,
    name: builtins.str,
    request: typing.Union[ApplicationInsightsStandardWebTestRequest, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    frequency: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    retry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ApplicationInsightsStandardWebTestTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    validation_rules: typing.Optional[typing.Union[ApplicationInsightsStandardWebTestValidationRules, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dbbf50c5ee756793e8be1e6fbeaa5430ba17f2435404a8af74e11699d17df64(
    *,
    url: builtins.str,
    body: typing.Optional[builtins.str] = None,
    follow_redirects_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationInsightsStandardWebTestRequestHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http_verb: typing.Optional[builtins.str] = None,
    parse_dependent_requests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05bbdd5e4d7479bafbd0aa8e1e79e018627cb7d997d715eebe763dda776ad47(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd26d44ddd78ca9e5f5fa7e223cc46aed2bd49c9caa58cc55523de7c88d559a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba06cf462a00590ffa886c6d3da4e1495a64cd8d42e313ec94cb5ef3d4601364(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d98590398f1f83fecae556386ae6d06b10a07bb5fdbde372a0f1d977c4ccbe9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0841ec752c0a9a81dea1cd0c0b885b862702b4136972bf76309816f1bf4214a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23dc2306ef08b46704ee2d54dd3c5ef7bc593f8dc3e74cc93b2a06e9d4441631(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e89558f34b213507b8cbe35a1e8be235b8b1723bd06aa5d15537376a9097f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationInsightsStandardWebTestRequestHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef1f0481bc2469f2a12ea3d4690809f7738c17933692b88c0e2f6c307fdedd7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd722b5d635f05644ac3ed508fa432fccebc2d5241434ed3b3fa36132da7fd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f54c50ec31b441b2db58f1e60f87b9cfe8305a9e9f9540fe4a2f62850d7d4b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41aa8a61d5bb9aec3f01fbd5cb14a85ef6af7c06ce9b508bd6c3801430aa8d65(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationInsightsStandardWebTestRequestHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a252a5c07b7d3bc7e48f7ed71329c3868b06b63cdc619c1245c22ae3d4e243(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8516dde87cea8b4a33174e98197863e093dcddf7846f95cfa8268b47d218e4d8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationInsightsStandardWebTestRequestHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09db51bcf295938aea60ea85dc0050e1bce751dda3378bb62fdcbab0785106c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bcb0afadf15a2284e3e4c128ccc87d81960430cc38e42f6eb8206976821f4a4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d98b08475f231d5ff334bdb894401fe78b79ecbaaed5f63d784092ef2b474a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0e967821691c891281dd071817822d60628bf03fb33d1fa94dad7853a0fa61(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b29dac5368131ca4942554adfd06e4b2864f37613a5919e1a276ea707f22fc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6a68622e190a92c0b8d946b57325a33d206cfe4e6c772b3cff39fbe99a0a3e(
    value: typing.Optional[ApplicationInsightsStandardWebTestRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff4dc7dc7fc761aa1a09ad0aae9624936d29c0ed49cfe4fe5b04eae0135329f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881295f13580ecb506210571640014d1036489579c70fe32a4fbdd514c61f0e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672fa182823e165dbaa766569532121c22bcd31a79106681a38b4871185bd29a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8de847ecaa37fb077e35984b658636631b6648bfb3f979a56905874ec64031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b75f83fa278dd7a09a9a0bb4de91e0d62c3160a61e5d81f295e1b6db62cbdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ae09e6000d96764c9b09c95fedeefb19d8fe8cb28709c0f1ae490fce355b9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50f7ec9764de1c3948f51a6e9920f2b84533cd730af1847410c057b05a5cf6e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationInsightsStandardWebTestTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859962fc82ef008ee34ce18531e84aaa742000948d26d25c8d80a99dbb3da554(
    *,
    content: typing.Optional[typing.Union[ApplicationInsightsStandardWebTestValidationRulesContent, typing.Dict[builtins.str, typing.Any]]] = None,
    expected_status_code: typing.Optional[jsii.Number] = None,
    ssl_cert_remaining_lifetime: typing.Optional[jsii.Number] = None,
    ssl_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5515d134aa1d8618374f77c6570b45c420d2656b73ba31a32deaaebaa3fe66e1(
    *,
    content_match: builtins.str,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pass_if_text_found: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ff58b3e4c69e82c8e9617b3e7464fcb708b4945aeddae4be7870b64d9b5e3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc10b666b73112a4749ff4474cbe6df7478b38462904d40ed5da3d6888cfec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ea08164f5887881904bfcb613683e91a483458c99bbf0f6bcaefa8b2be0d34(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360250c506e060b643381307eb9c3e59412899d10d8ed3466026245c5124e9e3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ff9a4a5ca28bf9581b2ed5f3338362b465069c67da9847da436603c25f5950(
    value: typing.Optional[ApplicationInsightsStandardWebTestValidationRulesContent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc2c2f34bed282d62b5241ce5b2f935ef10f5b09a93f412388f62cc7802d96b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7587adcfca5c91baef0875203a09102ce9639ba07f601cc37ea4148d97d92652(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19198babe63034cd0f35a9e7c4b09cd6461ea1480c1998bc7831ee002329ae09(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a2dda19d8bc1fecad0247be1ae20e84fcf128d0bdfbc205c98ec0b15506f4c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b875afa0c1fa662c2ea4cebdc27560d6f45d00ffc9c86d810a54facfabfee1e(
    value: typing.Optional[ApplicationInsightsStandardWebTestValidationRules],
) -> None:
    """Type checking stubs"""
    pass
