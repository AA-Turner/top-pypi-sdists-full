#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_spree
----------------------------------

Tests for `spree` module.
"""

import pytest 	# noqa


def test_products_all(resp, spree):
    "test fetching all products"
    products = spree.product.find()
    assert products.count == 16
    test_product = products[1]
    assert test_product['name'] == 'Ruby on Rails Bag'
    assert test_product['master']['sku'] == 'ROR-00012'
    assert test_product['description'] == 'Et illo et' \
        ' voluptatum corporis. Fugiat atque optio voluptates' \
        ' placeat ut odio. Iusto totam molestiae tenetur eaque' \
        ' molestias. Occaecati sunt sit magni voluptatibus qui ipsum.'
    assert test_product['price'] == '22.99'
    assert test_product['display_price'] == '$22.99'
    assert test_product['available_on'] == '2016-06-27T11:10:17.000Z'
    assert test_product['slug'] == 'ruby-on-rails-bag'
    assert test_product['shipping_category_id'] == 1


def test_finding_one_product(resp, spree):
    "test fetching product with respect to id"
    test_product = spree.product.get(2)
    assert test_product['name'] == 'Ruby on Rails Bag'
    assert test_product['master']['sku'] == 'ROR-00012'
    assert test_product['description'] == 'Et illo et' \
        ' voluptatum corporis. Fugiat atque optio voluptates' \
        ' placeat ut odio. Iusto totam molestiae tenetur eaque' \
        ' molestias. Occaecati sunt sit magni voluptatibus qui ipsum.'
    assert test_product['price'] == '22.99'
    assert test_product['display_price'] == '$22.99'
    assert test_product['available_on'] == '2016-06-27T11:10:17.000Z'
    assert test_product['slug'] == 'ruby-on-rails-bag'
    assert test_product['shipping_category_id'] == 1


def test_orders_all(resp, spree):
    "test fetching all orders"
    test_orders = spree.order.find()
    test_order = test_orders[0]
    assert test_order['number'] == 'R123456789'
    assert test_order['item_total'] == '15.99'
    assert test_order['state'] == 'complete'
    assert test_order['shipment_state'] == 'pending'
    assert test_order['payment_total'] == '0.0'
    assert test_order['token'] == 'aAoojFjB1_PCBeLR1VPnIg'


def test_finding_one_order(resp, spree):
    "test fetching order with respect to order_id"
    test_order = spree.order.get('R123456789')
    assert test_order['number'] == 'R123456789'
    assert test_order['item_total'] == '15.99'
    assert test_order['state'] == 'complete'
    assert test_order['shipment_state'] == 'pending'
    assert test_order['payment_total'] == '0.0'
    assert test_order['token'] == 'aAoojFjB1_PCBeLR1VPnIg'


def test_finding_stock_locations(resp, spree):
    "test finding stock locations"
    stock_locations = spree.stock_locations.find()

    # get a specific stock location with id
    stock_location = spree.stock_locations.get(1)
    assert stock_location == stock_locations[0]


def test_stock_items_all(resp, spree):
    "test fetching all stock items"
    stock_item = spree.get_stock_item(1)
    test_stock_items = stock_item.find()
    test_stock_item = test_stock_items[0]
    assert test_stock_item['count_on_hand'] == 10
    assert test_stock_item['stock_location_id'] == 1
    assert test_stock_item['variant_id'] == 4


def test_finding_one_stock_item(resp, spree):
    "test fetching all stock items"
    stock_item = spree.get_stock_item(1)
    test_stock_item = stock_item.get(4)
    assert test_stock_item['count_on_hand'] == 10
    assert test_stock_item['stock_location_id'] == 1
    assert test_stock_item['variant_id'] == 4


def test_variant_via_permalink(resp, spree):
    "test fetching variant by product permalink"
    variant = spree.variant('ruby-on-rails-jr-spaghetti')
    test_variants = variant.find()
    test_variant = test_variants[0]
    assert test_variant['sku'] == 'ROR-00013'
    assert test_variant['price'] == '19.99'
    assert test_variant['cost_price'] == '17.0'


def test_variant_with_out_permalink(resp, spree):
    "test fetching variant by product permalink"
    variant = spree.variant().get(4)
    assert variant['sku'] == 'ROR-00013'
    assert variant['price'] == '19.99'
    assert variant['cost_price'] == '17.0'
