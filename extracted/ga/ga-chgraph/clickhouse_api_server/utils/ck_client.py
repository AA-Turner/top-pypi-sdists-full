from contextlib import contextmanager
from clickhouse_driver import Client


def get_client(clickhouse_connect):
    if "user" in clickhouse_connect and "password" in clickhouse_connect:
        graph_client = Client(host=clickhouse_connect["ip"], port=clickhouse_connect["port"], user=clickhouse_connect["user"],
                              password=clickhouse_connect["password"])
    else:
        graph_client = Client(host=clickhouse_connect["ip"], port=clickhouse_connect["port"])
    graph_client.execute(" set max_query_size=100000000 ")
    return graph_client


@contextmanager
def get_client_new(clickhouse_connect):
    graph_client = None
    try:
        if "user" in clickhouse_connect and "password" in clickhouse_connect:
            graph_client = Client(host=clickhouse_connect.get("ip"), port=clickhouse_connect.get("port"),
                                  user=clickhouse_connect.get("user"),
                                  password=clickhouse_connect.get("password"))
        else:
            graph_client = Client(host=clickhouse_connect["ip"], port=clickhouse_connect["port"])
        graph_client.execute(" set max_query_size=100000000 ")
        yield graph_client
    except Exception as e:
        print("get clickhouse client error: {}".format(str(e)))
    finally:
        if graph_client:
            graph_client.disconnect()