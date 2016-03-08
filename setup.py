#!/usr/bin/env python

from setuptools import setup

setup (
    setup_requires=['pbr'],
    pbr=True,
    package_dir={ 'cdwcore':'src' },
    packages=['cdwcore' ],
    test_suite='test'
)
