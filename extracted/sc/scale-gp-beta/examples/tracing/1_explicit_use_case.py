"""
Simple mock database query.

Explicit control example - no explicit traces just manually passing a trace_id.
"""
import time
import uuid
import random
from typing import Any, Dict

import scale_gp_beta.lib.tracing as tracing
from scale_gp_beta import SGPClient


class MockDatabase:
    """A mock database class to simulate queries."""
    def __init__(self) -> None:
        self._data = {
            "SELECT * FROM users WHERE id = 1;": {"id": 1, "name": "Alice"},
            "SELECT * FROM users WHERE id = 2;": {"id": 2, "name": "Bob"},
        }

    def execute_query(self, query: str, trace_id: str) -> Dict[str, Any]:
        with tracing.create_span("db_query", input={"query": query}, trace_id=trace_id) as span:
            # simulate delay
            time.sleep(random.uniform(0.1, 0.3))

            result = self._data.get(query, {})
            span.output = {"result": result}
            return result

def get_user_from_db(db: MockDatabase, user_id: int, trace_id: str) -> Dict[str, Any]:
    with tracing.create_span("get_user_from_db", input={"user_id": user_id}, trace_id=trace_id):
        query = f"SELECT * FROM users WHERE id = {user_id};"

        return db.execute_query(query, trace_id)

def main() -> None:
    db = MockDatabase()
    trace_id = str(uuid.uuid4())
    with tracing.create_span("main", metadata={"env": "local"}, trace_id=trace_id):
        user = get_user_from_db(db, 1, trace_id)
        print(f"Retrieved user: {user.get('name')}")

if __name__ == "__main__":
    api_key = "xxx"
    account_id = "xxx"
    tracing.init(SGPClient(api_key=api_key, account_id=account_id), disabled=False)
    main()
