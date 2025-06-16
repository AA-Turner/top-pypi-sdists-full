import yaml

from datacontract_specification.model import DataContractSpecification


def test_roundtrip():
    data_contract_str = """
dataContractSpecification: 1.1.0
id: urn:datacontract:checkout:orders-latest
info:
  title: Orders Latest
  version: 2.0.0
  description: |
    Successful customer orders in the webshop.
    All orders since 2020-01-01.
    Orders with their line items are in their current state (no history included).
  owner: Checkout Team
  status: active
  contact:
    name: John Doe (Data Product Owner)
    url: https://teams.microsoft.com/l/channel/example/checkout
    """
    assert_equals_yaml(data_contract_str)

def assert_equals_yaml(data_contract_str):
    assert yaml.safe_load(data_contract_str) == yaml.safe_load(DataContractSpecification.from_string(data_contract_str).to_yaml())

def test_json_schema():
    assert "" != DataContractSpecification.json_schema()