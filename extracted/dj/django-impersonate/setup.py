import os
from distutils.core import setup

project_name = 'impersonate'
long_description = open('README.rst').read()

# Idea from django-registration setup.py
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk(project_name):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.') or dirname == '__pycache__':
            del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[(len(project_name) + 1) :]
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(
    name='django-impersonate',
    version=__import__(project_name).get_version(),
    package_dir={project_name: project_name},
    packages=packages,
    package_data={project_name: data_files},
    description='Django app to allow superusers to impersonate other users.',
    author='Peter Sanchez',
    author_email='pjs@petersanchez.com',
    license='BSD License',
    url='https://code.netlandish.com/~petersanchez/django-impersonate',
    long_description=long_description,
    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Environment :: Web Environment',
    ],
)
