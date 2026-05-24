"""
General test for the `simpy.core.Environment`.

"""

# Pytest gets the parameters "env" and "log" from the *conftest.py* file
import pytest


def test_event_queue_empty(env, log):
    """The simulation should stop if there are no more events, that means, no
    more active process."""

    def pem(env, log):
        while env.now < 2:
            log.append(env.now)
            yield env.timeout(1)

    env.process(pem(env, log))
    env.run(10)

    assert log == [0, 1]


def test_run_negative_until(env):
    """Test passing a negative time to run."""
    with pytest.raises(
        ValueError, match='must be greater than the current simulation time'
    ):
        env.run(-3)


def test_run_resume(env):
    """Stopped simulation can be resumed."""
    events = [env.timeout(t) for t in (5, 10, 15)]

    assert env.now == 0
    assert not any(event.processed for event in events)

    env.run(until=10)
    assert env.now == 10
    assert all(event.processed for event in events[:1])
    assert not any(event.processed for event in events[1:])

    env.run(until=15)
    assert env.now == 15
    assert all(event.processed for event in events[:2])
    assert not any(event.processed for event in events[2:])

    env.run()
    assert env.now == 15
    assert all(event.processed for event in events)


def test_run_until_value(env):
    """Anything that can be converted to a float is a valid until value."""
    env.run(until='3.141592')
    assert env.now == 3.141592


def test_run_with_processed_event(env):
    """An already processed event may also be passed as until value."""
    timeout = env.timeout(1, value='spam')
    assert env.run(until=timeout) == 'spam'
    assert env.now == 1

    # timeout has been processed, calling run again will return its value
    # again.

    assert env.run(until=timeout) == 'spam'
    assert env.now == 1


def test_run_with_untriggered_event(env):
    with pytest.raises(RuntimeError) as excinfo:
        env.run(until=env.event())
    assert str(excinfo.value).startswith(
        'No scheduled events left but "until" event was not triggered:'
    )


def test_run_all_until_callbacks(env):
    """Ensure `until` event callbacks are called when resuming simulation."""

    class System:
        def __init__(self, env):
            self.env = env
            self.counter = 0
            self.periodic_event = env.event()

        def periodic(self):
            for _ in range(3):
                yield self.env.timeout(1)
                event, self.periodic_event = self.periodic_event, self.env.event()
                event.succeed(self.counter)

        def consumer(self):
            while True:
                yield self.periodic_event
                self.counter += 1

    system = System(env)
    env.process(system.periodic())
    for _ in range(5):
        env.process(system.consumer())

    period_counter = env.run(until=system.periodic_event)
    assert env.now == 1
    # The periodic process triggers the periodic_event before any consumers can
    # respond to the periodic event. Thus the first period counter is 0.
    assert period_counter == 0
    # And because the simulation is supposed to stop when the `until` event is
    # _triggered_, i.e. "its callbacks are about to be invoked", the consumer
    # processes should not yet have observed the periodic_event and thus the
    # system.counter should remain at 0.
    assert system.counter == 0

    period_counter = env.run(until=system.periodic_event)
    assert env.now == 2
    # When simulation stops again, system.counter must reflect that each of the
    # consumer processes observed the first periodic_event, but not the second.
    assert period_counter == 5
    assert system.counter == 5

    period_counter = env.run(until=system.periodic_event)
    assert env.now == 3
    assert period_counter == 10
    assert system.counter == 10

    env.run()
    assert env.now == 3
    # After processing all events, the consumers will have observed the last of
    # the three periodic_events, incrementing system.counter to 3 * 5 = 15.
    assert system.counter == 15
