from rock.actions import Env
from rock.sdk.envs.rock_env import RockEnv


def make(env_id: str, **kwargs) -> Env:
    """
    Create a Rock environment instance.

    Args:
        env_id: Environment ID.
        **kwargs: Environment parameters, including session_name, etc.

    Returns:
        Environment instance.

    Raises:
        ValueError: When the environment ID is not supported.
    """

    return RockEnv(env_id=env_id, **kwargs)
