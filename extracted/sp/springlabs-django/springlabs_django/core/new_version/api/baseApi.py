# Django libraries
# 3rd Party libraries
import graphene
# Standard/core python libraries
# Our custom libraries (Managed by SPRINGLABS_DJANGO)
from .users.schema import ExampleDjangoQueries

# QUERY EXPOSE TO SCHEMA GRPAHENE


class Query(ExampleDjangoQueries, graphene.ObjectType):
    pass


# SCHEMA
schema = graphene.Schema(query=Query, auto_camelcase=False)
