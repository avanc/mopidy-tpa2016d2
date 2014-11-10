from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


setup(
    name='Mopidy-TPA2016D2',
    version=get_version('mopidy_tpa2016d2/__init__.py'),
    url='',
    license='Apache License, Version 2.0',
    author='Sven Klomp',
    author_email='mail@klomp.eu',
    description='Mopidy extension for controlling volume on TPA2016D2 amplifier',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 0.19',
        'Pykka >= 1.1',
    ],
    entry_points={
        'mopidy.ext': [
            'tpa2016d2 = mopidy_tpa2016d2:Extension',
        ],
    },
)
