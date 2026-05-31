import gymnasium as gym
import numpy as np
from gymnasium.utils.env_checker import data_equivalence
import matplotlib.pyplot as plt

from tests.python.test_atari_vector_env import obs_equivalence

env_id = "ALE/Breakout-v5"
num_envs=2
reset_seed=123
action_seed=123
rollout_length=100

disable_vector_args = dict(
    noop_max=0,
    use_fire_reset=False,
    reward_clipping=False,
    repeat_action_probability=0.0,
)
disable_env_args = dict(frameskip=1, repeat_action_probability=0.0)
disable_preprocessing_args = dict(noop_max=0)

"""Test if both environments produce similar results over a short rollout."""
gym_envs = gym.vector.SyncVectorEnv(
    [
        lambda: gym.wrappers.FrameStackObservation(
            gym.wrappers.AtariPreprocessing(
                gym.make(
                    env_id,
                    **disable_env_args,
                ),
                terminal_on_life_loss=True,  # to ensure some terminations
                **disable_preprocessing_args,
            ),
            stack_size=4,
            padding_type="zero",
        )
        for _ in range(num_envs)
    ],
    autoreset_mode=gym.vector.AutoresetMode.SAME_STEP,
)
ale_envs = gym.make_vec(
    env_id,
    num_envs,
    episodic_life=True,
    autoreset_mode=gym.vector.AutoresetMode.SAME_STEP,
    **disable_vector_args,
)
assert (
        gym_envs.metadata["autoreset_mode"] == ale_envs.metadata["autoreset_mode"]
), f"{gym_envs.metadata=}, {ale_envs.metadata=}"

gym_obs, gym_info = gym_envs.reset(seed=reset_seed)
ale_obs, ale_info = ale_envs.reset(seed=reset_seed)

assert data_equivalence(gym_obs, ale_obs)

gym_info = {
    key: value.astype(np.int32)
    for key, value in gym_info.items()
    if not key.startswith("_") and key != "seeds"
}
env_ids = ale_info.pop("env_id")
assert np.all(env_ids == np.arange(gym_envs.num_envs))
assert data_equivalence(gym_info, ale_info)

ale_envs.action_space.seed(action_seed)
has_autoreset = False
for t in range(rollout_length):
    actions = ale_envs.action_space.sample()

    gym_obs, gym_rewards, gym_terminations, gym_truncations, gym_info = (
        gym_envs.step(actions)
    )
    ale_obs, ale_rewards, ale_terminations, ale_truncations, ale_info = (
        ale_envs.step(actions)
    )

    assert obs_equivalence(gym_obs, ale_obs, t, autoreset_mode="SAME-STEP"), t
    assert data_equivalence(gym_rewards.astype(np.int32), ale_rewards), t
    assert data_equivalence(gym_terminations, ale_terminations), t
    assert data_equivalence(gym_truncations, ale_truncations), t

    env_ids = ale_info.pop("env_id")
    assert np.all(env_ids == np.arange(gym_envs.num_envs)), t

    episode_over = np.logical_or(gym_terminations, gym_truncations)
    if np.any(episode_over):
        has_autoreset = True

        gym_final_obs = gym_info.pop("final_obs")
        gym_info.pop("final_info")  # ALEV doesn't return final info
        gym_info = {
            key: value.astype(np.int32)
            for key, value in gym_info.items()
            if not key.startswith("_")
        }

        ale_final_obs = ale_info.pop("final_obs")
        assert data_equivalence(
            gym_info, ale_info
        ), f"{gym_info=}, {ale_info=}, {t=}"

        for i, ep_over in enumerate(episode_over):
            if ep_over:
                assert obs_equivalence(gym_final_obs[i], ale_final_obs[i], t, autoreset_mode="SAME-STEP"), t

        # print(f'{t=}, {gym_final_obs.shape=}, {ale_final_obs.shape=}')
        # print(f'{np.all(gym_final_obs[0] == ale_final_obs[0])=}')
        # print(f'{np.all(gym_final_obs[1] == ale_final_obs[1])=}')
        # fig, axs = plt.subplots(ncols=3, nrows=4)
        # for i in range(4):
        #     axs[i, 0].imshow(gym_final_obs[0][i])
        #     axs[i, 1].imshow(ale_final_obs[0][i])
        #     axs[i, 2].imshow(gym_final_obs[0][i].astype(np.int32) - ale_final_obs[0][i].astype(np.int32))
        # [ax.axis('off') for ax in axs.flatten()]
        # plt.show()
        # assert obs_equivalence(
        #     gym_final_obs, ale_final_obs, t, autoreset_mode="SAME-STEP"
        # )
    else:
        gym_info = {
            key: value.astype(np.int32)
            for key, value in gym_info.items()
            if not key.startswith("_") and key != "seeds"
        }

        print(f'{gym_info.keys()=}, {ale_info.keys()=}')
        assert data_equivalence(gym_info, ale_info), t

assert has_autoreset

gym_envs.close()
ale_envs.close()
