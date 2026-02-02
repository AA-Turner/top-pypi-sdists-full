import corvic.model._source as source
from corvic.op_graph import feature_type

# types
Text = feature_type.Text
Categorical = feature_type.Categorical
PrimaryKey = feature_type.PrimaryKey
Identifier = feature_type.Identifier
Numerical = feature_type.Numerical
MultiCategorical = feature_type.MultiCategorical
Timestamp = feature_type.Timestamp
Embedding = feature_type.Embedding
Unknown = feature_type.Unknown
ForeignKey = feature_type.ForeignKey

# factories
text = feature_type.text
categorical = feature_type.categorical
primary_key = feature_type.primary_key
identifier = feature_type.identifier
numerical = feature_type.numerical
multi_categorical = feature_type.multi_categorical
timestamp = feature_type.timestamp
embedding = feature_type.embedding
unknown = feature_type.unknown
foreign_key = source.foreign_key
image = feature_type.image

FeatureType = feature_type.FeatureType
