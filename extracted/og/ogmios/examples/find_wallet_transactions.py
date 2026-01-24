import ogmios

"""
This example prints all transactions involving a specific wallet address.
"""

target_addr = "addr_test1vzpwq95z3xyum8vqndgdd9mdnmafh3djcxnc6jemlgdmswcve6tkw"
batch_size = 1000


def print_first_shelley_blocks():
    with ogmios.Client() as client:
        # Set chain pointer to origin
        point, _, _ = client.find_intersection.execute([ogmios.Origin()])

        txs_found = 0
        while True:
            # Batch requests to improve performance
            for i in range(batch_size):
                client.next_block.send()

            for i in range(batch_size):
                direction, tip, block, id = client.next_block.receive()
                if direction.value == "forward":
                    # Find transactions involving the target address
                    if isinstance(block, ogmios.Block) and hasattr(block, "transactions"):
                        for tx in block.transactions:
                            if tx.get("outputs"):
                                for output in tx["outputs"]:
                                    if output["address"] == target_addr:
                                        txs_found += 1
                                        print(f"Transaction #{txs_found}: {tx.get('id')}")
                                        break

                    # Stop when we've reached the network tip
                    if tip.height == block.height:
                        print(f"Reached chain tip at slot {tip.slot}")
                        return


if __name__ == "__main__":
    print_first_shelley_blocks()
