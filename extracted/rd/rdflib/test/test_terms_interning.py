# import pickle

# from rdflib import BNode, URIRef


# def test_iri():
#     iri = URIRef("http://example.com")
#     iri2 = URIRef("http://example.com")
#     assert iri == iri2
#     assert iri is iri2

#     pickled = pickle.dumps(iri)
#     iri3 = pickle.loads(pickled)
#     assert iri == iri3
#     assert iri is iri3
#     assert iri2 is iri3


# def test_bnode():
#     bnode = BNode("123")
#     bnode2 = BNode("123")
#     assert bnode == bnode2
#     assert bnode is bnode2

#     pickled = pickle.dumps(bnode)
#     bnode3 = pickle.loads(pickled)
#     assert bnode == bnode3
#     assert bnode is bnode3
#     assert bnode2 is bnode3
