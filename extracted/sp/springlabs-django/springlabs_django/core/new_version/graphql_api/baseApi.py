# Django libraries
# 3rd Party libraries
import graphene
# Standard/core python libraries
# Our custom libraries (Managed by SPRINGLABS_DJANGO)
from .users.schema import ExampleDjangoUsersQueries

# QUERY EXPOSE TO SCHEMA GRPAHENE


class Query(ExampleDjangoUsersQueries, graphene.ObjectType):
    pass


# SCHEMA
schema = graphene.Schema(query=Query, auto_camelcase=False)
