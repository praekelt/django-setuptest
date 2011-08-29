Django Setuptest
================
**Simple module enabling Django app testing via $ python setup.py test.**


.. contents:: Contents
    :depth: 5


Normally when you execute ``$ python setup.py test`` for Django related modules you're almost certain to run into ``DJANGO_SETTINGS_MODULE`` environment variable issues, e.g.::

    ImportError: Settings cannot be imported, because environment variable DJANGO_SETTINGS_MODULE is undefined.

This module overcomes this by configuring the ``DJANGO_SETTINGS_MODULE`` environment variable before executing your test suite. As a bonus it also generates `Coverage <http://nedbatchelder.com/code/coverage/>`_ and `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_ reports as part of the test.

Installation
------------

#. Add the following to the the ``setup.py`` file **before** the setup call::

    from setuptools.command.test import test

    def run_tests(self):
        from setuptest.runtests import runtests
        return runtests(self)
    test.run_tests = run_tests

#. Provide a ``test_suite`` argument to the setup call specifying the test suite, e.g.::

    setup(
        # ...
        test_suite = "my_django_package.tests"
    )

#. Provide a ``tests_require`` argument to the setup call including ``django-setuptest`` and other package dependencies required to execute the tests, e.g.::

    setup(
        # ...
        tests_require=[
            'django-setuptest',
        ],
    )

# Specify the test specific Django settings in a ``settings`` module within the test suite, e.g. in ``my_django_package/tests/settings.py``::

    DATABASE_ENGINE = 'sqlite3'

    INSTALLED_APPS = [
        'my_django_package',
    ]

Usage
-----
Once correctly installed you can execute the tests from the command line::
    
    $ python setup.py test

To mute the output of `Coverage <http://nedbatchelder.com/code/coverage/>`_ and `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_ reports provide the ``--quiet`` option::
        
    $ python setup.py test --quiet

