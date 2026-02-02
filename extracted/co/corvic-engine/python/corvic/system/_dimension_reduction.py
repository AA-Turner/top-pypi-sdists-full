from typing import Any, Protocol

from numpy.typing import NDArray


class DimensionReducer(Protocol):
    def reduce_dimensions(
        self, vectors: NDArray[Any], output_dimensions: int, metric: str
    ) -> NDArray[Any]: ...


class UmapDimensionReducer(DimensionReducer):
    def reduce_dimensions(
        self, vectors: NDArray[Any], output_dimensions: int, metric: str
    ):
        n_neighbors = 15
        init = "spectral"
        # y spectral initialization cannot be used when n_neighbors
        # is greater or equal to the number of samples
        if vectors.shape[0] <= n_neighbors:
            init = "random"
            # n_neighbors is larger than the dataset size; truncating to X.shape[0] - 1
            n_neighbors = vectors.shape[0] - 1

        if vectors.shape[0] <= output_dimensions + 1:
            init = "random"

        # import umap locally to reduce loading time
        # TODO(Hunterlige): Replace with lazy_import
        from umap import umap_ as umap

        projector = umap.UMAP(
            n_neighbors=n_neighbors,
            n_components=output_dimensions,
            metric=metric,
            init=init,
            low_memory=False,
            verbose=True,
        )
        return projector.fit_transform(vectors)


class TruncateDimensionReducer(DimensionReducer):
    def reduce_dimensions(
        self, vectors: NDArray[Any], output_dimensions: int, metric: str
    ) -> NDArray[Any]:
        return vectors[:, :output_dimensions]
