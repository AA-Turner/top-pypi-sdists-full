from setuptools import setup, find_packages

# reading requirements.txt file for install_requires field
packages = []
with open('requirements.txt') as fp:
    for line in fp:
        line = line.replace(',', '').strip()
        if line.startswith('#'): continue
        if line != '': packages.append(line)

setup(
    name = 'aider',         
    packages = find_packages(),
    version = '0.2.6',      
    license='MIT',
    description = 'general utility functions',     
    long_description = open('README.rst').read(),
    author = 'Rajat',
    # author_email = 'dummy@gmail.com',     
    # url = 'https://github.com/rnm-patel/aider',
    # download_url = 'https://github.com/rnm-patel/aider/archive/v1.0.0-alpah.tar.gz',
    keywords = ['utility', 'generic', 'log', 'config', 'calendar'],
    include_package_data=True,
    install_requires=packages,
    #  project_urls={
    #     'Source Code': 'https://github.com/rnm-patel/aider',
    # },
    classifiers=[
        'Development Status :: 3 - Alpha',   
        'Intended Audience :: Developers',      
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)