#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import threading
from collections import defaultdict

from snowflake.snowpark_connect.utils.context import get_spark_session_id

# per session number sequences to generate unique snowpark columns
_session_sequences = defaultdict(int)

_lock = threading.Lock()


def next_unique_num():
    session_id = get_spark_session_id()
    with _lock:
        next_num = _session_sequences[session_id]
        _session_sequences[session_id] = next_num + 1
    return next_num
