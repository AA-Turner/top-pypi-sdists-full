import os
from collections import defaultdict
from ...imports import hashlib
from ...json_utils import safe_dump_to_json
from ...imports import make_list
from ...file_utils import get_files_and_dirs
# Canonical content hashes live in the stdlib-only core; quick_hash folds the
# file size into the digest (two files sharing a header no longer collide).
from abstract_essentials import full_hash, quick_hash
