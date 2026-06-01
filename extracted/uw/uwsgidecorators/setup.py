from distutils.core import setup

setup(
    name='uwsgidecorators',
    version='1.1.0',
    author='Adriano Di Luzio',
    author_email='adrianodl@hotmail.it',
    py_modules=['uwsgidecorators', ],
    url='http://uwsgi-docs.readthedocs.org/en/latest/PythonDecorators.html',
    description='uwsgidecorators standalone package',
    keywords=["uwsgi", "uwsgidecorators"],
    classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Development Status :: 6 - Mature",
            "Environment :: Other Environment",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Topic :: Internet :: WWW/HTTP :: WSGI",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
            "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    long_description="""\
uwsgidecorators (http://uwsgi-docs.readthedocs.org/en/latest/) module on Pypi.
People asked for it and here it is.
    """,
)
