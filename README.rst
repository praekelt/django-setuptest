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

#. Add the following to the package's ``setup.py`` file **before** the setup call::

    from setuptools.command.test import test

    def run_tests(self):
        from setuptest.runtests import runtests
        return runtests(self)
    test.run_tests = run_tests

    setup(
        # ...
    )

#. Provide a ``test_suite`` argument to the setup call specifying the test suite, e.g.::

    setup(
        # ...
        test_suite = "my_django_package.tests"
    )

#. Provide a ``tests_require`` argument to the setup call including ``django-setuptest`` (required) and other package dependencies needed to execute the tests, e.g.::

    setup(
        # ...
        tests_require=[
            'django-setuptest',
        ],
    )

#. Specify the test specific Django settings in a ``settings`` module within the test suite, e.g. in ``my_django_package/tests/settings.py``::

    DATABASE_ENGINE = 'sqlite3'

    INSTALLED_APPS = [
        'my_django_package',
    ]

Usage
-----
Once correctly installed you can execute the tests from the command line::
    
    $ python setup.py test

This should output your test results as well as `Coverage <http://nedbatchelder.com/code/coverage/>`_ and `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_ reports. *Note that an XML Coverage report is generated in a file called coverage.xml, and a PEP8 report is generated in a file called pep8.txt*

To mute the output of `Coverage <http://nedbatchelder.com/code/coverage/>`_ and `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_ reports provide the ``--quiet`` option::
        
    $ python setup.py test --quiet

Sample Output
-------------

Example output of dummy test including `Coverage <http://nedbatchelder.com/code/coverage/>`_ and `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_ reports::

    $ python setup.py test
    running test
    running egg_info
    writing django_dummy.egg-info/PKG-INFO
    writing top-level names to django_dummy.egg-info/top_level.txt
    writing dependency_links to django_dummy.egg-info/dependency_links.txt
    reading manifest file 'django_dummy.egg-info/SOURCES.txt'
    reading manifest template 'MANIFEST.in'
    writing manifest file 'django_dummy.egg-info/SOURCES.txt'
    running build_ext
    Creating test database for alias 'default'...
    E
    ======================================================================
    ERROR: test_something (dummy.tests.TestCase)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/shaun/tmp/django-dummy/dummy/tests/__init__.py", line 6, in test_something
        raise NotImplementedError('Test not implemented. Bad developer!')
    NotImplementedError: Test not implemented. Bad developer!
    
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s
    
    FAILED (errors=1)
    Destroying test database for alias 'default'...
    
    Coverage Report:
    Name              Stmts   Miss  Cover   Missing
    -----------------------------------------------
    dummy/models      20      2    90%   22, 55
    
    PEP8 Report:
    dummy/tests/settings.py:6:1: W391 blank line at end of file

    $


