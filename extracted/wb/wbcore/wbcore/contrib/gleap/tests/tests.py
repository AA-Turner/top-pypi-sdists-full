from wbcore.configs.registry import ConfigRegistry
from wbcore.contrib.gleap.hashes import get_hash_from_user


def test_different_user_id():
    hash1 = get_hash_from_user(1, "abc")
    hash2 = get_hash_from_user(2, "abc")

    assert hash1 != hash2


def test_same_user_id():
    hash1 = get_hash_from_user(1, "abc")
    hash2 = get_hash_from_user(1, "abc")

    assert hash1 == hash2


def test_different_secret():
    hash1 = get_hash_from_user(1, "abc")
    hash2 = get_hash_from_user(1, "abc1")

    assert hash1 != hash2


def test_gleap_config(config_registry: ConfigRegistry, api_request):
    gleap = config_registry.get_config_dict(api_request)["gleap"]
    assert gleap["user_identity_endpoint"]
    assert gleap["api_token"]
