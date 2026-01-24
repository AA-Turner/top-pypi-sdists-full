import setuptools

setuptools.setup(
    name="pb_bss_eval",
    version='0.0.2',
    author="Lukas Drude",
    author_email="mail@lukas-drude.de",
    description="EM algorithms for integrated spatial and spectral models.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=('pb_bss_eval.evaluation',)),
    py_modules=['pb_bss_eval', 'pb_bss_eval.evaluation'],
    install_requires=[
        'cached_property',
        'einops',
        'pystoi',
        'mir_eval',
        'pesq'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
