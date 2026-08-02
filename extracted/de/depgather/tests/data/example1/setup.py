from setuptools import setup  # pyright: ignore[reportMissingModuleSource]

setup(
	name="example",
	version="0.1.0",
	install_requires=[
		"requirements-parser>=0.13.0",
		"tomli>=2.2.1",
	],
	extras_require={
		"dev": [
			"basedpyright>=1.39.7",
			"coverage>=7.6.12",
			"pytest>=8.3.5",
			"ruff>=0.11.0",
		],
	},
)
