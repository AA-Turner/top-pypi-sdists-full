from contextlib import ExitStack
from collections import OrderedDict
import logging
import math

import numpy

import rasterio
from rasterio.windows import Window, subdivide
from rasterio._vendor import snuggs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(inputs, output):
    with ExitStack() as stack:
        sources = [
            stack.enter_context(rasterio.open(path))
            for path in inputs
        ]

        first = sources[0]
        kwargs = first.profile
        # kwargs.update(**creation_options)
        dtype = "uint8" or first.meta["dtype"]
        kwargs["dtype"] = dtype

        work_windows = [Window(0, 0, 16, 16)]

        dst = None
        wi = 0

        while wi < len(work_windows):
            window = work_windows[wi]
            ctxkwds = OrderedDict()

            for si, src in enumerate(sources):
                ctxkwds[f"_{si + 1}"] = src.read(masked=True, window=window)

            try:
                res = snuggs.eval("(* 0.5 _1)", **ctxkwds)
            except snuggs.ExpressionError as err:
                logger.error(f"Caught exception: {err=}")
                return

            # The first iteration is only to get sample results and from them
            # compute some properties of the output dataset.
            if wi == 0 and not dst:
                kwargs["count"] = res.shape[0] if len(res.shape) == 3 else 1
                dst = stack.enter_context(rasterio.open(output, "w", **kwargs))
                max_pixels = 16 * 1.0e+6 / (numpy.dtype(dst.dtypes[0]).itemsize * dst.count)
                chunk_size = int(math.floor(math.sqrt(max_pixels)))
                work_windows.extend(
                    subdivide(
                        Window(0, 0, dst.width, dst.height),
                        chunk_size,
                        chunk_size
                    )
                )

            # In subsequent iterations we write results.
            else:
                results = res.astype(dtype)

                if isinstance(results, numpy.ma.core.MaskedArray):
                    results = results.filled(float(kwargs["nodata"]))
                    if len(results.shape) == 2:
                        results = numpy.ma.expand_dims(results, axis=0)
                elif len(results.shape) == 2:
                    results = numpy.expand_dims(results, axis=0)

                dst.write(results, window=window)

            wi += 1


# if __name__ == "__main__":
inputs = ["tests/data/RGB.byte.tif"]
output = "test_calc.tif"
main(inputs, output)
