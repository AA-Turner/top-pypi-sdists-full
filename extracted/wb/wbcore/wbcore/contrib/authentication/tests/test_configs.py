from wbcore.configs.registry import ConfigRegistry


def test_authentication_config(config_registry: ConfigRegistry, api_request):
    authentication = config_registry.get_config_dict(api_request)["authentication"]
    assert authentication
