"""
## EUMDAC Library

EUMDAC is a Python library that simplifies access to the EUMETSAT Data Access Services.

## Classes
The main classes are:
- AccessToken - manages authentication, provides tokens to other classes
- DataStore - interfaces with EUMETSAT Data Store for accessing collections and performing searches
  - Collection - a Data Store collection of products, providing its metadata and allowing searching for products
  - Product - a Data Store product, providing its metadata and allowing downloading it (or some of its contents)
- DataTailor - interfaces with EUMETSAT Data Tailor Webservice for customising Data Store products

## Basic DataStore usage

   >>> from eumdac.token import AccessToken
   >>> from eumdac.datastore import DataStore
   >>> consumer_key = 'my-consumer-key'
   >>> consumer_secret = 'my-consumer-secret'
   >>> credentials = (consumer_key, consumer_secret)
   >>> token = AccessToken(credentials)
   >>> datastore = DataStore(token)
   >>> for collection in datastore.collections:
   ...     print(f"{collection} - {collection.title}")
   ...
   EO:EUM:DAT:MSG:HRSEVIRI - High Rate SEVIRI Level 1.5 Image Data - MSG - 0 degree
   EO:EUM:DAT:MSG:MSG15-RSS - Rapid Scan High Rate SEVIRI Level 1.5 Image Data - MSG
   EO:EUM:DAT:0080 - MVIRI Level 1.5 Climate Data Record - MFG - 0 degree
   EO:EUM:DAT:MSG:RSS-CLM - Rapid Scan Cloud Mask - MSG
   EO:EUM:DAT:0081 - MVIRI Level 1.5 Climate Data Record - MFG - 57 degree
   ...

## Copyright & License
© EUMETSAT 2024, MIT License

## Support
For all queries on this software package, please contact [ops@eumetsat.int](mailto:ops@eumetsat.int)


"""

from .__version__ import (
    __author__,
    __author_email__,  # noqa
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)
from .datastore import DataStore  # noqa
from .datatailor import DataTailor  # noqa
from .token import AccessToken  # noqa
