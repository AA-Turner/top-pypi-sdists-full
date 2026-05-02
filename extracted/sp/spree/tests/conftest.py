import os
import pytest
import responses
from spree import Spree


@pytest.fixture
def fp():
    def wrapper(rel_path):
        "return the full path of given rel_path"
        return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                rel_path
            )
        )
    return wrapper


@pytest.fixture
def spree():
    return Spree('http://mystore/api', 'some-key')


@pytest.yield_fixture
def resp(fp):
    rsps = responses.RequestsMock(False)
    rsps.start()

    "Products"
    rsps.add(
        responses.GET,
        'http://mystore/api/products',
        body=open(fp('responses/products.json'), 'r').read()
    )
    rsps.add(
        responses.GET,
        'http://mystore/api/products/2',
        body=open(fp('responses/product-2.json'), 'r').read()
    )

    "Orders"
    rsps.add(
        responses.GET,
        'http://mystore/api/orders',
        body=open(fp('responses/orders.json'), 'r').read()
    )
    rsps.add(
        responses.GET,
        'http://mystore/api/orders/R123456789',
        body=open(fp('responses/order-R123456789.json'), 'r').read()
    )

    "StockItems"
    rsps.add(
        responses.GET,
        'http://mystore/api/stock_locations/1/stock_items',
        body=open(fp('responses/stock_items.json'), 'r').read()
    )
    rsps.add(
        responses.GET,
        'http://mystore/api/stock_locations/1/stock_items/4',
        body=open(fp('responses/stock_item-4.json'), 'r').read()
    )

    "Variants"
    rsps.add(
        responses.GET,
        'http://mystore/api/products/ruby-on-rails-jr-spaghetti/variants',
        body=open(fp('responses/variant-ROR-00013.json'), 'r').read()
    )
    rsps.add(
        responses.GET,
        'http://mystore/api/variants',
        body=open(fp('responses/variant-ROR-00013.json'), 'r').read()
    )

    "Stock Locations"
    rsps.add(
        responses.GET,
        'http://mystore/api/stock_locations',
        body=open(fp('responses/stock_locations.json'), 'r').read()
    )
    rsps.add(
        responses.GET,
        'http://mystore/api/stock_locations/1',
        body=open(fp('responses/stock_location-1.json'), 'r').read()
    )

    yield rsps

    rsps.stop()
    rsps.reset()
