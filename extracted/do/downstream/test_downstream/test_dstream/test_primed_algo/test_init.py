from downstream import dstream
from downstream.dstream import primed_algo as algo_class


def test_nopad():
    algo = algo_class(algo=dstream.sticky_algo, lpad=0, rpad=0)
    assert algo._algo is dstream.sticky_algo
    assert algo._pad_offset == 0
    assert algo._pad_size == 0


def test_lpad():
    algo = algo_class(algo=dstream.sticky_algo, lpad=4, rpad=0)
    assert algo._algo is dstream.sticky_algo
    assert algo._pad_offset == 4
    assert algo._pad_size == 4


def test_rpad():
    algo = algo_class(algo=dstream.sticky_algo, lpad=0, rpad=4)
    assert algo._algo is dstream.sticky_algo
    assert algo._pad_offset == 0
    assert algo._pad_size == 4


def test_lrpad():
    algo = algo_class(algo=dstream.sticky_algo, lpad=4, rpad=4)
    assert algo._algo is dstream.sticky_algo
    assert algo._pad_offset == 4
    assert algo._pad_size == 8
