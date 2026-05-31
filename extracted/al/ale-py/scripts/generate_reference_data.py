#!/usr/bin/env python3
"""
Generate reference data from ALE for regression testing.

This script should be run BEFORE migrating to nanobind to establish
a baseline for comparison.

Usage:
  python generate_reference_data.py

Output:
  Creates 'ale_reference_data.npz' with various ALE outputs
"""

import numpy as np
from pathlib import Path
import pickle
import json

try:
    from ale_py import ALEInterface, roms
    print("Successfully imported ale_py")
except ImportError as e:
    print(f"Error importing ale_py: {e}")
    print("Make sure ALE is installed: pip install -e .")
    exit(1)


def generate_reference_data(output_file="ale_reference_data.npz", num_steps=100):
    """
    Generate comprehensive reference data from ALE.

    Args:
        output_file: Path to save the reference data
        num_steps: Number of game steps to record
    """
    print("=" * 60)
    print("Generating ALE Reference Data")
    print("=" * 60)
    print()

    # Initialize ALE
    ale = ALEInterface()

    # Try to load a ROM
    rom_path = None
    rom_name = None
    rom_files = ['breakout', 'pong', 'space_invaders']

    for rom_candidate in rom_files:
        try:
            rom_path = roms.get_rom_path(rom_candidate)
            if rom_path and Path(rom_path).exists():
                ale.loadROM(rom_path)
                rom_name = rom_candidate
                print(f"Loaded ROM: {rom_name}")
                break
        except Exception as e:
            continue

    if rom_path is None:
        print("Error: Could not load any ROM.")
        print("Please ensure at least one Atari ROM is available.")
        exit(1)

    print(f"Using ROM: {rom_name}")
    print(f"Generating {num_steps} steps of data...")
    print()

    # Metadata
    metadata = {
        'rom_name': rom_name,
        'rom_path': str(rom_path),
        'num_steps': num_steps,
        'ale_version': ale_py.__version__ if hasattr(ale_py, '__version__') else 'unknown',
        'sdl_support': ale_py.SDL_SUPPORT if hasattr(ale_py, 'SDL_SUPPORT') else False,
    }

    # Get static information
    legal_actions = ale.getLegalActionSet()
    minimal_actions = ale.getMinimalActionSet()
    available_modes = ale.getAvailableModes()
    available_difficulties = ale.getAvailableDifficulties()
    screen_dims = ale.getScreenDims()
    ram_size = ale.getRAMSize()
    audio_size = ale.getAudioSize()

    metadata['legal_actions'] = [int(a) for a in legal_actions]
    metadata['minimal_actions'] = [int(a) for a in minimal_actions]
    metadata['available_modes'] = [int(m) for m in available_modes]
    metadata['available_difficulties'] = [int(d) for d in available_difficulties]
    metadata['screen_dims'] = screen_dims
    metadata['ram_size'] = ram_size
    metadata['audio_size'] = audio_size

    print("Static Information:")
    print(f"  Screen dimensions: {screen_dims}")
    print(f"  RAM size: {ram_size}")
    print(f"  Audio size: {audio_size}")
    print(f"  Legal actions: {len(legal_actions)}")
    print(f"  Minimal actions: {len(minimal_actions)}")
    print(f"  Available modes: {available_modes}")
    print(f"  Available difficulties: {available_difficulties}")
    print()

    # Data arrays to collect
    data = {
        # Per-step data
        'screens': [],
        'screens_rgb': [],
        'screens_grayscale': [],
        'ram_states': [],
        'rewards': [],
        'lives': [],
        'frame_numbers': [],
        'episode_frame_numbers': [],
        'game_over_flags': [],
        'game_truncated_flags': [],

        # Actions taken
        'actions': [],

        # Serialized states (every 10 steps)
        'serialized_states': [],
        'serialized_state_steps': [],
    }

    # Pre-allocate arrays for better performance
    h, w = screen_dims
    data['screens'] = np.zeros((num_steps, h, w), dtype=np.uint8)
    data['screens_rgb'] = np.zeros((num_steps, h, w, 3), dtype=np.uint8)
    data['screens_grayscale'] = np.zeros((num_steps, h, w), dtype=np.uint8)
    data['ram_states'] = np.zeros((num_steps, ram_size), dtype=np.uint8)
    data['audio_states'] = np.zeros((num_steps, audio_size), dtype=np.uint8)
    data['rewards'] = np.zeros(num_steps, dtype=np.float32)
    data['lives'] = np.zeros(num_steps, dtype=np.int32)
    data['frame_numbers'] = np.zeros(num_steps, dtype=np.int32)
    data['episode_frame_numbers'] = np.zeros(num_steps, dtype=np.int32)
    data['game_over_flags'] = np.zeros(num_steps, dtype=bool)
    data['game_truncated_flags'] = np.zeros(num_steps, dtype=bool)
    data['actions'] = np.zeros(num_steps, dtype=np.int32)

    # Generate data
    print("Generating step data...")
    for step in range(num_steps):
        # Choose action (cycle through legal actions)
        action = legal_actions[step % len(legal_actions)]
        data['actions'][step] = action

        # Take action
        reward = ale.act(action)
        data['rewards'][step] = reward

        # Get screen data
        data['screens'][step] = ale.getScreen()
        data['screens_rgb'][step] = ale.getScreenRGB()
        data['screens_grayscale'][step] = ale.getScreenGrayscale()

        # Get RAM and Audio
        data['ram_states'][step] = ale.getRAM()
        data['audio_states'][step] = ale.getAudio()

        # Get state information
        data['lives'][step] = ale.lives()
        data['frame_numbers'][step] = ale.getFrameNumber()
        data['episode_frame_numbers'][step] = ale.getEpisodeFrameNumber()
        data['game_over_flags'][step] = ale.game_over()
        data['game_truncated_flags'][step] = ale.game_truncated()

        # Save state periodically
        if step % 10 == 0:
            state = ale.cloneState()
            try:
                serialized = state.serialize()
                data['serialized_states'].append(serialized)
                data['serialized_state_steps'].append(step)
            except Exception as e:
                # Skip serialization if it fails
                print("ERROR", e)

        # Reset if game over
        if ale.game_over():
            ale.reset_game()
            print(f"  Game over at step {step}, resetting...")

        # Progress indicator
        if (step + 1) % 20 == 0:
            print(f"  Step {step + 1}/{num_steps}")

    print()
    print("Data generation complete!")
    print()

    # Test state serialization/deserialization
    print("Testing state serialization...")
    if data['serialized_states']:
        # Clone and restore a state
        test_state = ale.cloneState()
        ale.act(legal_actions[0])  # Modify state
        ale.restoreState(test_state)  # Restore
        print("  State serialization test passed!")

    # Test pre-allocated buffer methods
    print("Testing pre-allocated buffer methods...")
    screen_buffer = np.zeros(screen_dims, dtype=np.uint8)
    ale.getScreen(screen_buffer)
    assert np.array_equal(screen_buffer, ale.getScreen()), "Screen buffer method mismatch!"

    rgb_buffer = np.zeros((*screen_dims, 3), dtype=np.uint8)
    ale.getScreenRGB(rgb_buffer)
    assert np.array_equal(rgb_buffer, ale.getScreenRGB()), "RGB buffer method mismatch!"

    ram_buffer = np.zeros(ram_size, dtype=np.uint8)
    ale.getRAM(ram_buffer)
    assert np.array_equal(ram_buffer, ale.getRAM()), "RAM buffer method mismatch!"
    print("  Buffer method tests passed!")
    print()

    # Save data
    print(f"Saving reference data to: {output_file}")

    # Save metadata as JSON
    metadata_file = output_file.replace('.npz', '_metadata.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"  Metadata saved to: {metadata_file}")

    # Save numpy arrays
    np.savez_compressed(
        output_file,
        **data
    )
    print(f"  Data saved to: {output_file}")

    # Print summary statistics
    print()
    print("=" * 60)
    print("Reference Data Summary")
    print("=" * 60)
    print(f"Steps recorded: {num_steps}")
    print(f"Total reward: {data['rewards'].sum():.2f}")
    print(f"Average reward: {data['rewards'].mean():.4f}")
    print(f"Max reward: {data['rewards'].max():.2f}")
    print(f"Min reward: {data['rewards'].min():.2f}")
    print(f"Games completed: {data['game_over_flags'].sum()}")
    print(f"Final lives: {data['lives'][-1]}")
    print(f"Final frame: {data['frame_numbers'][-1]}")
    print(f"Serialized states: {len(data['serialized_states'])}")
    print()

    # Print data shapes
    print("Data shapes:")
    for key, value in data.items():
        if isinstance(value, np.ndarray):
            print(f"  {key:30s}: {value.shape} ({value.dtype})")
        elif isinstance(value, list):
            print(f"  {key:30s}: list of {len(value)} items")

    print()
    print("=" * 60)
    print("Reference data generation complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Commit the current pybind11 version")
    print("2. Migrate to nanobind")
    print("3. Run validate_against_reference.py to verify identical behavior")


if __name__ == "__main__":
    import ale_py
    generate_reference_data()