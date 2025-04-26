import os

import coiled

try:
    from prefect_dask import DaskTaskRunner  # type: ignore
except ImportError:
    raise ImportError("`prefect-dask` not installed, cannot create `CoiledTaskRunner`.") from None
else:

    class CoiledTaskRunner(DaskTaskRunner):
        async def _start(self, *args, **kwargs):
            # If this is running on an existing cluster, re-use it if
            # cluster name not explicitly given.
            # Has to be in _start, b/c this is called just before flow runtime,
            # by the Prefect Worker implementation.
            # TODO: Configurable in re-using cluster for flows?
            name = self.cluster_kwargs.get("name")
            cluster_name = os.environ.get("COILED__CLUSTER_NAME")
            if not name and cluster_name:
                self.cluster_kwargs["name"] = cluster_name

            self.cluster_class = coiled.Cluster  # extra sure we're using Coiled here
            return await super()._start(*args, **kwargs)
