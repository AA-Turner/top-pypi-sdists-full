"""What a call shows and does about a machine that does not come."""

import io
import json
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from unittest.mock import MagicMock

import cloudpickle
import grpc
import pytest

from beta9 import Image, NoCapacityError, terminal
from beta9.abstractions.base import capacity
from beta9.abstractions.function import Function, _Invocation
from beta9.channel import (
    SCHEDULING_FAILURE_TRAILER,
    Channel,
    handle_grpc_error,
    scheduling_failure,
)
from beta9.clients.function import (
    FunctionInvokeRequest,
    FunctionInvokeResponse,
    FunctionServiceStub,
)
from beta9.clients.gateway import (
    GetOrCreateStubRequest,
    GetOrCreateStubResponse,
    ListPoolOffersResponse,
    ListTasksResponse,
    PoolOffer,
    StopTasksRequest,
    Task,
)

LIMIT = capacity.wait_limit_name()

# What the gateway says each wait is for (types.ContainerPendingPhase.Message).
WORDS = {
    ("queued", ""): "Waiting to be placed on a machine",
    ("provisioning", "worker_starting"): "No warm machine, starting one",
    (
        "provisioning",
        "backup_worker_starting",
    ): "Preferred capacity is unavailable, starting a machine on backup capacity",
    ("waiting_for_capacity", "no_capacity"): "No capacity available right now, waiting for some",
    (
        "waiting_for_capacity",
        "no_spare_capacity",
    ): "The Spot tier has no spare capacity right now, waiting for some",
    ("starting", ""): "Placed on a machine, starting the container",
}

ACCEPTED = FunctionInvokeResponse(task_id="task-1", container_id="container-1")
RESULT = FunctionInvokeResponse(
    task_id="task-1", done=True, exit_code=0, result=cloudpickle.dumps(1998)
)


def says(phase, reason="", waited_seconds=0):
    """A response that says what the call waits for."""
    return FunctionInvokeResponse(
        task_id="task-1",
        pending_phase=phase,
        pending_reason=reason,
        pending_waited_seconds=waited_seconds,
        pending_message=WORDS[(phase, reason)],
    )


NO_CAPACITY = says("waiting_for_capacity", "no_capacity", waited_seconds=130)
COLD_START = says("provisioning", "worker_starting")


@pytest.fixture
def output():
    buffer = io.StringIO()
    with terminal.redirect_terminal_to_buffer(buffer):
        yield buffer


@pytest.fixture
def clock(monkeypatch):
    """The clock that waits are measured on, moved by hand."""
    now = SimpleNamespace(at=1000.0)
    monkeypatch.setattr(capacity, "time", SimpleNamespace(monotonic=lambda: now.at))
    return now


@pytest.fixture
def spinner(monkeypatch):
    """A spinner on screen, whose text is kept each time it is set."""
    texts = []
    monkeypatch.setattr(terminal, "spinner_visible", lambda: True)
    monkeypatch.setattr(
        terminal, "update_progress", lambda text: texts.append(text() if callable(text) else text)
    )
    return texts


def waiting(title=None, limit=0.0, gpu="A10G"):
    """A call that waits, what it is told, and whether it was given up."""
    runner = SimpleNamespace(
        stub_request=GetOrCreateStubRequest(gpu=gpu), pool_config=None, headless=False
    )
    wait = capacity.CapacityWait(runner, title, limit)
    stop = MagicMock()
    return wait, lambda response: wait.told(response, stop, lambda: False), stop


# What a call that waits shows


def test_a_warm_start_says_nothing(output, spinner):
    wait, tell, _ = waiting("Running transcribe")
    tell(says("queued"))
    tell(says("starting"))
    wait.running()

    assert output.getvalue() == ""
    assert spinner == []


def test_each_change_is_one_line_where_there_is_no_spinner(output):
    _, tell, _ = waiting("Running transcribe")
    for response in (
        says("queued"),
        says("waiting_for_capacity", "no_capacity"),
        says("waiting_for_capacity", "no_capacity", waited_seconds=30),
        COLD_START,
        says("provisioning", "worker_starting", waited_seconds=45),
        says("starting"),
    ):
        tell(response)

    assert [line.strip() for line in output.getvalue().splitlines()] == [
        "No capacity available right now, waiting for some",
        "No warm machine, starting one",
        "Placed on a machine, starting the container (waited 0:45)",
    ]


def test_the_spinner_says_what_the_call_waits_for_and_counts_the_time(spinner, output):
    wait, tell, _ = waiting("Running transcribe")

    # The gateway says how long it has waited already: a client that joins
    # late counts from there.
    tell(says("provisioning", "worker_starting", waited_seconds=75))
    assert spinner == ["Running transcribe · no warm machine, starting one (1:15)"]

    tell(says("starting"))
    assert spinner[-1] == (
        "Running transcribe · placed on a machine, starting the container (waited 1:15)"
    )

    # Once the container has output the spinner is the step's own again.
    wait.running()
    assert spinner[-1] == "Running transcribe"
    assert output.getvalue() == "", "nothing is printed while the spinner says it"


def test_a_function_call_says_what_it_waits_for_and_returns_its_result(output):
    function = function_on(
        [
            [
                ACCEPTED,
                says("queued"),
                says("provisioning", "backup_worker_starting"),
                says("starting"),
                FunctionInvokeResponse(task_id="task-1", output="hello from the function\n"),
                RESULT,
            ]
        ]
    )

    assert function() == 1998

    said = output.getvalue()
    assert "Preferred capacity is unavailable, starting a machine on backup capacity" in said
    assert said.index("Placed on a machine") < said.index("hello from the function")


def test_a_gateway_that_says_nothing_about_waiting_changes_nothing(output):
    hello = FunctionInvokeResponse(task_id="task-1", output="hello\n")
    function = function_on([[ACCEPTED, hello, RESULT]])

    assert function() == 1998
    assert "machine" not in output.getvalue()


# How long a call may wait


@pytest.mark.parametrize(
    "value,seconds",
    [("", 0), ("0", 0), ("90", 90), ("90s", 90), ("5m", 300), ("1h", 3600), (" 2M ", 120)],
)
def test_the_limit_is_read_from_the_environment(monkeypatch, value, seconds):
    monkeypatch.setenv(LIMIT, value)

    assert capacity.wait_limit() == seconds


@pytest.mark.parametrize("value", ["soon", "-5", "5 minutes", "nan", "m"])
def test_a_limit_that_cannot_be_read_is_an_error(monkeypatch, capsys, value):
    monkeypatch.setenv(LIMIT, value)
    monkeypatch.setattr(terminal, "json_output", lambda: True)

    with pytest.raises(SystemExit):
        capacity.wait_limit()

    payload = json.loads(capsys.readouterr().out)
    assert payload["code"] == "INVALID_CONFIG"
    assert LIMIT in payload["error"]


def test_a_wait_counts_from_when_the_gateway_does(clock, output):
    _, tell, stop = waiting(limit=120)

    # A client that joins late hears how long the container has waited.
    tell(says("queued", waited_seconds=30))
    clock.at += 89
    tell(says("provisioning", "worker_starting", waited_seconds=80))
    stop.assert_not_called()

    clock.at += 1
    with pytest.raises(NoCapacityError):
        tell(says("provisioning", "worker_starting", waited_seconds=81))
    stop.assert_called_once()


def test_a_call_that_a_machine_has_starts_over_if_it_waits_again(clock, output):
    _, tell, stop = waiting(limit=120)
    tell(COLD_START)
    clock.at += 100
    tell(says("starting"))
    clock.at += 100

    # Another attempt, after the machine was lost, waits from the start.
    tell(COLD_START)
    clock.at += 119
    tell(says("provisioning", "worker_starting", waited_seconds=119))
    stop.assert_not_called()

    clock.at += 1
    with pytest.raises(NoCapacityError):
        tell(says("provisioning", "worker_starting", waited_seconds=120))


def test_time_without_capacity_adds_up_and_is_spoken_of_once(clock, output):
    _, tell, _ = waiting()

    tell(says("waiting_for_capacity", "no_capacity"))
    clock.at += 40
    tell(says("waiting_for_capacity", "no_capacity", waited_seconds=40))

    # A machine that is tried for and does not come is not time without
    # capacity, however long it takes.
    tell(COLD_START)
    clock.at += 300
    tell(says("provisioning", "worker_starting", waited_seconds=300))

    tell(says("waiting_for_capacity", "no_capacity"))
    clock.at += 19
    tell(says("waiting_for_capacity", "no_capacity", waited_seconds=19))
    assert "Still no" not in output.getvalue()

    clock.at += 1
    tell(says("waiting_for_capacity", "no_capacity", waited_seconds=20))
    assert "Still no A10G capacity after 1:00." in output.getvalue()

    clock.at += 100
    tell(says("waiting_for_capacity", "no_capacity", waited_seconds=120))
    assert output.getvalue().count("Still no") == 1


# A function call


def function_on(gateway_says, gpu="A10G", **kwargs):
    """A function on a gateway that answers each invocation with the next list of responses."""
    function = Function(
        cpu=1, memory=128, gpu=gpu, image=Image(python_version="python3.8"), **kwargs
    )(lambda: 1998)
    parent = function.parent
    parent.syncer = MagicMock()
    parent.prepare_runtime = MagicMock(return_value=True)
    parent.stub_id = "stub-1"
    parent.stub_request = GetOrCreateStubRequest(gpu=gpu if isinstance(gpu, str) else ",".join(gpu))
    parent.gateway_stub = MagicMock()
    parent.gateway_stub.list_pool_offers.return_value = ListPoolOffersResponse(
        ok=True,
        offers=[
            PoolOffer(id="dear", gpu="A10G", provider="p", hourly_cost_micros=900_000),
            PoolOffer(id="cheap", gpu="A10G", provider="p", hourly_cost_micros=600_000),
        ],
    )
    parent.gateway_stub.list_tasks.return_value = ListTasksResponse(
        ok=True, tasks=[Task(id="task-1", status="PENDING")]
    )
    parent.function_stub = MagicMock()
    parent.function_stub.function_invoke.side_effect = [iter(answer) for answer in gateway_says]
    return function


def stopped(function):
    """The tasks the function asked the gateway to stop."""
    return [call.args[0] for call in function.parent.gateway_stub.stop_tasks.call_args_list]


def invoked_on(function):
    """The stub of each invocation the function made."""
    calls = function.parent.function_stub.function_invoke.call_args_list
    return [call.args[0].stub_id for call in calls]


def test_a_call_gives_up_when_it_has_waited_as_long_as_it_may(monkeypatch, output):
    monkeypatch.setenv(LIMIT, "2m")
    function = function_on([[ACCEPTED, NO_CAPACITY, RESULT]])

    with pytest.raises(NoCapacityError) as gave_up:
        function()

    error = gave_up.value
    assert error.message == (
        "No A10G capacity became available in 2 minutes. The call was cancelled."
    )
    assert error.code == 1, "a script that does not catch it exits with status 1"
    assert "`beta9 machine reserve --gpu A10G`" in error.hint
    assert "`beta9 machine list` shows what can be reserved." in error.hint
    assert f"{LIMIT} limits the wait to 2 minutes." in error.hint
    # A call that is given up on does not run later.
    assert stopped(function) == [StopTasksRequest(task_ids=["task-1"])]

    said = output.getvalue()
    assert "✗ No A10G capacity became available in 2 minutes. The call was cancelled." in said
    assert "hint: " in said


def test_giving_up_has_a_code_a_script_can_branch_on(monkeypatch, capsys):
    monkeypatch.setenv(LIMIT, "120")
    monkeypatch.setattr(terminal, "json_output", lambda: True)
    function = function_on([[ACCEPTED, NO_CAPACITY, RESULT]], gpu=["A10G", "T4"])

    with pytest.raises(NoCapacityError):
        function()

    lines = capsys.readouterr().out.splitlines()
    payload = json.loads("\n".join(lines[lines.index("{") :]))
    assert payload["code"] == "CAPACITY"
    assert payload["error"] == (
        "No A10G or T4 capacity became available in 2 minutes. The call was cancelled."
    )
    assert "machine list" in payload["hint"]


@pytest.mark.parametrize(
    "said,kwargs,message,hint",
    [
        (
            says("provisioning", "worker_starting", waited_seconds=400),
            {},
            "A machine for this call was still starting after 7 minutes.",
            "machine list",
        ),
        (
            says("queued", waited_seconds=125),
            {},
            "This call was not placed on a machine in 2 minutes.",
            "machine list",
        ),
        (
            says("waiting_for_capacity", "no_spare_capacity", waited_seconds=125),
            {"gpu": "", "cpu_tier": "spot"},
            "No capacity became available in 2 minutes.",
            'cpu_tier="shared" or "performance" does not wait for it.',
        ),
    ],
)
def test_giving_up_says_what_the_call_waited_for(monkeypatch, output, said, kwargs, message, hint):
    monkeypatch.setenv(LIMIT, "120")
    function = function_on([[ACCEPTED, said, RESULT]], **kwargs)

    with pytest.raises(NoCapacityError) as gave_up:
        function()

    assert gave_up.value.message == f"{message} The call was cancelled."
    assert hint in gave_up.value.hint


def test_a_call_within_its_limit_runs(monkeypatch, output):
    monkeypatch.setenv(LIMIT, "10m")
    function = function_on([[ACCEPTED, NO_CAPACITY, says("starting"), RESULT]])

    assert function() == 1998
    assert stopped(function) == []


def test_a_call_with_no_limit_keeps_waiting_and_says_once_what_can_be_done(monkeypatch, output):
    monkeypatch.delenv(LIMIT, raising=False)
    function = function_on(
        [
            [
                ACCEPTED,
                says("waiting_for_capacity", "no_capacity", waited_seconds=20),
                NO_CAPACITY,
                says("waiting_for_capacity", "no_capacity", waited_seconds=140),
                says("starting"),
                RESULT,
            ]
        ]
    )

    assert function() == 1998

    said = " ".join(line.strip() for line in output.getvalue().splitlines())
    assert said.count("Still no A10G capacity after 2:10.") == 1
    assert f"The call keeps waiting; {LIMIT}=<seconds> gives up sooner." in said
    assert "`beta9 machine reserve --gpu A10G`" in said
    assert stopped(function) == []
    # Nobody is asked where nobody can answer.
    function.parent.gateway_stub.list_pool_offers.assert_not_called()


def test_a_call_on_the_spot_tier_is_told_what_does_not_wait(monkeypatch, output):
    monkeypatch.delenv(LIMIT, raising=False)
    spot = says("waiting_for_capacity", "no_spare_capacity", waited_seconds=70)
    function = function_on([[ACCEPTED, spot, says("starting"), RESULT]], gpu="", cpu_tier="spot")

    assert function() == 1998

    said = " ".join(line.strip() for line in output.getvalue().splitlines())
    assert "The Spot tier has no spare capacity right now, waiting for some" in said
    assert "Still no capacity after 1:10." in said
    assert 'cpu_tier="shared" or "performance" does not wait for it.' in said


def test_a_batch_says_things_once_and_reports_each_call_given_up_on(monkeypatch, output):
    monkeypatch.delenv(LIMIT, raising=False)
    function = function_on([[ACCEPTED, NO_CAPACITY, says("starting"), RESULT]] * 3)

    assert list(function.map([1, 2, 3])) == [1998, 1998, 1998]
    said = output.getvalue()
    assert said.count("Some calls are waiting: no capacity available right now") == 1
    assert said.count("Still no A10G capacity") == 1
    assert "Placed on a machine" not in said

    monkeypatch.setenv(LIMIT, "2m")
    function = function_on([[ACCEPTED, NO_CAPACITY, RESULT]] * 3)

    assert list(function.map([1, 2, 3])) == [None, None, None]
    said = output.getvalue()
    for index in (1, 2, 3):
        assert f"Input {index} failed: No A10G capacity became available in 2 minutes." in said
    assert len(stopped(function)) == 3


# A caller at a terminal


@pytest.fixture
def at_a_terminal(monkeypatch):
    """A caller who can be asked, and who answers each question with the next answer."""
    answers = []
    asked = []

    def select(title, options, default_index=0):
        asked.append((title, [option.label for option in options]))
        answer = answers.pop(0)
        if callable(answer):
            return answer(options)
        return answer

    monkeypatch.delenv(LIMIT, raising=False)
    # A spinner that is on screen stands in for the terminal's output, so
    # nobody can be asked anything until it is taken off.
    monkeypatch.setattr(terminal, "is_interactive", lambda: terminal._current_status is None)
    monkeypatch.setattr(terminal, "select", select)
    monkeypatch.setattr(terminal, "confirm", lambda *_args, **_kwargs: True)
    return SimpleNamespace(answers=answers, asked=asked)


QUESTION = "How do you want to proceed?"


def test_a_caller_at_a_terminal_is_asked_once_and_can_keep_waiting(at_a_terminal, output):
    at_a_terminal.answers.append(capacity.WAIT)
    function = function_on([[ACCEPTED, NO_CAPACITY, NO_CAPACITY, says("starting"), RESULT]])

    assert function() == 1998

    assert at_a_terminal.asked == [(QUESTION, ["Keep waiting", "Reserve a machine", "Cancel"])]
    said = " ".join(line.strip() for line in output.getvalue().splitlines())
    assert "No A10G capacity has been available for 2:10." in said
    assert "This is a platform limit, not your code." in said
    assert stopped(function) == []


def test_a_caller_who_cancels_stops_the_call(at_a_terminal, output):
    at_a_terminal.answers.append(capacity.CANCEL)
    function = function_on([[ACCEPTED, NO_CAPACITY, RESULT]])

    with pytest.raises(SystemExit) as exit:
        function()

    assert exit.value.code == 1
    assert not isinstance(exit.value, NoCapacityError)
    assert stopped(function) == [StopTasksRequest(task_ids=["task-1"])]
    assert "Cancelled. The function did not run." in output.getvalue()


def test_a_caller_can_reserve_a_machine_and_the_call_runs_on_it(at_a_terminal, monkeypatch, output):
    at_a_terminal.answers.extend(
        [
            capacity.RESERVE,
            lambda offers: offers[0].value,  # the cheapest offer
            "2h",  # for how long
        ]
    )
    ready = MagicMock(return_value=True)
    monkeypatch.setattr(capacity, "wait_for_pool_ready", ready)
    function = function_on([[ACCEPTED, NO_CAPACITY, RESULT], [ACCEPTED, RESULT]])
    gateway = function.parent.gateway_stub
    gateway.get_or_create_stub.return_value = GetOrCreateStubResponse(ok=True, stub_id="stub-2")

    assert function() == 1998

    # The stub was created again, on the offer that was chosen.
    pool = gateway.get_or_create_stub.call_args.args[0].pool
    assert (pool.offer_id, pool.ttl, pool.pricing) == ("cheap", "2h", "")
    assert function.parent.pool_config is pool
    ready.assert_called_once_with(gateway, pool.name)
    # The call that waited was given up, and made again on the machine.
    assert stopped(function) == [StopTasksRequest(task_ids=["task-1"])]
    assert invoked_on(function) == ["stub-1", "stub-2"]
    # The machine is reserved before the call that waits is given up.
    order = [
        call[0] for call in gateway.method_calls if call[0] in ("get_or_create_stub", "stop_tasks")
    ]
    assert order == ["get_or_create_stub", "stop_tasks"]


def test_a_call_that_got_a_machine_while_its_caller_chose_is_left_to_run(at_a_terminal, output):
    at_a_terminal.answers.append(capacity.RESERVE)
    function = function_on([[ACCEPTED, NO_CAPACITY, says("starting"), RESULT]])
    gateway = function.parent.gateway_stub
    gateway.list_tasks.return_value = ListTasksResponse(
        ok=True, tasks=[Task(id="task-1", status="RUNNING")]
    )

    assert function() == 1998

    assert "A machine took the call while you were choosing." in output.getvalue()
    gateway.get_or_create_stub.assert_not_called()
    assert stopped(function) == []


def test_a_caller_who_reserves_nothing_keeps_waiting(at_a_terminal, output):
    at_a_terminal.answers.append(capacity.RESERVE)
    function = function_on([[ACCEPTED, NO_CAPACITY, says("starting"), RESULT]])
    gateway = function.parent.gateway_stub
    gateway.list_pool_offers.return_value = ListPoolOffersResponse(ok=True, offers=[])

    assert function() == 1998

    said = output.getvalue()
    assert "No on-demand offers currently available for A10G." in said
    assert "No machine was reserved. Still waiting for capacity." in said
    assert stopped(function) == []
    assert invoked_on(function) == ["stub-1"]


def test_a_machine_that_is_reserved_and_not_ready_ends_the_call(at_a_terminal, monkeypatch, output):
    at_a_terminal.answers.extend([capacity.RESERVE, lambda offers: offers[0].value, "1h"])
    monkeypatch.setattr(capacity, "wait_for_pool_ready", lambda *_args: False)
    function = function_on([[ACCEPTED, NO_CAPACITY, RESULT]])
    gateway = function.parent.gateway_stub
    gateway.get_or_create_stub.return_value = GetOrCreateStubResponse(ok=True, stub_id="stub-2")

    with pytest.raises(SystemExit) as exit:
        function()

    assert exit.value.code == 1
    # The call does not run on other capacity once a machine is paid for.
    assert stopped(function) == [StopTasksRequest(task_ids=["task-1"])]
    assert invoked_on(function) == ["stub-1"]


@pytest.mark.parametrize(
    "said,kwargs,warning",
    [
        (
            says("waiting_for_capacity", "no_spare_capacity", waited_seconds=70),
            {"gpu": "", "cpu_tier": "spot"},
            'cpu_tier="shared" or "performance" does not wait for it.',
        ),
        (
            says("waiting_for_capacity", "no_capacity", waited_seconds=70),
            {"gpu": ""},
            "No capacity has been available for 1:10.",
        ),
        (
            says("waiting_for_capacity", "no_capacity", waited_seconds=70),
            {"gpu": "A10G", "pool": "my-pool"},
            "No A10G capacity has been available for 1:10.",
        ),
    ],
)
def test_a_machine_is_offered_only_where_one_would_help(
    at_a_terminal, output, said, kwargs, warning
):
    at_a_terminal.answers.append(capacity.WAIT)
    function = function_on([[ACCEPTED, said, says("starting"), RESULT]], **kwargs)

    assert function() == 1998

    assert at_a_terminal.asked == [(QUESTION, ["Keep waiting", "Cancel"])]
    assert warning in " ".join(line.strip() for line in output.getvalue().splitlines())


@pytest.mark.parametrize("batch", [True, False])
def test_a_batch_and_a_function_in_the_background_ask_nobody(at_a_terminal, output, batch):
    answer = [ACCEPTED, NO_CAPACITY, says("starting"), RESULT]
    if batch:
        function = function_on([answer] * 2)
        assert list(function.map([1, 2])) == [1998, 1998]
    else:
        function = function_on([answer], headless=True)
        assert function() == 1998

    assert at_a_terminal.asked == []
    assert output.getvalue().count("Still no A10G capacity") == 1


def test_a_paused_spinner_is_back_as_it_was():
    with terminal.redirect_terminal_to_buffer(io.StringIO()):
        with terminal.progress("Running transcribe") as running:
            with terminal.progress_paused():
                assert not terminal.spinner_visible()
                # What runs meanwhile has a spinner of its own.
                with terminal.progress("Finding available hardware...") as finding:
                    assert finding is not running
            with terminal.progress("still the first") as again:
                assert again is running


# A call whose container the scheduler gives up on ends by saying why


def invocation_that_ends(code, message, trailer=None):
    """Invoke a function on a gateway that accepts it, says it waits, and ends the stream."""
    attempts = []

    def invoke(request, context):
        attempts.append(dict(context.invocation_metadata()).get("x-beta9-task-id"))
        yield FunctionInvokeResponse(task_id="task-123", container_id="function-1")
        yield says("waiting_for_capacity", "no_capacity", waited_seconds=3)
        if trailer:
            context.set_trailing_metadata(((SCHEDULING_FAILURE_TRAILER, trailer),))
        context.abort(code, message)

    server = grpc.server(ThreadPoolExecutor(max_workers=2))
    server.add_generic_rpc_handlers(
        (
            grpc.method_handlers_generic_handler(
                "function.FunctionService",
                {
                    "FunctionInvoke": grpc.unary_stream_rpc_method_handler(
                        invoke,
                        request_deserializer=FunctionInvokeRequest().parse,
                        response_serializer=bytes,
                    )
                },
            ),
        )
    )
    port = server.add_insecure_port("127.0.0.1:0")
    server.start()
    channel = Channel(f"127.0.0.1:{port}", retry=(lambda _: None, False))
    responses = []
    try:
        with pytest.raises(grpc.RpcError) as raised:
            for response in _Invocation(
                FunctionServiceStub(channel), FunctionInvokeRequest(stub_id="stub")
            ):
                responses.append(response)
    finally:
        channel.close()
        server.stop(0).wait()
    return raised.value, responses, attempts


NO_A10G = "No A10G capacity became available in 20 minutes."


def reported(monkeypatch, capsys, error, json_mode):
    monkeypatch.setattr(terminal, "json_output", lambda: json_mode)
    with pytest.raises(SystemExit) as exit:
        handle_grpc_error(error)
    assert exit.value.code == 1
    return exit.value, capsys.readouterr()


def test_a_call_the_scheduler_gave_up_on_says_why_and_is_not_tried_again(monkeypatch, capsys):
    error, responses, attempts = invocation_that_ends(
        grpc.StatusCode.RESOURCE_EXHAUSTED, NO_A10G, "worker_capacity_timeout"
    )

    assert error.details() == NO_A10G
    assert scheduling_failure(error) == "worker_capacity_timeout"
    # It was told what it waited for, in the gateway's words, and the
    # gateway was asked once.
    assert [r.pending_phase for r in responses] == ["", "waiting_for_capacity"]
    assert responses[1].pending_message == "No capacity available right now, waiting for some"
    assert attempts == [""]

    raised, printed = reported(monkeypatch, capsys, error, json_mode=False)
    assert isinstance(raised, NoCapacityError), "a script can catch it"
    lines = printed.err.splitlines()
    assert lines[0] == f"✗ {NO_A10G}"
    assert "Resource limit exceeded" not in printed.err
    hint = " ".join(line.strip() for line in lines[1:])
    assert hint.startswith("hint: Try again in a few minutes.")
    assert "machine list" in hint

    _, printed = reported(monkeypatch, capsys, error, json_mode=True)
    payload = json.loads(printed.out)
    assert (payload["error"], payload["code"]) == (NO_A10G, "CAPACITY")
    assert "gpu=[" in payload["hint"]


def test_other_ends_are_reported_as_what_they_are(monkeypatch, capsys):
    message = 'The selected compute pool "gone" is unavailable or has no active controller.'
    error, _, _ = invocation_that_ends(grpc.StatusCode.UNKNOWN, message, "no_controller")
    _, printed = reported(monkeypatch, capsys, error, json_mode=True)
    assert json.loads(printed.out) == {"error": message, "code": "NOT_SCHEDULED"}

    # A limit that is not the scheduler's is reported as before.
    error, _, _ = invocation_that_ends(grpc.StatusCode.RESOURCE_EXHAUSTED, "too many tunnels")
    assert scheduling_failure(error) == ""
    _, printed = reported(monkeypatch, capsys, error, json_mode=True)
    assert json.loads(printed.out) == {
        "error": "Resource limit exceeded: too many tunnels",
        "code": "CAPACITY",
    }
