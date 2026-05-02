from lgt_jobs.lgt_data.enums import FeaturesEnum, FeatureOptions
from lgt_jobs.lgt_data.models.base import DictionaryModel


class Feature(DictionaryModel):
    display_name: str
    name: FeaturesEnum
    description: str | None = None
    limit: int | None = None
    options: FeatureOptions | None = None
