import ogmios

"""
This example shows how to use the ogmios-python library to asynchronously execute
multiple queries. This is useful for applications that need to query the chain
frequently.
"""

batch_size = 100


def async_queries():
    with ogmios.Client() as client:
        for i in range(batch_size):
            client.query_block_height.send(id=i)

        results = []
        for i in range(batch_size):
            results.append(client.query_block_height.receive())

        results.sort(key=lambda tup: tup[1])
        for height, id in results:
            print(f"Block height: {height} (ID: {id})")


if __name__ == "__main__":
    async_queries()
