"""
spotilyzer subcommands entry point
"""

# project imports
from .init import Init
from .create_candidates import CreateCandidates
from .show_candidates import ShowCandidates
from .group_requests import GroupRequests
from .size_fleets import SizeFleets

# exports
subcommands = [Init, CreateCandidates, ShowCandidates, GroupRequests,
               SizeFleets]
