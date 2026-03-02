from downstream.dstream import sticky_algo as algo


def test_sticky_get_ingest_capacity():
    assert algo.get_ingest_capacity(0) == 0
    assert algo.get_ingest_capacity(1) is None
    assert algo.get_ingest_capacity(2) is None
    assert algo.get_ingest_capacity(3) is None
    assert algo.get_ingest_capacity(4) is None
    assert algo.get_ingest_capacity(5) is None
    assert algo.get_ingest_capacity(6) is None
    assert algo.get_ingest_capacity(7) is None
    assert algo.get_ingest_capacity(8) is None
    assert algo.get_ingest_capacity(9) is None
    assert algo.get_ingest_capacity(10) is None
    assert algo.get_ingest_capacity(11) is None
    assert algo.get_ingest_capacity(12) is None
    assert algo.get_ingest_capacity(13) is None
    assert algo.get_ingest_capacity(14) is None
    assert algo.get_ingest_capacity(15) is None
    assert algo.get_ingest_capacity(16) is None
