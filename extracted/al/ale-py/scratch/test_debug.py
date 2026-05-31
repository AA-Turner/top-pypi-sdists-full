"""Debug test for segfault investigation."""
import ale_py
import gymnasium as gym
import numpy as np

gym.register_envs(ale_py)

env_id = "ALE/Breakout-v5"
batch_size = 4
num_envs = 8

print(f"Creating async environment: num_envs={num_envs}, batch_size={batch_size}")
async_envs = gym.make_vec(env_id, num_envs, batch_size=batch_size)

print("Resetting environment...")
async_obs, async_info = async_envs.reset(seed=123)
print(f"Reset successful - obs shape: {async_obs.shape}, dtype: {async_obs.dtype}")
print(f"Info keys: {async_info.keys()}")
print(f"env_id: {async_info['env_id']}")

print("\nStepping through a few iterations...")
for i in range(10):
    actions = async_envs.action_space.sample()
    print(f"\nStep {i}: actions shape={actions.shape}")

    try:
        obs, rewards, terminations, truncations, info = async_envs.step(actions)
        print(f"  obs shape: {obs.shape}, dtype: {obs.dtype}")
        print(f"  rewards: {rewards}")
        print(f"  terminations: {terminations}")
        print(f"  truncations: {truncations}")
        print(f"  env_ids: {info['env_id']}")
        print(f"  info keys: {info.keys()}")

        # Try to access the observation data
        print(f"  obs[0,0,0,0] = {obs[0,0,0,0]}")

    except Exception as e:
        print(f"ERROR at step {i}: {e}")
        import traceback
        traceback.print_exc()
        break

print("\nClosing environment...")
async_envs.close()
print("Done")
