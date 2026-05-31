"""Minimal test to isolate the crash."""
import ale_py
import gymnasium as gym
import numpy as np

gym.register_envs(ale_py)

print("Test 1: Sync mode (batch_size == num_envs)")
try:
    env = gym.make_vec("ALE/Breakout-v5", num_envs=4)
    obs, info = env.reset(seed=0)
    print(f"  Reset OK - obs shape: {obs.shape}")

    for i in range(5):
        actions = env.action_space.sample()
        obs, rew, term, trunc, info = env.step(actions)
        print(f"  Step {i} OK")

    env.close()
    print("  PASSED\n")
except Exception as e:
    print(f"  FAILED: {e}\n")

print("Test 2: Async mode (batch_size < num_envs)")
try:
    env = gym.make_vec("ALE/Breakout-v5", num_envs=8, batch_size=4)
    print(f"  Created env - num_envs={env.num_envs}, batch_size={env.ale.get_batch_size() if hasattr(env.ale, 'get_batch_size') else 'unknown'}")

    obs, info = env.reset(seed=0)
    print(f"  Reset OK - obs shape: {obs.shape}, env_ids: {info['env_id']}")

    for i in range(5):
        actions = env.action_space.sample()
        print(f"  Stepping with actions shape: {actions.shape}")
        obs, rew, term, trunc, info = env.step(actions)
        print(f"  Step {i} OK - env_ids: {info['env_id']}")

    env.close()
    print("  PASSED\n")
except Exception as e:
    print(f"  FAILED: {e}\n")
    import traceback
    traceback.print_exc()
