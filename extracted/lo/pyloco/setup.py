"pyloco setup module."

def main():

    from setuptools import setup
    from pyloco.manage import PylocoManager as mgr

    console_scripts = ["pyloco=pyloco.__main__:main"]

    #package_data={'pyloco': ["helptask.js", "helptask.css"]},

    setup(
        name=mgr._name_,
        version=mgr._version_,
        description=mgr._description_,
        long_description=mgr._long_description_,
        author=mgr._author_,
        author_email=mgr._author_email_,
        url=mgr._url_,
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Build Tools",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
        ],
        keywords="task",
        packages=[ "pyloco" ],
        include_package_data=True,
        install_requires=["ushlex", "websocket-client", "twine",
                          "typing", "SimpleWebSocketServer"],
        entry_points={ "console_scripts": console_scripts },
        test_suite="tests.pyloco_unittest_suite",
        project_urls={
            "Bug Reports": "https://github.com/grnydawn/pyloco/issues",
            "Source": "https://github.com/grnydawn/pyloco",
        }
    )

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
