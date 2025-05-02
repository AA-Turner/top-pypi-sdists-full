# vi:et:ts=4 sw=4 sts=4
import os
import sys

from setuptools import setup, find_packages


_DESC = (
    'pyparser is a collection of classes to make it easier to parse text data'
    'in a pythonic way.'
)

# add our path to sys.path
_PATH = os.path.join(os.path.dirname(__file__), 'src')
if _PATH not in sys.path:
    sys.path.append(_PATH)


from pyparser import __version__  # noqa


def main():
    """ Creates our package """

    install_requires = []

    with open('requirements.txt') as ifp:
        for dependency in ifp.readlines():
            dependency = dependency.strip()

            if len(dependency) == 0 or dependency.startswith('#'):
                continue

            install_requires.append(dependency)

    setup(
        name='pyparser',
        version=__version__,
        description=_DESC,
        packages=find_packages('src'),
        package_dir={'': 'src'},
        install_requires=install_requires,
        zip_safe=True,
        test_suite='tests',
        author='Gary Kramlich',
        author_email='grim@reaperworld.com',
        url='http://bitbucket.org/rw_grim/pyparser',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
    )


if __name__ == '__main__':
    main()

