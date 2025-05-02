from setuptools import setup
import os

import math_eval.math_eval as package


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')) as f:
    readme = f.read()

setup(
    name='math_eval',
    version=package.__version__,
    packages=['math_eval'],
    # package_data={'math_eval': ['cmap/*.pickle.gz']},
    install_requires=[],
    extras_require={
        "test_math_eval": ["pandas"]
    },
    description='Tool for safe (or less safe) evaluation of strings as math expressions',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT/X',
    author='Mark Johnston Olson',
    author_email='mjolsonsfca@gmail.com',
    url='https://github.com/molsonkiko/math_eval',
    # scripts=[ # maybe __main__ should be considered a script?
    # ],
    keywords=[
        'math',
        'safe eval tool',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Text Processing',
    ],
)