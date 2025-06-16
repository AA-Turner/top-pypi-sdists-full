import pytest

import kafka3.admin
from kafka3.errors import IllegalArgumentError


def test_config_resource():
    with pytest.raises(KeyError):
        bad_resource = kafka3.admin.ConfigResource('something', 'foo')
    good_resource = kafka3.admin.ConfigResource('broker', 'bar')
    assert good_resource.resource_type == kafka3.admin.ConfigResourceType.BROKER
    assert good_resource.name == 'bar'
    assert good_resource.configs is None
    good_resource = kafka3.admin.ConfigResource(kafka3.admin.ConfigResourceType.TOPIC, 'baz', {'frob': 'nob'})
    assert good_resource.resource_type == kafka3.admin.ConfigResourceType.TOPIC
    assert good_resource.name == 'baz'
    assert good_resource.configs == {'frob': 'nob'}


def test_new_partitions():
    good_partitions = kafka3.admin.NewPartitions(6)
    assert good_partitions.total_count == 6
    assert good_partitions.new_assignments is None
    good_partitions = kafka3.admin.NewPartitions(7, [[1, 2, 3]])
    assert good_partitions.total_count == 7
    assert good_partitions.new_assignments == [[1, 2, 3]]


def test_acl_resource():
    good_acl = kafka3.admin.ACL(
        "User:bar",
        "*",
        kafka3.admin.ACLOperation.ALL,
        kafka3.admin.ACLPermissionType.ALLOW,
        kafka3.admin.ResourcePattern(
            kafka3.admin.ResourceType.TOPIC,
            "foo",
            kafka3.admin.ACLResourcePatternType.LITERAL
        )
    )

    assert(good_acl.resource_pattern.resource_type == kafka3.admin.ResourceType.TOPIC)
    assert(good_acl.operation == kafka3.admin.ACLOperation.ALL)
    assert(good_acl.permission_type == kafka3.admin.ACLPermissionType.ALLOW)
    assert(good_acl.resource_pattern.pattern_type == kafka3.admin.ACLResourcePatternType.LITERAL)

    with pytest.raises(IllegalArgumentError):
        kafka3.admin.ACL(
            "User:bar",
            "*",
            kafka3.admin.ACLOperation.ANY,
            kafka3.admin.ACLPermissionType.ANY,
            kafka3.admin.ResourcePattern(
                kafka3.admin.ResourceType.TOPIC,
                "foo",
                kafka3.admin.ACLResourcePatternType.LITERAL
            )
        )

def test_new_topic():
    with pytest.raises(IllegalArgumentError):
        bad_topic = kafka3.admin.NewTopic('foo', -1, -1)
    with pytest.raises(IllegalArgumentError):
        bad_topic = kafka3.admin.NewTopic('foo', 1, -1)
    with pytest.raises(IllegalArgumentError):
        bad_topic = kafka3.admin.NewTopic('foo', 1, 1, {1: [1, 1, 1]})
    good_topic = kafka3.admin.NewTopic('foo', 1, 2)
    assert good_topic.name == 'foo'
    assert good_topic.num_partitions == 1
    assert good_topic.replication_factor == 2
    assert good_topic.replica_assignments == {}
    assert good_topic.topic_configs == {}
    good_topic = kafka3.admin.NewTopic('bar', -1, -1, {1: [1, 2, 3]}, {'key': 'value'})
    assert good_topic.name == 'bar'
    assert good_topic.num_partitions == -1
    assert good_topic.replication_factor == -1
    assert good_topic.replica_assignments == {1: [1, 2, 3]}
    assert good_topic.topic_configs == {'key': 'value'}
