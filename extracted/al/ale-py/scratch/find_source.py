import numpy as np

data = np.load("log_data.npz", allow_pickle=True)

sync_infos = data['sync_infos']
async_info = data["async_info"].item()
async_t = int(data["async_t"])
env_id = int(data["env_id"])
async_i = int(data["async_i"])
async_env_ids = data["async_env_ids"]
async_env_timestep = data["async_env_timestep"]

# The bad data at async_i=3
target_lives = int(async_info['lives'][async_i])
target_frame_num = int(async_info['frame_number'][async_i])
target_ep_frame_num = int(async_info['episode_frame_number'][async_i])

print("=" * 80)
print("Finding source of corrupted data")
print("=" * 80)
print(f"\nSearching for: lives={target_lives}, fn={target_frame_num}, efn={target_ep_frame_num}")
print(f"This data is at async_i={async_i}, claiming to be env_id={env_id}")
print()

# Search ALL environments at ALL timesteps for exact match
print("Searching all environments at all timesteps for EXACT match:")
exact_matches = []
for t in range(len(sync_infos)):
    for eid in range(8):
        if (sync_infos[t]['lives'][eid] == target_lives and
            sync_infos[t]['frame_number'][eid] == target_frame_num and
            sync_infos[t]['episode_frame_number'][eid] == target_ep_frame_num):
            exact_matches.append((t, eid))

if exact_matches:
    print(f"Found {len(exact_matches)} exact matches:")
    for t, eid in exact_matches:
        in_batch = "IN CURRENT BATCH" if eid in async_env_ids else ""
        expected_t = async_env_timestep[eid]
        timing = f"expected t={expected_t}, diff={t - expected_t}" if eid < len(async_env_timestep) else ""
        print(f"  t={t}, env={eid}  {timing}  {in_batch}")
else:
    print("No exact matches found!")

# Now check env 6 specifically since it has similar data
print("\n" + "=" * 80)
print("Checking env 6 specifically (has similar lives=4, efn=112)")
print("=" * 80)

env6_t = async_env_timestep[6]
print(f"Env 6 is at timestep {env6_t}")
print(f"Env 6 data at t={env6_t}: lives={sync_infos[env6_t]['lives'][6]}, fn={sync_infos[env6_t]['frame_number'][6]}, efn={sync_infos[env6_t]['episode_frame_number'][6]}")
print(f"Target data:              lives={target_lives}, fn={target_frame_num}, efn={target_ep_frame_num}")
print()

# Check env 6 around its expected timestep
print(f"Env 6 history around timestep {env6_t}:")
for t in range(max(0, env6_t - 5), min(len(sync_infos), env6_t + 5)):
    lives = sync_infos[t]['lives'][6]
    fn = sync_infos[t]['frame_number'][6]
    efn = sync_infos[t]['episode_frame_number'][6]

    match = ""
    if lives == target_lives and fn == target_frame_num and efn == target_ep_frame_num:
        match = " *** EXACT MATCH ***"
    elif lives == target_lives and efn == target_ep_frame_num:
        match = f" (lives+efn match, fn diff={fn - target_frame_num})"

    marker = " <- current" if t == env6_t else ""
    print(f"  t={t}: lives={lives}, fn={fn}, efn={efn}{marker}{match}")

# Also check env 2 to see if it ever had lives=4
print("\n" + "=" * 80)
print("Checking env 2 history (did it ever have lives=4?)")
print("=" * 80)

env2_had_4_lives = []
for t in range(len(sync_infos)):
    if sync_infos[t]['lives'][2] == 4:
        env2_had_4_lives.append(t)

if env2_had_4_lives:
    print(f"Env 2 had lives=4 at {len(env2_had_4_lives)} timesteps")
    print(f"First few: {env2_had_4_lives[:10]}")
    print(f"Last few: {env2_had_4_lives[-10:]}")
    print()

    # Check if any of those also have efn=108
    for t in env2_had_4_lives:
        if sync_infos[t]['episode_frame_number'][2] == target_ep_frame_num:
            fn = sync_infos[t]['frame_number'][2]
            print(f"  t={t}: lives=4, efn={target_ep_frame_num}, fn={fn} (target fn={target_frame_num}, diff={fn - target_frame_num})")
else:
    print("Env 2 NEVER had lives=4 in the entire run!")

# Check which env_id is in the async batch at position 2 (just before position 3)
print("\n" + "=" * 80)
print("Checking async batch composition")
print("=" * 80)
print(f"async_env_ids = {async_env_ids}")
print(f"async_i=2 is env_id={async_env_ids[2]}")
print(f"async_i=3 is env_id={async_env_ids[3]}")
print()
print("Could env 6's data (at async_i=2) have been copied to async_i=3?")
print(f"  async_i=2 (env 6): lives={async_info['lives'][2]}, fn={async_info['frame_number'][2]}, efn={async_info['episode_frame_number'][2]}")
print(f"  async_i=3 (env 2): lives={async_info['lives'][3]}, fn={async_info['frame_number'][3]}, efn={async_info['episode_frame_number'][3]}")