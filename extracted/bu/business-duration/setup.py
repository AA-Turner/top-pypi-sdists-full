from setuptools import setup

with open('README.rst') as f:
    readme = f.read()
	
setup(name='business_duration',
	version='0.67',
	description='Calculates business duration in days, hours, minutes and seconds by excluding weekends, public holidays and non-business hours',
	long_description=readme,
	url='https://github.com/gnaneshwar441/Business_Duration',
	author='Gnaneshwar G',
	author_email='gnaneshwar441@gmail.com',
	license='MIT',
	packages=['business_duration'],
	keywords = ['business', 'duration', 'time', 'hour', 'day', 'working'],
    install_requires=['numpy', 'pandas'],
	zip_safe=False)