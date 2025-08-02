from enum import Enum, IntEnum


class MetricEnum(Enum):
    MeanSquaredError = 'MeanSquaredError'
    MeanSquaredLogarithmicError = 'MeanSquaredLogarithmicError'
    MeanAbsoluteError = 'MeanAbsoluteError'
    MeanAbsolutePercentageError = 'MeanAbsolutePercentageError'
    Accuracy = 'Accuracy'
    BinaryAccuracy = 'BinaryAccuracy'
    MeanIOU = 'MeanIOU'
    ConfusionMatrixClassification = 'ConfusionMatrixClassification'
    ConfusionMatrixBinaryClassification = 'ConfusionMatrixBinaryClassification'


# backwards compatability: keeping it to not break old imports of Metric enum
# should not be copied to engine contracts
Metric = MetricEnum


class LeapDataType(Enum):
    Image = 'Image'
    Text = 'Text'
    Graph = 'Graph'
    HorizontalBar = 'HorizontalBar'
    ImageMask = 'ImageMask'
    TextMask = 'TextMask'
    ImageWithBBox = 'ImageWithBBox'
    ImageWithHeatmap = 'ImageWithHeatmap'
    Video = 'Video'


class MetricDirection(Enum):
    Upward = "Upward"
    Downward = "Downward"


class DatasetMetadataType(Enum):
    float = "float"
    string = "string"
    int = "int"
    boolean = "boolean"


class DataStateType(Enum):
    training = "training"
    validation = "validation"
    test = "test"
    unlabeled = "unlabeled"


class DataStateEnum(IntEnum):
    training = 0
    validation = 1
    test = 2
    unlabeled = 3


class ConfusionMatrixValue(Enum):
    Positive = "Positive"
    Negative = "Negative"


# todo: handle test not run due to error in pre process and Add to TestingSectionEnum Enum didn't run
class TestingSectionEnum(Enum):
    Warnings = "Warnings"
    Errors = "Errors"
