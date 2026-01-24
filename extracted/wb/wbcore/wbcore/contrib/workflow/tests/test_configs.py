from wbcore.configs.registry import ConfigRegistry


def test_workflow_config(config_registry: ConfigRegistry, api_request):
    workflow = config_registry.get_config_dict(api_request)["workflow"]
    assert workflow["endpoint"]
