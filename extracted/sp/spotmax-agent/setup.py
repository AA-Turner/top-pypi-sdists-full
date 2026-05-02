import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spotmax-agent",
    version="0.0.8",
    author="liuzoxan",
    author_email="liuzoxan@gmail.com",
    description="spotmax agent package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # 'pyautogui',
        # 'Django >= 1.11, != 1.11.1, <= 2',
    ],
    entry_points={
        'console_scripts': [
            'spotmax-agent=spotmax_agent:main'
        ],
    }
)
