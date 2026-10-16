from tmo.types.api_resource import ApiResourceMixin, api_field


class Model(ApiResourceMixin):
    """A ModelOps model. Core fields are typed; any other response key stays accessible."""

    _FIELDS = (
        "id",
        "name",
        "description",
        "source",
        "source_id",
        "project_id",
        "owner_id",
        "archived",
    )

    id = api_field("id")
    name = api_field("name")
    description = api_field("description")
    source = api_field("source")
    source_id = api_field("source_id")
    project_id = api_field("project_id")
    owner_id = api_field("owner_id")
    archived = api_field("archived")


class TrainedModel(ApiResourceMixin):
    """A ModelOps trained model. Core fields are typed; any other response key stays accessible."""

    _FIELDS = (
        "id",
        "model_id",
        "status",
        "project_id",
        "owner_id",
        "archived",
    )

    id = api_field("id")
    model_id = api_field("model_id")
    status = api_field("status")
    project_id = api_field("project_id")
    owner_id = api_field("owner_id")
    archived = api_field("archived")
