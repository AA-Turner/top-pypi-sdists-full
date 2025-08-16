#!/usr/bin/env python3

# Simple test to verify transform conversion without pyodide environment
import numpy as np
from itkwasm import Transform, TransformType, TransformParameterizations, FloatTypes, TransformList

# Create a test transform
transform_type = TransformType(
    transformParameterization=TransformParameterizations.Affine,
    parametersValueType=FloatTypes.Float64,
    inputDimension=3,
    outputDimension=3
)

fixed_parameters = np.array([0.0, 0.0, 0.0]).astype(np.float64)
parameters = np.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 10.0, 20.0, 30.0]).astype(np.float64)

transform = Transform(
    transformType=transform_type,
    numberOfParameters=12,
    numberOfFixedParameters=3,
    fixedParameters=fixed_parameters,
    parameters=parameters
)

transform_list: TransformList = [transform]

print("Transform created successfully")
print(f"Transform type: {transform.transformType.transformParameterization}")
print(f"Number of parameters: {transform.numberOfParameters}")
print(f"Number of fixed parameters: {transform.numberOfFixedParameters}")
print(f"Transform list length: {len(transform_list)}")
print("Test completed successfully")
