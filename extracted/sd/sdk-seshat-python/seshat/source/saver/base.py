from dataclasses import dataclass
from typing import List, Literal

from sqlalchemy import make_url

from seshat.data_class import SFrame
from seshat.general.exceptions import DataBaseNotSupportedError
from seshat.general.transformer_story.base import BaseTransformerStory
from seshat.transformer import Transformer
from seshat.transformer.schema import Schema

POSTGRES = "psql"


@dataclass
class SaveConfig:
    sf_key: str
    table: str
    schema: Schema
    clear_table: bool = False
    strategy: Literal["insert", "update", "copy"] = "insert"
    indexes: List[List[str] | str] = ()


class Saver(Transformer):
    """
    Base class for saving SFrame data to various destinations (databases, files, etc.).
    Unlike most transformers that modify data, Savers persist data and pass through the input unchanged.

    Parameters
    ----------
    url : str
        Connection URL or destination path for saving data.
    save_configs : List[SaveConfig]
        List of SaveConfig objects specifying how to save different SFrames.
        Each config defines: sf_key, table/destination, schema, strategy, and indexes.
    """

    def __init__(self, url: str, save_configs: List[SaveConfig], *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check for update configs id columns have been specified
        self.url = url
        db_type = self.db_type
        for config in save_configs:
            if config.strategy == "copy" and db_type != POSTGRES:
                raise DataBaseNotSupportedError(
                    "`copy` command only available in postgresql database"
                )
            elif config.strategy == "update":
                config.schema.get_id()
        self.save_configs = save_configs

    def __call__(self, sf_input: SFrame, *args, **kwargs):
        self.save(sf_input)
        return sf_input

    def calculate_complexity(self):
        return NotImplementedError()

    def save(self, sf: SFrame, *args, **kwargs):
        raise NotImplementedError()

    @property
    def db_type(self):
        url_obj = make_url(self.url)
        if url_obj.drivername in ["postgresql", "postgresql+psycopg2"]:
            return POSTGRES


class SaverStory(BaseTransformerStory):
    transformer = Saver

    use_cases = [
        "Persist processed data to external destinations within a pipeline",
        "Save intermediate results without interrupting the pipeline flow",
        "Configure multiple save destinations with different strategies (insert, update, copy)",
        "Apply schema transformations before saving data",
    ]

    logic_overview = (
        "Saver is an abstract base class for persisting SFrame data. It inherits from Transformer but "
        "overrides __call__() to save the data via save() and then return the input unchanged, allowing "
        "the pipeline to continue. Subclasses implement specific save() logic for different destinations."
    )

    steps = [
        "Validate save_configs during initialization (check strategies, schemas, etc.)",
        "When __call__() is invoked, call save() to persist the data",
        "Return sf_input unchanged to allow pipeline continuation",
    ]

    tags = ["saver", "persistence", "pass-through"]
