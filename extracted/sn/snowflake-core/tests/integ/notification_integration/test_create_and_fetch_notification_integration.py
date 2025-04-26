import pytest

from snowflake.core._common import CreateMode
from snowflake.core.exceptions import ConflictError, NotFoundError
from snowflake.core.notification_integration import (
    NotificationEmail,
    NotificationIntegration,
    NotificationQueueAwsSnsOutbound,
    NotificationQueueAzureEventGridInbound,
    NotificationQueueAzureEventGridOutbound,
    NotificationQueueGcpPubsubInbound,
    NotificationQueueGcpPubsubOutbound,
    NotificationWebhook,
    WebhookSecret,
)

from ..utils import random_string


# Note: all secret looking things in this file are made up

pytestmark = [
    # All tests in this file need this Snowflake version
    pytest.mark.min_sf_ver("8.36.0"),
    pytest.mark.internal_only,
]

@pytest.mark.use_accountadmin
def test_ni_creation_and_drop_notificationemail(notification_integrations, set_internal_params):
    allowed_recipients = ["test1@snowflake.com", "test2@snowflake.com"]
    default_recipients = ["test1@snowflake.com"]
    default_subject = "test default subject"
    new_integration = NotificationIntegration(
        name=random_string(3, "test_ni_creation_and_drop_"),
        notification_hook=NotificationEmail(
            allowed_recipients=allowed_recipients,
            default_recipients=default_recipients,
            default_subject=default_subject,
        ),
        enabled=True,
    )
    with set_internal_params({"ENABLE_LIMIT_RECIPIENTS_TO_SENDING_ACCOUNT": False}):
        pre_create_count = len(list(notification_integrations.iter()))
        ni = notification_integrations.create(new_integration)
        with pytest.raises(ConflictError):
            ni = notification_integrations.create(new_integration, mode=CreateMode.error_if_exists)
        fetched_ni = ni.fetch()
        assert fetched_ni.name == new_integration.name.upper()
        assert fetched_ni.enabled == new_integration.enabled
        assert fetched_ni.comment is None
        assert isinstance(fetched_ni.notification_hook, NotificationEmail)
        assert fetched_ni.notification_hook.allowed_recipients == allowed_recipients
        assert fetched_ni.notification_hook.default_recipients == default_recipients
        assert fetched_ni.notification_hook.default_subject == default_subject
        created_count = len(list(notification_integrations.iter()))
        ni.drop(if_exists=False)
        with pytest.raises(NotFoundError):
            ni.fetch()
        ni.drop(if_exists=True)
        with pytest.raises(NotFoundError):
            ni.drop(if_exists=False)
        after_drop_count = len(list(notification_integrations.iter()))
        assert pre_create_count + 1 == created_count == after_drop_count + 1


@pytest.mark.use_accountadmin
def test_ni_creation_and_drop_webhook(notification_integrations, cursor):
    webhook_url="https://events.pagerduty.com/v2/enqueue"
    webhook_template='{"key": "SNOWFLAKE_WEBHOOK_SECRET", "msg": "SNOWFLAKE_WEBHOOK_MESSAGE"}'
    webhook_headers={"content-type": "application/json", "user-content": "chrome"}
    database = cursor.execute("select current_database();").fetchone()[0]
    schema = cursor.execute("select current_schema();").fetchone()[0]
    cursor.execute("CREATE OR REPLACE SECRET mySecret TYPE=GENERIC_STRING SECRET_STRING='aaa'")
    try:
        new_integration = NotificationIntegration(
            name=random_string(3, "test_ni_creation_and_drop_webhook_"),
            enabled=False,
            notification_hook=NotificationWebhook(
                webhook_url=webhook_url,
                webhook_secret=WebhookSecret(
                    name="mySecret".upper(), database_name=database, schema_name=schema
                ),
                webhook_body_template=webhook_template,
                webhook_headers=webhook_headers,
            ),
        )
        pre_create_count = len(list(notification_integrations.iter()))
        ni = notification_integrations.create(new_integration)
        ni = notification_integrations.create(new_integration, mode=CreateMode.or_replace)
        fetched_ni = ni.fetch()
        assert fetched_ni.name == new_integration.name.upper()
        assert fetched_ni.enabled == new_integration.enabled
        assert fetched_ni.comment is None
        assert isinstance(fetched_ni.notification_hook, NotificationWebhook)
        assert fetched_ni.notification_hook.webhook_url == webhook_url
        assert fetched_ni.notification_hook.webhook_body_template == webhook_template
        assert fetched_ni.notification_hook.webhook_headers == webhook_headers
        assert fetched_ni.notification_hook.webhook_secret.name == "MYSECRET"
        assert fetched_ni.notification_hook.webhook_secret.database_name == database
        assert fetched_ni.notification_hook.webhook_secret.schema_name == schema
        created_count = len(list(notification_integrations.iter()))
        ni.drop(if_exists=False)
        with pytest.raises(NotFoundError):
            ni.fetch()
        ni.drop(if_exists=True)
        with pytest.raises(NotFoundError):
            ni.drop(if_exists=False)
        after_drop_count = len(list(notification_integrations.iter()))
        assert pre_create_count + 1 == created_count == after_drop_count + 1
        # We should be able to create the integration again now
        ni = notification_integrations.create(new_integration)
        ni.drop()
    finally:
        cursor.execute("DROP SECRET mySecret;")

def test_ni_creation_and_drop_awsoutbound(notification_integrations, setup_credentials_fixture):
    del setup_credentials_fixture
    aws_sns_topic_arn="arn:aws:sns:us-west-1:234567812345:sns-test-topic"
    aws_sns_role_arn="arn:aws:iam::234567812345:role/sns-test-topic"
    new_integration = NotificationIntegration(
        name=random_string(3, "test_ni_creation_and_drop_awsoutbound_"),
        enabled=False,
        notification_hook=NotificationQueueAwsSnsOutbound(
            aws_sns_topic_arn=aws_sns_topic_arn,
            aws_sns_role_arn=aws_sns_role_arn,
        )
    )
    pre_create_count = len(list(notification_integrations.iter()))
    ni = notification_integrations.create(new_integration)
    fetched_ni = ni.fetch()
    assert fetched_ni.name == new_integration.name.upper()
    assert fetched_ni.enabled == new_integration.enabled
    assert fetched_ni.comment is None
    assert isinstance(fetched_ni.notification_hook, NotificationQueueAwsSnsOutbound)
    assert fetched_ni.notification_hook.sf_aws_iam_user_arn is not None
    assert fetched_ni.notification_hook.sf_aws_external_id is not None
    assert fetched_ni.notification_hook.aws_sns_topic_arn == aws_sns_topic_arn
    assert fetched_ni.notification_hook.aws_sns_role_arn == aws_sns_role_arn
    created_count = len(list(notification_integrations.iter()))
    ni.drop(if_exists=False)
    with pytest.raises(NotFoundError):
        ni.fetch()
    ni.drop(if_exists=True)
    with pytest.raises(NotFoundError):
        ni.drop(if_exists=False)
    after_drop_count = len(list(notification_integrations.iter()))
    assert pre_create_count + 1 == created_count == after_drop_count + 1


def test_ni_creation_and_drop_azureoutbound(notification_integrations, setup_credentials_fixture):
    del setup_credentials_fixture
    azure_event_grid_topic_endpoint="https://test-snowapi-eventgrid-toopic.westus-1.eventgrid.azure.net/api/events"
    azure_tenant_id="fake.azsnowdevoutlook.onmicrosoft.com"
    new_integration = NotificationIntegration(
        name=random_string(3, "test_ni_creation_and_drop_azureoutbound_"),
        enabled=False,
        notification_hook=NotificationQueueAzureEventGridOutbound(
            azure_event_grid_topic_endpoint=azure_event_grid_topic_endpoint,
            azure_tenant_id=azure_tenant_id,
        )
    )
    pre_create_count = len(list(notification_integrations.iter()))
    ni = notification_integrations.create(new_integration)
    fetched_ni = ni.fetch()
    assert fetched_ni.name == new_integration.name.upper()
    assert fetched_ni.enabled == new_integration.enabled
    assert fetched_ni.comment is None
    assert isinstance(fetched_ni.notification_hook, NotificationQueueAzureEventGridOutbound)
    assert fetched_ni.notification_hook.azure_consent_url is not None
    assert fetched_ni.notification_hook.azure_multi_tenant_app_name is not None
    assert fetched_ni.notification_hook.azure_event_grid_topic_endpoint == azure_event_grid_topic_endpoint
    assert fetched_ni.notification_hook.azure_tenant_id == azure_tenant_id
    created_count = len(list(notification_integrations.iter()))
    ni.drop(if_exists=False)
    with pytest.raises(NotFoundError):
        ni.fetch()
    ni.drop(if_exists=True)
    with pytest.raises(NotFoundError):
        ni.drop(if_exists=False)
    after_drop_count = len(list(notification_integrations.iter()))
    assert pre_create_count + 1 == created_count == after_drop_count + 1


def test_ni_creation_and_drop_azureinbound(notification_integrations, setup_credentials_fixture):
    del setup_credentials_fixture
    azure_storage_queue_primary_uri="https://fake.queue.core.windows.net/snowapi_queue"
    azure_tenant_id="fake.onmicrosoft.com"
    new_integration = NotificationIntegration(
        name=random_string(3, "test_ni_creation_and_drop_azureoutbound_"),
        enabled=False,
        notification_hook=NotificationQueueAzureEventGridInbound(
            azure_storage_queue_primary_uri=azure_storage_queue_primary_uri,
            azure_tenant_id=azure_tenant_id,
        ),
    )
    pre_create_count = len(list(notification_integrations.iter()))
    ni = notification_integrations.create(new_integration)
    fetched_ni = ni.fetch()
    assert fetched_ni.name == new_integration.name.upper()
    assert fetched_ni.enabled == new_integration.enabled
    assert fetched_ni.comment is None
    assert isinstance(fetched_ni.notification_hook, NotificationQueueAzureEventGridInbound)
    assert fetched_ni.notification_hook.azure_consent_url is not None
    assert fetched_ni.notification_hook.azure_multi_tenant_app_name is not None
    assert fetched_ni.notification_hook.azure_storage_queue_primary_uri == azure_storage_queue_primary_uri
    assert fetched_ni.notification_hook.azure_tenant_id == azure_tenant_id
    created_count = len(list(notification_integrations.iter()))
    ni.drop(if_exists=False)
    with pytest.raises(NotFoundError):
        ni.fetch()
    ni.drop(if_exists=True)
    with pytest.raises(NotFoundError):
        ni.drop(if_exists=False)
    after_drop_count = len(list(notification_integrations.iter()))
    assert pre_create_count + 1 == created_count == after_drop_count + 1


def test_ni_creation_and_drop_gcpoutbound(notification_integrations, setup_credentials_fixture):
    del setup_credentials_fixture
    gcp_pubsub_topic_name="projects/fake-project-name/topics/pythonapi-test"
    new_integration = NotificationIntegration(
        name=random_string(3, "test_ni_creation_and_drop_gcpoutbound_"),
        enabled=False,
        notification_hook=NotificationQueueGcpPubsubOutbound(
            gcp_pubsub_topic_name=gcp_pubsub_topic_name,
        )
    )
    pre_create_count = len(list(notification_integrations.iter()))
    ni = notification_integrations.create(new_integration)
    fetched_ni = ni.fetch()
    assert fetched_ni.name == new_integration.name.upper()
    assert fetched_ni.enabled == new_integration.enabled
    assert fetched_ni.comment is None
    assert isinstance(fetched_ni.notification_hook, NotificationQueueGcpPubsubOutbound)
    assert fetched_ni.notification_hook.gcp_pubsub_service_account is not None
    assert fetched_ni.notification_hook.gcp_pubsub_topic_name == gcp_pubsub_topic_name
    created_count = len(list(notification_integrations.iter()))
    ni.drop(if_exists=False)
    with pytest.raises(NotFoundError):
        ni.fetch()
    ni.drop(if_exists=True)
    with pytest.raises(NotFoundError):
        ni.drop(if_exists=False)
    after_drop_count = len(list(notification_integrations.iter()))
    assert pre_create_count + 1 == created_count == after_drop_count + 1


def test_ni_creation_and_drop_gcpinbound(notification_integrations, setup_credentials_fixture):
    del setup_credentials_fixture
    gcp_pubsub_subscription_name="projects/snowapi-snowfort-project/subscriptions/sub2"
    new_integration = NotificationIntegration(
        name=random_string(3, "test_ni_creation_and_drop_gcpoutbound_"),
        enabled=False,
        notification_hook=NotificationQueueGcpPubsubInbound(
            gcp_pubsub_subscription_name=gcp_pubsub_subscription_name,
        )
    )
    pre_create_count = len(list(notification_integrations.iter()))
    ni = notification_integrations.create(new_integration)
    fetched_ni = ni.fetch()
    assert fetched_ni.name == new_integration.name.upper()
    assert fetched_ni.enabled == new_integration.enabled
    assert fetched_ni.comment is None
    assert isinstance(fetched_ni.notification_hook, NotificationQueueGcpPubsubInbound)
    assert fetched_ni.notification_hook.gcp_pubsub_service_account is not None
    assert fetched_ni.notification_hook.gcp_pubsub_subscription_name == gcp_pubsub_subscription_name
    created_count = len(list(notification_integrations.iter()))
    ni.drop(if_exists=False)
    with pytest.raises(NotFoundError):
        ni.fetch()
    ni.drop(if_exists=True)
    with pytest.raises(NotFoundError):
        ni.drop(if_exists=False)
    after_drop_count = len(list(notification_integrations.iter()))
    assert pre_create_count + 1 == created_count == after_drop_count + 1
