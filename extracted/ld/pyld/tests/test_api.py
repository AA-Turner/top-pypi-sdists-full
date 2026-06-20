import pyld.jsonld as jsonld
import rdflib

def test_input():
    input = {}

    dataset = jsonld.to_rdf(input)

    assert isinstance(dataset, rdflib.Dataset)

    output = jsonld.from_rdf(dataset)

    assert input == output


def test_legacy_input():
    input = {}
    
    dataset = jsonld.to_rdf(input, {})

    assert isinstance(dataset, rdflib.Dataset)

    output = jsonld.from_rdf(dataset)

    assert input == output