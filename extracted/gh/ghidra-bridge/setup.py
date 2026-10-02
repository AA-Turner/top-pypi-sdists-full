import setuptools
import subprocess

with open("README.md", "r") as fh:
    long_description = fh.read()

# determine the version, then write it out into the bridge.py file
version = (
    subprocess.check_output("git describe --tags", shell=True).decode("utf-8").strip()
)
# check if this is a non-tag release and remark it as a dev release
if "-" in version:
    ver, commits, hash = version.split("-")
    version = ver + ".dev" + commits

setuptools.setup(
    name="ghidra_bridge",
    version=version,
    author="justfoxing",
    author_email="justfoxingprojects@gmail.com",
    description="RPC bridge from Python to Ghidra Jython",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/justfoxing/ghidra_bridge",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["jfx_bridge>=1.0.0"],
)
