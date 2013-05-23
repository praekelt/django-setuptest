Django Setuptest
================
**Simple module enabling Django app testing via $ python setup.py test.**


.. contents:: Contents
    :depth: 5

Normally when you execute ``$ python setup.py test`` for Django related
modules you're almost certain to run into ``DJANGO_SETTINGS_MODULE``
environment variable issues, e.g.::

    ImportError: Settings cannot be imported, because environment variable
    DJANGO_SETTINGS_MODULE is undefined.

This module overcomes this by configuring the ``DJANGO_SETTINGS_MODULE``
environment variable before executing your test suite. As a bonus it also
generates Coverage_ and `PEP 8`_ reports as part of the test.


Installation
------------

#. Provide a ``test_suite`` argument to the setup call specifying the 
   ``setuptest.setuptest.SetupTestSuite`` test suite, e.g.::

    setup(
        # ...
        test_suite='setuptest.setuptest.SetupTestSuite',
    )

   Alternatively provide a ``cmdclass`` ``test`` argument to the setup call 
   specifying the ``setuptest.test`` command, e.g.::
    
    from setuptest import test

    #...

    setup(
        # ...
        cmdclass={'test': test},
    )

   This overrides Python's builtin ``test`` command to enable the Django 
   testrunner as well as allowing you to pass ``--failfast`` as a commandline
   argument, i.e.::

    $ python setup.py test --failfast

   For the ``cmdclass`` method to work ``django-setuptools`` should be 
   installed and available in your Python path prior to running the ``test`` 
   command, in which case ``django-setuptest`` is not required to be specified
   as part of the ``tests_required`` argument as detailed next.

#. Provide a ``tests_require`` argument to the setup call including
   ``django-setuptest`` (required only if not already installed) and other
   package dependencies needed to execute the tests, e.g.::

    setup(
        # ...
        tests_require=(
            'django-setuptest',
        ),
    )

#. Specify your test specific Django settings in a ``test_settings``
   module in the same path as your app's ``setup.py``.
   These settings will be used when executing the tests, e.g. in
   ``test_settings.py``::

    DATABASE_ENGINE = 'sqlite3'

    INSTALLED_APPS = (
        'myapp',
    )

#. In order for the test suite to find your tests you must provide either a 
   ``packages`` or ``py_modules`` argument to the setup call, e.g.::

    from setuptools import setup, find_packages
    
    setup(
        # ...
        packages=find_packages(),
    )
    
    # Or alternatively...
    
    setup(
        # ...
        py_modules=['myapp'],
    )

Usage
-----
Once correctly configured you can execute tests from the command line::
    
    $ python setup.py test
    
or, if you want the test suite to stop after the first test failure is 
detected::

    $ python setup.py test --failfast

This should output your test results as well as Coverage_ and `PEP 8`_
reports.

.. note::

    An XML Coverage report is generated in a file called ``coverage.xml``
    and a PEP8 report is generated in a file called ``pep8.txt``

To mute the output of the Coverage_ and `PEP 8`_ reports provide the
``--quiet`` option::

    $ python setup.py test --quiet

To automatically restart the test runner when code changes are detected (similar to how ``runserver`` restarts) provide the ``--autoreload`` option::

    $ python setup.py test --autoreload

To only run tests for a particular test case specify the test case as the ``--label`` option::

    $ python setup.py test --label app.TestCase

Or for a particular test method specify the test case's test method as the ``--label`` option::

    $ python setup.py test --label app.TestCase.test_method

Sample Output
-------------

Example output of dummy test including Coverage_ and `PEP 8`_ reports::

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
      File "/home/user/tmp/django-dummy/dummy/tests/__init__.py", line 6, in test_something
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
    dummy/tests/__init__.py:6:1: W391 blank line at end of file

    $


.. _Coverage: http://nedbatchelder.com/code/coverage/
.. _`PEP 8`: http://www.python.org/dev/peps/pep-0008/

