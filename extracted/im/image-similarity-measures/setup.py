# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['image_similarity_measures']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0',
 'opencv-python>=4.7.0.72,<5.0.0.0',
 'phasepack>=1.5,<2.0',
 'scikit-image>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'image-similarity-measures',
    'version': '0.3.6',
    'description': 'Evaluation metrics to assess the similarity between two images.',
    'long_description': '# Image Similarity Measures\n\nPython package and commandline tool to evaluate the similarity between two images with eight evaluation metrics:\n\n * <i><a href="https://en.wikipedia.org/wiki/Root-mean-square_deviation">Root mean square error (RMSE)</a></i>\n * <i><a href="https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio">Peak signal-to-noise ratio (PSNR)</a></i>\n * <i><a href="https://en.wikipedia.org/wiki/Structural_similarity">Structural Similarity Index (SSIM)</a></i>\n * <i><a href="https://www4.comp.polyu.edu.hk/~cslzhang/IQA/TIP_IQA_FSIM.pdf">Feature-based similarity index (FSIM)</a></i>\n * <i><a href="https://www.tandfonline.com/doi/full/10.1080/22797254.2019.1628617">Information theoretic-based Statistic Similarity Measure (ISSM)</a></i>\n * <i><a href="https://www.sciencedirect.com/science/article/abs/pii/S0924271618302636">Signal to reconstruction error ratio (SRE)</a></i>\n * <i><a href="https://ntrs.nasa.gov/citations/19940012238">Spectral angle mapper (SAM)</a></i>\n * <i><a href="https://ece.uwaterloo.ca/~z70wang/publications/quality_2c.pdf">Universal image quality index (UIQ)</a></i>\n\n## Installation\n\nSupports Python >=3.8.\n\n```bash\npip install image-similarity-measures\n```\n\n*Optional*: For faster evaluation of the FSIM metric, the `pyfftw` package is required, install via:\n\n```bash\npip install image-similarity-measures[speedups]\n```\n\n*Optional*: For reading TIFF images with `rasterio` instead of `OpenCV`, install:\n\n```bash\npip install image-similarity-measures[rasterio]\n```\n\n\n## Usage on commandline\n\nTo evaluate the similarity beteween two images, run on the commandline:\n\n```bash\nimage-similarity-measures --org_img_path=a.tif --pred_img_path=b.tif\n```\n\n**Note** that images that are used for evaluation should be **channel last**. The results are printed in \nmachine-readable JSON, so you can redirect the output of the command into a file.\n\n#### Parameters\n```\n  --org_img_path FILE   Path to original input image\n  --pred_img_path FILE  Path to predicted image\n  --metric METRIC       select an evaluation metric (fsim, issm, psnr, rmse,\n                        sam, sre, ssim, uiq, all) (can be repeated)\n```\n\n## Usage in Python\n\n```bash\nfrom image_similarity_measures.evaluate import evaluation\n\nevaluation(org_img_path="example/lafayette_org.tif", \n           pred_img_path="example/lafayette_pred.tif", \n           metrics=["rmse", "psnr"])\n```\n\n```bash\nfrom image_similarity_measures.quality_metrics import rmse\n\nrmse(org_img=np.random.rand(3,2,1), pred_img=np.random.rand(3,2,1))\n```\n\n## Contribute\n\nContributions are welcome! Please see README-dev.md for instructions.\n\n\n## Citation\nPlease use the following for citation purposes of this codebase:\n\n<strong>Müller, M. U., Ekhtiari, N., Almeida, R. M., and Rieke, C.: SUPER-RESOLUTION OF MULTISPECTRAL\nSATELLITE IMAGES USING CONVOLUTIONAL NEURAL NETWORKS, ISPRS Ann. Photogramm. Remote Sens.\nSpatial Inf. Sci., V-1-2020, 33–40, https://doi.org/10.5194/isprs-annals-V-1-2020-33-2020, 2020.</strong>\n',
    'author': 'UP42',
    'author_email': 'support@up42.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
