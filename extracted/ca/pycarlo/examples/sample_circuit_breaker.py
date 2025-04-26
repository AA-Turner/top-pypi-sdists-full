from pycarlo.core import Client, Session
from pycarlo.features.circuit_breakers import CircuitBreakerService

# Example from our test.snowflake account.
endpoint = "https://api.dev.getmontecarlo.com/graphql"

service = CircuitBreakerService(
    mc_client=Client(Session(mcd_profile="test-snow", endpoint=endpoint)), print_func=print
)
in_breach = service.trigger_and_poll(rule_uuid="87872875-fe80-4963-8ab0-c04397a6daae")
print("That can't be good. Our warehouse is broken." if in_breach else "Go, go, go!.")
