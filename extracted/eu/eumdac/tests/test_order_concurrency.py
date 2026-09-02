from pathlib import Path
from eumdac.order import (
    Order,
)
import concurrent.futures

from tests.base import FakeProduct, FakeCollection


def update_order(order, cid, pid, status, download_state):
    if download_state:
        download_states = {pid: download_state}
    else:
        download_states = None
    order.update(
        customisation_id=cid, product_id=pid, status=status, download_states=download_states
    )


def test_order_concurrency(tmp_path):
    products = []
    for i in range(0, 2):
        products.append(FakeProduct(id=str(i), collection=FakeCollection(str(i))))

    for repetitions in range(0, 100):
        o = Order(tmp_path / str(repetitions))
        o.initialize(
            chain=None, products=products, output_dir=Path("."), file_pattern=None, query=None
        )

        for p in products:
            o.update(
                customisation_id=p.collection._id,
                product_id=p._id,
                status="INIT",
                download_states={p._id: "INIT"},
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            f_res1 = [
                executor.submit(update_order, o, p.collection._id, p._id, "MOD", None)
                for p in products
            ]
            concurrent.futures.wait(
                f_res1, timeout=None, return_when=concurrent.futures.ALL_COMPLETED
            )
            f_res2 = [
                executor.submit(update_order, o, p.collection._id, p._id, None, "MOD")
                for p in products
            ]
            concurrent.futures.wait(
                f_res2, timeout=None, return_when=concurrent.futures.ALL_COMPLETED
            )

        with o.dict_from_file() as order_d:
            for product_id in order_d["products_to_process"].keys():
                ss = order_d["products_to_process"][product_id]["server_state"]

                if "download_states" in order_d["products_to_process"][product_id]:
                    download_states = order_d["products_to_process"][product_id]["download_states"]
                    dl_complete = [
                        True if ds == "MOD" else False for ds in download_states.values()
                    ]
                    assert all(dl_complete)
                    assert ss == "MOD"
