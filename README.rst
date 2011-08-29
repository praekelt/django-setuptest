Django Setuptest
================
**Simple lib enabling Django app testing via $python setup.py test.**


.. contents:: Contents
    :depth: 5


Installation
------------

#. Install or add ``django-setuptest`` to your Python path.

#. Add the following to the your setup.py file **before** the setup call::

    from setuptools.command.test import test

    def run_tests(self):
        from setuptest.runtests import runtests
        return runtests(self)
    test.run_tests = run_tests

#. Provide a ``test_suite`` argument to your setup call specifying the test suite, e.g.::

    setup(
        # ...
        test_suite = "my_django_package.tests"
    )

# Specify your test specific Django settings in a ``settings`` module within your test suite, e.g. in ``my_django_package/tests/settings.py``::

    DATABASE_ENGINE = 'sqlite3'

    INSTALLED_APPS = [
        'my_django_package',
    ]

Usage
-----
Once correctly installed you can execute your tests from the command line::
    
    $ python setup.py test


