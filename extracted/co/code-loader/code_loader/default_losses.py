from enum import Enum

from code_loader.default_metrics import mean_absolute_percentage_error_dimension_reduced, \
    mean_absolute_error_dimension_reduced, mean_squared_logarithmic_error_dimension_reduced, \
    mean_squared_error_dimension_reduced, categorical_crossentropy, binary_crossentropy


class LossName(Enum):
    MeanSquaredError = 'MeanSquaredError'
    MeanSquaredLogarithmicError = 'MeanSquaredLogarithmicError'
    MeanAbsoluteError = 'MeanAbsoluteError'
    MeanAbsolutePercentageError = 'MeanAbsolutePercentageError'
    CategoricalCrossentropy = 'CategoricalCrossentropy'
    BinaryCrossentropy = 'BinaryCrossentropy'


loss_name_to_function = {
    LossName.MeanSquaredError.name: mean_squared_error_dimension_reduced,
    LossName.MeanSquaredLogarithmicError.name: mean_squared_logarithmic_error_dimension_reduced,
    LossName.MeanAbsoluteError.name: mean_absolute_error_dimension_reduced,
    LossName.MeanAbsolutePercentageError.name: mean_absolute_percentage_error_dimension_reduced,
    LossName.CategoricalCrossentropy.name: categorical_crossentropy,
    LossName.BinaryCrossentropy.name: binary_crossentropy
}
