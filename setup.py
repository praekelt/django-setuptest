import codecs
from os import path
from setuptools import setup, find_packages


def read(filepath):
    filepath = path.join(path.dirname(__file__), filepath)
    return codecs.open(filepath, 'r', 'utf-8').read()

description = read('README.rst') + read('AUTHORS.rst') + read('CHANGELOG.rst')

setup(
    name='django-setuptest',
    version='0.1.2',
    description='Simple test suite enabling Django app testing via $ python setup.py test',
    long_description=description,
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/django-setuptest',
    packages=find_packages(),
    install_requires=[
        'coverage',
        'django',
        'pep8',
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
