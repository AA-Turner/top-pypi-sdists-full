from distutils.core import setup

setup(
    name='rentdynamics',
    version='1.1.1',
    description='Rent Dynamics Client Library',
    author='Rent Dynamics',
    author_email='dev-accounts@rentdynamics.com',
    url='https://github.com/RentDynamics/rentdynamics-py',
    packages=['rentdynamics'],
    install_requires=[
        'requests',
    ]
)
