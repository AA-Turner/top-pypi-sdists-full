import numpy as np
import polars as pl

from corvic.result import InternalError, InvalidArgumentError, Ok
from corvic.system._embedder import (
    EmbedTextContext,
    EmbedTextResult,
    TextEmbedder,
)


class RandomTextEmbedder(TextEmbedder):
    """Embed inputs by choosing random vectors.

    Useful for testing.
    """

    def embed(
        self, context: EmbedTextContext
    ) -> Ok[EmbedTextResult] | InvalidArgumentError | InternalError:
        rng = np.random.default_rng()

        match context.expected_coordinate_bitwidth:
            case 64:
                coord_dtype = pl.Float64()
            case 32:
                coord_dtype = pl.Float32()

        return Ok(
            EmbedTextResult(
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
