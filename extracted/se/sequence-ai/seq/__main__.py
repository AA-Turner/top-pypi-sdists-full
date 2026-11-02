"""`python -m seq …`: the `seq` command by another way in. macOS ships its own /usr/bin/seq (it prints sequences of
numbers), and where /usr/bin comes before the SDK's bin on PATH, `seq deploy` answers "seq: invalid floating point
argument: deploy"; `python -m seq deploy` reaches this CLI whatever PATH says. It is the console script's own entry
(seq_launch), so both say the same."""
import sys

from seq_launch import main

sys.exit(main())
