"""
Simple fibonacci tracing example. To run, first fill-in account_id and api key.

Using low-level Trace and Span objects.
"""

import time

import scale_gp_beta.lib.tracing as tracing
from scale_gp_beta import SGPClient


def fibonacci(curr: int) -> int:
    with tracing.create_span("fibonacci", input={"curr": curr}) as span:
        time.sleep(0.1)
        if curr < 2:
            span.output = {"res": curr}
            return curr

        res = fibonacci(curr - 1) + fibonacci(curr - 2)
        span.output = {"res": res}
    return res


def main() -> None:
    # create traces and spans with create_trace and create_span
    # can act directly or use context managers
    with tracing.create_trace("my_trace"):
        span = tracing.create_span("main", input={}, metadata={"env": "local"})
        span.start()

        fib = fibonacci(5)

        span.output = {"result": fib}
        span.end()


if __name__ == "__main__":
    api_key = "XXX"
    account_id = "XXX"

    # Initialise with a working client, can omit if two appropriate ENV VARs are set
    tracing.init(SGPClient(api_key=api_key, account_id=account_id), disabled=False)
    main()
