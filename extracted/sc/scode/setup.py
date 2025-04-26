import setuptools
from scode import __version__ as scode_version

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="scode", # Replace with your own username
    version=scode_version,
    maintainer_email="smchung218@gmail.com",
    description="The Private Package of Showm Company.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/showm-dev/Standard",
    packages=setuptools.find_packages(),
    package_data={
        'scode': ['Bell.wav'],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
    install_requires=[
        'selenium==3.141.0',
        'Pillow==9.5.0',
        'urllib3==1.26.12',
        'fake-useragent==1.5.1',
        'paramiko',
        'packaging',
        'dropbox',
        'python-dateutil',
        'requests',
        'pyperclip',
        'chromedriver-autoinstaller',
        'anticaptchaofficial',
        'python_anticaptcha',
        'feedparser',
        'tqdm',
        'chardet',
        'docx2txt',
        'pyautogui',
        'python-telegram-bot==13.15'
    ],
)
