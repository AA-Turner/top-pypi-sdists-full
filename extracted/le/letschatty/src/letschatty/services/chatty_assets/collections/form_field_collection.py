"""Form Field Collection - Pre-configured AssetCollection for Form Fields"""

from ..asset_service import AssetCollection
from ....models.company.form_field import FormField, FormFieldPreview
from ....models.data_base.mongo_connection import MongoConnection


class FormFieldCollection(AssetCollection[FormField, FormFieldPreview]):
    """Pre-configured collection for Form Field assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="form_fields",
            asset_type=FormField,
            connection=connection,
            create_instance_method=FormField.default_create_instance_method,
            preview_type=FormFieldPreview
        )
