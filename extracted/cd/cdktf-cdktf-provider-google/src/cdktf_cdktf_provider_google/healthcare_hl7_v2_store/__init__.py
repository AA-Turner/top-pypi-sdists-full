r'''
# `google_healthcare_hl7_v2_store`

Refer to the Terraform Registry for docs: [`google_healthcare_hl7_v2_store`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store).
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


class HealthcareHl7V2Store(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareHl7V2Store.HealthcareHl7V2Store",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store google_healthcare_hl7_v2_store}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notification_config: typing.Optional[typing.Union["HealthcareHl7V2StoreNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HealthcareHl7V2StoreNotificationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parser_config: typing.Optional[typing.Union["HealthcareHl7V2StoreParserConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        reject_duplicate_message: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["HealthcareHl7V2StoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store google_healthcare_hl7_v2_store} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset: Identifies the dataset addressed by this request. Must be in the format 'projects/{project}/locations/{location}/datasets/{dataset}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#dataset HealthcareHl7V2Store#dataset}
        :param name: The resource name for the Hl7V2Store. ** Changing this property may recreate the Hl7v2 store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#name HealthcareHl7V2Store#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#id HealthcareHl7V2Store#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-supplied key-value pairs used to organize HL7v2 stores. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}_-]{0,62} Label values are optional, must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}_-]{0,63} No more than 64 labels can be associated with a given store. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#labels HealthcareHl7V2Store#labels}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#notification_config HealthcareHl7V2Store#notification_config}
        :param notification_configs: notification_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#notification_configs HealthcareHl7V2Store#notification_configs}
        :param parser_config: parser_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#parser_config HealthcareHl7V2Store#parser_config}
        :param reject_duplicate_message: Determines whether duplicate messages are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#reject_duplicate_message HealthcareHl7V2Store#reject_duplicate_message}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#timeouts HealthcareHl7V2Store#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2f0161e9dddc8b58962ada094d9e8a206e15614b2209ee86207be6ae01ccfa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HealthcareHl7V2StoreConfig(
            dataset=dataset,
            name=name,
            id=id,
            labels=labels,
            notification_config=notification_config,
            notification_configs=notification_configs,
            parser_config=parser_config,
            reject_duplicate_message=reject_duplicate_message,
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
        '''Generates CDKTF code for importing a HealthcareHl7V2Store resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HealthcareHl7V2Store to import.
        :param import_from_id: The id of the existing HealthcareHl7V2Store that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HealthcareHl7V2Store to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb765bfdde27a274c21ddf7daf422136035c1c2ce444250f5306ac91bd1a212)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putNotificationConfig")
    def put_notification_config(self, *, pubsub_topic: builtins.str) -> None:
        '''
        :param pubsub_topic: The Cloud Pub/Sub topic that notifications of changes are published on. Supplied by the client. PubsubMessage.Data will contain the resource name. PubsubMessage.MessageId is the ID of this message. It is guaranteed to be unique within the topic. PubsubMessage.PublishTime is the time at which the message was published. Notifications are only sent if the topic is non-empty. Topic names must be scoped to a project. service-PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com must have publisher permissions on the given Cloud Pub/Sub topic. Not having adequate permissions will cause the calls that send notifications to fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#pubsub_topic HealthcareHl7V2Store#pubsub_topic}
        '''
        value = HealthcareHl7V2StoreNotificationConfig(pubsub_topic=pubsub_topic)

        return typing.cast(None, jsii.invoke(self, "putNotificationConfig", [value]))

    @jsii.member(jsii_name="putNotificationConfigs")
    def put_notification_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HealthcareHl7V2StoreNotificationConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ed0da1615b1d780e7d326fcd035438f460ef44d2a73c3d2e244be8ac852d7ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNotificationConfigs", [value]))

    @jsii.member(jsii_name="putParserConfig")
    def put_parser_config(
        self,
        *,
        allow_null_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        schema: typing.Optional[builtins.str] = None,
        segment_terminator: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_null_header: Determines whether messages with no header are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#allow_null_header HealthcareHl7V2Store#allow_null_header}
        :param schema: JSON encoded string for schemas used to parse messages in this store if schematized parsing is desired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#schema HealthcareHl7V2Store#schema}
        :param segment_terminator: Byte(s) to be used as the segment terminator. If this is unset, '\\r' will be used as segment terminator. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#segment_terminator HealthcareHl7V2Store#segment_terminator}
        :param version: The version of the unschematized parser to be used when a custom 'schema' is not set. Default value: "V1" Possible values: ["V1", "V2", "V3"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#version HealthcareHl7V2Store#version}
        '''
        value = HealthcareHl7V2StoreParserConfig(
            allow_null_header=allow_null_header,
            schema=schema,
            segment_terminator=segment_terminator,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putParserConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#create HealthcareHl7V2Store#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#delete HealthcareHl7V2Store#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#update HealthcareHl7V2Store#update}.
        '''
        value = HealthcareHl7V2StoreTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNotificationConfig")
    def reset_notification_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationConfig", []))

    @jsii.member(jsii_name="resetNotificationConfigs")
    def reset_notification_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationConfigs", []))

    @jsii.member(jsii_name="resetParserConfig")
    def reset_parser_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParserConfig", []))

    @jsii.member(jsii_name="resetRejectDuplicateMessage")
    def reset_reject_duplicate_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRejectDuplicateMessage", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfig")
    def notification_config(
        self,
    ) -> "HealthcareHl7V2StoreNotificationConfigOutputReference":
        return typing.cast("HealthcareHl7V2StoreNotificationConfigOutputReference", jsii.get(self, "notificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigs")
    def notification_configs(self) -> "HealthcareHl7V2StoreNotificationConfigsList":
        return typing.cast("HealthcareHl7V2StoreNotificationConfigsList", jsii.get(self, "notificationConfigs"))

    @builtins.property
    @jsii.member(jsii_name="parserConfig")
    def parser_config(self) -> "HealthcareHl7V2StoreParserConfigOutputReference":
        return typing.cast("HealthcareHl7V2StoreParserConfigOutputReference", jsii.get(self, "parserConfig"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "HealthcareHl7V2StoreTimeoutsOutputReference":
        return typing.cast("HealthcareHl7V2StoreTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigInput")
    def notification_config_input(
        self,
    ) -> typing.Optional["HealthcareHl7V2StoreNotificationConfig"]:
        return typing.cast(typing.Optional["HealthcareHl7V2StoreNotificationConfig"], jsii.get(self, "notificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigsInput")
    def notification_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcareHl7V2StoreNotificationConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcareHl7V2StoreNotificationConfigs"]]], jsii.get(self, "notificationConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="parserConfigInput")
    def parser_config_input(
        self,
    ) -> typing.Optional["HealthcareHl7V2StoreParserConfig"]:
        return typing.cast(typing.Optional["HealthcareHl7V2StoreParserConfig"], jsii.get(self, "parserConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="rejectDuplicateMessageInput")
    def reject_duplicate_message_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rejectDuplicateMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HealthcareHl7V2StoreTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HealthcareHl7V2StoreTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataset"))

    @dataset.setter
    def dataset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b55122f3e973e6c7e4164338cc80062e10d2b15ca5f15bf0aab30d7f26285a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8f209eca0c918e8a09e7ea113d3227074a09c408bc28bcb118d89b7d32aff5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e98e1dd70aac0c5eee658168909eb676d86bf453114e79a5931928daef0b23b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3249b475de65d7cf7b277b176edd822b3547b21863a5da10e6fe4d87585d13a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rejectDuplicateMessage")
    def reject_duplicate_message(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rejectDuplicateMessage"))

    @reject_duplicate_message.setter
    def reject_duplicate_message(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7288db335bf70e600ed3fd6b669a7a9ac52a41ea80814dd7ca847b0a88521f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rejectDuplicateMessage", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcareHl7V2Store.HealthcareHl7V2StoreConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dataset": "dataset",
        "name": "name",
        "id": "id",
        "labels": "labels",
        "notification_config": "notificationConfig",
        "notification_configs": "notificationConfigs",
        "parser_config": "parserConfig",
        "reject_duplicate_message": "rejectDuplicateMessage",
        "timeouts": "timeouts",
    },
)
class HealthcareHl7V2StoreConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dataset: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notification_config: typing.Optional[typing.Union["HealthcareHl7V2StoreNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HealthcareHl7V2StoreNotificationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parser_config: typing.Optional[typing.Union["HealthcareHl7V2StoreParserConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        reject_duplicate_message: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["HealthcareHl7V2StoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset: Identifies the dataset addressed by this request. Must be in the format 'projects/{project}/locations/{location}/datasets/{dataset}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#dataset HealthcareHl7V2Store#dataset}
        :param name: The resource name for the Hl7V2Store. ** Changing this property may recreate the Hl7v2 store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#name HealthcareHl7V2Store#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#id HealthcareHl7V2Store#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-supplied key-value pairs used to organize HL7v2 stores. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}_-]{0,62} Label values are optional, must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}_-]{0,63} No more than 64 labels can be associated with a given store. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#labels HealthcareHl7V2Store#labels}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#notification_config HealthcareHl7V2Store#notification_config}
        :param notification_configs: notification_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#notification_configs HealthcareHl7V2Store#notification_configs}
        :param parser_config: parser_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#parser_config HealthcareHl7V2Store#parser_config}
        :param reject_duplicate_message: Determines whether duplicate messages are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#reject_duplicate_message HealthcareHl7V2Store#reject_duplicate_message}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#timeouts HealthcareHl7V2Store#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(notification_config, dict):
            notification_config = HealthcareHl7V2StoreNotificationConfig(**notification_config)
        if isinstance(parser_config, dict):
            parser_config = HealthcareHl7V2StoreParserConfig(**parser_config)
        if isinstance(timeouts, dict):
            timeouts = HealthcareHl7V2StoreTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ab55ac96c0e64a367d2d9baccea877351342fd6bea2362c2462a147e212b1d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument notification_config", value=notification_config, expected_type=type_hints["notification_config"])
            check_type(argname="argument notification_configs", value=notification_configs, expected_type=type_hints["notification_configs"])
            check_type(argname="argument parser_config", value=parser_config, expected_type=type_hints["parser_config"])
            check_type(argname="argument reject_duplicate_message", value=reject_duplicate_message, expected_type=type_hints["reject_duplicate_message"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset": dataset,
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
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if notification_config is not None:
            self._values["notification_config"] = notification_config
        if notification_configs is not None:
            self._values["notification_configs"] = notification_configs
        if parser_config is not None:
            self._values["parser_config"] = parser_config
        if reject_duplicate_message is not None:
            self._values["reject_duplicate_message"] = reject_duplicate_message
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
    def dataset(self) -> builtins.str:
        '''Identifies the dataset addressed by this request. Must be in the format 'projects/{project}/locations/{location}/datasets/{dataset}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#dataset HealthcareHl7V2Store#dataset}
        '''
        result = self._values.get("dataset")
        assert result is not None, "Required property 'dataset' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name for the Hl7V2Store.

        ** Changing this property may recreate the Hl7v2 store (removing all data) **

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#name HealthcareHl7V2Store#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#id HealthcareHl7V2Store#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-supplied key-value pairs used to organize HL7v2 stores.

        Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must
        conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}_-]{0,62}

        Label values are optional, must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128
        bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}_-]{0,63}

        No more than 64 labels can be associated with a given store.

        An object containing a list of "key": value pairs.
        Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#labels HealthcareHl7V2Store#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def notification_config(
        self,
    ) -> typing.Optional["HealthcareHl7V2StoreNotificationConfig"]:
        '''notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#notification_config HealthcareHl7V2Store#notification_config}
        '''
        result = self._values.get("notification_config")
        return typing.cast(typing.Optional["HealthcareHl7V2StoreNotificationConfig"], result)

    @builtins.property
    def notification_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcareHl7V2StoreNotificationConfigs"]]]:
        '''notification_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#notification_configs HealthcareHl7V2Store#notification_configs}
        '''
        result = self._values.get("notification_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcareHl7V2StoreNotificationConfigs"]]], result)

    @builtins.property
    def parser_config(self) -> typing.Optional["HealthcareHl7V2StoreParserConfig"]:
        '''parser_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#parser_config HealthcareHl7V2Store#parser_config}
        '''
        result = self._values.get("parser_config")
        return typing.cast(typing.Optional["HealthcareHl7V2StoreParserConfig"], result)

    @builtins.property
    def reject_duplicate_message(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether duplicate messages are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#reject_duplicate_message HealthcareHl7V2Store#reject_duplicate_message}
        '''
        result = self._values.get("reject_duplicate_message")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["HealthcareHl7V2StoreTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#timeouts HealthcareHl7V2Store#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["HealthcareHl7V2StoreTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcareHl7V2StoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcareHl7V2Store.HealthcareHl7V2StoreNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={"pubsub_topic": "pubsubTopic"},
)
class HealthcareHl7V2StoreNotificationConfig:
    def __init__(self, *, pubsub_topic: builtins.str) -> None:
        '''
        :param pubsub_topic: The Cloud Pub/Sub topic that notifications of changes are published on. Supplied by the client. PubsubMessage.Data will contain the resource name. PubsubMessage.MessageId is the ID of this message. It is guaranteed to be unique within the topic. PubsubMessage.PublishTime is the time at which the message was published. Notifications are only sent if the topic is non-empty. Topic names must be scoped to a project. service-PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com must have publisher permissions on the given Cloud Pub/Sub topic. Not having adequate permissions will cause the calls that send notifications to fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#pubsub_topic HealthcareHl7V2Store#pubsub_topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08000442b57854dbf8f4bf2d28bf08bc5e4cf03ca01c648cc661164b91ce57cb)
            check_type(argname="argument pubsub_topic", value=pubsub_topic, expected_type=type_hints["pubsub_topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pubsub_topic": pubsub_topic,
        }

    @builtins.property
    def pubsub_topic(self) -> builtins.str:
        '''The Cloud Pub/Sub topic that notifications of changes are published on.

        Supplied by the client.
        PubsubMessage.Data will contain the resource name. PubsubMessage.MessageId is the ID of this message.
        It is guaranteed to be unique within the topic. PubsubMessage.PublishTime is the time at which the message
        was published. Notifications are only sent if the topic is non-empty. Topic names must be scoped to a
        project. service-PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com must have publisher permissions on the given
        Cloud Pub/Sub topic. Not having adequate permissions will cause the calls that send notifications to fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#pubsub_topic HealthcareHl7V2Store#pubsub_topic}
        '''
        result = self._values.get("pubsub_topic")
        assert result is not None, "Required property 'pubsub_topic' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcareHl7V2StoreNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcareHl7V2StoreNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareHl7V2Store.HealthcareHl7V2StoreNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2efef585a17f563ade766a45fc6b56f59d0c6be2ece6e16b465a4d2752a2363)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pubsubTopicInput")
    def pubsub_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubTopic")
    def pubsub_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pubsubTopic"))

    @pubsub_topic.setter
    def pubsub_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3aa75779fbe0ad4840717fd20f783d51bdc6a14e27f5c4f53ef6af9e1057c0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HealthcareHl7V2StoreNotificationConfig]:
        return typing.cast(typing.Optional[HealthcareHl7V2StoreNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcareHl7V2StoreNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64b942661544ed2e99a22ffa2757c295c857ce9471b39ab32db58f8b4a5f24d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcareHl7V2Store.HealthcareHl7V2StoreNotificationConfigs",
    jsii_struct_bases=[],
    name_mapping={"pubsub_topic": "pubsubTopic", "filter": "filter"},
)
class HealthcareHl7V2StoreNotificationConfigs:
    def __init__(
        self,
        *,
        pubsub_topic: builtins.str,
        filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pubsub_topic: The Cloud Pub/Sub topic that notifications of changes are published on. Supplied by the client. PubsubMessage.Data will contain the resource name. PubsubMessage.MessageId is the ID of this message. It is guaranteed to be unique within the topic. PubsubMessage.PublishTime is the time at which the message was published. Notifications are only sent if the topic is non-empty. Topic names must be scoped to a project. service-PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com must have publisher permissions on the given Cloud Pub/Sub topic. Not having adequate permissions will cause the calls that send notifications to fail. If a notification cannot be published to Cloud Pub/Sub, errors will be logged to Stackdriver Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#pubsub_topic HealthcareHl7V2Store#pubsub_topic}
        :param filter: Restricts notifications sent for messages matching a filter. If this is empty, all messages are matched. Syntax: https://cloud.google.com/appengine/docs/standard/python/search/query_strings. Fields/functions available for filtering are: - messageType, from the MSH-9.1 field. For example, NOT messageType = "ADT". - send_date or sendDate, the YYYY-MM-DD date the message was sent in the dataset's timeZone, from the MSH-7 segment. For example, send_date < "2017-01-02". - sendTime, the timestamp when the message was sent, using the RFC3339 time format for comparisons, from the MSH-7 segment. For example, sendTime < "2017-01-02T00:00:00-05:00". - sendFacility, the care center that the message came from, from the MSH-4 segment. For example, sendFacility = "ABC". - PatientId(value, type), which matches if the message lists a patient having an ID of the given value and type in the PID-2, PID-3, or PID-4 segments. For example, PatientId("123456", "MRN"). - labels.x, a string value of the label with key x as set using the Message.labels map. For example, labels."priority"="high". The operator :* can be used to assert the existence of a label. For example, labels."priority":*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#filter HealthcareHl7V2Store#filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0df8c5b80b8077aa3f05f35132eea114ceeb762c362ca5fa7bf8cb0943f9db2)
            check_type(argname="argument pubsub_topic", value=pubsub_topic, expected_type=type_hints["pubsub_topic"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pubsub_topic": pubsub_topic,
        }
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def pubsub_topic(self) -> builtins.str:
        '''The Cloud Pub/Sub topic that notifications of changes are published on.

        Supplied by the client.
        PubsubMessage.Data will contain the resource name. PubsubMessage.MessageId is the ID of this message.
        It is guaranteed to be unique within the topic. PubsubMessage.PublishTime is the time at which the message
        was published. Notifications are only sent if the topic is non-empty. Topic names must be scoped to a
        project. service-PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com must have publisher permissions on the given
        Cloud Pub/Sub topic. Not having adequate permissions will cause the calls that send notifications to fail.

        If a notification cannot be published to Cloud Pub/Sub, errors will be logged to Stackdriver

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#pubsub_topic HealthcareHl7V2Store#pubsub_topic}
        '''
        result = self._values.get("pubsub_topic")
        assert result is not None, "Required property 'pubsub_topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''Restricts notifications sent for messages matching a filter. If this is empty, all messages are matched. Syntax: https://cloud.google.com/appengine/docs/standard/python/search/query_strings.

        Fields/functions available for filtering are:

        - messageType, from the MSH-9.1 field. For example, NOT messageType = "ADT".
        - send_date or sendDate, the YYYY-MM-DD date the message was sent in the dataset's timeZone, from the MSH-7 segment. For example, send_date < "2017-01-02".
        - sendTime, the timestamp when the message was sent, using the RFC3339 time format for comparisons, from the MSH-7 segment. For example, sendTime < "2017-01-02T00:00:00-05:00".
        - sendFacility, the care center that the message came from, from the MSH-4 segment. For example, sendFacility = "ABC".
        - PatientId(value, type), which matches if the message lists a patient having an ID of the given value and type in the PID-2, PID-3, or PID-4 segments. For example, PatientId("123456", "MRN").
        - labels.x, a string value of the label with key x as set using the Message.labels map. For example, labels."priority"="high". The operator :* can be used to assert the existence of a label. For example, labels."priority":*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#filter HealthcareHl7V2Store#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcareHl7V2StoreNotificationConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcareHl7V2StoreNotificationConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareHl7V2Store.HealthcareHl7V2StoreNotificationConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20f577a49215f65f8927a86fc5aeb5c7b3a6fd6af428269c17eb6eb76ff27314)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HealthcareHl7V2StoreNotificationConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51c827d8f3c6f6bf59bda5cd9c1c383405e0557a78b7eb137784026587d49178)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HealthcareHl7V2StoreNotificationConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7655fc513e81138b18f7f1822d63d66cb81cdca15ed7d59e25b4fd7b1fc107c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cd5e48b372dfb49d38972cd8bc0222121d80e8b9179aaed2d2ffbc81aadcd44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cbe860081f4f40d62b133aec2e36562184417775a9647b218639d0e2470cc82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcareHl7V2StoreNotificationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcareHl7V2StoreNotificationConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcareHl7V2StoreNotificationConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad95d996197877f0358385dd93c0e7513952bc9242d3192781d669b5be4794c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HealthcareHl7V2StoreNotificationConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareHl7V2Store.HealthcareHl7V2StoreNotificationConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf19a6dc4b9908038a7584566798b850b6bb65a8be9299c1cf17fe14cbbb4b4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubTopicInput")
    def pubsub_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1fb3bce1b4c5a1b8b544bc11e9db7d1743f4f042c5a10e528f7c27e0c4d50b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pubsubTopic")
    def pubsub_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pubsubTopic"))

    @pubsub_topic.setter
    def pubsub_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d513b1ee6efa77e216c8bf7fbbfcf17a3fe3582379ca06c721ad34065677fad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareHl7V2StoreNotificationConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareHl7V2StoreNotificationConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareHl7V2StoreNotificationConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2617e63918e37efeb3b792e6393b533142aefab3b9b09e63a3528e185f2d4979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcareHl7V2Store.HealthcareHl7V2StoreParserConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allow_null_header": "allowNullHeader",
        "schema": "schema",
        "segment_terminator": "segmentTerminator",
        "version": "version",
    },
)
class HealthcareHl7V2StoreParserConfig:
    def __init__(
        self,
        *,
        allow_null_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        schema: typing.Optional[builtins.str] = None,
        segment_terminator: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_null_header: Determines whether messages with no header are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#allow_null_header HealthcareHl7V2Store#allow_null_header}
        :param schema: JSON encoded string for schemas used to parse messages in this store if schematized parsing is desired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#schema HealthcareHl7V2Store#schema}
        :param segment_terminator: Byte(s) to be used as the segment terminator. If this is unset, '\\r' will be used as segment terminator. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#segment_terminator HealthcareHl7V2Store#segment_terminator}
        :param version: The version of the unschematized parser to be used when a custom 'schema' is not set. Default value: "V1" Possible values: ["V1", "V2", "V3"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#version HealthcareHl7V2Store#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8653c23f288df1a3a69e8db3e5b32373c9f34d651327ab063dad8c57230f30)
            check_type(argname="argument allow_null_header", value=allow_null_header, expected_type=type_hints["allow_null_header"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument segment_terminator", value=segment_terminator, expected_type=type_hints["segment_terminator"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_null_header is not None:
            self._values["allow_null_header"] = allow_null_header
        if schema is not None:
            self._values["schema"] = schema
        if segment_terminator is not None:
            self._values["segment_terminator"] = segment_terminator
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def allow_null_header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether messages with no header are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#allow_null_header HealthcareHl7V2Store#allow_null_header}
        '''
        result = self._values.get("allow_null_header")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''JSON encoded string for schemas used to parse messages in this store if schematized parsing is desired.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#schema HealthcareHl7V2Store#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_terminator(self) -> typing.Optional[builtins.str]:
        '''Byte(s) to be used as the segment terminator. If this is unset, '\\r' will be used as segment terminator.

        A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#segment_terminator HealthcareHl7V2Store#segment_terminator}
        '''
        result = self._values.get("segment_terminator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The version of the unschematized parser to be used when a custom 'schema' is not set.

        Default value: "V1" Possible values: ["V1", "V2", "V3"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#version HealthcareHl7V2Store#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcareHl7V2StoreParserConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcareHl7V2StoreParserConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareHl7V2Store.HealthcareHl7V2StoreParserConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86741cd6b6d89671967aee0c900adc5540795a2565ad1ed3cc4cf9e6dabc4137)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowNullHeader")
    def reset_allow_null_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowNullHeader", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @jsii.member(jsii_name="resetSegmentTerminator")
    def reset_segment_terminator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSegmentTerminator", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="allowNullHeaderInput")
    def allow_null_header_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowNullHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentTerminatorInput")
    def segment_terminator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "segmentTerminatorInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowNullHeader")
    def allow_null_header(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowNullHeader"))

    @allow_null_header.setter
    def allow_null_header(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5018228a6d4becaa252ec22f6b2985c64cd45f7ce7d0afa43cddb8e2a7f0d571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowNullHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f5f1f01cd3677b356bb9554b6b2d5e3bd43e05cd946e5f4b53d8bc477d4563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="segmentTerminator")
    def segment_terminator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "segmentTerminator"))

    @segment_terminator.setter
    def segment_terminator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24eaafd2801d763507d7e1d6f5cb042d817c239fbacf523e50e9d4031cfad818)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentTerminator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e128729f6fb6903bbed499b04e015291cbc840759916fdcc82e3992c743fcec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HealthcareHl7V2StoreParserConfig]:
        return typing.cast(typing.Optional[HealthcareHl7V2StoreParserConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcareHl7V2StoreParserConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2675c2f28ce2d7b4d2591ea8c34da248cd1d4e28b6c27810064687d5d1c95ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcareHl7V2Store.HealthcareHl7V2StoreTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class HealthcareHl7V2StoreTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#create HealthcareHl7V2Store#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#delete HealthcareHl7V2Store#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#update HealthcareHl7V2Store#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f1e8917e3dbadd277e39ef0be9418645cf71fe6450b095e7a25f0fb04bbd150)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#create HealthcareHl7V2Store#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#delete HealthcareHl7V2Store#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_hl7_v2_store#update HealthcareHl7V2Store#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcareHl7V2StoreTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcareHl7V2StoreTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareHl7V2Store.HealthcareHl7V2StoreTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fedf0bc9f857fd34177e585ee1e6941d8290670031c38678e5f712d61cb5278)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81b73c054f3c3a487b3a304216719ff3f9fdd235d21aafbf0a322032252887fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75a77117dd566b9b5ccaee18ecf6939add2d5cb8425d651a4367e988d4940ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ab3e55df1e9d775cf124c15ed19243512a02d385cb4689ba5fe0ee070a5478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareHl7V2StoreTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareHl7V2StoreTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareHl7V2StoreTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80982dbc54a3ea38bff004a9393451caf01109ad95508025a5541b2a5c8dd4c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "HealthcareHl7V2Store",
    "HealthcareHl7V2StoreConfig",
    "HealthcareHl7V2StoreNotificationConfig",
    "HealthcareHl7V2StoreNotificationConfigOutputReference",
    "HealthcareHl7V2StoreNotificationConfigs",
    "HealthcareHl7V2StoreNotificationConfigsList",
    "HealthcareHl7V2StoreNotificationConfigsOutputReference",
    "HealthcareHl7V2StoreParserConfig",
    "HealthcareHl7V2StoreParserConfigOutputReference",
    "HealthcareHl7V2StoreTimeouts",
    "HealthcareHl7V2StoreTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fc2f0161e9dddc8b58962ada094d9e8a206e15614b2209ee86207be6ae01ccfa(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    notification_config: typing.Optional[typing.Union[HealthcareHl7V2StoreNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HealthcareHl7V2StoreNotificationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parser_config: typing.Optional[typing.Union[HealthcareHl7V2StoreParserConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    reject_duplicate_message: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[HealthcareHl7V2StoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ffb765bfdde27a274c21ddf7daf422136035c1c2ce444250f5306ac91bd1a212(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed0da1615b1d780e7d326fcd035438f460ef44d2a73c3d2e244be8ac852d7ea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HealthcareHl7V2StoreNotificationConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b55122f3e973e6c7e4164338cc80062e10d2b15ca5f15bf0aab30d7f26285a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f209eca0c918e8a09e7ea113d3227074a09c408bc28bcb118d89b7d32aff5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98e1dd70aac0c5eee658168909eb676d86bf453114e79a5931928daef0b23b6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3249b475de65d7cf7b277b176edd822b3547b21863a5da10e6fe4d87585d13a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7288db335bf70e600ed3fd6b669a7a9ac52a41ea80814dd7ca847b0a88521f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ab55ac96c0e64a367d2d9baccea877351342fd6bea2362c2462a147e212b1d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dataset: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    notification_config: typing.Optional[typing.Union[HealthcareHl7V2StoreNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HealthcareHl7V2StoreNotificationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parser_config: typing.Optional[typing.Union[HealthcareHl7V2StoreParserConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    reject_duplicate_message: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[HealthcareHl7V2StoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08000442b57854dbf8f4bf2d28bf08bc5e4cf03ca01c648cc661164b91ce57cb(
    *,
    pubsub_topic: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2efef585a17f563ade766a45fc6b56f59d0c6be2ece6e16b465a4d2752a2363(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3aa75779fbe0ad4840717fd20f783d51bdc6a14e27f5c4f53ef6af9e1057c0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64b942661544ed2e99a22ffa2757c295c857ce9471b39ab32db58f8b4a5f24d(
    value: typing.Optional[HealthcareHl7V2StoreNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0df8c5b80b8077aa3f05f35132eea114ceeb762c362ca5fa7bf8cb0943f9db2(
    *,
    pubsub_topic: builtins.str,
    filter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f577a49215f65f8927a86fc5aeb5c7b3a6fd6af428269c17eb6eb76ff27314(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c827d8f3c6f6bf59bda5cd9c1c383405e0557a78b7eb137784026587d49178(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7655fc513e81138b18f7f1822d63d66cb81cdca15ed7d59e25b4fd7b1fc107c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd5e48b372dfb49d38972cd8bc0222121d80e8b9179aaed2d2ffbc81aadcd44(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cbe860081f4f40d62b133aec2e36562184417775a9647b218639d0e2470cc82(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad95d996197877f0358385dd93c0e7513952bc9242d3192781d669b5be4794c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcareHl7V2StoreNotificationConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf19a6dc4b9908038a7584566798b850b6bb65a8be9299c1cf17fe14cbbb4b4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1fb3bce1b4c5a1b8b544bc11e9db7d1743f4f042c5a10e528f7c27e0c4d50b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d513b1ee6efa77e216c8bf7fbbfcf17a3fe3582379ca06c721ad34065677fad1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2617e63918e37efeb3b792e6393b533142aefab3b9b09e63a3528e185f2d4979(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareHl7V2StoreNotificationConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8653c23f288df1a3a69e8db3e5b32373c9f34d651327ab063dad8c57230f30(
    *,
    allow_null_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    schema: typing.Optional[builtins.str] = None,
    segment_terminator: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86741cd6b6d89671967aee0c900adc5540795a2565ad1ed3cc4cf9e6dabc4137(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5018228a6d4becaa252ec22f6b2985c64cd45f7ce7d0afa43cddb8e2a7f0d571(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f5f1f01cd3677b356bb9554b6b2d5e3bd43e05cd946e5f4b53d8bc477d4563(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24eaafd2801d763507d7e1d6f5cb042d817c239fbacf523e50e9d4031cfad818(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e128729f6fb6903bbed499b04e015291cbc840759916fdcc82e3992c743fcec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2675c2f28ce2d7b4d2591ea8c34da248cd1d4e28b6c27810064687d5d1c95ae(
    value: typing.Optional[HealthcareHl7V2StoreParserConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1e8917e3dbadd277e39ef0be9418645cf71fe6450b095e7a25f0fb04bbd150(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fedf0bc9f857fd34177e585ee1e6941d8290670031c38678e5f712d61cb5278(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b73c054f3c3a487b3a304216719ff3f9fdd235d21aafbf0a322032252887fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75a77117dd566b9b5ccaee18ecf6939add2d5cb8425d651a4367e988d4940ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ab3e55df1e9d775cf124c15ed19243512a02d385cb4689ba5fe0ee070a5478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80982dbc54a3ea38bff004a9393451caf01109ad95508025a5541b2a5c8dd4c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareHl7V2StoreTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
