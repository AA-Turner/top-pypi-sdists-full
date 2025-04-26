import json
from typing import Optional, cast

from vars import ensure_endpoint_env_var, ensure_token_env_vars

from pycarlo.common.settings import (
    HEADER_MCD_TELEMETRY_REASON,
    HEADER_MCD_TELEMETRY_SERVICE,
    RequestReason,
)
from pycarlo.core import Client, Mutation, Query, Session

CONFIRMATION_ICON = "✔️"
CONFIRMATION_SEPARATOR = "="


def test_with_query(client: Client):
    query = Query()
    query.get_user.__fields__("email")
    query.get_user.account.connections.__fields__("uuid")
    print(
        client(
            query,
            additional_headers={
                HEADER_MCD_TELEMETRY_REASON: RequestReason.SERVICE.value,
                HEADER_MCD_TELEMETRY_SERVICE: "sanity_check",
            },
        ).get_user.email
    )


def test_with_mutation(client: Client):
    mutation = Mutation()
    mutation.create_or_update_user_settings(
        key="test",
        description="test description",
        value=json.dumps({"value": "test value"}),
    )
    result = client(
        mutation,
        additional_headers={
            HEADER_MCD_TELEMETRY_REASON: RequestReason.SERVICE.value,
            HEADER_MCD_TELEMETRY_SERVICE: "sanity_check",
        },
    ).create_or_update_user_settings
    print(result.user_settings.key)


def test_with_string(client: Client):
    get_table_query = """
    query getTables{
      getTables(first: 10) {
        edges {
          node {
            fullTableId
          }
        }
      }
    }
    """
    response = cast(
        Query,
        client(
            get_table_query,
            additional_headers={
                HEADER_MCD_TELEMETRY_REASON: RequestReason.SERVICE.value,
                HEADER_MCD_TELEMETRY_SERVICE: "sanity_check",
            },
        ),
    )
    for edge in response.get_tables.edges:
        print(edge.node.full_table_id)  # type: ignore
    print(response["get_tables"]["edges"][0]["node"]["full_table_id"])


def print_confirmation(text: str):
    separator = CONFIRMATION_SEPARATOR * (len(text) + 2)
    print()
    print(separator)
    print(text, CONFIRMATION_ICON)
    print(separator)
    print()


def sanity_check(
    mcd_url: Optional[str] = None,
    mcd_id: Optional[str] = None,
    mcd_token: Optional[str] = None,
):
    session = Session(
        endpoint=mcd_url,  # type: ignore
        mcd_id=mcd_id,
        mcd_token=mcd_token,
    )
    client = Client(session=session)

    test_with_query(client=client)
    print_confirmation("running queries with Query object")

    test_with_mutation(client=client)
    print_confirmation("running queries with Mutation object")

    test_with_string(client=client)
    print_confirmation("running queries with string")


if __name__ == "__main__":
    api_id, api_token = ensure_token_env_vars()
    api_url = ensure_endpoint_env_var()
    sanity_check(mcd_url=api_url, mcd_id=api_id, mcd_token=api_token)
