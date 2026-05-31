
import numpy as np

data = np.load("log_data.npz", allow_pickle=True)
print(f'{data.keys()=}')

sync_infos = data['sync_infos']
async_info = data["async_info"].item()
async_t = data["async_t"]
env_id = data["env_id"]
async_i = data["async_i"]

print(f'{async_info=}')
print(f'{sync_infos=}')
print(f'{async_t=}')
print(f'{async_i=}')
print(f'{env_id=}')
for key in async_info:
    print(f'{key=}, sync={sync_infos[async_t][key][env_id]}, async={async_info[key][async_i]}')

async_env_ids = data["async_env_ids"]
print(f'{async_env_ids=}')

async_env_timestep = data["async_env_timestep"]
print(f'{async_env_timestep=}')

for env_id, async_t in enumerate(async_env_timestep):
    print(f'{env_id=}, async_t={async_t}, frame_number={sync_infos[async_t]["frame_number"][env_id]}')
