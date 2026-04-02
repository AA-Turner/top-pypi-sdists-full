from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except ImportError:
    long_description = ''

setup(
    name='atlassian-jwt',
    packages=['atlassian_jwt'],
    version='3.0.0',
    description='JSON web token: pyjwt plus Atlassian query-string-hash claim',
    long_description=long_description,
    author='Atlassian',
    author_email='bedwards@atlassian.com',
    url='https://bitbucket.org/atlassian/atlassian-jwt-py',
    install_requires=[
        'PyJWT>=2.2.0'
    ],
    keywords=[
        'jwt',
        'json',
        'web',
        'token',
        'pyjwt',
        'atlassian',
        'connect',
        'addon',
        'query',
        'string',
        'hash',
        'qsh',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
