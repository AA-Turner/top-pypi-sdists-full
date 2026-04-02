from seshat.data_class import SFrame
from seshat.general.transformer_story.base import BaseTransformerStory
from seshat.source.mixins import SQLMixin
from seshat.transformer import Transformer
from seshat.transformer.schema import Schema


class SQLTableExistenceValidator(Transformer, SQLMixin):
    def __init__(
        self,
        schema: Schema,
        url: str,
        table_name: str,
        group_keys=None,
    ):
        super().__init__(group_keys)
        self.table_name = table_name
        self.schema = schema
        self.url = url

    def __call__(self, sf_input: SFrame = None, *args, **kwargs):
        self.ensure_table_exists(self.table_name, self.schema)
        return sf_input

    def calculate_complexity(self):
        return 10


class SQLTableExistenceValidatorStory(BaseTransformerStory):
    transformer = SQLTableExistenceValidator
    use_cases = [
        "To ensure a specific SQL table exists in a database before data operations, creating it if it doesn't.",
        "To validate and prepare the database schema for subsequent data loading or processing steps.",
    ]
    logic_overview = (
        "This transformer checks for the existence of a SQL table specified by `table_name` "
        "and `schema` in the database identified by `url`. If the table does not exist, "
        "it is created based on the provided `schema`. The input SFrame is passed through unchanged."
    )
    steps = [
        "Connects to the database using the provided `url`.",
        "Checks if the table specified by `table_name` exists.",
        "If the table does not exist, it is created using the provided `schema`.",
        "The original input SFrame is returned without modification.",
    ]
    tags = ["pseudo", "validator"]
