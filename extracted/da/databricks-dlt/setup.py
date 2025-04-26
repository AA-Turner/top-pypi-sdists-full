from importlib.machinery import SourceFileLoader

from setuptools import find_namespace_packages, setup

# The package isn't loaded before it is installed, so we can't directly import the module, which is why we need to read it from the file.
version = SourceFileLoader("stubs.dlt.version", "version.py").load_module().VERSION

with open("README.md") as f:
    readme_contents = f.read()

with open("LICENSE.md") as f:
    license_contents = f.read()

# Append the text from LICENSE.md to the end of the README.md content
readme_contents_with_license = readme_contents + "\n" + license_contents

try:
    # Overwrite the existing README.md file with the readme + license content for the setup() step.
    # The original version will be restored to it's original state after setup() finishes.
    with open("README.md", "w") as f:
        f.write(readme_contents_with_license)

    # Used strictly for requirements.txt.
    def remove_comments_and_empty_lines(lines):
        def is_comment_or_empty(line):
            stripped = line.strip()
            return stripped == "" or stripped.startswith("#")

        return [line for line in lines if not is_comment_or_empty(line)]

    with open("requirements.txt", "r") as f:
        REQUIREMENTS = remove_comments_and_empty_lines(f.readlines())

    setup(
        name="databricks-dlt",
        version=version,
        author_email="feedback@databricks.com",
        license="Databricks Proprietary License",
        license_files=("LICENSE.md", "NOTICE.md"),
        long_description=readme_contents_with_license,
        long_description_content_type="text/markdown",
        packages=find_namespace_packages(include=["dlt"]),
        include_package_data=True,
        python_requires=">=3.9",
        install_requires=REQUIREMENTS,
        author="Databricks",
        description="Databricks DLT Library",
    )
finally:
    # Restore the README.md file to it's original state
    with open("README.md", "w") as f:
        f.write(readme_contents)
