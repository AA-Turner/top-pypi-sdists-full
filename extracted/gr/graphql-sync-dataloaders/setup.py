# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphql_sync_dataloaders']

package_data = \
{'': ['*']}

install_requires = \
['graphql-core>=3.2.0,<3.3.0']

setup_kwargs = {
    'name': 'graphql-sync-dataloaders',
    'version': '0.1.1',
    'description': 'Use DataLoaders in your Python GraphQL servers that have to run in a sync context (i.e. Django).',
    'long_description': '# graphql-sync-dataloaders\n\nUse DataLoaders in your Python GraphQL servers that have to run in a sync\ncontext (i.e. Django).\n\n## Requirements\n\n* Python 3.8+\n* graphql-core >=3.2.0\n\n## Installation\n\nThis package can be installed from [PyPi](https://pypi.python.org/pypi/graphql-sync-dataloaders) by running:\n\n```bash\npip install graphql-sync-dataloaders\n```\n\n## Strawberry setup\n\nWhen creating your Strawberry Schema pass `DeferredExecutionContext` as the\n`execution_context_class` argument:\n\n```python\n# schema.py\nimport strawberry\nfrom graphql_sync_dataloaders import DeferredExecutionContext\n\nschema = strawberry.Schema(Query, execution_context_class=DeferredExecutionContext)\n```\n\nThen create your dataloaders using the `SyncDataLoader` class:\n\n```python\nfrom typing import List\n\nfrom graphql_sync_dataloaders import SyncDataLoader\n\nfrom .app import models  # your Django models\n\ndef load_users(keys: List[int]) -> List[User]:\n    qs = models.User.objects.filter(id__in=keys)\n    user_map = {user.id: user for user in qs}\n    return [user_map.get(key, None) for key in keys]\n\nuser_loader = SyncDataLoader(load_users)\n```\n\nYou can then use the loader in your resolvers and it will automatically be\nbatched to reduce the number of SQL queries:\n\n```python\nimport strawberry\n\n@strawberry.type\nclass Query:\n    @strawberry.field\n    def get_user(self, id: strawberry.ID) -> User:\n        return user_loader.load(id)\n```\n\n**Note: You probably want to setup your loaders in context. See\nhttps://strawberry.rocks/docs/guides/dataloaders#usage-with-context for more\ndetails**\n\nThe following query will only make 1 SQL query:\n\n```graphql\nfragment UserDetails on User {\n  username\n}\n\nquery {\n  user1: getUser(id: \'1\') {\n    ...UserDetails\n  }\n  user2: getUser(id: \'2\') {\n    ...UserDetails\n  }\n  user3: getUser(id: \'3\') {\n    ...UserDetails\n  }\n}\n```\n\n\n## Graphene-Django setup\n\n**Requires graphene-django >=3.0.0b8**\n\nWhen setting up your GraphQLView pass `DeferredExecutionContext` as the\n`execution_context_class` argument:\n\n```python\n# urls.py\nfrom django.urls import path\nfrom graphene_django.views import GraphQLView\nfrom graphql_sync_dataloaders import DeferredExecutionContext\n\nfrom .schema import schema\n\nurlpatterns = [\n    path(\n        "graphql",\n        csrf_exempt(\n            GraphQLView.as_view(\n                schema=schema, \n                execution_context_class=DeferredExecutionContext\n            )\n        ),\n    ),\n]\n```\n\nThen create your dataloaders using the `SyncDataLoader` class:\n\n```python\nfrom typing import List\n\nfrom graphql_sync_dataloaders import SyncDataLoader\n\nfrom .app import models  # your Django models\n\ndef load_users(keys: List[int]) -> List[User]:\n    qs = models.User.objects.filter(id__in=keys)\n    user_map = {user.id: user for user in qs}\n    return [user_map.get(key, None) for key in keys]\n\nuser_loader = SyncDataLoader(load_users)\n```\n\nYou can then use the loader in your resolvers and it will automatically be\nbatched to reduce the number of SQL queries:\n\n```python\nimport graphene\n\nclass Query(graphene.ObjectType):\n    get_user = graphene.Field(User, id=graphene.ID)\n\n    def resolve_get_user(root, info, id):\n        return user_loader.load(id)\n```\n\nThe following query will only make 1 SQL query:\n\n```graphql\nfragment UserDetails on User {\n  username\n}\n\nquery {\n  user1: getUser(id: \'1\') {\n    ...UserDetails\n  }\n  user2: getUser(id: \'2\') {\n    ...UserDetails\n  }\n  user3: getUser(id: \'3\') {\n    ...UserDetails\n  }\n}\n```\n\n## How it works\n\nThis library implements a custom version of the graphql-core\n[ExecutionContext class](https://github.com/graphql-python/graphql-core/blob/5f6a1944cf6923f6249d1575f5b3aad87e629c66/src/graphql/execution/execute.py#L171)\nthat is aware of the `SyncFuture` objects defined in this library. A\n`SyncFuture` represents a value that hasn\'t been resolved to a value yet\n(similiar to asycnio Futures or JavaScript Promises) and that is what the\n`SyncDataLoader` returns when you call the `.load` function.\n\nWhen the custom `ExecutionContext` encounters a `SyncFuture` that gets returned\nfrom a resolver and it keeps track of them. Then after the first pass of the\nexection it triggers the `SyncFuture` callbacks until there are none left. Once\nthere are none left the data is fully resolved and can be returned to the\ncaller synchronously. This allows us to implement a `DataLoader` pattern that\nbatches calls to a loader function, and it allows us to do this in a fully\nsynchronously way.\n\n## Credits\n\n[@Cito](https://github.com/Cito) for graphql-core and for implementing the first version of this in https://github.com/graphql-python/graphql-core/pull/155\n',
    'author': 'Jonathan Kim',
    'author_email': 'hello@jkimbo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jkimbo/graphql-sync-dataloaders',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
