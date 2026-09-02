import pytest

from pathlib import Path
from dataclasses import asdict

from eumdac.tailor_models import Chain
from eumdac.order import (
    Order,
    new_order_filename,
    resolve_order,
    get_default_order_dir,
)

from tests.base import FakeProduct, FakeCollection, FakeCustomisation, FakeTailor

order_test_path = Path("test_order.yml")

fake_chain = Chain()
fake_chain.id = "id"
fake_chain.description = "description"


@pytest.fixture
def products():
    return [FakeProduct()]


@pytest.fixture
def tailor_order(tmp_path, products):
    order = Order(order_file=tmp_path / "test_tailor_order.yml")
    order.initialize(
        fake_chain,
        products=products,
        output_dir=tmp_path / "output",
        file_pattern=None,
        query=None,
    )
    yield order

    order.delete()


@pytest.fixture
def download_order(tmp_path, products):
    order = Order(order_file=tmp_path / "test_download_order.yml")
    order.initialize(
        None, products=products, output_dir=tmp_path / "output", file_pattern=None, query=None
    )
    yield order

    order.delete()


def test_order_status(tailor_order, products):
    assert tailor_order.status() == "NOT COMPLETED"

    for p in products:
        tailor_order.update(None, p._id, "FAILED", None)
    assert tailor_order.status() == "FAILED"

    for p in products:
        tailor_order.update(None, p._id, "DONE", None)
    assert tailor_order.status() == "NOT COMPLETED"

    for p in products:
        tailor_order.update(None, p._id, "DONE", {"fn": "DOWNLOADED"})
    assert tailor_order.status() == "DONE"


def test_order_collections(tailor_order, products):
    for p in products:
        assert p.collection._id in tailor_order.collections()


def test_order_pretty(tailor_order, download_order):
    for order in [tailor_order, download_order]:
        ps = order.pretty_string(True)
        assert str(order) in ps
        assert order.status() in ps
        assert str(order.collections()) in ps


def test_order_deserialization(tailor_order):
    with tailor_order.dict_from_file() as order_dict:
        assert isinstance(order_dict, dict)
        assert "output_dir" in order_dict
        assert "chain" in order_dict
        assert "products_to_process" in order_dict
        for ptp in order_dict["products_to_process"].values():
            assert ptp["col_id"] is not None
            assert ptp["server_state"] == "UNSUBMITTED"
            assert ptp["customisation"] is None


def test_order_update(tmp_path):
    p = tmp_path / order_test_path

    collection_id = "test_col_id"
    product_id = "test_prod_id"
    status = "test_status"
    download_states = {"test": "test_download_state"}
    query = {"test": "test_query_parameter"}
    products = [FakeProduct(id=product_id, collection=FakeCollection(id=collection_id))]
    order = Order(order_file=p)
    order.initialize(
        fake_chain,
        products=products,
        output_dir=tmp_path / "output",
        file_pattern=None,
        query=query,
    )
    order.update(collection_id, product_id, status, download_states)

    with order.dict_from_file() as order_dict:
        assert isinstance(order_dict, dict)
        assert order_dict["query"] == query
        for ptp in order_dict["products_to_process"].values():
            assert ptp["server_state"] == status
            assert ptp["download_states"] == download_states

    if p.exists():
        p.unlink()


def test_order_remote_delete_failed(tailor_order, products):
    with tailor_order.dict_from_file() as order_dict:
        for ptp in order_dict["products_to_process"].values():
            ptp["server_state"] = "FAILED"
    tailor_order._locked_serialize(order_dict)

    for p in products:
        tailor_order.update("test_customisation", p._id, "FAILED", {"fn": "DOWNLOADED"})

    tailor_order.remote_delete_failed(FakeTailor())


def test_order_resolve_product_num(tailor_order, products):
    cnt = 1
    for p in products:
        total_products, num = tailor_order.resolve_product_num(product_id=p._id)
        assert total_products >= num
        assert num == cnt
        cnt += 1

    with pytest.raises(KeyError):
        _, __ = tailor_order.resolve_product_num(product_id="INVALID")


def test_order_filehandling(tmp_path):
    order_dir = tmp_path / "orders"
    order_dir.mkdir()
    order_filename1 = new_order_filename(order_dir)
    assert order_filename1.exists()

    order = Order(order_filename1)
    collection_id = "test_col_id"
    product_id = "test_prod_id"
    products = [FakeProduct(id=product_id, collection=FakeCollection(id=collection_id))]
    order.initialize(
        fake_chain,
        products=products,
        output_dir=tmp_path / "output",
        file_pattern=None,
        query=None,
    )

    assert order_filename1.exists()

    order_filename2 = new_order_filename(order_dir)
    assert order_filename2.exists()
    assert order_filename2 != order_filename1

    order = Order(order_filename2)
    collection_id = "test_col_id"
    product_id = "test_prod_id"
    products = [FakeProduct(id=product_id, collection=FakeCollection(id=collection_id))]
    order.initialize(
        fake_chain,
        products=products,
        output_dir=tmp_path / "output",
        file_pattern=None,
        query=None,
    )

    assert order_filename2.exists()

    o = resolve_order(order_dir, "latest")
    assert o._order_file == order._order_file
