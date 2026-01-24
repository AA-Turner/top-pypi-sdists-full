import time
from datetime import datetime

from tango import TimeVal
from tango.test_utils import assert_close


def test_timeval():
    # test constructors
    from_default = TimeVal()
    assert from_default.tv_sec == 0
    assert from_default.tv_usec == 0
    assert from_default.tv_nsec == 0

    from_ints = TimeVal(1, 2, 3)
    assert from_ints.tv_sec == 1
    assert from_ints.tv_usec == 2
    assert from_ints.tv_nsec == 3

    from_int = TimeVal(100)
    assert from_int.tv_sec == 100
    assert from_int.tv_usec == 0
    assert from_int.tv_nsec == 0

    from_float = TimeVal(100.200300400)
    assert from_float.tv_sec == 100
    assert from_float.tv_usec == 200300
    assert from_float.tv_nsec == 400

    from_datetime = TimeVal(datetime.now())
    assert from_datetime.tv_sec > 0

    # test convertors:
    now_float = time.time()
    now_tv = TimeVal(now_float)
    assert_close(now_float, now_tv.totime())

    now_datetime = datetime.now()
    now_tv = TimeVal(now_datetime)
    assert now_tv.todatetime() == now_datetime
