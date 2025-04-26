#!/bin/python
# coding: utf-8

##########################################################################################################################################

from setuptools import setup

##########################################################################################################################################

def readme():
	with open("README.md") as f:
		return f.read()

##########################################################################################################################################

DESCRIPTION = "A wrapper to JSON parsers allowing comments, multiline strings and trailing commas"

##########################################################################################################################################

setup (
	name = "jsoncomment",
	version = "0.4.2",
	description = DESCRIPTION,
	long_description = readme(),
	long_description_content_type = "text/markdown",
	author = "Gaspare Iengo",
	author_email = "gaspareiengo@gmail.com",
	keywords = "json comments multiline",
	url = "https://bitbucket.org/Dando_Real_ITA/json-comment",
	license = "MIT",

	classifiers = [
		"Development Status :: 4 - Beta",
		"Intended Audience :: End Users/Desktop",
		"License :: OSI Approved :: MIT License",
		"Natural Language :: English",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3.3",
		"Topic :: Software Development :: Pre-processors",
		"Topic :: Text Editors :: Text Processing",
	],

	packages = ["jsoncomment"],
	python_requires = ">=3.3",
	install_requires = [
		"json-spec"
	],
	extras_require = {
		"ujson":  ["ujson>=1.30"],
	},

	include_package_data = True,
	zip_safe = False
)

##########################################################################################################################################
