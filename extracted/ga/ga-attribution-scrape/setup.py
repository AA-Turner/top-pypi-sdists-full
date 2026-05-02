import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ga-attribution-scrape",
    version="0.2.1",
    author="Lewis Bryan",
    author_email="lewis.a.bryan@googlemail.com",
    description="Scrapes attribution data from GAs Model Comparison Tool through JS Network and sends to Bigquery.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lewisaustinbryan/ga-attribution-scrape",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'google-auth',
        'google-api-python-client',
        'google-cloud-bigquery',
        'oauth2client',
        'pandas-gbq',
        'pandas',
        'tqdm'
      ],
    python_requires='>=3.6',
)
