from setuptools import setup


SETUP = {
    'name': "oci-image",
    'version': '1.0.0',
    'author': "Cory Johns",
    'author_email': "johnsca@gmail.com",
    'url': "https://github.com/juju-solutions/resource-oci-image",
    'py_modules': ['oci_image'],
    'install_requires': [
    ],
    'license': "Apache License 2.0",
    "long_description_content_type": "text/markdown",
    'long_description': open('README.md').read(),
    'description': 'Helper for dealing with OCI Image resources in '
                   'the charm operator framework',
}


if __name__ == '__main__':
    setup(**SETUP)
