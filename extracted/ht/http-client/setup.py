from setuptools import setup

setup(
    name="http_client",
    version="0.1.22",
    packages=["http_client"],
    install_requires=["pycurl", "six"],
    author="Minh Son Huynh",
    author_email="minhsonftu@gmail.com",
    description="Fast and robust HTTP client based on PyCurl",
    url="https://github.com/huynhminhson/http_client",
    license="MIT",
)
