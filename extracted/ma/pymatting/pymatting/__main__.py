import argparse
import sys
from pymatting import *

def main(argv=None):
    """
    CLI interface for cutting out a subject from a given input image and trimap.

    Examples
    --------
    >>> pymatting image.png trimap.png cutout.png
    """
    description = "Generate a cutout image from an input image and an input trimap using closed-form alpha matting and multi-level foreground estimation."
    parser = argparse.ArgumentParser(prog="cutout", description=description)
    parser.add_argument("image", metavar="image.png", type=str, help="Path of input image")
    parser.add_argument("trimap", metavar="trimap.png", type=str, help="Path of input trimap")
    parser.add_argument("cutout", metavar="cutout.png", type=str, help="Path of output cutout image")
    parser.add_argument("--scale", type=float, default=1.0, help="Scale factor applied to the input image and trimap (default: 1.0)")
    parser.add_argument("--method", type=str, default="cf", choices=["cf", "sm", "knn", "lkm"], help="Alpha matting method to use (default: cf)")
    parser.add_argument("--radius", type=int, default=None, help="Neighborhood radius for the matting Laplacian (default for cf: 1, default for lkm: 10)")
    parser.add_argument("--epsilon", type=float, default=1e-7, help="Epsilon value for the matting Laplacian (default: 1e-7)")
    args = parser.parse_args(argv)

    scale = args.scale
    method = args.method
    radius = args.radius
    epsilon = args.epsilon

    image = load_image(args.image, "RGB", scale, "box")
    trimap = load_image(args.trimap, "GRAY", scale, "nearest")

    if method == "cf":
        if radius is None:
            radius = 1

        alpha = estimate_alpha_cf(image, trimap, laplacian_kwargs={
            "radius": radius,
            "epsilon": epsilon,
        })

        foreground = estimate_foreground_ml(image, alpha)

    elif method == "knn":
        alpha = estimate_alpha_knn(image, trimap)

        foreground = estimate_foreground_ml(image, alpha)

    elif method == "lkm":
        if radius is None:
            radius = 10

        alpha = estimate_alpha_lkm(image, trimap, laplacian_kwargs={
            "radius": radius,
            "epsilon": epsilon,
        })

        foreground = estimate_foreground_ml(image, alpha)

    elif method == "sm":
        alpha, foreground, _ = estimate_alpha_sm(
            image, trimap, return_foreground_background=True
        )

    cutout = stack_images(foreground, alpha)
    save_image(args.cutout, cutout)

    return 0


if __name__ == "__main__":
    sys.exit(main())
