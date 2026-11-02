"""
`seq eval replay` - the console's 3D replay player, served on this machine, and `seq.read_replay`.

The player's files under `player/` are the console's own, as its site serves them (MANIFEST.json says which, with each
file's sha256); tools/replay_player.py copies them and checks them against the console before a release is built.
"""
