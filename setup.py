#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages
import os

VERSION = __import__('foafssl').__version__

def read(*path):
    return open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *path)).read()

setup(
    name='django-foafssl',
    version=VERSION,
    description='FOAF+SSL tools for Django',
    long_description=read('docs', 'intro.txt'),
    author='Duy',
    author_email='duy@rhizomtik.net',
    url='http://git.rhizomatik.net/django-foafssl',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Framework :: Django',
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='foaf, ssl, foaf+ssl, certificate, client certificate, authentication, authorization,django',
    include_package_data=True,
    zip_safe=False,
    # Ignore the tarballs we built our own in a source distribution
    exclude_package_data={
        'requirements': ['%s/*.tar.gz' % VERSION],
    },
    # include templates and docs
#    setup_requires=[
#        'setuptools_dummy',
#    ],

)

