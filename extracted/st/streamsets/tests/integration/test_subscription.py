#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025

# fmt: off
import pytest

from streamsets.sdk.utils import get_random_string

# fmt: on


def test_add_subscription(sch):
    subscription_builder = sch.get_subscription_builder()
    subscription_builder.add_event(event_type='Pipeline Committed')
    subscription_builder.set_email_action(
        recipients=['cake@cake.com'], subject='{{PIPELINE_NAME}} pipeline was commited', body=('{{PIPELINE_COMMITER}}')
    )
    subscription_name = 'Test_Subscription_{}'.format(get_random_string())

    try:
        subscription = subscription_builder.build(name=subscription_name)
        sch.add_subscription(subscription)
        assert sch.subscriptions[-1].name == subscription_name
    except Exception:
        raise ValueError("Couldn't add subscription")
    finally:
        sch.delete_subscription(sch.subscriptions.get(name=subscription_name))


def test_missing_action(sch):
    subscription_builder = sch.get_subscription_builder()
    subscription_builder.add_event(event_type='Pipeline Committed')
    subscription = subscription_builder.build(name='Test_Subscription_Missing_Action')

    with pytest.raises(ValueError, match="Missing action for subscription."):
        sch.add_subscription(subscription)


def test_wrong_action_type(sch):
    subscription_builder = sch.get_subscription_builder()
    subscription_builder.add_event(event_type='Pipeline Committed')
    subscription_builder.set_email_action(
        recipients=['cake@cake.com'], subject='{{PIPELINE_NAME}} pipeline was commited', body=('{{PIPELINE_COMMITER}}')
    )
    subscription = subscription_builder.build(name='Test_Subscription_Wrong_Action_Type')
    subscription.action.event_type = 'EMAIL2'

    with pytest.raises(ValueError, match="Unknown action for subscription."):
        sch.add_subscription(subscription)
