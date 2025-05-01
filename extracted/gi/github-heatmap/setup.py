from setuptools import find_packages, setup

setup(
    name="github_heatmap",
    author="malinkang",
    author_email="linkang.ma@gmail.com",
    url="https://github.com/malinkang/GitHubPoster",
    license="MIT",
    version="1.2.9",
    description="Make everything a GitHub svg poster and Skyline!",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "svgwrite",
        "pendulum==3.0.0",
        "colour",
    ],
    extras_require={
        "garmin": ["garminconnect"],
        "gpx": ["gpxpy"],
        "strava": ["stravalib"],
        "github": ["PyGithub"],
        "skyline": ["sdf_fork"],
        "todoist": ["pandas"],
        "all": [
            "twint_fork",
            "garminconnect",
            "gpxpy",
            "stravalib",
            "PyGithub",
            "sdf_fork",
            "pandas",
        ],
    },
    entry_points={
        "console_scripts": ["github_heatmap = github_heatmap.cli:main"],
    },
)
