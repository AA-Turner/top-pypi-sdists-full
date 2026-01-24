from typing import Callable, Optional

from chalk._lsp.error_builder import get_resolver_error_builder
from chalk.features import DataFrame
from chalk.features.feature_field import Feature
from chalk.features.feature_set import Features
from chalk.features.resolver import RESOLVER_REGISTRY, OnlineResolver, ResourceHint
from chalk.features.underscore import Underscore
from chalk.ml.model_reference import MODEL_REFERENCE_REGISTRY
from chalk.ml.model_version import ModelVersion
from chalk.utils.collections import ensure_tuple


def build_inference_function(
    model_version: ModelVersion, pkey: Feature, output_features: Optional[Feature | list[Feature]] = None
) -> Callable[[DataFrame], DataFrame]:
    """Build the core inference function that takes a DataFrame and returns predictions.

    Uses ModelInference.prepare_input() and extract_output() for model-specific logic.

    Parameters
    ----------
    model_version
        The model version to use for prediction
    pkey
        The primary key feature to exclude from predictions
    output_features
        Optional output feature(s) to add predictions to the DataFrame.
        Can be a single Feature or a list of Features for multi-output models.

    Returns
    -------
    Callable[[DataFrame], DataFrame]
        Function that takes a DataFrame and returns predictions
    """
    # For all other models, use the ModelInference prepare_input/extract_output methods
    pkey_string = str(pkey)

    def fn(inp: DataFrame):
        # Get features (excluding primary key) as PyArrow table
        feature_table = inp[[c for c in inp.columns if c != pkey_string]].to_pyarrow()

        # Use model-specific input preparation (default: __array__(), ONNX: struct array)
        model_input = model_version.predictor.prepare_input(feature_table)

        # Run prediction
        result = model_version.predict(model_input)

        if output_features is not None:
            # Normalize to list for uniform processing
            features_list = output_features if isinstance(output_features, list) else [output_features]

            # Extract output for each feature and build columns dict
            columns_dict = {}
            for output_feature in features_list:
                # Use model-specific output extraction (default: identity, ONNX: extract field)
                output_feature_name = str(output_feature).split(".")[-1]
                result_data = model_version.predictor.extract_output(result, output_feature_name)
                columns_dict[output_feature] = result_data

            return inp[pkey_string].with_columns(columns_dict)

        return result

    return fn


def generate_inference_resolver(
    inputs: list[Underscore] | Underscore, model_version: ModelVersion, resource_hint: Optional[ResourceHint] = None
) -> Feature:
    output_feature = Feature()
    previous_hook = output_feature.hook

    def hook(features: type[Features]) -> None:
        if previous_hook:
            previous_hook(features)

        pkey = features.__chalk_primary__
        if pkey is None:
            raise ValueError(f"Feature class {features} does not have a primary key defined")

        def resolver_factory():
            # Use the extracted build_inference_function
            cleaned_inputs = []
            inputs_list = inputs if isinstance(inputs, list) else [inputs]
            for i in inputs_list:
                try:
                    cleaned_inputs.append(Feature.from_root_fqn(output_feature.namespace + str(i)[1:]))
                except Exception as e:
                    raise ValueError(f"Could not find feature for input {i}: {e}")

            fn = build_inference_function(model_version, pkey, output_feature)

            identifier = model_version.identifier or ""
            model_reference = MODEL_REFERENCE_REGISTRY.get((model_version.name, identifier), None)
            if model_reference is not None:
                model_reference.relations.append(([i.fqn for i in cleaned_inputs], output_feature.fqn))

            return OnlineResolver(
                function_definition="",
                filename="",
                fqn=f"{model_version.name}__{output_feature.namespace}_{output_feature.name}",
                doc=None,
                inputs=[DataFrame[[pkey, *ensure_tuple(cleaned_inputs)]]],
                state=None,
                output=Features[DataFrame[output_feature, pkey]],
                fn=fn,
                environment=None,
                machine_type=None,
                default_args=[None],
                timeout=None,
                cron=None,
                when=None,
                tags=None,
                owner=None,
                resource_hint=resource_hint or model_version.resource_hint,
                data_sources=None,
                is_sql_file_resolver=False,
                source_line=None,
                lsp_builder=get_resolver_error_builder(fn),
                parse=None,
                static=False,
                total=False,
                autogenerated=False,
                unique_on=None,
                partitioned_by=None,
                data_lineage=None,
                sql_settings=None,
            )

        RESOLVER_REGISTRY.add_to_deferred_registry(resolver_factory, override=False)

    output_feature.hook = hook

    return output_feature
