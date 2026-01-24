import time
import ogmios

"""
This example shows how to use the ogmios-python library to view new blocks as they are added to the
blockchain.
"""


def live_block_viewer():
    with ogmios.Client() as client:
        # Set chain pointer to origin
        point, tip, id = client.find_intersection.execute([ogmios.Origin()])

        # Now set chain pointer to tip
        _, _, _ = client.find_intersection.execute([tip.to_point()])

        # Tail blockchain as new blocks come in beyond the current tip
        while True:
            direction, tip, point, _ = client.next_block.execute()
            if direction == ogmios.Direction.forward:
                print(f"New block: {point}")
            time.sleep(1)


if __name__ == "__main__":
    live_block_viewer()
