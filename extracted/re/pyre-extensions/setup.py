
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyre-extensions",
    version="0.0.32",
    author="Facebook",
    author_email="pyre@fb.com",
    description="Type system extensions for use with the pyre type checker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pyre-check.org",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development',
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    install_requires=["typing-inspect", "typing-extensions"],
)
        