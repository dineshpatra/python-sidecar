# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='python-sidecar',
    version='2.0',
    description='A sidecar REST api to maintain the nova evacuation process',
    author='Binoy MV, Dinesh Patra',
    author_email='binoy.mv@poornam.com, dinesh.p@poornam.com',
    install_requires=[
        "pecan",
    ],
    license='NephoScale',
    keywords='Nova evacuation',
    test_suite='sidecar',
    packages=find_packages(exclude=['ez_setup'])
)
