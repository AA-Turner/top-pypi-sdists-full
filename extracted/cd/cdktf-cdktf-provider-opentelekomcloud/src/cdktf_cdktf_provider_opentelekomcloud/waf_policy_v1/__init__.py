r'''
# `opentelekomcloud_waf_policy_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_waf_policy_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1).
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


class WafPolicyV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafPolicyV1.WafPolicyV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1 opentelekomcloud_waf_policy_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        action: typing.Optional[typing.Union["WafPolicyV1Action", typing.Dict[builtins.str, typing.Any]]] = None,
        full_detection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        level: typing.Optional[jsii.Number] = None,
        options: typing.Optional[typing.Union["WafPolicyV1Options", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["WafPolicyV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1 opentelekomcloud_waf_policy_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#name WafPolicyV1#name}.
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#action WafPolicyV1#action}
        :param full_detection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#full_detection WafPolicyV1#full_detection}.
        :param hosts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#hosts WafPolicyV1#hosts}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#id WafPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#level WafPolicyV1#level}.
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#options WafPolicyV1#options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#timeouts WafPolicyV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d705473c8c03e500e1b33552bd9896efd55c3ddaabc812d207a81d8e9fe96b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WafPolicyV1Config(
            name=name,
            action=action,
            full_detection=full_detection,
            hosts=hosts,
            id=id,
            level=level,
            options=options,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a WafPolicyV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WafPolicyV1 to import.
        :param import_from_id: The id of the existing WafPolicyV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WafPolicyV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e202244efc56edc5de545c7ece83dfd63bc1ab1e95becdd904646bbc9ab474a0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAction")
    def put_action(self, *, category: builtins.str) -> None:
        '''
        :param category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#category WafPolicyV1#category}.
        '''
        value = WafPolicyV1Action(category=category)

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putOptions")
    def put_options(
        self,
        *,
        antitamper: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        common: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler_other: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler_scanner: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler_script: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        webattack: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        webshell: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        whiteblackip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param antitamper: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#antitamper WafPolicyV1#antitamper}.
        :param cc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#cc WafPolicyV1#cc}.
        :param common: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#common WafPolicyV1#common}.
        :param crawler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler WafPolicyV1#crawler}.
        :param crawler_engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler_engine WafPolicyV1#crawler_engine}.
        :param crawler_other: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler_other WafPolicyV1#crawler_other}.
        :param crawler_scanner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler_scanner WafPolicyV1#crawler_scanner}.
        :param crawler_script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler_script WafPolicyV1#crawler_script}.
        :param custom: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#custom WafPolicyV1#custom}.
        :param ignore: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#ignore WafPolicyV1#ignore}.
        :param privacy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#privacy WafPolicyV1#privacy}.
        :param webattack: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#webattack WafPolicyV1#webattack}.
        :param webshell: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#webshell WafPolicyV1#webshell}.
        :param whiteblackip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#whiteblackip WafPolicyV1#whiteblackip}.
        '''
        value = WafPolicyV1Options(
            antitamper=antitamper,
            cc=cc,
            common=common,
            crawler=crawler,
            crawler_engine=crawler_engine,
            crawler_other=crawler_other,
            crawler_scanner=crawler_scanner,
            crawler_script=crawler_script,
            custom=custom,
            ignore=ignore,
            privacy=privacy,
            webattack=webattack,
            webshell=webshell,
            whiteblackip=whiteblackip,
        )

        return typing.cast(None, jsii.invoke(self, "putOptions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#create WafPolicyV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#delete WafPolicyV1#delete}.
        '''
        value = WafPolicyV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetFullDetection")
    def reset_full_detection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFullDetection", []))

    @jsii.member(jsii_name="resetHosts")
    def reset_hosts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHosts", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLevel")
    def reset_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevel", []))

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

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
    @jsii.member(jsii_name="action")
    def action(self) -> "WafPolicyV1ActionOutputReference":
        return typing.cast("WafPolicyV1ActionOutputReference", jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> "WafPolicyV1OptionsOutputReference":
        return typing.cast("WafPolicyV1OptionsOutputReference", jsii.get(self, "options"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WafPolicyV1TimeoutsOutputReference":
        return typing.cast("WafPolicyV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional["WafPolicyV1Action"]:
        return typing.cast(typing.Optional["WafPolicyV1Action"], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="fullDetectionInput")
    def full_detection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fullDetectionInput"))

    @builtins.property
    @jsii.member(jsii_name="hostsInput")
    def hosts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="levelInput")
    def level_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "levelInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(self) -> typing.Optional["WafPolicyV1Options"]:
        return typing.cast(typing.Optional["WafPolicyV1Options"], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafPolicyV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafPolicyV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="fullDetection")
    def full_detection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fullDetection"))

    @full_detection.setter
    def full_detection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee8e47a6a8c4dffd1fe9bfde7021abdb58b391ff7b6130fd8cd24caefdb3989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullDetection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hosts")
    def hosts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hosts"))

    @hosts.setter
    def hosts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ae930521258b365b64696bf4a2b746db59c4a872e47de7c115a80250234439)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hosts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df0ff862dca3ededc77b7b224c004d226ad2a385995e931d681ff7cae95e88c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "level"))

    @level.setter
    def level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8476e594ad9c865438a76fd62955a31896c0f952db6773b450e678cddbbefe5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6becfa9d28ff7805be4f6e7e6e929bd76b0bc6827c77384484ccc71a0301a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafPolicyV1.WafPolicyV1Action",
    jsii_struct_bases=[],
    name_mapping={"category": "category"},
)
class WafPolicyV1Action:
    def __init__(self, *, category: builtins.str) -> None:
        '''
        :param category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#category WafPolicyV1#category}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28242c54c5819a16f4f26c30590bd5f49814e84933526622e3203acb80e1832b)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "category": category,
        }

    @builtins.property
    def category(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#category WafPolicyV1#category}.'''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafPolicyV1Action(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafPolicyV1ActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafPolicyV1.WafPolicyV1ActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bdd22d2d9e2bae35a81cdae5dea7c26d92fbededc1464c96cafaa4735f8ea84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0270439956f7b50cc4d96d9d0d4d12123b8728ae5233a2a3fb3b3f57c125005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WafPolicyV1Action]:
        return typing.cast(typing.Optional[WafPolicyV1Action], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[WafPolicyV1Action]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c0a6f34f3377c5443dec3210735908728944e3982958bc7f380c2826e8be6e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafPolicyV1.WafPolicyV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "action": "action",
        "full_detection": "fullDetection",
        "hosts": "hosts",
        "id": "id",
        "level": "level",
        "options": "options",
        "timeouts": "timeouts",
    },
)
class WafPolicyV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        action: typing.Optional[typing.Union[WafPolicyV1Action, typing.Dict[builtins.str, typing.Any]]] = None,
        full_detection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        level: typing.Optional[jsii.Number] = None,
        options: typing.Optional[typing.Union["WafPolicyV1Options", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["WafPolicyV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#name WafPolicyV1#name}.
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#action WafPolicyV1#action}
        :param full_detection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#full_detection WafPolicyV1#full_detection}.
        :param hosts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#hosts WafPolicyV1#hosts}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#id WafPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#level WafPolicyV1#level}.
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#options WafPolicyV1#options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#timeouts WafPolicyV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(action, dict):
            action = WafPolicyV1Action(**action)
        if isinstance(options, dict):
            options = WafPolicyV1Options(**options)
        if isinstance(timeouts, dict):
            timeouts = WafPolicyV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b55b4ad94d3e9ec281f4faee5fe77c27923f1b17861e3bfe15d5861f25543b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument full_detection", value=full_detection, expected_type=type_hints["full_detection"])
            check_type(argname="argument hosts", value=hosts, expected_type=type_hints["hosts"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if action is not None:
            self._values["action"] = action
        if full_detection is not None:
            self._values["full_detection"] = full_detection
        if hosts is not None:
            self._values["hosts"] = hosts
        if id is not None:
            self._values["id"] = id
        if level is not None:
            self._values["level"] = level
        if options is not None:
            self._values["options"] = options
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#name WafPolicyV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional[WafPolicyV1Action]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#action WafPolicyV1#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[WafPolicyV1Action], result)

    @builtins.property
    def full_detection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#full_detection WafPolicyV1#full_detection}.'''
        result = self._values.get("full_detection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hosts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#hosts WafPolicyV1#hosts}.'''
        result = self._values.get("hosts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#id WafPolicyV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def level(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#level WafPolicyV1#level}.'''
        result = self._values.get("level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def options(self) -> typing.Optional["WafPolicyV1Options"]:
        '''options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#options WafPolicyV1#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional["WafPolicyV1Options"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WafPolicyV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#timeouts WafPolicyV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WafPolicyV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafPolicyV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafPolicyV1.WafPolicyV1Options",
    jsii_struct_bases=[],
    name_mapping={
        "antitamper": "antitamper",
        "cc": "cc",
        "common": "common",
        "crawler": "crawler",
        "crawler_engine": "crawlerEngine",
        "crawler_other": "crawlerOther",
        "crawler_scanner": "crawlerScanner",
        "crawler_script": "crawlerScript",
        "custom": "custom",
        "ignore": "ignore",
        "privacy": "privacy",
        "webattack": "webattack",
        "webshell": "webshell",
        "whiteblackip": "whiteblackip",
    },
)
class WafPolicyV1Options:
    def __init__(
        self,
        *,
        antitamper: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        common: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler_other: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler_scanner: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler_script: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        webattack: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        webshell: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        whiteblackip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param antitamper: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#antitamper WafPolicyV1#antitamper}.
        :param cc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#cc WafPolicyV1#cc}.
        :param common: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#common WafPolicyV1#common}.
        :param crawler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler WafPolicyV1#crawler}.
        :param crawler_engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler_engine WafPolicyV1#crawler_engine}.
        :param crawler_other: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler_other WafPolicyV1#crawler_other}.
        :param crawler_scanner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler_scanner WafPolicyV1#crawler_scanner}.
        :param crawler_script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler_script WafPolicyV1#crawler_script}.
        :param custom: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#custom WafPolicyV1#custom}.
        :param ignore: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#ignore WafPolicyV1#ignore}.
        :param privacy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#privacy WafPolicyV1#privacy}.
        :param webattack: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#webattack WafPolicyV1#webattack}.
        :param webshell: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#webshell WafPolicyV1#webshell}.
        :param whiteblackip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#whiteblackip WafPolicyV1#whiteblackip}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de22792c382529576fd1c9fbdd4a2dc4484514e89cebd8593e4a6fd927037abd)
            check_type(argname="argument antitamper", value=antitamper, expected_type=type_hints["antitamper"])
            check_type(argname="argument cc", value=cc, expected_type=type_hints["cc"])
            check_type(argname="argument common", value=common, expected_type=type_hints["common"])
            check_type(argname="argument crawler", value=crawler, expected_type=type_hints["crawler"])
            check_type(argname="argument crawler_engine", value=crawler_engine, expected_type=type_hints["crawler_engine"])
            check_type(argname="argument crawler_other", value=crawler_other, expected_type=type_hints["crawler_other"])
            check_type(argname="argument crawler_scanner", value=crawler_scanner, expected_type=type_hints["crawler_scanner"])
            check_type(argname="argument crawler_script", value=crawler_script, expected_type=type_hints["crawler_script"])
            check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
            check_type(argname="argument ignore", value=ignore, expected_type=type_hints["ignore"])
            check_type(argname="argument privacy", value=privacy, expected_type=type_hints["privacy"])
            check_type(argname="argument webattack", value=webattack, expected_type=type_hints["webattack"])
            check_type(argname="argument webshell", value=webshell, expected_type=type_hints["webshell"])
            check_type(argname="argument whiteblackip", value=whiteblackip, expected_type=type_hints["whiteblackip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if antitamper is not None:
            self._values["antitamper"] = antitamper
        if cc is not None:
            self._values["cc"] = cc
        if common is not None:
            self._values["common"] = common
        if crawler is not None:
            self._values["crawler"] = crawler
        if crawler_engine is not None:
            self._values["crawler_engine"] = crawler_engine
        if crawler_other is not None:
            self._values["crawler_other"] = crawler_other
        if crawler_scanner is not None:
            self._values["crawler_scanner"] = crawler_scanner
        if crawler_script is not None:
            self._values["crawler_script"] = crawler_script
        if custom is not None:
            self._values["custom"] = custom
        if ignore is not None:
            self._values["ignore"] = ignore
        if privacy is not None:
            self._values["privacy"] = privacy
        if webattack is not None:
            self._values["webattack"] = webattack
        if webshell is not None:
            self._values["webshell"] = webshell
        if whiteblackip is not None:
            self._values["whiteblackip"] = whiteblackip

    @builtins.property
    def antitamper(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#antitamper WafPolicyV1#antitamper}.'''
        result = self._values.get("antitamper")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#cc WafPolicyV1#cc}.'''
        result = self._values.get("cc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def common(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#common WafPolicyV1#common}.'''
        result = self._values.get("common")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crawler(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler WafPolicyV1#crawler}.'''
        result = self._values.get("crawler")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crawler_engine(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler_engine WafPolicyV1#crawler_engine}.'''
        result = self._values.get("crawler_engine")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crawler_other(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler_other WafPolicyV1#crawler_other}.'''
        result = self._values.get("crawler_other")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crawler_scanner(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler_scanner WafPolicyV1#crawler_scanner}.'''
        result = self._values.get("crawler_scanner")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crawler_script(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#crawler_script WafPolicyV1#crawler_script}.'''
        result = self._values.get("crawler_script")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def custom(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#custom WafPolicyV1#custom}.'''
        result = self._values.get("custom")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ignore(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#ignore WafPolicyV1#ignore}.'''
        result = self._values.get("ignore")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def privacy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#privacy WafPolicyV1#privacy}.'''
        result = self._values.get("privacy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def webattack(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#webattack WafPolicyV1#webattack}.'''
        result = self._values.get("webattack")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def webshell(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#webshell WafPolicyV1#webshell}.'''
        result = self._values.get("webshell")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def whiteblackip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#whiteblackip WafPolicyV1#whiteblackip}.'''
        result = self._values.get("whiteblackip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafPolicyV1Options(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafPolicyV1OptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafPolicyV1.WafPolicyV1OptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__770ee044dc6c660205e6b871128191269a5c3c823130d299e0c6ce12ed537066)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAntitamper")
    def reset_antitamper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAntitamper", []))

    @jsii.member(jsii_name="resetCc")
    def reset_cc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCc", []))

    @jsii.member(jsii_name="resetCommon")
    def reset_common(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommon", []))

    @jsii.member(jsii_name="resetCrawler")
    def reset_crawler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawler", []))

    @jsii.member(jsii_name="resetCrawlerEngine")
    def reset_crawler_engine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawlerEngine", []))

    @jsii.member(jsii_name="resetCrawlerOther")
    def reset_crawler_other(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawlerOther", []))

    @jsii.member(jsii_name="resetCrawlerScanner")
    def reset_crawler_scanner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawlerScanner", []))

    @jsii.member(jsii_name="resetCrawlerScript")
    def reset_crawler_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawlerScript", []))

    @jsii.member(jsii_name="resetCustom")
    def reset_custom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustom", []))

    @jsii.member(jsii_name="resetIgnore")
    def reset_ignore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnore", []))

    @jsii.member(jsii_name="resetPrivacy")
    def reset_privacy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivacy", []))

    @jsii.member(jsii_name="resetWebattack")
    def reset_webattack(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebattack", []))

    @jsii.member(jsii_name="resetWebshell")
    def reset_webshell(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebshell", []))

    @jsii.member(jsii_name="resetWhiteblackip")
    def reset_whiteblackip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhiteblackip", []))

    @builtins.property
    @jsii.member(jsii_name="antitamperInput")
    def antitamper_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "antitamperInput"))

    @builtins.property
    @jsii.member(jsii_name="ccInput")
    def cc_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ccInput"))

    @builtins.property
    @jsii.member(jsii_name="commonInput")
    def common_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "commonInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlerEngineInput")
    def crawler_engine_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crawlerEngineInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlerInput")
    def crawler_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crawlerInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlerOtherInput")
    def crawler_other_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crawlerOtherInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlerScannerInput")
    def crawler_scanner_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crawlerScannerInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlerScriptInput")
    def crawler_script_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crawlerScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="customInput")
    def custom_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreInput")
    def ignore_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreInput"))

    @builtins.property
    @jsii.member(jsii_name="privacyInput")
    def privacy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privacyInput"))

    @builtins.property
    @jsii.member(jsii_name="webattackInput")
    def webattack_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "webattackInput"))

    @builtins.property
    @jsii.member(jsii_name="webshellInput")
    def webshell_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "webshellInput"))

    @builtins.property
    @jsii.member(jsii_name="whiteblackipInput")
    def whiteblackip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "whiteblackipInput"))

    @builtins.property
    @jsii.member(jsii_name="antitamper")
    def antitamper(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "antitamper"))

    @antitamper.setter
    def antitamper(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e8ea3c6ba58e05fe42badde88120c80fd3740507a0e6c8dd9c382ed798c057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "antitamper", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cc")
    def cc(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cc"))

    @cc.setter
    def cc(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d26c6b2dbe6d44e4b458998b7d0c4026233dffcbbddb7fd31513f5364d7b0d3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="common")
    def common(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "common"))

    @common.setter
    def common(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67d4edf8fd2807c1e44aca2f89cb47e80f3e46804d2015ad4f02b14002b1bbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "common", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crawler")
    def crawler(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crawler"))

    @crawler.setter
    def crawler(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be10bb087c58c3274ec0a4f0ffe991180387c51230528ede7b5180cc94c3ebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crawlerEngine")
    def crawler_engine(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crawlerEngine"))

    @crawler_engine.setter
    def crawler_engine(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a879a3cd40fd159119ccf8cb13eb5991677c39210705a652a59dc14f86492b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawlerEngine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crawlerOther")
    def crawler_other(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crawlerOther"))

    @crawler_other.setter
    def crawler_other(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec088ee8573d3feb33d8f3a9c3a732049bf6bde043f328ea9ca9a538293d9e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawlerOther", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crawlerScanner")
    def crawler_scanner(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crawlerScanner"))

    @crawler_scanner.setter
    def crawler_scanner(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d81ec85e8883509f9cc26faf33f80fdb5154c482abf082c40c1cf12b820b0a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawlerScanner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crawlerScript")
    def crawler_script(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crawlerScript"))

    @crawler_script.setter
    def crawler_script(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b97a8e9da386fa855b2e451218b030808f8245207891ced86becfbf470c17f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawlerScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="custom")
    def custom(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "custom"))

    @custom.setter
    def custom(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65191838f558fb2b4c68b6c3f9d35622a1b1c08aac7998925892489ed29b291f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "custom", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignore"))

    @ignore.setter
    def ignore(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d676836a13b3e040d395ba3852f9268fa68f64a464459f6c83ee3be2c6b7094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privacy")
    def privacy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privacy"))

    @privacy.setter
    def privacy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed1fb63aae3351022b5e9f68809e1bf942b438ae6770157a0de3bffc93d7fa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privacy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webattack")
    def webattack(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "webattack"))

    @webattack.setter
    def webattack(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2ff52d34a26eed019e083c876df2ccd9fd5f7b13124f39aa34f48c4dc40a46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webattack", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webshell")
    def webshell(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "webshell"))

    @webshell.setter
    def webshell(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f61571307766a9b7b09edeb3f5dbe0505dcc02d846de644bcc30285c68cd44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webshell", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="whiteblackip")
    def whiteblackip(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "whiteblackip"))

    @whiteblackip.setter
    def whiteblackip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5150941970ac8ce2e4a5f5e87db60b1c50f3ab461de75badb86d13a1164f4a9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "whiteblackip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WafPolicyV1Options]:
        return typing.cast(typing.Optional[WafPolicyV1Options], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[WafPolicyV1Options]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1cc0f25b84dca6a003faf3d022e01bb2ae38306c241e57efad8ac9f7b354e78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafPolicyV1.WafPolicyV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class WafPolicyV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#create WafPolicyV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#delete WafPolicyV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96bb049a04bcafce8b31e9b6db94a4c9c3491b38e473653ab825b85cfc85f549)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#create WafPolicyV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_policy_v1#delete WafPolicyV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafPolicyV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafPolicyV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafPolicyV1.WafPolicyV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4b5cc3f6a5ae6d0794bc595979090267051fb164bb8d9bc77d9c88fcac1fbb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63e79303a76b1dec564b1d8c3d2d03d3080837b25affc88d996d43fad056466)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77eedbc6617a30f9fa90afe2cd696cc95004ae932d6608189b0c081b92596ee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafPolicyV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafPolicyV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafPolicyV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21fd1654f5869a4601198045e667f24eb6e41a0649595192459beb3294d31aa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WafPolicyV1",
    "WafPolicyV1Action",
    "WafPolicyV1ActionOutputReference",
    "WafPolicyV1Config",
    "WafPolicyV1Options",
    "WafPolicyV1OptionsOutputReference",
    "WafPolicyV1Timeouts",
    "WafPolicyV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__28d705473c8c03e500e1b33552bd9896efd55c3ddaabc812d207a81d8e9fe96b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    action: typing.Optional[typing.Union[WafPolicyV1Action, typing.Dict[builtins.str, typing.Any]]] = None,
    full_detection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    level: typing.Optional[jsii.Number] = None,
    options: typing.Optional[typing.Union[WafPolicyV1Options, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[WafPolicyV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e202244efc56edc5de545c7ece83dfd63bc1ab1e95becdd904646bbc9ab474a0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee8e47a6a8c4dffd1fe9bfde7021abdb58b391ff7b6130fd8cd24caefdb3989(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ae930521258b365b64696bf4a2b746db59c4a872e47de7c115a80250234439(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df0ff862dca3ededc77b7b224c004d226ad2a385995e931d681ff7cae95e88c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8476e594ad9c865438a76fd62955a31896c0f952db6773b450e678cddbbefe5e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6becfa9d28ff7805be4f6e7e6e929bd76b0bc6827c77384484ccc71a0301a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28242c54c5819a16f4f26c30590bd5f49814e84933526622e3203acb80e1832b(
    *,
    category: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bdd22d2d9e2bae35a81cdae5dea7c26d92fbededc1464c96cafaa4735f8ea84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0270439956f7b50cc4d96d9d0d4d12123b8728ae5233a2a3fb3b3f57c125005(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0a6f34f3377c5443dec3210735908728944e3982958bc7f380c2826e8be6e8(
    value: typing.Optional[WafPolicyV1Action],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b55b4ad94d3e9ec281f4faee5fe77c27923f1b17861e3bfe15d5861f25543b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    action: typing.Optional[typing.Union[WafPolicyV1Action, typing.Dict[builtins.str, typing.Any]]] = None,
    full_detection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    level: typing.Optional[jsii.Number] = None,
    options: typing.Optional[typing.Union[WafPolicyV1Options, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[WafPolicyV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de22792c382529576fd1c9fbdd4a2dc4484514e89cebd8593e4a6fd927037abd(
    *,
    antitamper: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    common: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crawler: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crawler_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crawler_other: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crawler_scanner: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crawler_script: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ignore: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    webattack: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    webshell: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    whiteblackip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770ee044dc6c660205e6b871128191269a5c3c823130d299e0c6ce12ed537066(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e8ea3c6ba58e05fe42badde88120c80fd3740507a0e6c8dd9c382ed798c057(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26c6b2dbe6d44e4b458998b7d0c4026233dffcbbddb7fd31513f5364d7b0d3c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67d4edf8fd2807c1e44aca2f89cb47e80f3e46804d2015ad4f02b14002b1bbf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be10bb087c58c3274ec0a4f0ffe991180387c51230528ede7b5180cc94c3ebd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a879a3cd40fd159119ccf8cb13eb5991677c39210705a652a59dc14f86492b0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec088ee8573d3feb33d8f3a9c3a732049bf6bde043f328ea9ca9a538293d9e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d81ec85e8883509f9cc26faf33f80fdb5154c482abf082c40c1cf12b820b0a6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b97a8e9da386fa855b2e451218b030808f8245207891ced86becfbf470c17f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65191838f558fb2b4c68b6c3f9d35622a1b1c08aac7998925892489ed29b291f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d676836a13b3e040d395ba3852f9268fa68f64a464459f6c83ee3be2c6b7094(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed1fb63aae3351022b5e9f68809e1bf942b438ae6770157a0de3bffc93d7fa6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2ff52d34a26eed019e083c876df2ccd9fd5f7b13124f39aa34f48c4dc40a46(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f61571307766a9b7b09edeb3f5dbe0505dcc02d846de644bcc30285c68cd44(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5150941970ac8ce2e4a5f5e87db60b1c50f3ab461de75badb86d13a1164f4a9c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1cc0f25b84dca6a003faf3d022e01bb2ae38306c241e57efad8ac9f7b354e78(
    value: typing.Optional[WafPolicyV1Options],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96bb049a04bcafce8b31e9b6db94a4c9c3491b38e473653ab825b85cfc85f549(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b5cc3f6a5ae6d0794bc595979090267051fb164bb8d9bc77d9c88fcac1fbb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63e79303a76b1dec564b1d8c3d2d03d3080837b25affc88d996d43fad056466(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77eedbc6617a30f9fa90afe2cd696cc95004ae932d6608189b0c081b92596ee3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fd1654f5869a4601198045e667f24eb6e41a0649595192459beb3294d31aa5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafPolicyV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
