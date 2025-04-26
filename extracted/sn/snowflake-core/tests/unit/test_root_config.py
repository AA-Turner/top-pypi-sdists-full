import pytest

from snowflake.core._internal.root_configuration import RootConfiguration


def test_root_config():
    test_root_config = RootConfiguration()
    assert test_root_config.get_user_agents() == ""
    assert not test_root_config.has_user_agents()

    with pytest.raises(ValueError):
        test_root_config.append_user_agent("python_api")
    with pytest.raises(ValueError):
        test_root_config.append_user_agent("py%", "1.2")
    with pytest.raises(ValueError):
        test_root_config.append_user_agent("py", "/1.")

    test_root_config.append_user_agent("Snowflake", "1.2.3")
    assert test_root_config.get_user_agents() == "Snowflake/1.2.3"
    assert test_root_config.has_user_agents()

    test_root_config.append_user_agent("custom_ui")
    assert test_root_config.get_user_agents() == "Snowflake/1.2.3 custom_ui"
    assert test_root_config.has_user_agents()

    test_root_config = RootConfiguration()
    test_root_config.append_user_agent("custom_ui")
    assert test_root_config.get_user_agents() == "custom_ui"
    assert test_root_config.has_user_agents()
