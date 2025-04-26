import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='cron-schedule-triggers',
      version='0.0.11',
      description='Cron Schedule Triggers ~ A library for determining Quartz Cron schedule trigger dates.',
      url='https://gitlab.com/dameon.andersen/cstriggers',
      author='Dameon Andersen',
      author_email='dameon.andersen@facteon.global',
      packages=setuptools.find_packages(),
      python_requires='>=3.6',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      licence="MIT",
      zip_safe=False,
      keywords="quartz cron notation cronjob aws rate schedule scheduling office/business triggers tasks jobs runner "
               "rq queue apscheduler calendar date datetime",
      install_requires=[
            line.rstrip('\n') for line
            in open("cstriggers/requirements/base.txt", "r")
      ]
)
