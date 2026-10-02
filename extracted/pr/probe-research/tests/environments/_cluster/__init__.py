"""Shared harness for the cluster environment tests (Slurm, NFS home, no-egress, multi-node DDP).

Everything here drives Docker from the pytest process; the SDK under test is the
RELEASED probe-research inside the containers, never this tree's code.
"""
