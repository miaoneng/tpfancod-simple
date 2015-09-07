import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="A simplified fan controller for Thinkpad series based in tpfancod",
    version="0.1.a",
    author="striges",
    author_email="sugar1987cn@gmail.com",
    description=("An demonstration of how to create, document, and publish "
                 "to the cheese shop a5 pypi.org."),
    license="BSD 3-Clauses",
    keywords="Thinkpad fancontrol",
    url="http://github.com/striges/tpfancod-simple",
    packages=['tpfancod_simple'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
