from setuptools import setup

setup(
    name='pip-hello-world',
    version='0.1',
    license='BSD',
    author='benlindsay',
    author_email='benjlindsay@gmail.com',
    url='http://www.hello.com',
    long_description="README.txt",
    packages=['helloworld', 'helloworld.images'],
    include_package_data=True,
    package_data={'helloworld.images' : ['hello.gif']},
    description="Hello World testing setuptools",
)
