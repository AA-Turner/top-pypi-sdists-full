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
print("RACE CONDITION ANALYSIS")
print("=" * 80)

# The claim: env_id=2 at async_i=3 has wrong data
# The async data shows: lives=4, frame_number=3592, episode_frame_number=108
target_lives = async_info['lives'][async_i]
target_frame_num = async_info['frame_number'][async_i]
target_ep_frame_num = async_info['episode_frame_number'][async_i]

print(f"\nAsync position {async_i} claims to be env {env_id}:")
print(f"  Actual data: lives={target_lives}, fn={target_frame_num}, efn={target_ep_frame_num}")
print(f"  Expected (sync t={async_t}, env={env_id}): lives={sync_infos[async_t]['lives'][env_id]}, fn={sync_infos[async_t]['frame_number'][env_id]}, efn={sync_infos[async_t]['episode_frame_number'][env_id]}")
print()

print("Checking if this async data actually belongs to a DIFFERENT environment:")
print(f"async_env_timestep = {async_env_timestep}")
print()

# For each environment, check if the async data matches that env's expected timestep
for check_env in range(8):
    expected_t = async_env_timestep[check_env]
    sync_lives = sync_infos[expected_t]['lives'][check_env]
    sync_fn = sync_infos[expected_t]['frame_number'][check_env]
    sync_efn = sync_infos[expected_t]['episode_frame_number'][check_env]

    lives_match = sync_lives == target_lives
    fn_match = sync_fn == target_frame_num
    efn_match = sync_efn == target_ep_frame_num

    if lives_match and efn_match and fn_match:
        print(f"*** EXACT MATCH *** env={check_env} at timestep {expected_t}")
        print(f"    lives={sync_lives}, fn={sync_fn}, efn={sync_efn}")
        if check_env != env_id:
            print(f"    ^^^ THIS IS THE CULPRIT! Env {check_env} overwrote env {env_id}'s data!")
    elif lives_match and efn_match:
        print(f"Partial match: env={check_env} at timestep {expected_t}")
        print(f"    lives={sync_lives} ✓, fn={sync_fn} (async={target_frame_num}, diff={sync_fn - target_frame_num}), efn={sync_efn} ✓")
    elif lives_match or efn_match or fn_match:
        matches = []
        if lives_match: matches.append("lives")
        if fn_match: matches.append("fn")
        if efn_match: matches.append("efn")
        print(f"Weak match: env={check_env} at timestep {expected_t} matches: {', '.join(matches)}")

print("\n" + "=" * 80)
print("DETAILED COMPARISON")
print("=" * 80)

# Check specifically the environments in the current async batch
print(f"\nCurrent async batch env_ids: {async_env_ids}")
print(f"Failed on async_i={async_i}, which claims to be env_id={env_id}")
print()

for i, claimed_env in enumerate(async_env_ids):
    async_data = {
        'lives': async_info['lives'][i],
        'frame_number': async_info['frame_number'][i],
        'episode_frame_number': async_info['episode_frame_number'][i]
    }

    expected_t = async_env_timestep[claimed_env]
    expected_data = {
        'lives': sync_infos[expected_t]['lives'][claimed_env],
        'frame_number': sync_infos[expected_t]['frame_number'][claimed_env],
        'episode_frame_number': sync_infos[expected_t]['episode_frame_number'][claimed_env]
    }

    marker = " <-- FAILURE" if i == async_i else ""
    match = "✓" if async_data == expected_data else "✗"
    print(f"{match} async_i={i}, env_id={claimed_env} at t={expected_t}{marker}")
    print(f"    Async:    {async_data}")
    print(f"    Expected: {expected_data}")

    # Does this async data match a DIFFERENT environment in the batch?
    if async_data != expected_data:
        print(f"    Checking if this matches another env in the batch:")
        for other_env in range(8):
            other_t = async_env_timestep[other_env]
            if (sync_infos[other_t]['lives'][other_env] == async_data['lives'] and
                sync_infos[other_t]['frame_number'][other_env] == async_data['frame_number'] and
                sync_infos[other_t]['episode_frame_number'][other_env] == async_data['episode_frame_number']):
                print(f"      *** MATCHES env={other_env} at t={other_t} ***")
    print()