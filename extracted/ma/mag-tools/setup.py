from setuptools import setup, find_packages

setup(
    name='mag_tools',
    version='0.3.142',
    packages=find_packages(),
    install_requires=[],
    author='xlcao',
    author_email='xl_cao@hotmail.com',
    description='常用工具包',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='http://gitlab.magnetitech.com:8088/sources/frame/py-frame/mag_tools.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)