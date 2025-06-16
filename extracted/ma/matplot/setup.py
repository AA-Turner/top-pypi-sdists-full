# -*- coding: utf-8 -*-
"pyloco task setup script"

if __name__ == "__main__":

    from setuptools import setup, find_packages

    __taskname__ = "matplot"

    setup(
        name="matplot",
        version="0.1.9",
        packages=find_packages(),
        package_data={},
        install_requires=["pyloco>=0.0.134", "matplotlib>=3.1.1"],
        entry_points = {"pyloco.task": ["{taskname} = {taskname}:entry_task".format(taskname=__taskname__)]},
    )
