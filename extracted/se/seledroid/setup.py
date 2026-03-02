from os.path import dirname, join, abspath
from setuptools import setup

setup(
    name="seledroid",
    version="2.0.4",
    description="Android WebDriver based WebView",
    long_description=open(join(abspath(dirname(__file__)), "README.md")).read(),
    long_description_content_type="text/markdown",
    author="luanon404",
    author_email="luanon404@gmail.com",
    url="https://github.com/luanon404/Seledroid",
    python_requires="~=3.7",
    package_dir={
        "seledroid": "seledroid",
        "seledroid.webdriver": "seledroid/webdriver"
    },
    packages=[
        "seledroid",
        "seledroid.webdriver",
        "seledroid.webdriver.chrome",
        "seledroid.webdriver.remote",
        "seledroid.webdriver.common",
        "seledroid.webdriver.support"
    ],
    include_package_data=True,
    install_requires=[""],
    zip_safe=False
)
