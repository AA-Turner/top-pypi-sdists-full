from setuptools import setup

setup(
    name="interpolate",
    version="0.5.2",

    py_modules=['interpolate'],

    zip_safe=True,

    author="Ed Kellett",
    author_email="edk141@gmail.com",
    license="MIT",
    url="http://edk141.co.uk/a/interpolate",

    description="string interpolation",

    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],

    long_description='''
It's a thing for interpolating strings.

See http://edk141.co.uk/a/interpolate
'''
)
