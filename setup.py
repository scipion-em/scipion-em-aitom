"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='scipion-em-aitom',  # Required
    version='0.1',  # Required
    description='Scipion AITom plugin.',  # Required
    long_description=long_description,  # Optional
    url='https://github.com/scipion-em/scipion-em-aitom',  # Optional
    author='you',  # Optional
    author_email='you@yourinstitution.email',  # Optional
    keywords='scipion cryoem imageprocessing scipion-2.0',  # Optional
    packages=find_packages(),
    install_requires=[requirements],
    package_data={  # Optional
       'myplugin': ['logo.gif', 'protocols.conf'],
    }
)
