import numpy as np

data = np.load("log_data.npz", allow_pickle=True)

sync_infos = data['sync_infos']
async_info = data["async_info"].item()
async_env_ids = data["async_env_ids"]
async_env_timestep = data["async_env_timestep"]

print("=" * 80)
print("VERIFICATION: async_i=3 has env 6's PREVIOUS timestep data")
print("=" * 80)
print()

print(f"async_env_ids = {async_env_ids}")
print(f"async_env_timestep = {async_env_timestep}")
print()

# Check async_i=2 (should be env 6 at timestep 884)
env6_i = 2
env6_id = async_env_ids[env6_i]
env6_expected_t = async_env_timestep[env6_id]

print(f"async_i={env6_i} (env {env6_id}):")
print(f"  Expected timestep: {env6_expected_t}")
print(f"  Actual async data: lives={async_info['lives'][env6_i]}, fn={async_info['frame_number'][env6_i]}, efn={async_info['episode_frame_number'][env6_i]}")
print(f"  Sync at t={env6_expected_t}: lives={sync_infos[env6_expected_t]['lives'][env6_id]}, fn={sync_infos[env6_expected_t]['frame_number'][env6_id]}, efn={sync_infos[env6_expected_t]['episode_frame_number'][env6_id]}")
print(f"  Match: {async_info['lives'][env6_i] == sync_infos[env6_expected_t]['lives'][env6_id]}")
print()

# Check async_i=3 (should be env 2 at timestep 882)
env2_i = 3
env2_id = async_env_ids[env2_i]
env2_expected_t = async_env_timestep[env2_id]

print(f"async_i={env2_i} (env {env2_id}):")
print(f"  Expected timestep: {env2_expected_t}")
print(f"  Actual async data: lives={async_info['lives'][env2_i]}, fn={async_info['frame_number'][env2_i]}, efn={async_info['episode_frame_number'][env2_i]}")
print(f"  Sync at t={env2_expected_t}: lives={sync_infos[env2_expected_t]['lives'][env2_id]}, fn={sync_infos[env2_expected_t]['frame_number'][env2_id]}, efn={sync_infos[env2_expected_t]['episode_frame_number'][env2_id]}")
print(f"  Match: {async_info['lives'][env2_i] == sync_infos[env2_expected_t]['lives'][env2_id]}")
print()

print("=" * 80)
print("HYPOTHESIS: async_i=3 contains env 6's data from timestep 883")
print("=" * 80)
print()

env6_prev_t = env6_expected_t - 1
print(f"Env 6 at timestep {env6_prev_t} (one before expected):")
print(f"  Sync data: lives={sync_infos[env6_prev_t]['lives'][env6_id]}, fn={sync_infos[env6_prev_t]['frame_number'][env6_id]}, efn={sync_infos[env6_prev_t]['episode_frame_number'][env6_id]}")
print(f"  async_i=3 data: lives={async_info['lives'][env2_i]}, fn={async_info['frame_number'][env2_i]}, efn={async_info['episode_frame_number'][env2_i]}")
print(f"  EXACT MATCH: {async_info['lives'][env2_i] == sync_infos[env6_prev_t]['lives'][env6_id] and async_info['frame_number'][env2_i] == sync_infos[env6_prev_t]['frame_number'][env6_id] and async_info['episode_frame_number'][env2_i] == sync_infos[env6_prev_t]['episode_frame_number'][env6_id]}")
print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"The batch contains env_ids: {async_env_ids}")
print(f"  async_i=2 (env 6): CORRECT data from timestep {env6_expected_t}")
print(f"  async_i=3 (env 2): WRONG - has env 6's data from timestep {env6_prev_t}")
print()
print("This suggests env 6's output buffer from the previous step wasn't cleared")
print("or was written to the wrong position (async_i=3 instead of staying at async_i=2)")
