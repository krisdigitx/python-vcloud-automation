import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "vuman",
    version = "2.5",
    author = "KSHK",
    author_email = "alpha@krisindigitalage.com",
    description = ("VCloud Automation Tool"),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "https://github.com/krisdigitx/python-vcloud-automation",
    packages=['vcloud-automation'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points = {
    'console_scripts': [
        'vcloud-auto = vcloud-automation.vcloud-automation:main',
    ],
    }
)
