from setuptools import setup, find_packages
from os import path
from io import open

_here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(_here, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CAMS_radiation_client',
    version='0.0.1',
    description=('CAMS radiation client - for solar radiation data.'),
    author='Giorgio Balestrieri',
    author_email='gbalestrieri@tesla.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples', 'sandbox']),
    install_requires=['pandas', 'requests']
    )