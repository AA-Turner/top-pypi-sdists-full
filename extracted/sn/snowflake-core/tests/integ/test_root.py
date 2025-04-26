import pytest

from snowflake.core._internal.root_configuration import RootConfiguration
from snowflake.core._root import Root


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_extracting_tokens(root):
    # Be careful with failures here not to print tokens.
    #  To avoid printing local variables use pytest.fail
    if root._session_token is None:
        pytest.fail("session token should not be None")
    if root._master_token is None:
        pytest.fail("master token should not be None")

@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_init_root_with_user_agents(connection):
    root_config = RootConfiguration()
    root_config.append_user_agent("Snowflake", "1.2.3")
    assert "Snowflake/1.2.3" in Root(connection, root_config).root_config.get_user_agents()

    with pytest.raises(ValueError):
        root_config.append_user_agent("python_api")
    with pytest.raises(ValueError):
        root_config.append_user_agent("python_api", "1.2")

    root_config.append_user_agent("custom_ui")

    new_root = Root(connection, root_config)
    assert "Snowflake/1.2.3" in new_root.root_config.get_user_agents()
    assert "custom_ui" in new_root.root_config.get_user_agents()

