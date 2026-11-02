# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_etag']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fastapi-etag',
    'version': '0.4.0',
    'description': 'Convenience library for working with etags in fastapi',
    'long_description': '# fastapi-etag\n\n## Quickstart\n\nBasic etag support for FastAPI, allowing you to benefit from conditional caching in web browsers and reverse-proxy caching layers.\n\nThis does not generate etags that are a hash of the response content, but instead lets you pass in a custom etag generating function per endpoint that is called before executing the route function.  \nThis lets you bypass expensive API calls when client includes a matching etag in the `If-None-Match` header, in this case your endpoint is never called, instead returning a 304 response telling the client nothing has changed.\n\nThe etag logis is implemented with a fastapi dependency that you can add to your routes or entire routers.\n\nHere\'s how you use it:\n\n```python3\n# app.py\n\nfrom fastapi import FastAPI\nfrom starlette.requests import Request\nfrom fastapi_etag import Etag, add_exception_handler\n\napp = FastAPI()\nadd_exception_handler(app)\n\n\nasync def get_hello_etag(request: Request):\n    return "etagfor" + request.path_params["name"]\n\n\n@app.get("/hello/{name}", dependencies=[Depends(Etag(get_hello_etag))])\nasync def hello(name: str):\n    return {"hello": name}\n\n```\n\nRun this example with `uvicorn: uvicorn --port 8090 app:app`\n\nLet\'s break it down:\n\n```python3\nadd_exception_handler(app)\n```\n\nThe dependency raises a special `CacheHit` exception to exit early when there\'s a an etag match, this adds a standard exception handler to the app to generate a correct 304 response from the exception.\n\n```python3\nasync def get_hello_etag(request: Request):\n    name = request.path_params.get("name")\n    return f"etagfor{name}"\n```\n\nThis is the function that generates the etag for your endpoint.  \nIt can do anything you want, it could for example return a hash of a last modified timestamp in your database.  \nIt can be either a normal function or an async function.  \nOnly requirement is that it accepts one argument (request) and that it returns either a string (the etag) or `None` (in which case no etag header is added)\n\n\n```python3\n@app.get("/hello/{name}", dependencies=[Depends(Etag(get_hello_etag))])\ndef hello(name: str):\n\t...\n```\n\nThe `Etag` dependency is called like any fastapi dependency.\nIt always adds the etag returned by your etag gen function to the response.  \nIf client passes a matching etag in the `If-None-Match` header, it will raise a `CacheHit` exception which triggers a 304 response before calling your endpoint.\n\n\nNow try it with curl:\n\n```\ncurl -i "http://localhost:8090/hello/bob"\nHTTP/1.1 200 OK\ndate: Mon, 30 Dec 2019 21:55:43 GMT\nserver: uvicorn\ncontent-length: 15\ncontent-type: application/json\netag: W/"etagforbob"\n\n{"hello":"bob"}\n```\n\nEtag header is added\n\nNow including the etag in `If-None-Match` header (mimicking a web browser):\n\n```\ncurl -i -X GET "http://localhost:8090/hello/bob" -H "If-None-Match: W/\\"etagforbob\\""\nHTTP/1.1 304 Not Modified\ndate: Mon, 30 Dec 2019 21:57:37 GMT\nserver: uvicorn\netag: W/"etagforbob"\n```\n\nIt now returns no content, only the 304 telling us nothing has changed.\n\n### Add response headers\n\nIf you want to add some extra response headers to the 304 and regular response,\nyou can add the `extra_headers` argument with a dict of headers:\n\n```\n@app.get(\n    "/hello/{name}",\n    dependencies=[\n        Depends(\n            Etag(\n                get_hello_etag,\n                extra_headers={"Cache-Control": "public, max-age: 30"},\n            )\n        )\n    ],\n)\ndef hello(name: str):\n\t...\n```\n\nThis will add the `cache-control` header on all responses from the endpoint.\n\n\n## Contributing\n\nSee [CONTRIBUTING.md](CONTRIBUTING.md)\n\n',
    'author': 'Steinthor Palsson',
    'author_email': 'steini90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/steinitzu/fastapi-etag',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
