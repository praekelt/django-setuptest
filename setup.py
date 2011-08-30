from setuptools import setup, find_packages

setup(
    name='django-setuptest',
    version='0.0.3',
    description='Simple module enabling Django app testing via $ python setup.py test',
    long_description=open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/django-setuptest',
    packages=find_packages(),
    include_package_data=True,
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
