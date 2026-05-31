import numpy as np

data = np.load("log_data.npz", allow_pickle=True)

sync_infos = data['sync_infos']
async_info = data["async_info"].item()
async_t = int(data["async_t"])
env_id = int(data["env_id"])
async_i = int(data["async_i"])
async_env_ids = data["async_env_ids"]
async_env_timestep = data["async_env_timestep"]

print("=" * 80)
print("FAILURE ANALYSIS")
print("=" * 80)
print(f"\nFailed at: async_t={async_t}, env_id={env_id}, async_i={async_i}")
print(f"async_env_ids (batch returned): {async_env_ids}")
print(f"async_env_timestep (per env): {async_env_timestep}")
print()

# The issue: env_id=2 should be at timestep 882
# Let's check what happened around this time
print(f"Environment {env_id} should be at timestep {async_t}")
print(f"But async_env_timestep[{env_id}] = {async_env_timestep[env_id]}")
print()

# Check the async data
print("Async data returned (batch_size=4):")
for i, eid in enumerate(async_env_ids):
    print(f"  async_i={i}, env_id={eid}:")
    for key in async_info:
        print(f"    {key}: {async_info[key][i]}")
print()

# Check sync data at timestep async_t for env_id
print(f"Sync data at timestep {async_t} for env {env_id}:")
for key in async_info:
    print(f"  {key}: {sync_infos[async_t][key][env_id]}")
print()

# The critical comparison that failed
print("MISMATCH:")
for key in async_info:
    sync_val = sync_infos[async_t][key][env_id]
    async_val = async_info[key][async_i]
    match = "✓" if sync_val == async_val else "✗"
    print(f"  {match} {key}: sync={sync_val}, async={async_val}")
print()

# Let's trace back the history for env_id=2
print(f"\nHistory of environment {env_id}:")
print(f"{'Timestep':<10} {'Lives':<6} {'FrameNum':<10} {'EpFrameNum':<12}")
print("-" * 40)

# Find when env_id=2 appeared in async batches
print("\nWhen did env_id=2 appear in async batches?")
# We need to reconstruct the async batch history
# The test increments async_env_timestep after each async step
# So we need to trace through the sync timeline and see which envs were returned

# Let's look at the last few timesteps for env 2 in sync
lookback = 20
for t in range(max(0, async_t - lookback), min(len(sync_infos), async_t + 5)):
    lives = sync_infos[t]['lives'][env_id]
    frame_num = sync_infos[t]['frame_number'][env_id]
    ep_frame_num = sync_infos[t]['episode_frame_number'][env_id]
    marker = " <- EXPECTED" if t == async_t else ""
    print(f"{t:<10} {lives:<6} {frame_num:<10} {ep_frame_num:<12}{marker}")
print()

# Look at the values more carefully
# The async shows episode_frame_number=108, lives=4
# Let's find where in sync history env_id=2 had these values
print(f"\nSearching for when env {env_id} had lives=4 and episode_frame_number=108:")
found_matches = []
for t in range(len(sync_infos)):
    if (sync_infos[t]['lives'][env_id] == 4 and
        sync_infos[t]['episode_frame_number'][env_id] == 108):
        found_matches.append(t)
        print(f"  Found at timestep t={t}: frame_number={sync_infos[t]['frame_number'][env_id]}")

if found_matches:
    print(f"\nClosest match to async frame_number={async_info['frame_number'][async_i]}:")
    for t in found_matches:
        fn = sync_infos[t]['frame_number'][env_id]
        diff = abs(fn - async_info['frame_number'][async_i])
        print(f"  t={t}, frame_number={fn}, diff={diff}")
print()

# Check if this is a life reset issue
print(f"\nChecking for life loss events for env {env_id} around timestep {async_t}:")
for t in range(max(0, async_t - 10), min(len(sync_infos), async_t + 2)):
    if t > 0:
        prev_lives = sync_infos[t-1]['lives'][env_id]
        curr_lives = sync_infos[t]['lives'][env_id]
        if prev_lives != curr_lives:
            print(f"  t={t}: lives changed from {prev_lives} -> {curr_lives}")
            print(f"    episode_frame_number: {sync_infos[t]['episode_frame_number'][env_id]}")