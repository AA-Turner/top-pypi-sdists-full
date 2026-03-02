from downstream._auxlib._pick_batched_chunk_size import pick_batched_chunk_size


def test_pick_batched_chunk_size():
    assert pick_batched_chunk_size() > 0
