r'''
# AWS::IoTEvents Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

AWS IoT Events enables you to monitor your equipment or device fleets for
failures or changes in operation, and to trigger actions when such events
occur.

## `DetectorModel`

The following example creates an AWS IoT Events detector model to your stack.
The detector model need a reference to at least one AWS IoT Events input.
AWS IoT Events inputs enable the detector to get MQTT payload values from IoT Core rules.

You can define built-in actions to use a timer or set a variable, or send data to other AWS resources.
See also [@aws-cdk/aws-iotevents-actions-alpha](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-iotevents-actions-alpha-readme.html) for other actions.

```python
import aws_cdk.aws_iotevents_alpha as iotevents
import aws_cdk.aws_iotevents_actions_alpha as actions
import aws_cdk.aws_lambda as lambda_

# func: lambda.IFunction


input = iotevents.Input(self, "MyInput",
    input_name="my_input",  # optional
    attribute_json_paths=["payload.deviceId", "payload.temperature"]
)

warm_state = iotevents.State(
    state_name="warm",
    on_enter=[iotevents.Event(
        event_name="test-enter-event",
        condition=iotevents.Expression.current_input(input),
        actions=[actions.LambdaInvokeAction(func)]
    )],
    on_input=[iotevents.Event( # optional
        event_name="test-input-event",
        actions=[actions.LambdaInvokeAction(func)])],
    on_exit=[iotevents.Event( # optional
        event_name="test-exit-event",
        actions=[actions.LambdaInvokeAction(func)])]
)
cold_state = iotevents.State(
    state_name="cold"
)

# transit to coldState when temperature is less than 15
warm_state.transition_to(cold_state,
    event_name="to_coldState",  # optional property, default by combining the names of the States
    when=iotevents.Expression.lt(
        iotevents.Expression.input_attribute(input, "payload.temperature"),
        iotevents.Expression.from_string("15")),
    executing=[actions.LambdaInvokeAction(func)]
)
# transit to warmState when temperature is greater than or equal to 15
cold_state.transition_to(warm_state,
    when=iotevents.Expression.gte(
        iotevents.Expression.input_attribute(input, "payload.temperature"),
        iotevents.Expression.from_string("15"))
)

iotevents.DetectorModel(self, "MyDetectorModel",
    detector_model_name="test-detector-model",  # optional
    description="test-detector-model-description",  # optional property, default is none
    evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
    detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
    initial_state=warm_state
)
```

To grant permissions to put messages in the input,
you can use the `grantWrite()` method:

```python
import aws_cdk.aws_iam as iam
import aws_cdk.aws_iotevents_alpha as iotevents

# grantable: iam.IGrantable

input = iotevents.Input.from_input_name(self, "MyInput", "my_input")

input.grant_write(grantable)
```
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

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_iotevents as _aws_cdk_aws_iotevents_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents-alpha.ActionBindOptions",
    jsii_struct_bases=[],
    name_mapping={"role": "role"},
)
class ActionBindOptions:
    def __init__(self, *, role: "_aws_cdk_aws_iam_ceddda9d.IRole") -> None:
        '''(experimental) Options when binding a Action to a detector model.

        :param role: (experimental) The IAM role assumed by IoT Events to perform the action.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iotevents_alpha as iotevents_alpha
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            
            action_bind_options = iotevents_alpha.ActionBindOptions(
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20926fde4fb434b37799340fd54ef134711c796795e21eba90a4992ceeec9a82)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role": role,
        }

    @builtins.property
    def role(self) -> "_aws_cdk_aws_iam_ceddda9d.IRole":
        '''(experimental) The IAM role assumed by IoT Events to perform the action.

        :stability: experimental
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.IRole", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents-alpha.ActionConfig",
    jsii_struct_bases=[],
    name_mapping={"configuration": "configuration"},
)
class ActionConfig:
    def __init__(
        self,
        *,
        configuration: typing.Union["_aws_cdk_aws_iotevents_ceddda9d.CfnDetectorModel.ActionProperty", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Properties for a AWS IoT Events action.

        :param configuration: (experimental) The configuration for this action.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk.aws_iotevents.ActionProperty import ActionProperty
            from aws_cdk.aws_iotevents.ClearTimerProperty import ClearTimerProperty
            from aws_cdk.aws_iotevents.DynamoDBProperty import DynamoDBProperty
            from aws_cdk.aws_iotevents.PayloadProperty import PayloadProperty, PayloadProperty, PayloadProperty, PayloadProperty, PayloadProperty, PayloadProperty, PayloadProperty, PayloadProperty
            from aws_cdk.aws_iotevents.DynamoDBv2Property import DynamoDBv2Property
            from aws_cdk.aws_iotevents.FirehoseProperty import FirehoseProperty
            from aws_cdk.aws_iotevents.IotEventsProperty import IotEventsProperty
            from aws_cdk.aws_iotevents.IotSiteWiseProperty import IotSiteWiseProperty
            from aws_cdk.aws_iotevents.AssetPropertyValueProperty import AssetPropertyValueProperty
            from aws_cdk.aws_iotevents.AssetPropertyVariantProperty import AssetPropertyVariantProperty
            from aws_cdk.aws_iotevents.AssetPropertyTimestampProperty import AssetPropertyTimestampProperty
            from aws_cdk.aws_iotevents.IotTopicPublishProperty import IotTopicPublishProperty
            from aws_cdk.aws_iotevents.LambdaProperty import LambdaProperty
            from aws_cdk.aws_iotevents.ResetTimerProperty import ResetTimerProperty
            from aws_cdk.aws_iotevents.SetTimerProperty import SetTimerProperty
            from aws_cdk.aws_iotevents.SetVariableProperty import SetVariableProperty
            from aws_cdk.aws_iotevents.SnsProperty import SnsProperty
            from aws_cdk.aws_iotevents.SqsProperty import SqsProperty
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iotevents_alpha as iotevents_alpha
            
            action_config = iotevents_alpha.ActionConfig(
                configuration=ActionProperty(
                    clear_timer=ClearTimerProperty(
                        timer_name="timerName"
                    ),
                    dynamo_db=DynamoDBProperty(
                        hash_key_field="hashKeyField",
                        hash_key_value="hashKeyValue",
                        table_name="tableName",
            
                        # the properties below are optional
                        hash_key_type="hashKeyType",
                        operation="operation",
                        payload=PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        payload_field="payloadField",
                        range_key_field="rangeKeyField",
                        range_key_type="rangeKeyType",
                        range_key_value="rangeKeyValue"
                    ),
                    dynamo_dBv2=DynamoDBv2Property(
                        table_name="tableName",
            
                        # the properties below are optional
                        payload=PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    firehose=FirehoseProperty(
                        delivery_stream_name="deliveryStreamName",
            
                        # the properties below are optional
                        payload=PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        separator="separator"
                    ),
                    iot_events=IotEventsProperty(
                        input_name="inputName",
            
                        # the properties below are optional
                        payload=PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    iot_site_wise=IotSiteWiseProperty(
                        property_value=AssetPropertyValueProperty(
                            value=AssetPropertyVariantProperty(
                                boolean_value="booleanValue",
                                double_value="doubleValue",
                                integer_value="integerValue",
                                string_value="stringValue"
                            ),
            
                            # the properties below are optional
                            quality="quality",
                            timestamp=AssetPropertyTimestampProperty(
                                time_in_seconds="timeInSeconds",
            
                                # the properties below are optional
                                offset_in_nanos="offsetInNanos"
                            )
                        ),
            
                        # the properties below are optional
                        asset_id="assetId",
                        entry_id="entryId",
                        property_alias="propertyAlias",
                        property_id="propertyId"
                    ),
                    iot_topic_publish=IotTopicPublishProperty(
                        mqtt_topic="mqttTopic",
            
                        # the properties below are optional
                        payload=PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    lambda_=LambdaProperty(
                        function_arn="functionArn",
            
                        # the properties below are optional
                        payload=PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    reset_timer=ResetTimerProperty(
                        timer_name="timerName"
                    ),
                    set_timer=SetTimerProperty(
                        timer_name="timerName",
            
                        # the properties below are optional
                        duration_expression="durationExpression",
                        seconds=123
                    ),
                    set_variable=SetVariableProperty(
                        value="value",
                        variable_name="variableName"
                    ),
                    sns=SnsProperty(
                        target_arn="targetArn",
            
                        # the properties below are optional
                        payload=PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    sqs=SqsProperty(
                        queue_url="queueUrl",
            
                        # the properties below are optional
                        payload=PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        use_base64=False
                    )
                )
            )
        '''
        if isinstance(configuration, dict):
            configuration = _aws_cdk_aws_iotevents_ceddda9d.CfnDetectorModel.ActionProperty(**configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f323a9d2882ca041d51982b91761780eaa296bcbf7dca146de7d419c348bb55)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration": configuration,
        }

    @builtins.property
    def configuration(
        self,
    ) -> "_aws_cdk_aws_iotevents_ceddda9d.CfnDetectorModel.ActionProperty":
        '''(experimental) The configuration for this action.

        :stability: experimental
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast("_aws_cdk_aws_iotevents_ceddda9d.CfnDetectorModel.ActionProperty", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents-alpha.DetectorModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "initial_state": "initialState",
        "description": "description",
        "detector_key": "detectorKey",
        "detector_model_name": "detectorModelName",
        "evaluation_method": "evaluationMethod",
        "role": "role",
    },
)
class DetectorModelProps:
    def __init__(
        self,
        *,
        initial_state: "State",
        description: typing.Optional[builtins.str] = None,
        detector_key: typing.Optional[builtins.str] = None,
        detector_model_name: typing.Optional[builtins.str] = None,
        evaluation_method: typing.Optional["EventEvaluation"] = None,
        role: typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"] = None,
    ) -> None:
        '''(experimental) Properties for defining an AWS IoT Events detector model.

        :param initial_state: (experimental) The state that is entered at the creation of each detector.
        :param description: (experimental) A brief description of the detector model. Default: none
        :param detector_key: (experimental) The value used to identify a detector instance. When a device or system sends input, a new detector instance with a unique key value is created. AWS IoT Events can continue to route input to its corresponding detector instance based on this identifying information. This parameter uses a JSON-path expression to select the attribute-value pair in the message payload that is used for identification. To route the message to the correct detector instance, the device must send a message payload that contains the same attribute-value. Default: - none (single detector instance will be created and all inputs will be routed to it)
        :param detector_model_name: (experimental) The name of the detector model. Default: - CloudFormation will generate a unique name of the detector model
        :param evaluation_method: (experimental) Information about the order in which events are evaluated and how actions are executed. When setting to SERIAL, variables are updated and event conditions are evaluated in the order that the events are defined. When setting to BATCH, variables within a state are updated and events within a state are performed only after all event conditions are evaluated. Default: EventEvaluation.BATCH
        :param role: (experimental) The role that grants permission to AWS IoT Events to perform its operations. Default: - a role will be created with default permissions

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_iotevents_alpha as iotevents
            import aws_cdk.aws_iotevents_actions_alpha as actions
            import aws_cdk.aws_lambda as lambda_
            
            # func: lambda.IFunction
            
            
            input = iotevents.Input(self, "MyInput",
                input_name="my_input",  # optional
                attribute_json_paths=["payload.deviceId", "payload.temperature"]
            )
            
            warm_state = iotevents.State(
                state_name="warm",
                on_enter=[iotevents.Event(
                    event_name="test-enter-event",
                    condition=iotevents.Expression.current_input(input),
                    actions=[actions.LambdaInvokeAction(func)]
                )],
                on_input=[iotevents.Event( # optional
                    event_name="test-input-event",
                    actions=[actions.LambdaInvokeAction(func)])],
                on_exit=[iotevents.Event( # optional
                    event_name="test-exit-event",
                    actions=[actions.LambdaInvokeAction(func)])]
            )
            cold_state = iotevents.State(
                state_name="cold"
            )
            
            # transit to coldState when temperature is less than 15
            warm_state.transition_to(cold_state,
                event_name="to_coldState",  # optional property, default by combining the names of the States
                when=iotevents.Expression.lt(
                    iotevents.Expression.input_attribute(input, "payload.temperature"),
                    iotevents.Expression.from_string("15")),
                executing=[actions.LambdaInvokeAction(func)]
            )
            # transit to warmState when temperature is greater than or equal to 15
            cold_state.transition_to(warm_state,
                when=iotevents.Expression.gte(
                    iotevents.Expression.input_attribute(input, "payload.temperature"),
                    iotevents.Expression.from_string("15"))
            )
            
            iotevents.DetectorModel(self, "MyDetectorModel",
                detector_model_name="test-detector-model",  # optional
                description="test-detector-model-description",  # optional property, default is none
                evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
                detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
                initial_state=warm_state
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d902e3d8a0311f2011ce495879c5df80f7a1a1d93daab226cad28456583025)
            check_type(argname="argument initial_state", value=initial_state, expected_type=type_hints["initial_state"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument detector_key", value=detector_key, expected_type=type_hints["detector_key"])
            check_type(argname="argument detector_model_name", value=detector_model_name, expected_type=type_hints["detector_model_name"])
            check_type(argname="argument evaluation_method", value=evaluation_method, expected_type=type_hints["evaluation_method"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "initial_state": initial_state,
        }
        if description is not None:
            self._values["description"] = description
        if detector_key is not None:
            self._values["detector_key"] = detector_key
        if detector_model_name is not None:
            self._values["detector_model_name"] = detector_model_name
        if evaluation_method is not None:
            self._values["evaluation_method"] = evaluation_method
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def initial_state(self) -> "State":
        '''(experimental) The state that is entered at the creation of each detector.

        :stability: experimental
        '''
        result = self._values.get("initial_state")
        assert result is not None, "Required property 'initial_state' is missing"
        return typing.cast("State", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A brief description of the detector model.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detector_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The value used to identify a detector instance.

        When a device or system sends input, a new
        detector instance with a unique key value is created. AWS IoT Events can continue to route
        input to its corresponding detector instance based on this identifying information.

        This parameter uses a JSON-path expression to select the attribute-value pair in the message
        payload that is used for identification. To route the message to the correct detector instance,
        the device must send a message payload that contains the same attribute-value.

        :default: - none (single detector instance will be created and all inputs will be routed to it)

        :stability: experimental
        '''
        result = self._values.get("detector_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detector_model_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the detector model.

        :default: - CloudFormation will generate a unique name of the detector model

        :stability: experimental
        '''
        result = self._values.get("detector_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def evaluation_method(self) -> typing.Optional["EventEvaluation"]:
        '''(experimental) Information about the order in which events are evaluated and how actions are executed.

        When setting to SERIAL, variables are updated and event conditions are evaluated in the order
        that the events are defined.
        When setting to BATCH, variables within a state are updated and events within a state are
        performed only after all event conditions are evaluated.

        :default: EventEvaluation.BATCH

        :stability: experimental
        '''
        result = self._values.get("evaluation_method")
        return typing.cast(typing.Optional["EventEvaluation"], result)

    @builtins.property
    def role(self) -> typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"]:
        '''(experimental) The role that grants permission to AWS IoT Events to perform its operations.

        :default: - a role will be created with default permissions

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DetectorModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents-alpha.Event",
    jsii_struct_bases=[],
    name_mapping={
        "event_name": "eventName",
        "actions": "actions",
        "condition": "condition",
    },
)
class Event:
    def __init__(
        self,
        *,
        event_name: builtins.str,
        actions: typing.Optional[typing.Sequence["IAction"]] = None,
        condition: typing.Optional["Expression"] = None,
    ) -> None:
        '''(experimental) Specifies the actions to be performed when the condition evaluates to ``true``.

        :param event_name: (experimental) The name of the event.
        :param actions: (experimental) The actions to be performed. Default: - no actions will be performed
        :param condition: (experimental) The Boolean expression that, when ``true``, causes the actions to be performed. Default: - none (the actions are always executed)

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iotevents_alpha as iotevents_alpha
            
            # action: iotevents_alpha.IAction
            # expression: iotevents_alpha.Expression
            
            event = iotevents_alpha.Event(
                event_name="eventName",
            
                # the properties below are optional
                actions=[action],
                condition=expression
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d011d9ef714eac2a8c23fd4d92c98bce14bf856ec60df19a14f5bb6c1794b23)
            check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_name": event_name,
        }
        if actions is not None:
            self._values["actions"] = actions
        if condition is not None:
            self._values["condition"] = condition

    @builtins.property
    def event_name(self) -> builtins.str:
        '''(experimental) The name of the event.

        :stability: experimental
        '''
        result = self._values.get("event_name")
        assert result is not None, "Required property 'event_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(self) -> typing.Optional[typing.List["IAction"]]:
        '''(experimental) The actions to be performed.

        :default: - no actions will be performed

        :stability: experimental
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List["IAction"]], result)

    @builtins.property
    def condition(self) -> typing.Optional["Expression"]:
        '''(experimental) The Boolean expression that, when ``true``, causes the actions to be performed.

        :default: - none (the actions are always executed)

        :stability: experimental
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["Expression"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Event(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-iotevents-alpha.EventEvaluation")
class EventEvaluation(enum.Enum):
    '''(experimental) Information about the order in which events are evaluated and how actions are executed.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iotevents_alpha as iotevents
        import aws_cdk.aws_iotevents_actions_alpha as actions
        import aws_cdk.aws_lambda as lambda_
        
        # func: lambda.IFunction
        
        
        input = iotevents.Input(self, "MyInput",
            input_name="my_input",  # optional
            attribute_json_paths=["payload.deviceId", "payload.temperature"]
        )
        
        warm_state = iotevents.State(
            state_name="warm",
            on_enter=[iotevents.Event(
                event_name="test-enter-event",
                condition=iotevents.Expression.current_input(input),
                actions=[actions.LambdaInvokeAction(func)]
            )],
            on_input=[iotevents.Event( # optional
                event_name="test-input-event",
                actions=[actions.LambdaInvokeAction(func)])],
            on_exit=[iotevents.Event( # optional
                event_name="test-exit-event",
                actions=[actions.LambdaInvokeAction(func)])]
        )
        cold_state = iotevents.State(
            state_name="cold"
        )
        
        # transit to coldState when temperature is less than 15
        warm_state.transition_to(cold_state,
            event_name="to_coldState",  # optional property, default by combining the names of the States
            when=iotevents.Expression.lt(
                iotevents.Expression.input_attribute(input, "payload.temperature"),
                iotevents.Expression.from_string("15")),
            executing=[actions.LambdaInvokeAction(func)]
        )
        # transit to warmState when temperature is greater than or equal to 15
        cold_state.transition_to(warm_state,
            when=iotevents.Expression.gte(
                iotevents.Expression.input_attribute(input, "payload.temperature"),
                iotevents.Expression.from_string("15"))
        )
        
        iotevents.DetectorModel(self, "MyDetectorModel",
            detector_model_name="test-detector-model",  # optional
            description="test-detector-model-description",  # optional property, default is none
            evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
            detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
            initial_state=warm_state
        )
    '''

    BATCH = "BATCH"
    '''(experimental) When setting to BATCH, variables within a state are updated and events within a state are performed only after all event conditions are evaluated.

    :stability: experimental
    '''
    SERIAL = "SERIAL"
    '''(experimental) When setting to SERIAL, variables are updated and event conditions are evaluated in the order that the events are defined.

    :stability: experimental
    '''


class Expression(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-iotevents-alpha.Expression",
):
    '''(experimental) Expression for events in Detector Model state.

    :see: https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        import aws_cdk.aws_iotevents_alpha as iotevents
        import aws_cdk.aws_iotevents_actions_alpha as actions
        
        # input: iotevents.IInput
        
        state = iotevents.State(
            state_name="MyState",
            on_enter=[iotevents.Event(
                event_name="test-event",
                condition=iotevents.Expression.current_input(input),
                actions=[
                    actions.SetTimerAction("MyTimer", {
                        "duration": cdk.Duration.seconds(60)
                    })
                ]
            )]
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="add")
    @builtins.classmethod
    def add(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Addition operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00ceabb0ede02d4380a4342f031d6be9754aefee9150d91438094660e3e224d)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "add", [left, right]))

    @jsii.member(jsii_name="and")
    @builtins.classmethod
    def and_(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the AND operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb657c9d1f5239bad7dc15c788a3c4568756deddd703e2936eb79dfd6e1e5e7)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "and", [left, right]))

    @jsii.member(jsii_name="bitwiseAnd")
    @builtins.classmethod
    def bitwise_and(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Bitwise AND operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4d1b0710c65a884840ad11a36b4a2f776a0bf7edcadfaaf5cc05b0634998df)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "bitwiseAnd", [left, right]))

    @jsii.member(jsii_name="bitwiseOr")
    @builtins.classmethod
    def bitwise_or(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Bitwise OR operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158b8f2b0d42d9578359dbde6c6dc9f03406d9a60e26ede145cd68636c2babb0)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "bitwiseOr", [left, right]))

    @jsii.member(jsii_name="bitwiseXor")
    @builtins.classmethod
    def bitwise_xor(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Bitwise XOR operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e507a6a82637d2e3488c2e0d1405f53c2bfd9381427fe81037ed35e4042b93a2)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "bitwiseXor", [left, right]))

    @jsii.member(jsii_name="concat")
    @builtins.classmethod
    def concat(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the String Concatenation operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__951c85762063ee723db575c93c9d39e513caa1cb4eee6125a60249c45ec61d55)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "concat", [left, right]))

    @jsii.member(jsii_name="currentInput")
    @builtins.classmethod
    def current_input(cls, input: "IInput") -> "Expression":
        '''(experimental) Create a expression for function ``currentInput()``.

        It is evaluated to true if the specified input message was received.

        :param input: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d943ce7eee4836819e633481bdedbe381730dd09b452e013e3bf35b97a9f4afd)
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
        return typing.cast("Expression", jsii.sinvoke(cls, "currentInput", [input]))

    @jsii.member(jsii_name="divide")
    @builtins.classmethod
    def divide(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Division operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59c45964852335e15516d903c4714951f31a7334f996786264301ec89357fa2)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "divide", [left, right]))

    @jsii.member(jsii_name="eq")
    @builtins.classmethod
    def eq(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Equal operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf88dbf0a05c3e5688acc26ce923a2a292b496326d719c6a53fcbeb22f59fca)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "eq", [left, right]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, value: builtins.str) -> "Expression":
        '''(experimental) Create a expression from the given string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164b59baba0ca822f434f4240dc0cd06ccdc11fcd517dbf2f21ec05c192fc595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("Expression", jsii.sinvoke(cls, "fromString", [value]))

    @jsii.member(jsii_name="gt")
    @builtins.classmethod
    def gt(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Greater Than operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046e4ec6595fc3c216112690fe9df979c56626cd2b56182d59fc12b828328665)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "gt", [left, right]))

    @jsii.member(jsii_name="gte")
    @builtins.classmethod
    def gte(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Greater Than Or Equal operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ef0fc64bc29e1baa653b1564ee7ce3bcd75abd660b17c9fcc4d6028f667607)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "gte", [left, right]))

    @jsii.member(jsii_name="inputAttribute")
    @builtins.classmethod
    def input_attribute(cls, input: "IInput", path: builtins.str) -> "Expression":
        '''(experimental) Create a expression for get an input attribute as ``$input.TemperatureInput.temperatures[2]``.

        :param input: -
        :param path: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e976d2600e930a8c63d36a87c6600d130a4be2bbf30ac8ea7a876616f732a2b)
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("Expression", jsii.sinvoke(cls, "inputAttribute", [input, path]))

    @jsii.member(jsii_name="lt")
    @builtins.classmethod
    def lt(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Less Than operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b211100df1735870fb20810afb89a0341e5cd5c04d151184fa3b80dde8b350d)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "lt", [left, right]))

    @jsii.member(jsii_name="lte")
    @builtins.classmethod
    def lte(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Less Than Or Equal operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d6651a11477f0528ea018f78c0db056db0a2c6fe88aa67d5ec4b0c1a08a8aa)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "lte", [left, right]))

    @jsii.member(jsii_name="multiply")
    @builtins.classmethod
    def multiply(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Multiplication operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73fbf50c17f9fc9ecf0bd79ad5cf069625e620d7652482bec27c83027bae505c)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "multiply", [left, right]))

    @jsii.member(jsii_name="neq")
    @builtins.classmethod
    def neq(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Not Equal operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e06ba597dcf358eba5c06ae3ade694de5145901fac304df3ed64e41be5c0326)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "neq", [left, right]))

    @jsii.member(jsii_name="or")
    @builtins.classmethod
    def or_(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the OR operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9656095a9323d4674a3a5c3bbb7555bde9a15a359b724999125901c33ba7919)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "or", [left, right]))

    @jsii.member(jsii_name="subtract")
    @builtins.classmethod
    def subtract(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Subtraction operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3096dbaab9161d4178d2450d8513da3ff03ad224206dd9ed13a7af5f8cce1e)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "subtract", [left, right]))

    @jsii.member(jsii_name="timeout")
    @builtins.classmethod
    def timeout(cls, timer_name: builtins.str) -> "Expression":
        '''(experimental) Create a expression for function ``timeout("timer-name")``.

        It is evaluated to true if the specified timer has elapsed.
        You can define a timer only using the ``setTimer`` action.

        :param timer_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10fd51ce70ba2476a4cf6830d7c1c19a309583a11be0a3cd56cf1392471b6c1e)
            check_type(argname="argument timer_name", value=timer_name, expected_type=type_hints["timer_name"])
        return typing.cast("Expression", jsii.sinvoke(cls, "timeout", [timer_name]))

    @jsii.member(jsii_name="evaluate")
    @abc.abstractmethod
    def evaluate(
        self,
        parent_priority: typing.Optional[jsii.Number] = None,
    ) -> builtins.str:
        '''(experimental) This is called to evaluate the expression.

        :param parent_priority: priority of the parent of this expression, used for determining whether or not to add parenthesis around the expression. This is intended to be set according to MDN rules, see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Operator_Precedence#table for details

        :stability: experimental
        '''
        ...


class _ExpressionProxy(Expression):
    @jsii.member(jsii_name="evaluate")
    def evaluate(
        self,
        parent_priority: typing.Optional[jsii.Number] = None,
    ) -> builtins.str:
        '''(experimental) This is called to evaluate the expression.

        :param parent_priority: priority of the parent of this expression, used for determining whether or not to add parenthesis around the expression. This is intended to be set according to MDN rules, see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Operator_Precedence#table for details

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ef328d6e6c693a42a6f99711997502550840a487667f3ddeb2789b9655e1aa)
            check_type(argname="argument parent_priority", value=parent_priority, expected_type=type_hints["parent_priority"])
        return typing.cast(builtins.str, jsii.invoke(self, "evaluate", [parent_priority]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Expression).__jsii_proxy_class__ = lambda : _ExpressionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iotevents-alpha.IAction")
class IAction(typing_extensions.Protocol):
    '''(experimental) An abstract action for DetectorModel.

    :stability: experimental
    '''

    pass


class _IActionProxy:
    '''(experimental) An abstract action for DetectorModel.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iotevents-alpha.IAction"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAction).__jsii_proxy_class__ = lambda : _IActionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iotevents-alpha.IDetectorModel")
class IDetectorModel(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an AWS IoT Events detector model.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="detectorModelName")
    def detector_model_name(self) -> builtins.str:
        '''(experimental) The name of the detector model.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IDetectorModelProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an AWS IoT Events detector model.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iotevents-alpha.IDetectorModel"

    @builtins.property
    @jsii.member(jsii_name="detectorModelName")
    def detector_model_name(self) -> builtins.str:
        '''(experimental) The name of the detector model.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "detectorModelName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDetectorModel).__jsii_proxy_class__ = lambda : _IDetectorModelProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iotevents-alpha.IInput")
class IInput(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an AWS IoT Events input.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="inputArn")
    def input_arn(self) -> builtins.str:
        '''(experimental) The ARN of the input.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="inputName")
    def input_name(self) -> builtins.str:
        '''(experimental) The name of the input.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        *actions: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant the indicated permissions on this input to the given IAM principal (Role/Group/User).

        :param grantee: the principal.
        :param actions: the set of actions to allow (i.e. "iotevents:BatchPutMessage").

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant write permissions on this input and its contents to an IAM principal (Role/Group/User).

        :param grantee: the principal.

        :stability: experimental
        '''
        ...


class _IInputProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an AWS IoT Events input.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iotevents-alpha.IInput"

    @builtins.property
    @jsii.member(jsii_name="inputArn")
    def input_arn(self) -> builtins.str:
        '''(experimental) The ARN of the input.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "inputArn"))

    @builtins.property
    @jsii.member(jsii_name="inputName")
    def input_name(self) -> builtins.str:
        '''(experimental) The name of the input.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "inputName"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        *actions: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant the indicated permissions on this input to the given IAM principal (Role/Group/User).

        :param grantee: the principal.
        :param actions: the set of actions to allow (i.e. "iotevents:BatchPutMessage").

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07908005477c33cbef478a78f4bc98aeb9279c1c6e351886cdf2e5f0a9722a9)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant write permissions on this input and its contents to an IAM principal (Role/Group/User).

        :param grantee: the principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40be6f6250ceea796c11fa1915d4e36aba135380312fd5e2c8fd455b69e6704c)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantWrite", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInput).__jsii_proxy_class__ = lambda : _IInputProxy


@jsii.implements(IInput)
class Input(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iotevents-alpha.Input",
):
    '''(experimental) Defines an AWS IoT Events input in this stack.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iotevents_alpha as iotevents
        import aws_cdk.aws_iam as iam
        
        # role: iam.IRole
        
        
        input = iotevents.Input(self, "MyInput",
            attribute_json_paths=["payload.temperature", "payload.transactionId"]
        )
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
            actions=[
                actions.IotEventsPutMessageAction(input,
                    batch_mode=True,  # optional property, default is 'false'
                    message_id="${payload.transactionId}",  # optional property, default is a new UUID
                    role=role
                )
            ]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        attribute_json_paths: typing.Sequence[builtins.str],
        input_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param attribute_json_paths: (experimental) An expression that specifies an attribute-value pair in a JSON structure. Use this to specify an attribute from the JSON payload that is made available by the input. Inputs are derived from messages sent to AWS IoT Events (BatchPutMessage). Each such message contains a JSON payload. The attribute (and its paired value) specified here are available for use in the condition expressions used by detectors.
        :param input_name: (experimental) The name of the input. Default: - CloudFormation will generate a unique name of the input

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6b910e5d5b2caa5522c7d8f662e72786dd2ecef872db369f0324a113a31cd8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InputProps(
            attribute_json_paths=attribute_json_paths, input_name=input_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromInputName")
    @builtins.classmethod
    def from_input_name(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        input_name: builtins.str,
    ) -> "IInput":
        '''(experimental) Import an existing input.

        :param scope: -
        :param id: -
        :param input_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39889e8c7b2c8ede06baf32b4fdb8cf7df18d2c1612748c2be32038a152f9832)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
        return typing.cast("IInput", jsii.sinvoke(cls, "fromInputName", [scope, id, input_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        *actions: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) [disable-awslint:no-grants].

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c8bce12719999ba437b9d271c94d5a64ea8f7ec3195e3590af06b04f17cdf6)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) [disable-awslint:no-grants].

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ccf828d87dc30a5ca383166bc3b63f5e7c539e64335595946ba8c9a07ae980b)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantWrite", [grantee]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="inputArn")
    def input_arn(self) -> builtins.str:
        '''(experimental) The ARN of the input.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inputArn"))

    @builtins.property
    @jsii.member(jsii_name="inputName")
    def input_name(self) -> builtins.str:
        '''(experimental) The name of the input.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inputName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents-alpha.InputProps",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_json_paths": "attributeJsonPaths",
        "input_name": "inputName",
    },
)
class InputProps:
    def __init__(
        self,
        *,
        attribute_json_paths: typing.Sequence[builtins.str],
        input_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining an AWS IoT Events input.

        :param attribute_json_paths: (experimental) An expression that specifies an attribute-value pair in a JSON structure. Use this to specify an attribute from the JSON payload that is made available by the input. Inputs are derived from messages sent to AWS IoT Events (BatchPutMessage). Each such message contains a JSON payload. The attribute (and its paired value) specified here are available for use in the condition expressions used by detectors.
        :param input_name: (experimental) The name of the input. Default: - CloudFormation will generate a unique name of the input

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_iotevents_alpha as iotevents
            import aws_cdk.aws_iotevents_actions_alpha as actions
            import aws_cdk.aws_lambda as lambda_
            
            # func: lambda.IFunction
            
            
            input = iotevents.Input(self, "MyInput",
                input_name="my_input",  # optional
                attribute_json_paths=["payload.deviceId", "payload.temperature"]
            )
            
            warm_state = iotevents.State(
                state_name="warm",
                on_enter=[iotevents.Event(
                    event_name="test-enter-event",
                    condition=iotevents.Expression.current_input(input),
                    actions=[actions.LambdaInvokeAction(func)]
                )],
                on_input=[iotevents.Event( # optional
                    event_name="test-input-event",
                    actions=[actions.LambdaInvokeAction(func)])],
                on_exit=[iotevents.Event( # optional
                    event_name="test-exit-event",
                    actions=[actions.LambdaInvokeAction(func)])]
            )
            cold_state = iotevents.State(
                state_name="cold"
            )
            
            # transit to coldState when temperature is less than 15
            warm_state.transition_to(cold_state,
                event_name="to_coldState",  # optional property, default by combining the names of the States
                when=iotevents.Expression.lt(
                    iotevents.Expression.input_attribute(input, "payload.temperature"),
                    iotevents.Expression.from_string("15")),
                executing=[actions.LambdaInvokeAction(func)]
            )
            # transit to warmState when temperature is greater than or equal to 15
            cold_state.transition_to(warm_state,
                when=iotevents.Expression.gte(
                    iotevents.Expression.input_attribute(input, "payload.temperature"),
                    iotevents.Expression.from_string("15"))
            )
            
            iotevents.DetectorModel(self, "MyDetectorModel",
                detector_model_name="test-detector-model",  # optional
                description="test-detector-model-description",  # optional property, default is none
                evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
                detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
                initial_state=warm_state
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376cf48a441c56ac544e20bd1c4b475e409bf23ca70ecba8aaf70b2377adc21f)
            check_type(argname="argument attribute_json_paths", value=attribute_json_paths, expected_type=type_hints["attribute_json_paths"])
            check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attribute_json_paths": attribute_json_paths,
        }
        if input_name is not None:
            self._values["input_name"] = input_name

    @builtins.property
    def attribute_json_paths(self) -> typing.List[builtins.str]:
        '''(experimental) An expression that specifies an attribute-value pair in a JSON structure.

        Use this to specify an attribute from the JSON payload that is made available
        by the input. Inputs are derived from messages sent to AWS IoT Events (BatchPutMessage).
        Each such message contains a JSON payload. The attribute (and its paired value)
        specified here are available for use in the condition expressions used by detectors.

        :stability: experimental
        '''
        result = self._values.get("attribute_json_paths")
        assert result is not None, "Required property 'attribute_json_paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def input_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the input.

        :default: - CloudFormation will generate a unique name of the input

        :stability: experimental
        '''
        result = self._values.get("input_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InputProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class State(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iotevents-alpha.State"):
    '''(experimental) Defines a state of a detector.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        import aws_cdk.aws_iotevents_alpha as iotevents
        import aws_cdk.aws_iotevents_actions_alpha as actions
        
        # input: iotevents.IInput
        
        state = iotevents.State(
            state_name="MyState",
            on_enter=[iotevents.Event(
                event_name="test-event",
                condition=iotevents.Expression.current_input(input),
                actions=[
                    actions.SetTimerAction("MyTimer", {
                        "duration": cdk.Duration.seconds(60)
                    })
                ]
            )]
        )
    '''

    def __init__(
        self,
        *,
        state_name: builtins.str,
        on_enter: typing.Optional[typing.Sequence[typing.Union["Event", typing.Dict[builtins.str, typing.Any]]]] = None,
        on_exit: typing.Optional[typing.Sequence[typing.Union["Event", typing.Dict[builtins.str, typing.Any]]]] = None,
        on_input: typing.Optional[typing.Sequence[typing.Union["Event", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param state_name: (experimental) The name of the state.
        :param on_enter: (experimental) Specifies the events on enter. The conditions of the events will be evaluated when entering this state. If the condition of the event evaluates to ``true``, the actions of the event will be executed. Default: - no events will trigger on entering this state
        :param on_exit: (experimental) Specifies the events on exit. The conditions of the events are evaluated when an exiting this state. If the condition evaluates to ``true``, the actions of the event will be executed. Default: - no events will trigger on exiting this state
        :param on_input: (experimental) Specifies the events on input. The conditions of the events will be evaluated when any input is received. If the condition of the event evaluates to ``true``, the actions of the event will be executed. Default: - no events will trigger on input in this state

        :stability: experimental
        '''
        props = StateProps(
            state_name=state_name,
            on_enter=on_enter,
            on_exit=on_exit,
            on_input=on_input,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="transitionTo")
    def transition_to(
        self,
        target_state: "State",
        *,
        when: "Expression",
        event_name: typing.Optional[builtins.str] = None,
        executing: typing.Optional[typing.Sequence["IAction"]] = None,
    ) -> None:
        '''(experimental) Add a transition event to the state.

        The transition event will be triggered if condition is evaluated to ``true``.

        :param target_state: the state that will be transit to when the event triggered.
        :param when: (experimental) The condition that is used to determine to cause the state transition and the actions. When this was evaluated to ``true``, the state transition and the actions are triggered.
        :param event_name: (experimental) The name of the event. Default: string combining the names of the States as ``${originStateName}_to_${targetStateName}``
        :param executing: (experimental) The actions to be performed with the transition. Default: - no actions will be performed

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea498411b2c15daca7c1a0bd009b1ab034e25c1ed1f4bde74aec05b0bef984c)
            check_type(argname="argument target_state", value=target_state, expected_type=type_hints["target_state"])
        options = TransitionOptions(
            when=when, event_name=event_name, executing=executing
        )

        return typing.cast(None, jsii.invoke(self, "transitionTo", [target_state, options]))

    @builtins.property
    @jsii.member(jsii_name="stateName")
    def state_name(self) -> builtins.str:
        '''(experimental) The name of the state.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stateName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents-alpha.StateProps",
    jsii_struct_bases=[],
    name_mapping={
        "state_name": "stateName",
        "on_enter": "onEnter",
        "on_exit": "onExit",
        "on_input": "onInput",
    },
)
class StateProps:
    def __init__(
        self,
        *,
        state_name: builtins.str,
        on_enter: typing.Optional[typing.Sequence[typing.Union["Event", typing.Dict[builtins.str, typing.Any]]]] = None,
        on_exit: typing.Optional[typing.Sequence[typing.Union["Event", typing.Dict[builtins.str, typing.Any]]]] = None,
        on_input: typing.Optional[typing.Sequence[typing.Union["Event", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties for defining a state of a detector.

        :param state_name: (experimental) The name of the state.
        :param on_enter: (experimental) Specifies the events on enter. The conditions of the events will be evaluated when entering this state. If the condition of the event evaluates to ``true``, the actions of the event will be executed. Default: - no events will trigger on entering this state
        :param on_exit: (experimental) Specifies the events on exit. The conditions of the events are evaluated when an exiting this state. If the condition evaluates to ``true``, the actions of the event will be executed. Default: - no events will trigger on exiting this state
        :param on_input: (experimental) Specifies the events on input. The conditions of the events will be evaluated when any input is received. If the condition of the event evaluates to ``true``, the actions of the event will be executed. Default: - no events will trigger on input in this state

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Example automatically generated from non-compiling source. May contain errors.
            import aws_cdk.aws_iotevents_alpha as iotevents
            import aws_cdk.aws_iotevents_actions_alpha as actions
            
            # input: iotevents.IInput
            
            state = iotevents.State(
                state_name="MyState",
                on_enter=[iotevents.Event(
                    event_name="test-event",
                    condition=iotevents.Expression.current_input(input),
                    actions=[
                        actions.SetTimerAction("MyTimer", {
                            "duration": cdk.Duration.seconds(60)
                        })
                    ]
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9334619972ce54dfff64763d224f35d2a1a36545b9caebc0960ebdc079de71)
            check_type(argname="argument state_name", value=state_name, expected_type=type_hints["state_name"])
            check_type(argname="argument on_enter", value=on_enter, expected_type=type_hints["on_enter"])
            check_type(argname="argument on_exit", value=on_exit, expected_type=type_hints["on_exit"])
            check_type(argname="argument on_input", value=on_input, expected_type=type_hints["on_input"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "state_name": state_name,
        }
        if on_enter is not None:
            self._values["on_enter"] = on_enter
        if on_exit is not None:
            self._values["on_exit"] = on_exit
        if on_input is not None:
            self._values["on_input"] = on_input

    @builtins.property
    def state_name(self) -> builtins.str:
        '''(experimental) The name of the state.

        :stability: experimental
        '''
        result = self._values.get("state_name")
        assert result is not None, "Required property 'state_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def on_enter(self) -> typing.Optional[typing.List["Event"]]:
        '''(experimental) Specifies the events on enter.

        The conditions of the events will be evaluated when entering this state.
        If the condition of the event evaluates to ``true``, the actions of the event will be executed.

        :default: - no events will trigger on entering this state

        :stability: experimental
        '''
        result = self._values.get("on_enter")
        return typing.cast(typing.Optional[typing.List["Event"]], result)

    @builtins.property
    def on_exit(self) -> typing.Optional[typing.List["Event"]]:
        '''(experimental) Specifies the events on exit.

        The conditions of the events are evaluated when an exiting this state.
        If the condition evaluates to ``true``, the actions of the event will be executed.

        :default: - no events will trigger on exiting this state

        :stability: experimental
        '''
        result = self._values.get("on_exit")
        return typing.cast(typing.Optional[typing.List["Event"]], result)

    @builtins.property
    def on_input(self) -> typing.Optional[typing.List["Event"]]:
        '''(experimental) Specifies the events on input.

        The conditions of the events will be evaluated when any input is received.
        If the condition of the event evaluates to ``true``, the actions of the event will be executed.

        :default: - no events will trigger on input in this state

        :stability: experimental
        '''
        result = self._values.get("on_input")
        return typing.cast(typing.Optional[typing.List["Event"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents-alpha.TransitionOptions",
    jsii_struct_bases=[],
    name_mapping={"when": "when", "event_name": "eventName", "executing": "executing"},
)
class TransitionOptions:
    def __init__(
        self,
        *,
        when: "Expression",
        event_name: typing.Optional[builtins.str] = None,
        executing: typing.Optional[typing.Sequence["IAction"]] = None,
    ) -> None:
        '''(experimental) Properties for options of state transition.

        :param when: (experimental) The condition that is used to determine to cause the state transition and the actions. When this was evaluated to ``true``, the state transition and the actions are triggered.
        :param event_name: (experimental) The name of the event. Default: string combining the names of the States as ``${originStateName}_to_${targetStateName}``
        :param executing: (experimental) The actions to be performed with the transition. Default: - no actions will be performed

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_iotevents_alpha as iotevents
            import aws_cdk.aws_iotevents_actions_alpha as actions
            import aws_cdk.aws_lambda as lambda_
            
            # func: lambda.IFunction
            
            
            input = iotevents.Input(self, "MyInput",
                input_name="my_input",  # optional
                attribute_json_paths=["payload.deviceId", "payload.temperature"]
            )
            
            warm_state = iotevents.State(
                state_name="warm",
                on_enter=[iotevents.Event(
                    event_name="test-enter-event",
                    condition=iotevents.Expression.current_input(input),
                    actions=[actions.LambdaInvokeAction(func)]
                )],
                on_input=[iotevents.Event( # optional
                    event_name="test-input-event",
                    actions=[actions.LambdaInvokeAction(func)])],
                on_exit=[iotevents.Event( # optional
                    event_name="test-exit-event",
                    actions=[actions.LambdaInvokeAction(func)])]
            )
            cold_state = iotevents.State(
                state_name="cold"
            )
            
            # transit to coldState when temperature is less than 15
            warm_state.transition_to(cold_state,
                event_name="to_coldState",  # optional property, default by combining the names of the States
                when=iotevents.Expression.lt(
                    iotevents.Expression.input_attribute(input, "payload.temperature"),
                    iotevents.Expression.from_string("15")),
                executing=[actions.LambdaInvokeAction(func)]
            )
            # transit to warmState when temperature is greater than or equal to 15
            cold_state.transition_to(warm_state,
                when=iotevents.Expression.gte(
                    iotevents.Expression.input_attribute(input, "payload.temperature"),
                    iotevents.Expression.from_string("15"))
            )
            
            iotevents.DetectorModel(self, "MyDetectorModel",
                detector_model_name="test-detector-model",  # optional
                description="test-detector-model-description",  # optional property, default is none
                evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
                detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
                initial_state=warm_state
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b52f607996c1f375655bb2034e782fd3132aeebbca7488c0a83d710d6b43f0d9)
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
            check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
            check_type(argname="argument executing", value=executing, expected_type=type_hints["executing"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "when": when,
        }
        if event_name is not None:
            self._values["event_name"] = event_name
        if executing is not None:
            self._values["executing"] = executing

    @builtins.property
    def when(self) -> "Expression":
        '''(experimental) The condition that is used to determine to cause the state transition and the actions.

        When this was evaluated to ``true``, the state transition and the actions are triggered.

        :stability: experimental
        '''
        result = self._values.get("when")
        assert result is not None, "Required property 'when' is missing"
        return typing.cast("Expression", result)

    @builtins.property
    def event_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the event.

        :default: string combining the names of the States as ``${originStateName}_to_${targetStateName}``

        :stability: experimental
        '''
        result = self._values.get("event_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executing(self) -> typing.Optional[typing.List["IAction"]]:
        '''(experimental) The actions to be performed with the transition.

        :default: - no actions will be performed

        :stability: experimental
        '''
        result = self._values.get("executing")
        return typing.cast(typing.Optional[typing.List["IAction"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IDetectorModel)
class DetectorModel(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iotevents-alpha.DetectorModel",
):
    '''(experimental) Defines an AWS IoT Events detector model in this stack.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iotevents_alpha as iotevents
        import aws_cdk.aws_iotevents_actions_alpha as actions
        import aws_cdk.aws_lambda as lambda_
        
        # func: lambda.IFunction
        
        
        input = iotevents.Input(self, "MyInput",
            input_name="my_input",  # optional
            attribute_json_paths=["payload.deviceId", "payload.temperature"]
        )
        
        warm_state = iotevents.State(
            state_name="warm",
            on_enter=[iotevents.Event(
                event_name="test-enter-event",
                condition=iotevents.Expression.current_input(input),
                actions=[actions.LambdaInvokeAction(func)]
            )],
            on_input=[iotevents.Event( # optional
                event_name="test-input-event",
                actions=[actions.LambdaInvokeAction(func)])],
            on_exit=[iotevents.Event( # optional
                event_name="test-exit-event",
                actions=[actions.LambdaInvokeAction(func)])]
        )
        cold_state = iotevents.State(
            state_name="cold"
        )
        
        # transit to coldState when temperature is less than 15
        warm_state.transition_to(cold_state,
            event_name="to_coldState",  # optional property, default by combining the names of the States
            when=iotevents.Expression.lt(
                iotevents.Expression.input_attribute(input, "payload.temperature"),
                iotevents.Expression.from_string("15")),
            executing=[actions.LambdaInvokeAction(func)]
        )
        # transit to warmState when temperature is greater than or equal to 15
        cold_state.transition_to(warm_state,
            when=iotevents.Expression.gte(
                iotevents.Expression.input_attribute(input, "payload.temperature"),
                iotevents.Expression.from_string("15"))
        )
        
        iotevents.DetectorModel(self, "MyDetectorModel",
            detector_model_name="test-detector-model",  # optional
            description="test-detector-model-description",  # optional property, default is none
            evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
            detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
            initial_state=warm_state
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        initial_state: "State",
        description: typing.Optional[builtins.str] = None,
        detector_key: typing.Optional[builtins.str] = None,
        detector_model_name: typing.Optional[builtins.str] = None,
        evaluation_method: typing.Optional["EventEvaluation"] = None,
        role: typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param initial_state: (experimental) The state that is entered at the creation of each detector.
        :param description: (experimental) A brief description of the detector model. Default: none
        :param detector_key: (experimental) The value used to identify a detector instance. When a device or system sends input, a new detector instance with a unique key value is created. AWS IoT Events can continue to route input to its corresponding detector instance based on this identifying information. This parameter uses a JSON-path expression to select the attribute-value pair in the message payload that is used for identification. To route the message to the correct detector instance, the device must send a message payload that contains the same attribute-value. Default: - none (single detector instance will be created and all inputs will be routed to it)
        :param detector_model_name: (experimental) The name of the detector model. Default: - CloudFormation will generate a unique name of the detector model
        :param evaluation_method: (experimental) Information about the order in which events are evaluated and how actions are executed. When setting to SERIAL, variables are updated and event conditions are evaluated in the order that the events are defined. When setting to BATCH, variables within a state are updated and events within a state are performed only after all event conditions are evaluated. Default: EventEvaluation.BATCH
        :param role: (experimental) The role that grants permission to AWS IoT Events to perform its operations. Default: - a role will be created with default permissions

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da82ccd2a09d39b64b375cad3ffd5ac6581f089409316fa7b74c022b59a9d4dc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DetectorModelProps(
            initial_state=initial_state,
            description=description,
            detector_key=detector_key,
            detector_model_name=detector_model_name,
            evaluation_method=evaluation_method,
            role=role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDetectorModelName")
    @builtins.classmethod
    def from_detector_model_name(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        detector_model_name: builtins.str,
    ) -> "IDetectorModel":
        '''(experimental) Import an existing detector model.

        :param scope: -
        :param id: -
        :param detector_model_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b301f20279c5f2e72ae53d77871525685e63f098d5614659271ab5ebeab20a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument detector_model_name", value=detector_model_name, expected_type=type_hints["detector_model_name"])
        return typing.cast("IDetectorModel", jsii.sinvoke(cls, "fromDetectorModelName", [scope, id, detector_model_name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="detectorModelName")
    def detector_model_name(self) -> builtins.str:
        '''(experimental) The name of the detector model.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "detectorModelName"))


__all__ = [
    "ActionBindOptions",
    "ActionConfig",
    "DetectorModel",
    "DetectorModelProps",
    "Event",
    "EventEvaluation",
    "Expression",
    "IAction",
    "IDetectorModel",
    "IInput",
    "Input",
    "InputProps",
    "State",
    "StateProps",
    "TransitionOptions",
]

publication.publish()

def _typecheckingstub__20926fde4fb434b37799340fd54ef134711c796795e21eba90a4992ceeec9a82(
    *,
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f323a9d2882ca041d51982b91761780eaa296bcbf7dca146de7d419c348bb55(
    *,
    configuration: typing.Union[_aws_cdk_aws_iotevents_ceddda9d.CfnDetectorModel.ActionProperty, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d902e3d8a0311f2011ce495879c5df80f7a1a1d93daab226cad28456583025(
    *,
    initial_state: State,
    description: typing.Optional[builtins.str] = None,
    detector_key: typing.Optional[builtins.str] = None,
    detector_model_name: typing.Optional[builtins.str] = None,
    evaluation_method: typing.Optional[EventEvaluation] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d011d9ef714eac2a8c23fd4d92c98bce14bf856ec60df19a14f5bb6c1794b23(
    *,
    event_name: builtins.str,
    actions: typing.Optional[typing.Sequence[IAction]] = None,
    condition: typing.Optional[Expression] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00ceabb0ede02d4380a4342f031d6be9754aefee9150d91438094660e3e224d(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb657c9d1f5239bad7dc15c788a3c4568756deddd703e2936eb79dfd6e1e5e7(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4d1b0710c65a884840ad11a36b4a2f776a0bf7edcadfaaf5cc05b0634998df(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158b8f2b0d42d9578359dbde6c6dc9f03406d9a60e26ede145cd68636c2babb0(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e507a6a82637d2e3488c2e0d1405f53c2bfd9381427fe81037ed35e4042b93a2(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951c85762063ee723db575c93c9d39e513caa1cb4eee6125a60249c45ec61d55(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d943ce7eee4836819e633481bdedbe381730dd09b452e013e3bf35b97a9f4afd(
    input: IInput,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59c45964852335e15516d903c4714951f31a7334f996786264301ec89357fa2(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf88dbf0a05c3e5688acc26ce923a2a292b496326d719c6a53fcbeb22f59fca(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164b59baba0ca822f434f4240dc0cd06ccdc11fcd517dbf2f21ec05c192fc595(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046e4ec6595fc3c216112690fe9df979c56626cd2b56182d59fc12b828328665(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ef0fc64bc29e1baa653b1564ee7ce3bcd75abd660b17c9fcc4d6028f667607(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e976d2600e930a8c63d36a87c6600d130a4be2bbf30ac8ea7a876616f732a2b(
    input: IInput,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b211100df1735870fb20810afb89a0341e5cd5c04d151184fa3b80dde8b350d(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d6651a11477f0528ea018f78c0db056db0a2c6fe88aa67d5ec4b0c1a08a8aa(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73fbf50c17f9fc9ecf0bd79ad5cf069625e620d7652482bec27c83027bae505c(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e06ba597dcf358eba5c06ae3ade694de5145901fac304df3ed64e41be5c0326(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9656095a9323d4674a3a5c3bbb7555bde9a15a359b724999125901c33ba7919(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3096dbaab9161d4178d2450d8513da3ff03ad224206dd9ed13a7af5f8cce1e(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10fd51ce70ba2476a4cf6830d7c1c19a309583a11be0a3cd56cf1392471b6c1e(
    timer_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ef328d6e6c693a42a6f99711997502550840a487667f3ddeb2789b9655e1aa(
    parent_priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07908005477c33cbef478a78f4bc98aeb9279c1c6e351886cdf2e5f0a9722a9(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40be6f6250ceea796c11fa1915d4e36aba135380312fd5e2c8fd455b69e6704c(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6b910e5d5b2caa5522c7d8f662e72786dd2ecef872db369f0324a113a31cd8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    attribute_json_paths: typing.Sequence[builtins.str],
    input_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39889e8c7b2c8ede06baf32b4fdb8cf7df18d2c1612748c2be32038a152f9832(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    input_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c8bce12719999ba437b9d271c94d5a64ea8f7ec3195e3590af06b04f17cdf6(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccf828d87dc30a5ca383166bc3b63f5e7c539e64335595946ba8c9a07ae980b(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376cf48a441c56ac544e20bd1c4b475e409bf23ca70ecba8aaf70b2377adc21f(
    *,
    attribute_json_paths: typing.Sequence[builtins.str],
    input_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea498411b2c15daca7c1a0bd009b1ab034e25c1ed1f4bde74aec05b0bef984c(
    target_state: State,
    *,
    when: Expression,
    event_name: typing.Optional[builtins.str] = None,
    executing: typing.Optional[typing.Sequence[IAction]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9334619972ce54dfff64763d224f35d2a1a36545b9caebc0960ebdc079de71(
    *,
    state_name: builtins.str,
    on_enter: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_exit: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_input: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52f607996c1f375655bb2034e782fd3132aeebbca7488c0a83d710d6b43f0d9(
    *,
    when: Expression,
    event_name: typing.Optional[builtins.str] = None,
    executing: typing.Optional[typing.Sequence[IAction]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da82ccd2a09d39b64b375cad3ffd5ac6581f089409316fa7b74c022b59a9d4dc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    initial_state: State,
    description: typing.Optional[builtins.str] = None,
    detector_key: typing.Optional[builtins.str] = None,
    detector_model_name: typing.Optional[builtins.str] = None,
    evaluation_method: typing.Optional[EventEvaluation] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b301f20279c5f2e72ae53d77871525685e63f098d5614659271ab5ebeab20a5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    detector_model_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IAction, IDetectorModel, IInput]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
