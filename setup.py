# setup.py
from setuptools import setup, find_packages

setup(
    name="spiffy",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click==7.1.2",
        "pandas",
        "spotipy",
        "pydantic",
        "pydantic-settings",
    ],
    entry_points="""
        [console_scripts]
        spiffy=spiffy.cli:cli
    """,
)
