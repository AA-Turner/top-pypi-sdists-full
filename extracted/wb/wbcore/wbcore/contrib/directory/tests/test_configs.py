from wbcore.configs.registry import ConfigRegistry


def test_profile_config(config_registry: ConfigRegistry, api_request):
    profile = config_registry.get_config_dict(api_request)["profile"]
    assert profile
