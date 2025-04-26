import setuptools

setuptools.setup(
    name='pyzed',
    version="1.3.0",
    install_requires=[
        'durationpy',
        'python-dateutil',
        'requests',
    ],
    py_modules=['pyzed'],
    python_requires='>=3.3',
)
