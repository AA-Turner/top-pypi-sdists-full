import copy
import json
from io import StringIO
from unittest import TestCase
from unittest.mock import ANY, MagicMock, Mock, call, patch

import click
from box import Box, BoxList

from montecarlodata.common.data import (
    AWSArn,
    BucketRow,
    DcResourceProperties,
    EventProperties,
    ResourceProperties,
)
from montecarlodata.common.resources import CloudResourceService
from montecarlodata.common.user import UserService
from montecarlodata.utils import AwsClientWrapper
from tests.helpers import capture_function
from tests.test_common_user import _SAMPLE_CONFIG

_SAMPLE_REGION = "us-east-1"
_SAMPLE_BUCKET_NAME = "bucket"
_SAMPLE_BASE_OPTIONS = {"foo": "bar"}
_SAMPLE_DC_OUTPUT = [
    {
        "OutputKey": "PrivateS3BucketArn",
        "OutputValue": f"arn:aws:s3:::{_SAMPLE_BUCKET_NAME}",
    }
]
_SAMPLE_CONNECTION_PATH = "test"
_SAMPLE_ACCOUNT_ID = "1234"
_SAMPLE_EXTERNAL_ID = "5678"
_SAMPLE_TIME = "ts"
_SAMPLE_POLICY_FILE = {"hello": "world"}
_SAMPLE_TRUST_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": f"arn:aws:iam::{_SAMPLE_ACCOUNT_ID}:root"},
            "Action": "sts:AssumeRole",
            "Condition": {"StringEquals": {"sts:ExternalId": _SAMPLE_EXTERNAL_ID}},
        }
    ],
}
_SAMPLE_EMR_NAME = "name"
_SAMPLE_EMR_ID = "cluster_id"
_SAMPLE_EMR_ID_2 = "cluster_id_2"
_SAMPLE_EMR_STATE = "WAITING"
_SAMPLE_EMR_STATUS = {"State": _SAMPLE_EMR_STATE}
_SAMPLE_EMR_LOG_URI = "s3://bucket/path"
_SAMPLE_EMR_LOG_URI_2 = "s3://bucket_2/path"

_SAMPLE_BUCKETS_FILE = """bucket_name,prefix,suffix
foo,,
bar,prefix1,
baz,,suffix1
qux,prefix2,suffix2
"""

_SAMPLE_EVENT_PAYLOAD = {
    "bucket_name": "mcd-test-events",
    "collector_aws_profile": "dev",
    "prefix": None,
    "suffix": None,
    "topic_arn": None,
    "bucket_aws_profile": None,
    "event_type": "metadata",
}
_SAMPLE_BUCKETS_FILE_EVENT_PAYLOAD = {
    "buckets_filename": "buckets.csv",
    "collector_aws_profile": "dev",
    "prefix": None,
    "suffix": None,
    "topic_arn": None,
    "bucket_aws_profile": None,
    "event_type": "query-logs",
}
_SAMPLE_COLLECTOR = {
    "uuid": "e34eaf86-092d-47ac-97c3-cfa8b6a6e7fe",
    "stackArn": "arn:aws:cloudformation:us-east-1:123456789:stack/loki/99",
    "active": True,
    "customerAwsAccountId": "123456789",
    "templateVersion": "42",
    "codeVersion": "2042",
    "lastUpdated": None,
}

_SAMPLE_DC_CLIENT = Mock()
_SAMPLE_CUST_RESOURCES_CLIENT = Mock()

_SAMPLE_RESOURCE_PROPERTY_1 = ResourceProperties(
    bucket_name="mcd-test-events",
    client=copy.deepcopy(_SAMPLE_CUST_RESOURCES_CLIENT),
    account_id="123456789",
    region="us-east-1",
)
_SAMPLE_RESOURCE_PROPERTY_2 = ResourceProperties(
    bucket_name="mcd-test-events-us-east-2",
    client=copy.deepcopy(_SAMPLE_CUST_RESOURCES_CLIENT),
    account_id="123456789",
    region="us-east-2",
)

_SAMPLE_RESOURCE_PROPERTIES = [_SAMPLE_RESOURCE_PROPERTY_1, _SAMPLE_RESOURCE_PROPERTY_2]
_SAMPLE_EVENT_DETAILS = EventProperties(
    event_type="metadata",
    event_queue_arn="arn:aws:sqs:us-east-1:123456789:loki-MetadataEventQueue-42",
    collection_region="us-east-1",
    collection_account_id="123456789",
    collection_client=_SAMPLE_DC_CLIENT,
    resource_properties=_SAMPLE_RESOURCE_PROPERTIES,
)


class CloudResourcesTest(TestCase):
    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._aws_wrapper_mock = Mock(autospec=AwsClientWrapper)

        self._service = CloudResourceService(
            _SAMPLE_CONFIG,
            command_name="test",
            aws_wrapper=self._aws_wrapper_mock,
            user_service=self._user_service_mock,
        )

    def tearDown(self) -> None:
        _SAMPLE_DC_CLIENT.reset_mock()
        _SAMPLE_CUST_RESOURCES_CLIENT.reset_mock()

    @patch.object(CloudResourceService, "_read_json")
    def test_create_role_with_invalid_policy(self, mock_read):
        mock_read.side_effect = json.decoder.JSONDecodeError
        self._user_service_mock.active_collector = {"customerAwsAccountId": _SAMPLE_ACCOUNT_ID}

        with self.assertRaises(click.exceptions.Abort):
            self._service.create_role(path_to_policy_doc="invalid")

    @patch.object(CloudResourceService, "_read_json")
    def test_create_role_with_missing_values(self, mock_read):
        mock_read.return_value = _SAMPLE_POLICY_FILE
        self._user_service_mock.active_collector = {}
        with self.assertRaises(click.exceptions.Abort):
            self._service.create_role(path_to_policy_doc="foo")

    @patch.object(CloudResourceService, "_read_json")
    @patch.object(CloudResourceService, "_generate_random_token")
    @patch("time.time", MagicMock(return_value=_SAMPLE_TIME))
    def test_create_role(self, mock_token, mock_read):
        path_to_policy_doc = "foo"
        mock_read.return_value = _SAMPLE_POLICY_FILE
        mock_token.return_value = _SAMPLE_EXTERNAL_ID
        sample_collector = {
            **_SAMPLE_COLLECTOR,
            "customerAwsAccountId": _SAMPLE_ACCOUNT_ID,
            "agents": [],
        }
        self._user_service_mock.active_collector = sample_collector
        self._user_service_mock.get_collector.return_value = Box(sample_collector)
        self._user_service_mock.get_collector_agent.return_value = None

        self._service.create_role(path_to_policy_doc=path_to_policy_doc)

        mock_read.assert_called_once_with(path_to_policy_doc)
        mock_token.assert_called_once_with()

        self._aws_wrapper_mock.create_role.assert_called_once_with(
            role_name=f"monte-carlo-integration-role-{_SAMPLE_TIME}",
            trust_policy=json.dumps(_SAMPLE_TRUST_POLICY),
            tags=self._service._MCD_TAGS,
        )

        self._aws_wrapper_mock.attach_inline_policy.assert_called_once_with(
            role_name=f"monte-carlo-integration-role-{_SAMPLE_TIME}",
            policy_name=f"monte-carlo-integration-cli-policy-{_SAMPLE_TIME}",
            policy_doc=json.dumps(_SAMPLE_POLICY_FILE),
        )

    def test_generate_policy(self):
        policy = self._service._generate_trust_policy(
            account_id=_SAMPLE_ACCOUNT_ID, external_id=_SAMPLE_EXTERNAL_ID
        )

        self.assertEqual(policy, json.dumps(_SAMPLE_TRUST_POLICY))

    @patch.object(click, "echo")
    def test_get_aws_account_id(self, mock_echo):
        aws_remote_agent_data = {
            "uuid": "remote-aws-agent",
            "agentType": "REMOTE_AGENT",
            "platform": "AWS",
            "storageType": "S3",
            "endpoint": "arn:aws:lambda:us-east-1:210987654321:function:mcd-agent-Lambda",
            "isDeleted": False,
            "imageVersion": "800",
        }
        self._user_service_mock.get_collector.return_value = Box(
            {**_SAMPLE_COLLECTOR, "agents": [aws_remote_agent_data]}
        )
        self._user_service_mock.get_collector_agent.return_value = Box(aws_remote_agent_data)
        self.assertEqual("210987654321", self._service._get_aws_account_id())
        mock_echo.assert_not_called()

        self._user_service_mock.get_collector.reset_mock()
        self._user_service_mock.get_collector_agent.reset_mock()
        mock_echo.reset_mock()

        gcp_remote_agent_data = {
            "uuid": "remote-gcp-agent",
            "agentType": "REMOTE_AGENT",
            "platform": "GCP",
            "storageType": "GCS",
            "endpoint": "https://example.com",
            "isDeleted": False,
            "imageVersion": "800",
        }
        self._user_service_mock.get_collector.return_value = Box(
            {**_SAMPLE_COLLECTOR, "agents": [gcp_remote_agent_data]}
        )
        self._user_service_mock.get_collector_agent.return_value = Box(gcp_remote_agent_data)
        with self.assertRaises(click.exceptions.Abort):
            self._service._get_aws_account_id()
        mock_echo.assert_called_once_with(
            "Error - The collector is configured with a non-AWS agent", err=True
        )

        self._user_service_mock.get_collector.reset_mock()
        self._user_service_mock.get_collector_agent.reset_mock()
        mock_echo.reset_mock()

        s3_data_store_agent_data = {
            "uuid": "s3-data-store-agent",
            "agentType": "DATA_STORE_AGENT",
            "platform": "AWS",
            "storageType": "S3",
            "endpoint": "s3-bucket",
            "isDeleted": False,
            "imageVersion": "800",
        }
        self._user_service_mock.get_collector.return_value = Box(
            {**_SAMPLE_COLLECTOR, "agents": [s3_data_store_agent_data]}
        )
        self._user_service_mock.get_collector_agent.return_value = Box(s3_data_store_agent_data)
        self.assertEqual("123456789", self._service._get_aws_account_id())
        mock_echo.assert_not_called()

        self._user_service_mock.get_collector.reset_mock()
        self._user_service_mock.get_collector_agent.reset_mock()
        mock_echo.reset_mock()

        self._user_service_mock.get_collector.return_value = Box(
            {**_SAMPLE_COLLECTOR, "agents": []}
        )
        self._user_service_mock.get_collector_agent.return_value = None
        self.assertEqual("123456789", self._service._get_aws_account_id())
        mock_echo.assert_not_called()

    def test_list_emr_clusters(self):
        self._aws_wrapper_mock.get_emr_cluster_details.return_value = [
            {
                "Name": _SAMPLE_EMR_NAME,
                "Id": _SAMPLE_EMR_ID,
                "Status": _SAMPLE_EMR_STATUS,
                "LogUri": _SAMPLE_EMR_LOG_URI,
            }
        ]

        std_out = capture_function(
            self._service.list_emr_clusters, {"table_format": "plain"}
        ).std_out

        expected_output = (
            "Name    Id          State    LogUri\n"
            f"{_SAMPLE_EMR_NAME}    {_SAMPLE_EMR_ID}  {_SAMPLE_EMR_STATE}  {_SAMPLE_EMR_LOG_URI}"
        )
        self.assertEqual(std_out.getvalue().strip(), expected_output)

    def test_list_emr_clusters_no_wait(self):
        self._aws_wrapper_mock.get_emr_cluster_details.return_value = [
            {
                "Name": _SAMPLE_EMR_NAME,
                "Id": _SAMPLE_EMR_ID,
                "Status": _SAMPLE_EMR_STATUS,
                "LogUri": _SAMPLE_EMR_LOG_URI,
            }
        ]

        std_out = capture_function(self._service.list_emr_clusters, {"no_grid": True}).std_out
        expected_output = "  ".join(
            [_SAMPLE_EMR_NAME, _SAMPLE_EMR_ID, _SAMPLE_EMR_STATE, _SAMPLE_EMR_LOG_URI]
        )
        self.assertEqual(std_out.getvalue().strip().strip(), expected_output)

    def test_list_emr_clusters_only_log_locations(self):
        self._aws_wrapper_mock.get_emr_cluster_details.return_value = [
            {
                "Name": _SAMPLE_EMR_NAME,
                "Id": _SAMPLE_EMR_ID,
                "Status": _SAMPLE_EMR_STATUS,
                "LogUri": _SAMPLE_EMR_LOG_URI,
            },
            {
                "Name": _SAMPLE_EMR_NAME,
                "Id": _SAMPLE_EMR_ID_2,
                "Status": _SAMPLE_EMR_STATUS,
                "LogUri": _SAMPLE_EMR_LOG_URI_2,
            },
        ]

        std_out = capture_function(
            self._service.list_emr_clusters, {"only_log_locations": True}
        ).std_out
        self.assertEqual(
            set(std_out.getvalue().strip().split("\n")),
            {_SAMPLE_EMR_LOG_URI, _SAMPLE_EMR_LOG_URI_2},
        )

    def test_list_emr_clusters_no_clusters(self):
        self._aws_wrapper_mock.get_emr_cluster_details.return_value = []
        self._user_service_mock.active_collector = {"customerAwsAccountId": _SAMPLE_ACCOUNT_ID}

        std_out = capture_function(
            self._service.list_emr_clusters, {"table_format": "plain"}
        ).std_out
        self.assertEqual(std_out.getvalue().strip(), "Name    Id    State    LogUri")

    @patch("montecarlodata.common.resources.click")
    @patch.object(CloudResourceService, "_initialize_events")
    @patch.object(CloudResourceService, "_create_or_update_event_topic")
    @patch.object(CloudResourceService, "_update_event_q")
    @patch.object(CloudResourceService, "_create_topic_subscription")
    @patch.object(CloudResourceService, "_create_event_notification")
    def test_add_events_flow(
        self,
        mock_notification,
        mock_topic_sub,
        mock_q,
        mock_topic,
        mock_setup,
        mock_click,
    ):
        self._user_service_mock.get_collector.return_value = Box(_SAMPLE_COLLECTOR)
        mock_setup.return_value = _SAMPLE_EVENT_DETAILS

        self._service.add_events(**_SAMPLE_EVENT_PAYLOAD)

        self._user_service_mock.get_collector.assert_called_once_with(dc_id=None, agent_id=None)

        mock_setup.assert_called_once_with(
            collector_props=_SAMPLE_COLLECTOR, **_SAMPLE_EVENT_PAYLOAD
        )
        mock_topic.assert_called_once_with(event_details=_SAMPLE_EVENT_DETAILS, skip_prompts=False)
        mock_q.assert_called_once_with(event_details=_SAMPLE_EVENT_DETAILS, skip_prompts=False)
        mock_topic_sub.assert_called_once_with(
            event_details=_SAMPLE_EVENT_DETAILS, skip_prompts=False
        )
        mock_notification.assert_called_once_with(
            event_details=_SAMPLE_EVENT_DETAILS, skip_prompts=False
        )

        mock_click.assert_has_calls(
            [
                call.echo("[Gathering collector and resource details]"),
                call.echo("\nProcess complete. Have a nice day!"),
            ]
        )

    def test_add_events_with_an_inactive_collector(self):
        dc_id = "thor"
        inactive_collector = Box(copy.deepcopy(_SAMPLE_COLLECTOR))
        inactive_collector.active = False

        self._user_service_mock.get_collector.return_value = inactive_collector
        with self.assertRaises(click.exceptions.Abort):
            self._service.add_events(**_SAMPLE_EVENT_PAYLOAD, **{"dc_id": dc_id})
        self._user_service_mock.get_collector.assert_called_once_with(dc_id=dc_id, agent_id=None)

    @patch("montecarlodata.common.resources.AwsClientWrapper")
    @patch.object(CloudResourceService, "_get_relevant_q")
    def test_initialize_events(self, mock_get_q, aws_wrapper):
        derived_bucket_location, dc_outputs, q_arn = (
            "thor",
            {"foo": "bar"},
            "arn:aws:sqs:us-east-1:12345:odin",
        )
        aws_wrapper().get_bucket_location.return_value = derived_bucket_location
        aws_wrapper().region = derived_bucket_location
        aws_wrapper().get_stack_outputs.return_value = dc_outputs
        aws_wrapper().get_caller_identity.return_value = AWSArn(q_arn).account

        mock_get_q.return_value = q_arn

        answer = self._service._initialize_events(
            collector_props=Box(_SAMPLE_COLLECTOR), **_SAMPLE_EVENT_PAYLOAD
        )
        expected = EventProperties(
            event_type=_SAMPLE_EVENT_PAYLOAD["event_type"],
            event_queue_arn=q_arn,
            collection_region=AWSArn(q_arn).region,
            collection_account_id=AWSArn(_SAMPLE_COLLECTOR["stackArn"]).account,
            collection_client=ANY,
            resource_properties=[
                ResourceProperties(
                    account_id=AWSArn(q_arn).account,
                    region=derived_bucket_location,
                    bucket_name=_SAMPLE_EVENT_PAYLOAD["bucket_name"],
                    client=ANY,
                )
            ],
        )
        self.assertEqual(answer, expected)

        aws_wrapper.assert_has_calls(
            [
                call(
                    profile_name=_SAMPLE_EVENT_PAYLOAD["collector_aws_profile"],
                    region_name="us-east-1",
                ),
                call().get_stack_outputs(stack_id=_SAMPLE_COLLECTOR["stackArn"]),
                call(profile_name=None),
                call().get_bucket_location(bucket_name="mcd-test-events"),
                call(
                    profile_name=None,
                    region_name=derived_bucket_location,
                ),
                call().get_caller_identity(),
            ]
        )
        mock_get_q.assert_called_once_with("metadata", dc_outputs)

    @patch("montecarlodata.common.resources.AwsClientWrapper")
    @patch.object(CloudResourceService, "_get_relevant_q")
    @patch.object(CloudResourceService, "parse_buckets_file")
    def test_initialize_events_from_buckets_file(self, mock_parse_buckets, mock_get_q, aws_wrapper):
        derived_bucket_location, dc_outputs, q_arn = (
            "thor",
            {"foo": "bar"},
            "arn:aws:sqs:us-east-1:12345:odin",
        )
        aws_wrapper().get_bucket_location.return_value = derived_bucket_location
        aws_wrapper().region = derived_bucket_location
        aws_wrapper().get_stack_outputs.return_value = dc_outputs
        aws_wrapper().get_caller_identity.return_value = AWSArn(q_arn).account

        mock_get_q.return_value = q_arn
        mock_parse_buckets.return_value = [
            BucketRow(bucket_name="foo"),
            BucketRow(bucket_name="bar"),
            BucketRow(bucket_name="baz"),
        ]

        answer = self._service._initialize_events(
            collector_props=Box(_SAMPLE_COLLECTOR), **_SAMPLE_BUCKETS_FILE_EVENT_PAYLOAD
        )
        expected = EventProperties(
            event_type=_SAMPLE_BUCKETS_FILE_EVENT_PAYLOAD["event_type"],
            event_queue_arn=q_arn,
            collection_region=AWSArn(q_arn).region,
            collection_account_id=AWSArn(_SAMPLE_COLLECTOR["stackArn"]).account,
            collection_client=ANY,
            resource_properties=[
                ResourceProperties(
                    account_id=AWSArn(q_arn).account,
                    region=derived_bucket_location,
                    bucket_name="foo",
                    client=ANY,
                ),
                ResourceProperties(
                    account_id=AWSArn(q_arn).account,
                    region=derived_bucket_location,
                    bucket_name="bar",
                    client=ANY,
                ),
                ResourceProperties(
                    account_id=AWSArn(q_arn).account,
                    region=derived_bucket_location,
                    bucket_name="baz",
                    client=ANY,
                ),
            ],
        )

        self.assertEqual(answer, expected)

        aws_wrapper.assert_has_calls(
            [
                call(
                    profile_name=_SAMPLE_EVENT_PAYLOAD["collector_aws_profile"],
                    region_name="us-east-1",
                ),
                call().get_stack_outputs(stack_id=_SAMPLE_COLLECTOR["stackArn"]),
                call(profile_name=None),
                call().get_bucket_location(bucket_name="foo"),
                call(
                    profile_name=None,
                    region_name=derived_bucket_location,
                ),
                call().get_bucket_location(bucket_name="bar"),
                call().get_bucket_location(bucket_name="baz"),
                call().get_caller_identity(),
                call().get_caller_identity(),
                call().get_caller_identity(),
            ]
        )
        mock_get_q.assert_called_once_with("query-logs", dc_outputs)

    @patch("builtins.open")
    def test_parse_buckets_file(self, mock_open):
        mock_open.return_value = StringIO(_SAMPLE_BUCKETS_FILE)
        answer = self._service.parse_buckets_file("test_filename")
        expected = [
            BucketRow(bucket_name="foo", prefix="", suffix=""),
            BucketRow(bucket_name="bar", prefix="prefix1", suffix=""),
            BucketRow(bucket_name="baz", prefix="", suffix="suffix1"),
            BucketRow(bucket_name="qux", prefix="prefix2", suffix="suffix2"),
        ]

        self.assertEqual(answer, expected)

    def test_get_relevant_q(self):
        m_out, q_out = "loki", "thor"
        sample_outputs = [
            {
                "OutputKey": "MetadataEventQueue",
                "OutputValue": m_out,
                "Description": "Metadata event queue ARN",
            },
            {
                "OutputKey": "PublicIP",
                "OutputValue": "127.0.0.1",
                "Description": "Does stuff",
            },
            {
                "OutputKey": "QueryLogEventQueue",
                "OutputValue": q_out,
                "Description": "Query log event queue ARN",
            },
        ]

        self.assertEqual(
            self._service._get_relevant_q(event_type="metadata", outputs=BoxList(sample_outputs)),
            m_out,
        )
        self.assertEqual(
            self._service._get_relevant_q(event_type="query-logs", outputs=BoxList(sample_outputs)),
            q_out,
        )
        with self.assertRaises(click.exceptions.Abort):
            self._service._get_relevant_q(
                event_type="invalid", outputs=BoxList(sample_outputs)
            )  # bad event type
        with self.assertRaises(click.exceptions.Abort):
            self._service._get_relevant_q(
                event_type="metadata", outputs=Box({})
            )  # missing event config

    @patch("montecarlodata.common.resources.prompt_connection")
    @patch.object(CloudResourceService, "_extend_topic_policy")
    @patch.object(CloudResourceService, "_is_preexisting_topic_policy")
    @patch.object(CloudResourceService, "_get_preexisting_topic_policy")
    @patch.object(CloudResourceService, "_save_event_properties")
    def test_create_or_update_event_topic(
        self,
        mock_save_event_properties,
        mock_get_preexisting,
        mock_is_preexisting,
        mock_extend_policy,
        mock_prompt,
    ):
        attributes = Box({"Condition": {"StringEquals": {"aws:SourceArn": "foo"}}})

        events = copy.deepcopy(_SAMPLE_EVENT_DETAILS)
        for resource in events.resource_properties:
            region = resource.region
            topic_arn = (
                f"arn:aws:sns:{region}:12345:monte-carlo-data-{region}-metadata-events-topic"
            )
            resource.client.create_sns_topic.return_value = topic_arn
            resource.client.get_topic_attributes.return_value = attributes

        mock_get_preexisting.return_value = attributes
        mock_is_preexisting.return_value = False
        mock_extend_policy.return_value = attributes

        self._service._create_or_update_event_topic(event_details=events, skip_prompts=True)

        mock_is_preexisting.assert_has_calls(
            [
                call(
                    topic_policy_id="monte-carlo-data-metadata-loki-MetadataEventQueue-42-ID",
                    topic_attributes=attributes,
                ),
                call(
                    topic_policy_id="monte-carlo-data-metadata-loki-MetadataEventQueue-42-ID",
                    topic_attributes=attributes,
                ),
            ]
        )
        mock_extend_policy.assert_has_calls(
            [
                call(
                    topic_attributes=Box({"Condition": {"StringEquals": {"aws:SourceArn": "foo"}}}),
                    new_statements=[
                        {
                            "Sid": "monte-carlo-data-metadata-loki-MetadataEventQueue-42-ID",
                            "Effect": "Allow",
                            "Principal": {"AWS": "123456789"},
                            "Action": "sns:Subscribe",
                            "Resource": "arn:aws:sns:us-east-1:12345:monte-carlo-data-us-east-1-metadata-events-topic",
                        }
                    ],
                    update_statements={
                        "monte-carlo-data-metadata-monte-carlo-data-us-east-1-metadata-events-topic-ID": Box(
                            {
                                "Condition": {
                                    "StringEquals": {
                                        "aws:SourceArn": [
                                            "foo",
                                            "arn:aws:s3:::mcd-test-events",
                                        ]
                                    }
                                }
                            }
                        )
                    },
                ),
                call(
                    topic_attributes=Box({"Condition": {"StringEquals": {"aws:SourceArn": "foo"}}}),
                    new_statements=[
                        {
                            "Sid": "monte-carlo-data-metadata-loki-MetadataEventQueue-42-ID",
                            "Effect": "Allow",
                            "Principal": {"AWS": "123456789"},
                            "Action": "sns:Subscribe",
                            "Resource": "arn:aws:sns:us-east-2:12345:monte-carlo-data-us-east-2-metadata-events-topic",
                        }
                    ],
                    update_statements={
                        "monte-carlo-data-metadata-monte-carlo-data-us-east-2-metadata-events-topic-ID": Box(
                            {
                                "Condition": {
                                    "StringEquals": {
                                        "aws:SourceArn": [
                                            "foo",
                                            "arn:aws:s3:::mcd-test-events-us-east-2",
                                        ]
                                    }
                                }
                            }
                        )
                    },
                ),
            ]
        )

        for resource in events.resource_properties:
            resource.client.set_topic_attributes.assert_called_once_with(
                arn=resource.topic_arn, name="Policy", value=attributes
            )
            resource.client.get_topic_attributes.assert_called_once_with(arn=resource.topic_arn)
            resource.client.create_sns_topic.assert_called_once_with(name=resource.topic_name)
        mock_prompt.assert_has_calls(
            [
                call(
                    message="Create topic 'monte-carlo-data-us-east-1-metadata-events-topic' in 'us-east-1' (123456789)? "
                    "This is an idempotent operation.",
                    skip_prompt=True,
                ),
                call(message="Please confirm", skip_prompt=True),
                call(
                    message="Create topic 'monte-carlo-data-us-east-2-metadata-events-topic' in 'us-east-2' (123456789)? "
                    "This is an idempotent operation.",
                    skip_prompt=True,
                ),
                call(message="Please confirm", skip_prompt=True),
            ]
        )

        mock_save_event_properties.assert_called()

    def test_create_or_update_event_topic_arn_invalid(self):
        events = copy.deepcopy(_SAMPLE_EVENT_DETAILS)

        with self.assertRaises(click.exceptions.Abort):
            for resource in events.resource_properties:
                resource.topic_arn = "foo"
            self._service._create_or_update_event_topic(
                event_details=events, skip_prompts=True
            )  # invalid ARN

    def test_create_or_update_event_topic_region_invalid(self):
        events = copy.deepcopy(_SAMPLE_EVENT_DETAILS)

        with self.assertRaises(click.exceptions.Abort):
            for resource in events.resource_properties:
                resource.topic_arn = (
                    "arn:aws:sns:us-west-1:12345:monte-carlo-data-us-east-1-metadata-events-topic"
                )
            self._service._create_or_update_event_topic(
                event_details=events, skip_prompts=True
            )  # region mismatch

    def test_preexisting_topic_policy(self):
        sid, topic_attributes = "foo", Box({"Attributes": {"Policy": '{"Statement": []}'}})
        self.assertFalse(self._service._is_preexisting_topic_policy(sid, topic_attributes))

        topic_attributes = Box({"Attributes": {"Policy": '{"Statement": [{"Sid": "foo"}]}'}})
        self.assertTrue(self._service._is_preexisting_topic_policy(sid, topic_attributes))

    def test_extend_topic_policy(self):
        topic_attributes = Box({"Attributes": {"Policy": '{"Statement": [{"Sid": "foo"}]}'}})
        new_statements = [{"x": "y"}]
        self.assertEqual(
            self._service._extend_topic_policy(
                topic_attributes, new_statements, update_statements=[]
            ),
            '{"Statement": [{"Sid": "foo"}, {"x": "y"}]}',
        )

    def test_extend_topic_policy_with_updates(self):
        topic_attributes = Box({"Attributes": {"Policy": '{"Statement": [{"Sid": "foo"}]}'}})
        new_statements = [{"x": "y"}]
        update_statements = {"foo": {"Sid": "foo", "bar": "baz"}}
        self.assertEqual(
            self._service._extend_topic_policy(
                topic_attributes, new_statements, update_statements=update_statements
            ),
            '{"Statement": [{"Sid": "foo", "bar": "baz"}, {"x": "y"}]}',
        )

    def test_extend_topic_policy_topic_attributes_without_sid(self):
        topic_attributes = Box({"Attributes": {"Policy": '{"Statement": [{"foo": "bar"}]}'}})
        new_statements = [{"x": "y"}]
        update_statements = {"foo": {"Sid": "foo", "bar": "baz"}}
        self.assertEqual(
            '{"Statement": [{"foo": "bar"}, {"x": "y"}]}',
            self._service._extend_topic_policy(topic_attributes, new_statements, update_statements),
        )

    @patch("montecarlodata.common.resources.prompt_connection")
    @patch.object(CloudResourceService, "_save_event_properties")
    def test_update_event_q(self, mock_save_event_properties, mock_prompt):
        name = "loki-MetadataEventQueue-42"
        _SAMPLE_DC_CLIENT.get_q_attributes.return_value = None

        events = copy.deepcopy(_SAMPLE_EVENT_DETAILS)
        for resource in events.resource_properties:
            resource.topic_arn = f"arn:aws:sns:{resource.region}:12345:monte-carlo-data-{resource.region}-metadata-events-topic"

        self._service._update_event_q(event_details=events, skip_prompts=True)

        events.collection_client.set_q_attributes.assert_called_once_with(
            name=name,
            attributes={
                "Policy": '{"Version": "2008-10-17", "Statement": [{"Sid": "__owner", "Effect": "Allow", "Principal": '
                '{"AWS": "arn:aws:iam::123456789:root"}, "Action": "SQS:*", "Resource": '
                '"arn:aws:sqs:us-east-1:123456789:loki-MetadataEventQueue-42"}, '
                '{"Sid": "__sender", "Effect": "Allow", "Principal": {"AWS": "*"}, "Action": '
                '"SQS:SendMessage", "Resource": "arn:aws:sqs:us-east-1:123456789:loki-MetadataEventQueue-42",'
                ' "Condition": {"ArnLike": {"aws:SourceArn": '
                '["arn:aws:sns:us-east-1:12345:monte-carlo-data-us-east-1-metadata-events-topic",'
                ' "arn:aws:sns:us-east-2:12345:monte-carlo-data-us-east-2-metadata-events-topic"]}}}]}'
            },
        )
        events.collection_client.get_q_attributes.assert_called_once_with(
            name=name, attributes=["Policy"]
        )
        mock_prompt.assert_called_once_with(message="Please confirm", skip_prompt=True)
        mock_save_event_properties.assert_called()

    @patch("montecarlodata.common.resources.prompt_connection")
    @patch.object(CloudResourceService, "_extend_q_policy")
    @patch.object(CloudResourceService, "_save_event_properties")
    def test_update_event_q_with_existing(
        self, mock_save_event_properties, mock_extend, mock_prompt
    ):
        name, mock_extend.return_value = "loki-MetadataEventQueue-42", {"foo": "bar"}

        _SAMPLE_DC_CLIENT.get_q_attributes.return_value = Box({"Attributes": {"Policy": "{}"}})
        self._service._update_event_q(event_details=_SAMPLE_EVENT_DETAILS, skip_prompts=True)

        _SAMPLE_DC_CLIENT.get_q_attributes.assert_called_once_with(name=name, attributes=["Policy"])
        _SAMPLE_DC_CLIENT.set_q_attributes.assert_called_once_with(
            name=name, attributes={"Policy": '{"foo": "bar"}'}
        )
        mock_prompt.assert_called_once_with(message="Please confirm", skip_prompt=True)
        mock_save_event_properties.assert_called()

    @patch("montecarlodata.common.resources.prompt_connection")
    @patch.object(CloudResourceService, "_extend_q_policy")
    def test_update_event_q_with_no_delta(self, mock_extend, mock_prompt):
        name, mock_extend.return_value = "loki-MetadataEventQueue-42", {"foo": "bar"}

        _SAMPLE_DC_CLIENT.get_q_attributes.return_value = Box(
            {"Attributes": {"Policy": '{"foo": "bar"}'}}
        )
        self._service._update_event_q(event_details=_SAMPLE_EVENT_DETAILS, skip_prompts=True)

        _SAMPLE_DC_CLIENT.get_q_attributes.assert_called_once_with(name=name, attributes=["Policy"])
        _SAMPLE_DC_CLIENT.set_q_attributes.assert_not_called()
        mock_prompt.assert_not_called()

    def test_extend_q_policy(self):
        events = copy.deepcopy(_SAMPLE_EVENT_DETAILS)
        for resource in events.resource_properties:
            resource.topic_arn = "bar"

        # Existing is string
        existing_policy = Box(
            {
                "Statement": [
                    {
                        "Sid": "__sender",
                        "Condition": {"ArnLike": {"aws:SourceArn": "foo"}},
                    }
                ]
            }
        )
        self.assertEqual(
            self._service._extend_q_policy(
                existing_policy=existing_policy,
                event_details=events,
                topic_arns=["bar"],
            ),
            {
                "Statement": [
                    {
                        "Sid": "__sender",
                        "Condition": {"ArnLike": {"aws:SourceArn": ["foo", "bar"]}},
                    }
                ]
            },
        )

        # Existing is list
        existing_policy = Box(
            {
                "Statement": [
                    {
                        "Sid": "__sender",
                        "Condition": {"ArnLike": {"aws:SourceArn": ["foo", "qux"]}},
                    }
                ]
            }
        )
        self.assertEqual(
            self._service._extend_q_policy(
                existing_policy=existing_policy,
                event_details=events,
                topic_arns=["bar"],
            ),
            {
                "Statement": [
                    {
                        "Sid": "__sender",
                        "Condition": {"ArnLike": {"aws:SourceArn": ["foo", "qux", "bar"]}},
                    }
                ]
            },
        )

        # Existing has duplicate
        existing_policy = Box(
            {
                "Statement": [
                    {
                        "Sid": "__sender",
                        "Condition": {"ArnLike": {"aws:SourceArn": "bar"}},
                    }
                ]
            }
        )
        self.assertEqual(
            self._service._extend_q_policy(
                existing_policy=existing_policy,
                event_details=events,
                topic_arns=["bar"],
            ),
            {
                "Statement": [
                    {
                        "Sid": "__sender",
                        "Condition": {"ArnLike": {"aws:SourceArn": "bar"}},
                    }
                ]
            },
        )
        existing_policy = Box(
            {
                "Statement": [
                    {
                        "Sid": "__sender",
                        "Condition": {"ArnLike": {"aws:SourceArn": ["foo", "bar"]}},
                    }
                ]
            }
        )
        self.assertEqual(
            self._service._extend_q_policy(
                existing_policy=existing_policy,
                event_details=events,
                topic_arns=["foo", "bar"],
            ),
            {
                "Statement": [
                    {
                        "Sid": "__sender",
                        "Condition": {"ArnLike": {"aws:SourceArn": ["foo", "bar"]}},
                    }
                ]
            },
        )

        # Incompatible format
        with self.assertRaises(click.exceptions.Abort):
            self._service._extend_q_policy(
                existing_policy=Box({"Statement": [{"Sid": "unk"}]}),
                event_details=events,
                topic_arns=["bar"],
            )

    @patch("montecarlodata.common.resources.prompt_connection")
    @patch.object(CloudResourceService, "_merge_event_notifications")
    @patch.object(CloudResourceService, "_save_event_properties")
    def test_create_event_notification(
        self, mock_save_event_properties, mock_merge_events, mock_prompt
    ):
        events = copy.deepcopy(_SAMPLE_EVENT_DETAILS)
        new_config, existing_config = {"foo": "bar"}, {"bar": "foo"}

        for resource in events.resource_properties:
            resource.topic_arn = (
                "arn:aws:sns:us-east-1:12345:monte-carlo-data-us-east-1-metadata-events-topic"
            )
            resource.prefix = "lake"
            resource.client.get_bucket_event_config.return_value = existing_config

        mock_merge_events.return_value = new_config
        self._service._create_event_notification(event_details=events, skip_prompts=True)

        expected_merge_events_calls = [
            call(
                setting_id="monte-carlo-data-us-east-1-metadata-events-topic-lake-notification",
                existing_config=existing_config,
                resource_details=resource,
            )
            for resource in events.resource_properties
        ]
        self.assertEqual(mock_merge_events.call_args_list, expected_merge_events_calls)

        for resource in events.resource_properties:
            resource.client.get_bucket_event_config.assert_called_once_with(
                name=resource.bucket_name
            )
            resource.client.set_bucket_event_config.assert_called_once_with(
                name=resource.bucket_name, notification_config=new_config
            )

        expected_prompt_calls = [
            call(message="Please confirm", skip_prompt=True) for _ in events.resource_properties
        ]
        self.assertEqual(mock_prompt.call_args_list, expected_prompt_calls)

        mock_save_event_properties.assert_called()

    @patch("montecarlodata.common.resources.prompt_connection")
    @patch.object(CloudResourceService, "_merge_event_notifications")
    @patch.object(CloudResourceService, "_save_event_properties")
    def test_create_event_notification_with_no_delta(
        self, mock_save_event_properties, mock_merge_events, mock_prompt
    ):
        events = copy.deepcopy(_SAMPLE_EVENT_DETAILS)
        new_config, existing_config = {"foo": "bar"}, {"foo": "bar"}

        for resource in events.resource_properties:
            resource.topic_arn = (
                "arn:aws:sns:us-east-1:12345:monte-carlo-data-us-east-1-metadata-events-topic"
            )
            resource.client.get_bucket_event_config.return_value = existing_config

        mock_merge_events.return_value = new_config
        self._service._create_event_notification(event_details=events, skip_prompts=True)
        expected_merge_events_calls = [
            call(
                setting_id="monte-carlo-data-us-east-1-metadata-events-topic-notification",
                existing_config=existing_config,
                resource_details=resource,
            )
            for resource in events.resource_properties
        ]
        self.assertEqual(mock_merge_events.call_args_list, expected_merge_events_calls)

        for resource in events.resource_properties:
            resource.client.get_bucket_event_config.assert_called_once_with(
                name=resource.bucket_name
            )
            resource.client.set_bucket_event_config.assert_not_called()

        mock_prompt.assert_not_called()
        mock_save_event_properties.assert_called()

    def test_merge_event_notifications(self):
        setting_id = "foo"
        events = copy.deepcopy(_SAMPLE_EVENT_DETAILS)

        for resource in events.resource_properties:
            resource.topic_arn = f"arn:aws:sns:{resource.region}:12345:monte-carlo-data-{resource.region}-metadata-events-topic"
            expected_config = {
                "Id": setting_id,
                "TopicArn": resource.topic_arn,
                "Events": ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"],
                "Filter": {
                    "Key": {
                        "FilterRules": [
                            {"Name": "Prefix", "Value": ""},
                            {"Name": "Suffix", "Value": ""},
                        ]
                    }
                },
            }
            # ID already exists
            existing_setting = {"TopicConfigurations": [{"Id": setting_id}]}
            self.assertEqual(
                self._service._merge_event_notifications(setting_id, existing_setting, resource),
                existing_setting,
            )

            # Topic already exits
            existing_setting = {
                "TopicConfigurations": [{"Id": "bar"}],
                "QueueConfigurations": [{"foo": "bar"}],
            }
            self.assertEqual(
                self._service._merge_event_notifications(setting_id, existing_setting, resource),
                {
                    "TopicConfigurations": [{"Id": "bar"}, expected_config],
                    "QueueConfigurations": [{"foo": "bar"}],
                },
            )

            # No topic config
            self.assertEqual(
                self._service._merge_event_notifications(setting_id, {}, resource),
                {"TopicConfigurations": [expected_config]},
            )

            existing_setting = {"QueueConfigurations": [{"foo": "bar"}]}
            self.assertEqual(
                self._service._merge_event_notifications(setting_id, existing_setting, resource),
                {
                    "TopicConfigurations": [expected_config],
                    "QueueConfigurations": [{"foo": "bar"}],
                },
            )

    @patch("montecarlodata.common.resources.prompt_connection")
    @patch.object(CloudResourceService, "_save_event_properties")
    def test_create_topic_subscription(self, mock_save_event_properties, mock_prompt):
        events = copy.deepcopy(_SAMPLE_EVENT_DETAILS)
        for resource in events.resource_properties:
            resource.client.list_topic_subscriptions.return_value = None
        self._service._create_topic_subscription(event_details=events, skip_prompts=True)

        for resource in events.resource_properties:
            resource.client.list_topic_subscriptions.assert_called_once_with(arn=resource.topic_arn)
            resource.client.subscribe_to_topic.assert_called_once_with(
                arn=resource.topic_arn,
                endpoint=events.event_queue_arn,
                attributes={"RawMessageDelivery": "true"},
            )

        mock_prompt.assert_has_calls(
            [
                call(message="Please confirm", skip_prompt=True),
                call(message="Please confirm", skip_prompt=True),
            ]
        )
        mock_save_event_properties.assert_called()

    @patch("montecarlodata.common.resources.prompt_connection")
    @patch.object(CloudResourceService, "_save_event_properties")
    def test_create_topic_subscription_with_preexisting_endpoint(
        self, mock_save_event_properties, mock_prompt
    ):
        events = copy.deepcopy(_SAMPLE_EVENT_DETAILS)
        for resource in events.resource_properties:
            resource.client.list_topic_subscriptions.return_value = [
                [
                    {
                        "SubscriptionArn": "odin",
                        "Owner": "12345",
                        "Protocol": "sqs",
                        "Endpoint": events.event_queue_arn,
                        "TopicArn": resource.topic_arn,
                    }
                ]
            ]

        self._service._create_topic_subscription(event_details=events, skip_prompts=True)

        for resource in events.resource_properties:
            resource.client.list_topic_subscriptions.assert_called_once_with(arn=resource.topic_arn)
            _SAMPLE_CUST_RESOURCES_CLIENT.subscribe_to_topic.cassert_not_called()

        mock_prompt.assert_not_called()
        mock_save_event_properties.assert_called()

    @patch("montecarlodata.common.resources.AwsClientWrapper")
    def test_get_dc_resource_props(self, aws_wrapper_mock):
        arn = "arn:aws:cloudformation:us-east-1:1234:stack/foo/bar"
        collector_props = Box({"stackArn": arn})

        self.maxDiff = None
        self.assertEqual(
            self._service.get_dc_resource_props(collector_props=collector_props),
            DcResourceProperties(
                collector_arn=AWSArn(arn),
                collector_props=collector_props,
                collection_region="us-east-1",
                resources_region="us-east-1",
                collection_client=aws_wrapper_mock(),
                resources_client=aws_wrapper_mock(),
            ),
        )
        aws_wrapper_mock.assert_has_calls(
            [
                call(
                    profile_name=None,
                    region_name="us-east-1",
                ),
                call(
                    profile_name=None,
                    region_name="us-east-1",
                ),
            ]
        )

    def test_parse_stack_prop_list(self):
        self.assertEqual(
            self._service._parse_stack_prop_list(
                key="foo", val="bar", struct=[{"foo": "baz", "bar": "qux"}]
            ),
            Box({"baz": "qux"}),
        )
