import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="ynabi",
    version="1.0.0",
    author="Andreas Skielboe",
    author_email="andreas@skielboe.com",
    description=("Import bank transactions to YNAB."),
    license="The Unlicense",
    keywords="",
    url="",
    packages=find_packages(),
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Utilities",
        "License :: All Rights Reserved",
    ],
    install_requires=["requests"],
    include_package_data=True,
)
