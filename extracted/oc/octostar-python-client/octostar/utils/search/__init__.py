"""
# General queries against the search engine.
Use this to query the search engine for data. Do note that the search engine can find entities by
keywords, full text search, vector search (e.g. faces, rag), which are features not available in the ontology.

Example of a query:
```json
{ "query": { "bool": { "must": [{ "terms": { "_id": [your_ids] } }] } }, "_source": ["annotations", "annotations.*"] }
```
Include `<object>.*` next to an object that holds vectors. Without it, OpenSearch 3.5 and later return each vector as `1`.

"""
