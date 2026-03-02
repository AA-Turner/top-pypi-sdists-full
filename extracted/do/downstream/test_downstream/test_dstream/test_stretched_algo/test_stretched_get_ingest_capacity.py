from downstream.dstream import stretched_algo as algo


def test_stretched_get_ingest_capacity():
    assert algo.get_ingest_capacity(0) == 0
    assert algo.get_ingest_capacity(1) == 0
    assert algo.get_ingest_capacity(2) == 3
    assert algo.get_ingest_capacity(3) == 0
    assert algo.get_ingest_capacity(4) == 15
    assert algo.get_ingest_capacity(5) == 0
    assert algo.get_ingest_capacity(6) == 0
    assert algo.get_ingest_capacity(7) == 0
    assert algo.get_ingest_capacity(8) == 255
    assert algo.get_ingest_capacity(9) == 0
    assert algo.get_ingest_capacity(10) == 0
    assert algo.get_ingest_capacity(11) == 0
    assert algo.get_ingest_capacity(12) == 0
    assert algo.get_ingest_capacity(13) == 0
    assert algo.get_ingest_capacity(14) == 0
    assert algo.get_ingest_capacity(15) == 0
    assert algo.get_ingest_capacity(16) == 65535
