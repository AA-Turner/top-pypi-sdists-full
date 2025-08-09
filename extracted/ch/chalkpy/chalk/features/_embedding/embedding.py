from __future__ import annotations

from datetime import timedelta
from io import BytesIO
from typing import Any, Callable

import pyarrow as pa

from chalk._lsp.error_builder import get_resolver_error_builder
from chalk.features._embedding.cohere import CohereProvider
from chalk.features._embedding.embedding_provider import EmbeddingProvider
from chalk.features._embedding.openai import OpenAIProvider
from chalk.features._embedding.sentence_transformer import SentenceTransformerProvider
from chalk.features._embedding.vertexai import VertexAIProvider
from chalk.features._vector import Vector
from chalk.features.dataframe import DataFrame
from chalk.features.feature_field import Feature
from chalk.features.feature_set import Features
from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature
from chalk.features.resolver import RESOLVER_REGISTRY, OnlineResolver, ResourceHint
from chalk.features.underscore import Underscore, UnderscoreFunction
from chalk.serialization.parsed_annotation import ParsedAnnotation
from chalk.utils.collections import ensure_tuple

SUPPORTED_LOCAL_MODELS = {
    "all-MiniLM-L6-v2",  # https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
    "sample-bert",  # For internal Chalk use
}

# This will eventually be included in SUPPORTED_LOCAL_MODELS
SUPPORTED_IMAGE_MODELS = {
    "siglip-base-patch16-224-vision": {
        "image_size": 224,
        "output_size": 768,
        "model_path": "/chalk_root/engine/models/onnx/siglip-base-patch16-224-vision/model.onnx",
    }
}


def _get_provider(provider: str, model: str, dimensions: int | None = None) -> EmbeddingProvider:
    """Factory function to get an EmbeddingProvider"""
    if provider == "openai":
        return OpenAIProvider(model, dimensions)
    elif provider == "cohere":
        return CohereProvider(model, dimensions)
    elif provider == "vertexai":
        return VertexAIProvider(model, dimensions)
    elif provider == "sentence-transformers":
        return SentenceTransformerProvider(model, dimensions)
    raise ValueError(
        f"Unsupported embedding provider: {provider}. The supported providers are ['openai', 'cohere', 'vertexai']."
    )


def embed(
    input: Callable[[], Any],
    model: str | None = None,
    model_path: str | None = None,
    tokenizer_path: str | None = None,
    provider: str | None = None,
    name: str | None = None,
    owner: str | None = None,
    tags: list[str] | None = None,
    max_staleness: str | timedelta | None | ellipsis = ...,
    description: str | None = None,
    version: int | None = None,
    default_version: int = 1,
    etl_offline_to_online: bool | None = None,
    offline_ttl: ellipsis | str | timedelta | None = ...,
    default: Any = None,
    dimensions: int | None = None,
    resource_group: str | None = None,
    resource_hint: ResourceHint | None = None,
) -> Any:
    """Specify an embedding feature.

    Parameters
    ----------
    input
        The input for the embedding. This argument is callable
        to allow for forward references to features of the same
        class.
    provider
        The AI provider to use for the embedding.
    model
        The model to generate the embedding.
    model_path
        The path to the embedding model file: currently, `onnx` models are supported.
    tokenizer_path
        The path to the tokenizer for the model file. This is only used running an embedding model locally.
    dimensions
        The dimensionality of the embedding. If not specified, the default dimensionality will be used.
        Supported dimensionality varies based on the model.
    owner
        You may also specify which person or group is responsible for a feature.
        The owner tag will be available in Chalk's web portal.
        Alerts that do not otherwise have an owner will be assigned
        to the owner of the monitored feature.
        Read more at https://docs.chalk.ai/docs/feature-discovery#owner
    tags
        Add metadata to a feature for use in filtering, aggregations,
        and visualizations. For example, you can use tags to assign
        features to a team and find all features for a given team.
        Read more at https://docs.chalk.ai/docs/feature-discovery#tags
    max_staleness
        When a feature is expensive or slow to compute, you may wish to cache its value.
        Chalk uses the terminology "maximum staleness" to describe how recently a feature
        value needs to have been computed to be returned without re-running a resolver.
        Read more at https://docs.chalk.ai/docs/feature-caching
    etl_offline_to_online
        When `True`, Chalk copies this feature into the online environment
        when it is computed in offline resolvers.
        Read more at https://docs.chalk.ai/docs/reverse-etl
    version
        The maximum version for a feature. Versioned features can be
        referred to with the `@` operator:

        >>> from chalk.features import Vector, features
        >>> @features
        ... class Document:
        ...     id: str
        ...     content: str
        ...     score: Vector = embed(
        ...         input=lambda: Document.content,
        ...         provider="openai",
        ...         model="text-embedding-ada-002",
        ...         version=2,
        ...     )
        >>> str(Document.content @ 2)
        "document.content@2"

        See more at https://docs.chalk.ai/docs/feature-versions
    default_version
        The default version for a feature. When you reference a
        versioned feature without the `@` operator, you reference
        the `default_version`. Set to `1` by default.

        >>> from chalk.features import Vector, features
        >>> @features
        ... class Document:
        ...     id: str
        ...     content: str
        ...     embedding: Vector = embed(
        ...         input=lambda: Document.content,
        ...         provider="openai",
        ...         model="text-embedding-ada-002",
        ...         version=2,
        ...         default_version=2,
        ...     )
        >>> str(Document.content)
        "document.content"

        See more at https://docs.chalk.ai/docs/feature-versions#default-versions

    Other Parameters
    ----------------
    name
        The name for the feature. By default, the name of a feature is
        the name of the attribute on the class, prefixed with
        the camel-cased name of the class. Note that if you provide an
        explicit name, the namespace, determined by the feature class,
        will still be prepended. See `features` for more details.
    description
        Descriptions are typically provided as comments preceding
        the feature definition. For example, you can document a
        `fraud_score` feature with information about the values
        as follows:

        >>> @features
        ... class Document:
        ...     # 0 to 100 score indicating an identity match.
        ...     embedding: Vector = embed(...)

        You can also specify the description directly with this parameter.
        Read more at https://docs.chalk.ai/docs/feature-discovery#description
    offline_ttl
    default
        The default value to use for this embedding feature when no value is available.
        This can be useful when you want to provide a fallback embedding value.
    resource_group
        The resource group for the embed resolver: this is used to isolate execution of
        the resolver onto a separate pod (or set of nodes), allowing model inference
        to be run in a separate environment, such as on a GPU-enabled node.
    resource_hint
        The resource hint for the embed resolver: Can be either CPU, GPU, or IO.
        Chalk uses the resource hint to optimize resolver execution.

    Examples
    --------
    >>> from chalk.features import Vector, features
    >>> @features
    ... class Document:
    ...     id: str
    ...     content: str
    ...     embedding: Vector = embed(
    ...         input=lambda: Document.content,
    ...         provider="openai",
    ...         model="text-embedding-ada-002",
    ...     )
    """
    if provider is None:
        if model in SUPPORTED_IMAGE_MODELS.keys():
            try:
                import numpy as np  # pyright: ignore
                import onnxruntime as ort  # pyright: ignore
                from PIL import Image  # pyright: ignore
            except ImportError:
                raise ImportError(f"Missing required imports to run {model}. Need onnxruntime and/or pillow.")
            model_variables = SUPPORTED_IMAGE_MODELS[model]  # pyright: ignore
            output_feature = Feature(
                name=name,
                owner=owner,
                tags=tags,
                typ=Vector[model_variables["output_size"]],
                max_staleness=max_staleness,
                description=description,
                version=version,
                default_version=default_version,
                etl_offline_to_online=etl_offline_to_online,
                offline_ttl=offline_ttl,
                default=default,
            )
            previous_hook = output_feature.hook

            def hook(features: type[Features]) -> None:
                if previous_hook:
                    previous_hook(features)

                def resolver_factory():
                    def fn(image_data: bytes):
                        if not isinstance(image_data, bytes):  # pyright: ignore
                            raise Exception("Image data must be type `bytes`.")
                        image = Image.open(BytesIO(image_data)).convert("RGB")
                        resized_image = image.resize(
                            (model_variables["image_size"], model_variables["image_size"])  # pyright: ignore
                        )

                        pixel_values = np.array(resized_image).astype(np.float32) / 255.0
                        pixel_values_normed = (pixel_values - 0.5) / 0.5
                        pixel_values_transposed = pixel_values_normed.transpose(2, 0, 1)
                        pixel_values_final = np.expand_dims(pixel_values_transposed, axis=0)

                        # Ideally this would only run once - but it will run for each embedding.
                        session = ort.InferenceSession(model_variables["model_path"])  # pyright: ignore
                        image_embeds = session.run(output_names=None, input_feed={"pixel_values": pixel_values_final})
                        return image_embeds

                    return OnlineResolver(
                        function_definition="",
                        filename="",
                        fqn=f"__chalk__embedding__resolver__namespace__{output_feature.namespace}__name__{output_feature.name}",
                        doc=None,
                        inputs=ensure_tuple(input()),
                        state=None,
                        output=Features[output_feature],
                        fn=fn,
                        environment=None,
                        tags=output_feature.tags,
                        machine_type=None,
                        default_args=[None],
                        owner=output_feature.owner,
                        timeout=None,
                        cron=None,
                        when=None,
                        data_sources=None,
                        is_sql_file_resolver=False,
                        source_line=None,
                        lsp_builder=get_resolver_error_builder(fn),
                        parse=None,
                        resource_hint=resource_hint,
                        resource_group=resource_group,
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

        if not isinstance(input, Underscore):
            raise TypeError(
                "When using `model_path` and `provider`, the `input` must be an underscore not a lambda expression: `_.content`."
            )

        if model in SUPPORTED_LOCAL_MODELS:
            return UnderscoreFunction("onnx_run_embedding", input, model_name=model)

        if model_path is not None and tokenizer_path is not None:
            return UnderscoreFunction("onnx_run_embedding", input, model_path=model_path, tokenizer_path=tokenizer_path)

        raise ValueError(
            f"If `provider` is None, you must specify either: both a `model_path` and `tokenizer_path`, or one of the supported local embedding models ({', '.join(list(SUPPORTED_LOCAL_MODELS))})."
        )

    if model is None:
        raise ValueError("If provider is set, then model must also be set")

    embedding_provider = _get_provider(provider, model, dimensions)
    # Manually set the dimensions of the Vector when using embedding
    typ = ParsedAnnotation(underlying=embedding_provider.get_vector_class())
    output_feature = Feature(
        name=name,
        owner=owner,
        tags=tags,
        typ=typ,
        max_staleness=max_staleness,
        description=description,
        version=version,
        default_version=default_version,
        etl_offline_to_online=etl_offline_to_online,
        offline_ttl=offline_ttl,
        default=default,
    )
    previous_hook = output_feature.hook

    def hook(features: type[Features]) -> None:
        if previous_hook:
            previous_hook(features)

        def resolver_factory():
            inputs = ensure_tuple(input())
            input_features_or_literals = tuple(
                unwrap_feature(x) if isinstance(x, (Feature, FeatureWrapper)) else x for x in inputs
            )
            input_features: list[Feature] = []
            input_schema: list[pa.DataType] = []
            for x in input_features_or_literals:
                if isinstance(x, Feature):
                    input_features.append(x)
                    input_schema.append(x.converter.pyarrow_dtype)
                    continue
                if not isinstance(x, str):
                    raise TypeError("Embedding function literals must be strings")
                input_schema.append(pa.large_utf8())
            if features.__chalk_primary__ not in input_features:
                assert features.__chalk_primary__ is not None
                input_features.append(features.__chalk_primary__)
            error_str = embedding_provider.validate_input_schema(input_schema)
            if error_str:
                raise ValueError(
                    (
                        f"The first argument of the `embedding` function for feature '{output_feature.root_fqn}' returned an "
                        f"unsupported input schema for embedding model "
                        f"'{embedding_provider.get_provider_name()}/{embedding_provider.get_model_name()}': {error_str}."
                    )
                )

            async def fn(raw_inputs: DataFrame):
                # We need to build the input table by combining the literals with the features
                input_arrays: list[pa.Array | pa.ChunkedArray] = []
                raw_input_table = raw_inputs.to_pyarrow()
                assert features.__chalk_primary__ is not None
                pkeys = raw_input_table.column(features.__chalk_primary__.root_fqn)
                for x in input_features_or_literals:
                    if isinstance(x, Feature):
                        input_arrays.append(raw_input_table.column(x.root_fqn))
                    else:
                        input_arrays.append(pa.nulls(len(raw_input_table), pa.large_utf8()).fill_null(x))
                unified_inputs_table = pa.Table.from_arrays(
                    input_arrays, names=[f"col_{i}" for i in range(len(input_arrays))]
                )
                i = 0
                async for embeddings in embedding_provider.async_generate_embedding(unified_inputs_table):
                    t = pa.Table.from_arrays(
                        [embeddings, pkeys.slice(i, len(embeddings))],
                        [output_feature.root_fqn, features.__chalk_primary__.root_fqn],
                    )
                    i += len(embeddings)

                    yield t

            return OnlineResolver(
                function_definition="",
                filename="",
                fqn=f"__chalk__embedding__resolver__namespace__{output_feature.namespace}__name__{output_feature.name}",
                doc=None,
                inputs=[DataFrame[tuple(input_features)]],
                state=None,
                output=Features[DataFrame[output_feature, features.__chalk_primary__]],
                fn=fn,
                environment=None,
                tags=output_feature.tags,
                machine_type=None,
                default_args=[None],
                owner=output_feature.owner,
                timeout=None,
                cron=None,
                when=None,
                data_sources=None,
                is_sql_file_resolver=False,
                source_line=None,
                lsp_builder=get_resolver_error_builder(fn),
                parse=None,
                resource_hint=resource_hint,
                resource_group=resource_group,
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
