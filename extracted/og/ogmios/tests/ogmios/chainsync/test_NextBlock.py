import pytest

from ogmios.datatypes import Origin, Direction, Era

from tests.ogmios.test_fixtures import (
    client,
    last_byron_block_point,
    last_shelley_block_point,
    last_allegra_block_point,
    last_mary_block_point,
    last_alonzo_block_point,
    era,
)

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_NextBlock_origin(client):
    intersection, _, _ = client.find_intersection.execute([Origin()])
    assert isinstance(intersection, Origin)

    my_id = "12345"
    direction, tip, block, id = client.next_block.execute(my_id)
    assert direction == Direction.backward
    assert block == Origin()
    assert id == my_id
    assert tip.height > 0
    assert tip.slot > 0

    direction, _, block, _ = client.next_block.execute()
    assert direction == Direction.forward
    assert block.height == 0
    assert block.era == "byron"

    direction, _, block, _ = client.next_block.execute()
    assert direction == Direction.forward
    assert block.height == 1
    assert block.era == "byron"


def test_NextBlock_byronEra(client):
    intersection, _, _ = client.find_intersection.execute([Origin()])
    assert isinstance(intersection, Origin)

    for i in range(10):
        direction, tip, block, _ = client.next_block.execute()
        if direction.value == "forward":
            assert block.era == Era.byron.value


def test_NextBlock_shelleyEra(client, era, last_byron_block_point):
    if Era.get_index(era) < Era.get_index(Era.shelley):
        pytest.skip("Test only valid for shelley era")

    intersection, _, _ = client.find_intersection.execute([last_byron_block_point, Origin()])

    for _ in range(10):
        direction, tip, block, _ = client.next_block.execute()
        if direction.value == "forward":
            print(f"Slot: {block.slot}, Hash: {block.id}, Era: {block.era}")
            assert block.era == Era.shelley.value


def test_NextBlock_allegraEra(client, era, last_shelley_block_point):
    if Era.get_index(era) < Era.get_index(Era.allegra):
        pytest.skip("Test only valid for allegra era")

    intersection, _, _ = client.find_intersection.execute([last_shelley_block_point, Origin()])

    for _ in range(10):
        direction, tip, block, _ = client.next_block.execute()
        if direction.value == "forward":
            print(f"Slot: {block.slot}, Hash: {block.id}, Era: {block.era}")
            assert block.era == Era.allegra.value


def test_NextBlock_maryEra(client, era, last_allegra_block_point):
    if Era.get_index(era) < Era.get_index(Era.mary):
        pytest.skip("Test only valid for mary era")

    intersection, _, _ = client.find_intersection.execute([last_allegra_block_point, Origin()])

    for _ in range(10):
        direction, tip, block, _ = client.next_block.execute()
        if direction.value == "forward":
            print(f"Slot: {block.slot}, Hash: {block.id}, Era: {block.era}")
            assert block.era == Era.mary.value


def test_NextBlock_alonzoEra(client, era, last_mary_block_point):
    if Era.get_index(era) < Era.get_index(Era.alonzo):
        pytest.skip("Test only valid for alonzo era")

    intersection, _, _ = client.find_intersection.execute([last_mary_block_point, Origin()])

    for _ in range(10):
        direction, tip, block, _ = client.next_block.execute()
        if direction.value == "forward":
            print(f"Slot: {block.slot}, Hash: {block.id}, Era: {block.era}")
            assert block.era == Era.alonzo.value


def test_NextBlock_babbageEra(client, era, last_alonzo_block_point):
    if Era.get_index(era) < Era.get_index(Era.babbage):
        pytest.skip("Test only valid for babbage era")

    intersection, _, _ = client.find_intersection.execute([last_alonzo_block_point, Origin()])

    for _ in range(10):
        direction, tip, block, _ = client.next_block.execute()
        if direction.value == "forward":
            print(f"Slot: {block.slot}, Hash: {block.id}, Era: {block.era}")
            assert block.era == Era.babbage.value
