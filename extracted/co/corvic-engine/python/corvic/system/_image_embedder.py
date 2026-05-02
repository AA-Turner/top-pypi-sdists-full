from io import BytesIO
from typing import Any

import numpy as np
import polars as pl
from PIL import Image, UnidentifiedImageError

from corvic.result import InternalError, InvalidArgumentError, Ok
from corvic.system._embedder import (
    EmbedImageContext,
    EmbedImageResult,
    ImageEmbedder,
)


class RandomImageEmbedder(ImageEmbedder):
    """Embed inputs by choosing random vectors.

    Useful for testing.
    """

    def embed(
        self, context: EmbedImageContext
    ) -> Ok[EmbedImageResult] | InvalidArgumentError | InternalError:
        rng = np.random.default_rng()

        match context.expected_coordinate_bitwidth:
            case 64:
                coord_dtype = pl.Float64()
            case 32:
                coord_dtype = pl.Float32()

        return Ok(
            EmbedImageResult(
                context=context,
                embeddings=pl.Series(
                    rng.random(
                        size=(len(context.inputs), context.expected_vector_length)
                    ),
                    dtype=pl.List(
                        coord_dtype,
                    ),
                ),
            )
        )


def image_from_bytes(
    image: bytes, mode: str = "RGB"
) -> Ok[Image.Image] | InvalidArgumentError:
    try:
        return Ok(Image.open(BytesIO(initial_bytes=image)).convert(mode=mode))
    except UnidentifiedImageError:
        return InvalidArgumentError("invalid image format")


class Clip(ImageEmbedder):
    """Clip image embedder.

    CLIP (Contrastive Language-Image Pre-Training) is a neural network trained
    on a variety of (image, text) pairs. It can be instructed in natural language
    to predict the most relevant text snippet, given an image, without
    directly optimizing for the task, similarly to the zero-shot capabilities of
    GPT-2 and 3. We found CLIP matches the performance of the original ResNet50
    on ImageNet “zero-shot” without using any of the original 1.28M labeled examples,
    overcoming several major challenges in computer vision.
    """

    def embed(
        self, context: EmbedImageContext
    ) -> Ok[EmbedImageResult] | InvalidArgumentError | InternalError:
        import torch
        from transformers import CLIPModel, CLIPProcessor

        model: CLIPModel = CLIPModel.from_pretrained(  # pyright: ignore[reportUnknownMemberType, reportAssignmentType]
            pretrained_model_name_or_path="openai/clip-vit-large-patch14"
        )
        processor: CLIPProcessor = CLIPProcessor.from_pretrained(  # pyright: ignore[reportUnknownMemberType, reportAssignmentType]
            "openai/clip-vit-large-patch14"
        )
        model.eval()
        match context.expected_coordinate_bitwidth:
            case 64:
                coord_dtype = pl.Float64()
            case 32:
                coord_dtype = pl.Float32()

        images = list[Image.Image]()
        for initial_bytes in context.inputs:
            match image_from_bytes(image=initial_bytes):
                case Ok(image):
                    images.append(image)
                case InvalidArgumentError() as err:
                    return err

        with torch.no_grad():
            inputs: dict[str, torch.FloatTensor] = processor(  # pyright: ignore[reportAssignmentType]
                images=images, return_tensors="pt"
            )
            image_features = model.get_image_features(
                pixel_values=inputs["pixel_values"]
            )

        image_features_numpy: np.ndarray[Any, Any] = image_features.numpy()  #  pyright: ignore[reportUnknownMemberType]
        return Ok(
            EmbedImageResult(
                context=context,
                embeddings=pl.Series(
                    values=image_features_numpy[:, : context.expected_vector_length],
                    dtype=pl.List(
                        coord_dtype,
                    ),
                ),
            )
        )


class CombinedImageEmbedder(ImageEmbedder):
    def __init__(self):
        self._clip_embedder = Clip()
        self._random_embedder = RandomImageEmbedder()

    def embed(
        self, context: EmbedImageContext
    ) -> Ok[EmbedImageResult] | InvalidArgumentError | InternalError:
        if context.model_name == "random":
            return self._random_embedder.embed(context)
        return self._clip_embedder.embed(context)
