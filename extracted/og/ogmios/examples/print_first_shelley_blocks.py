import ogmios

"""
This example prints the first 14 blocks of the Shelley era.

Set NETWORK to 'mainnet' or 'preprod' depending on the network Ogmios is connected to.
"""

NETWORK = "preprod"

if NETWORK == "mainnet":
    last_byron_block = ogmios.Point(
        slot=4492799, id="f8084c61b6a238acec985b59310b6ecec49c0ab8352249afd7268da5cff2a457"
    )
elif NETWORK == "preprod":
    last_byron_block = ogmios.Point(
        slot=84242, id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
    )
else:
    print("Invalid network. Please set NETWORK to 'mainnet' or 'preprod'.")
    exit(1)


def print_first_shelley_blocks():
    with ogmios.Client() as client:
        # Set chain pointer to origin
        try:
            point, tip, id = client.find_intersection.execute([last_byron_block])
        except ogmios.ResponseError:
            print("Intersection not found. Make sure you're connected to the proper network.")
            return

        blocks_printed = 0
        while True:
            direction, tip, point, id = client.next_block.execute()
            if direction.value == "forward":
                blocks_printed += 1
                print(f"Shelley block #{blocks_printed}: {point}")
                if blocks_printed >= 14:
                    break


if __name__ == "__main__":
    print_first_shelley_blocks()
