import sqlalchemy
from sqladmin.fields import SelectField

from project.sqladmin_.model_view.common import SimpleMV
from project.sqlalchemy_db_.sqlalchemy_model import StoryLogDBM


class StoryLogMV(SimpleMV, model=StoryLogDBM):
    name = StoryLogDBM.get_cls_entity_name()
    name_plural = StoryLogDBM.get_cls_entity_name_plural()
    icon = "fa-solid fa-book"
    column_list = StoryLogDBM.get_column_and_relationship_names_()
    column_details_list = StoryLogDBM.get_column_and_relationship_names_() + StoryLogDBM.get_sd_property_names()
    form_columns = StoryLogDBM.get_column_and_relationship_names_(include_column_pk=False)
    form_overrides = {
        StoryLogDBM.level.key: SelectField,
        StoryLogDBM.type.key: SelectField,
    }
    form_args = {
        StoryLogDBM.level.key: {
            "choices": [(level, level) for level in StoryLogDBM.Levels.values_list()],
            "description": f"Choose {StoryLogDBM.level.key}"
        },
        StoryLogDBM.type.key: {
            "choices": [(level, level) for level in StoryLogDBM.Types.values_list()],
            "description": f"Choose {StoryLogDBM.type.key}"
        }
    }
    column_sortable_list = sqlalchemy.inspect(StoryLogDBM).columns
