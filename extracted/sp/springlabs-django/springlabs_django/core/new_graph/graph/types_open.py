# GRAPH_NAME GRAPHENE ObjectType (Managed by SPRINGLABS_DJANGO)
class GRAPH_NAMEType(graphene.ObjectType):
    id_user = graphene.ID(description="A unique int value identifying User",
        required=False)
    username = graphene.String(description="A unique string value identifying User",
        required=False)
    email = graphene.String(description="A unique string value identifying User's email",
                            required=False)
    first_name = graphene.String(description="A string value identifying User's name",
        required=False)
    last_name = graphene.String(description="A string value identifying User's last name",
                                required=False)

    class Meta:
        name = "GRAPH_NAME"
        description = "Manejo de GRAPH_NAME"
# END GRAPH_NAME GRAPHENE ObjectType (Managed by SPRINGLABS_DJANGO)