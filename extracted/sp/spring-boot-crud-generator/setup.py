from setuptools import setup, find_packages

setup(
    name="spring-boot-crud-generator",
    version="0.0.8",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "spring-crud=springcrud.crud:main",
        ],
    },
    install_requires=[],
    author="wonow",
    author_email="wonowdaily@gmail.com",
    description="Spring Boot CRUD 코드 생성기",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wonowonow/spring-boot-crud-generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 