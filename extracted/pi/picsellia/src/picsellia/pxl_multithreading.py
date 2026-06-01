import logging
import os
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import tqdm

from picsellia.utils import chunk_list

logger = logging.getLogger("picsellia")


def do_chunk_called_function(
    items: list[Any], f: Callable, chunk_size: int = 100
) -> list:
    if len(items) < chunk_size:
        return [f(items)]

    results = []
    with tqdm.tqdm(
        total=len(items), initial=0, ncols=100, colour="red", ascii=False
    ) as pbar:
        for item_chunked, _packet in chunk_list(items, chunk_size):
            results.append(f(item_chunked))
            pbar.update(len(item_chunked))
    return results


def do_mlt_function(
    items: list[Any],
    f: Callable,
    h: Callable = lambda _: _,
    max_workers: int | None = None,
) -> dict:
    if max_workers is None or max_workers <= 0:
        max_workers = os.cpu_count() + 4

    with tqdm.tqdm(total=len(items), ncols=100, colour="green", ascii=False) as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(f, item): h(item) for item in items}
            results = {}
            for future in as_completed(futures):
                arg = futures[future]
                try:
                    results[arg] = future.result()
                except Exception as e:
                    logger.error(
                        f"Something went wrong while executing an asynchronous task for item {arg}. Error: {e}"
                    )
                    results[arg] = None
                pbar.update(1)
    return results


PAGINATION_LIMIT = 1000


def do_paginate(
    limit: int | None, offset: int | None, page_size: int | None, f: Callable
):
    if page_size is None or page_size <= 0 or page_size > PAGINATION_LIMIT:
        page_size = PAGINATION_LIMIT
    else:
        page_size = page_size

    if limit is None or limit < 0:
        limit = None
        first_limit = page_size
    else:
        first_limit = min(page_size, limit)

    if offset is None or offset < 0:
        first_offset = 0
    else:
        first_offset = offset

    items, total = f(first_limit, first_offset)

    if len(items) == 0:
        return items

    total_count = limit if limit is not None else total
    k = 1
    if _shall_continue(k, page_size, total, limit, len(items)):
        with tqdm.tqdm(
            total=total_count, initial=len(items), ncols=100, colour="blue", ascii=False
        ) as pbar:
            while _shall_continue(k, page_size, total, limit, len(items)):
                k_limit = (
                    page_size if limit is None else min(page_size, limit - len(items))
                )
                k_offset = first_offset + k * page_size
                k_items, _ = f(k_limit, k_offset)
                items += k_items
                k += 1
                pbar.update(len(k_items))

    return items


def _shall_continue(
    k: int, page_size: int, total: int, limit: int, computed: int
) -> bool:
    return k * page_size < total and (limit is None or computed < limit)
