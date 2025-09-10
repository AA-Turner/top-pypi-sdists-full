import structlog

from pytest_structlog import StructuredLogCapture


def spline_reticulator():
    logger = structlog.get_logger()
    logger.info("reticulating splines")
    for i in range(3):
        logger.debug("processing", spline=i)
    logger.info("reticulated splines", n_splines=3)


def test_spline_reticulator(log: StructuredLogCapture):
    assert len(log.events) == 0
    spline_reticulator()
    assert len(log.events) == 5

    # can assert on the event only
    assert log.has("reticulating splines")

    # can assert with subcontext
    assert log.has("reticulated splines")
    assert log.has("reticulated splines", n_splines=3)
    assert log.has("reticulated splines", n_splines=3, level="info")

    # but not incorrect context
    assert not log.has("reticulated splines", n_splines=42)
    assert not log.has("reticulated splines", key="bogus")

    # can assert with the event dicts directly
    assert log.events == [
        {"event": "reticulating splines", "level": "info"},
        {"event": "processing", "level": "debug", "spline": 0},
        {"event": "processing", "level": "debug", "spline": 1},
        {"event": "processing", "level": "debug", "spline": 2},
        {"event": "reticulated splines", "level": "info", "n_splines": 3},
    ]

    # can use friendly factory methods for the events to assert on
    assert log.events == [
        log.info("reticulating splines"),
        log.debug("processing", spline=0),
        log.debug("processing", spline=1),
        log.debug("processing", spline=2),
        log.info("reticulated splines", n_splines=3),
    ]

    # can use membership to check for a single event's data
    assert {"event": "reticulating splines", "level": "info"} in log.events

    # can use >= to specify only the events you're interested in
    assert log.events >= [
        {"event": "processing", "level": "debug", "spline": 0},
        {"event": "processing", "level": "debug", "spline": 2},
    ]

    # or put the comparison the other way around if you prefer
    assert [
        {"event": "processing", "level": "debug", "spline": 0},
        {"event": "processing", "level": "debug", "spline": 2},
    ] <= log.events

    # note: comparisons are order sensitive!
    assert not [
        {"event": "processing", "level": "debug", "spline": 2},
        {"event": "processing", "level": "debug", "spline": 0},
    ] <= log.events

    # count of events
    assert log.count("processing") == 3
