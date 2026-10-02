from distutils.core import setup
setup(
  name="PythonDNS",
  packages=["PythonDNS"],
  version="0.1",
  license="MIT",
  description="Python-based DNS Interception and Proxy",
  url="https://github.com/endail/PythonDNS",
  download_url="https://github.com/endail/PythonDNS/archive/0.1.tar.gz",
  keywords=["python", "dns"],
  install_requires=[
          "dnslib"
      ],
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
  ],
)