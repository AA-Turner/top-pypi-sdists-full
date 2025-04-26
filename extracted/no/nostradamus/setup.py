from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="nostradamus",
    version="0.1",
    description="A time-series forecasting python package",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/naftalic/nostradamus",
    author="Naftali Cohen",
    author_email="naftalic@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["nostradamus"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "weather-reporter=weather_reporter.cli:main",
        ]
    },
)
