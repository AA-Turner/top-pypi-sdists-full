from setuptools import setup, find_packages

setup(
    name='gen_wrappers',
    version='0.7.1',
    author='d8ahazard',
    author_email='d8ahazard@gmail.com',
    description='A set of wrapper classes for various generative API projects',
    long_description_content_type='text/markdown',
    url='https://github.com/d8ahazard/gen_wrappers',  # Change this to your repository URL
    packages=find_packages(),
    install_requires=[
        "httpx",
        "requests",
        "pydantic",
        "fastapi"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
)
