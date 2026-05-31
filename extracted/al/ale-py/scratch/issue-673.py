from ale_py.vector_env import AtariVectorEnv
import numpy as np

envs = AtariVectorEnv(game='breakout', num_envs=2)
envs.reset()

mask = np.array([False, True])
envs.reset(options=dict(reset_mask=mask))
print("done")
envs.close()
