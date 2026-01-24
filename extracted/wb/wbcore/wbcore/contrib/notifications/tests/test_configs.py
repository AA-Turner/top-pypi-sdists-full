from wbcore.configs.registry import ConfigRegistry


def test_notifications_config(config_registry: ConfigRegistry, api_request):
    notifications = config_registry.get_config_dict(api_request)["notifications"]
    assert notifications["endpoint"]
    assert notifications["token"]
