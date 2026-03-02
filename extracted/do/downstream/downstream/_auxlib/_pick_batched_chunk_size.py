from ._is_in_unit_test import is_in_unit_test


def pick_batched_chunk_size() -> int:
    """Implementation detail for chunk-wise batched parallelism."""
    # use smaller chunk size for tests to ensure multiple chunk scenario tested
    return [262144, 4][bool(is_in_unit_test())]
