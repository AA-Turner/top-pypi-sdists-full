from enum import Enum

from tmo.decorators.functional import functional


class DataType(Enum):
    FLOAT = "float"
    INTEGER = "integer"


class TypeEnum(Enum):
    ENTITY = "entity"
    FEATURE = "feature"
    TARGET = "target"


class CatalogType(Enum):
    VANTAGE = "VANTAGE"
    NO_CATALOG = "NO_CATALOG"


class CatalogBodyType(Enum):
    VANTAGE = "CatalogBody"
    NO_CATALOG = "NoCatalogBody"


@functional
class Variable(object):
    name: str = None  # NOSONAR
    data_type: DataType = None  # NOSONAR
    type: TypeEnum = None  # NOSONAR
    selected: str = None  # NOSONAR
    entity_id: str = None  # NOSONAR


@functional
class FeaturesEntityTargets(object):
    entity: str = None  # NOSONAR
    sql: str = None  # NOSONAR
    variables: list[Variable] = []

    def set_columns(self, columns: list[Variable]) -> object:
        join = self.variables + columns
        self.variables = join
        return self

    def add_column(self, variable: Variable) -> object:
        v = [variable]
        join = self.variables + v
        self.variables = join
        return self


@functional
class Predictions(object):
    database: str = None  # NOSONAR
    entity_sql: str = None  # NOSONAR
    table: str = None  # NOSONAR


@functional
class Metadata(object):
    entity_and_targets: FeaturesEntityTargets = None  # NOSONAR
    features: FeaturesEntityTargets = None  # NOSONAR
    predictions: Predictions = None  # NOSONAR
    type: CatalogBodyType = None  # NOSONAR


@functional
class FeatureMetadata(object):
    database: str = None  # NOSONAR
    table: str = None  # NOSONAR
