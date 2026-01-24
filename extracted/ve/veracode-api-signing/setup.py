from importlib.util import find_spec, module_from_spec

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PROJECT_NAME = 'veracode-api-signing'
# TODO: replace PROJECT_URL with new GitHub location when open-sourced
PROJECT_URL = "https://docs.veracode.com/r/t_install_api_authen"
doclink = "Please visit {}.".format(PROJECT_URL)

spec = find_spec('veracode_api_signing._version')
module = module_from_spec(spec)
spec.loader.exec_module(module)

with open('veracode_api_signing/_version.py') as f:
    exec(f.read())

setup(
    name=PROJECT_NAME,
    version=__version__,
    description='Easily sign any request destined for the Veracode API Gateway',
    long_description=doclink,
    author='Veracode',
    url=PROJECT_URL,
    packages=[
        'veracode_api_signing'
    ],
    package_dir={
        'veracode_api_signing': 'veracode_api_signing'
    },
    entry_points={
        'console_scripts': [
            'veracode_hmac_auth = veracode_api_signing.cli:main'
        ],
        'httpie.plugins.auth.v1': [
            'httpie_veracode_hmac_auth = ' +
            'veracode_api_signing.plugin_httpie:HttpiePluginVeracodeHmacAuth',
        ],
    },
    python_requires='>=3.9',
    include_package_data=True,
    install_requires=[
        'docopt>=0.6.2',
        'httpie>=3.2.4',
        'pip>=25.3',
        'requests>=2.27.1',
        'setuptools>=70.0.0'
    ],
    license="MIT",
    zip_safe=False,
    keywords='veracode-api-signing',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ]
)
