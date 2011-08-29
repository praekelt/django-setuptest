import sys
import pep8

from coverage import coverage
from django.conf import settings
from importlib import import_module
from StringIO import StringIO

def init(test_suite):
    test_settings = import_module('%s.settings' % test_suite)

    foo_settings = {}
    for attr in dir(test_settings):
        if '__' not in attr:
            foo_settings[attr] = getattr(test_settings, attr)

    if not settings.configured:
        settings.configure(**foo_settings)

def runpep8(package):
    # Hook into stdout.
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    # Run Pep8 checks.
    pep8.options, pep8.args = pep8.process_options()
    pep8.input_dir(package)

    # Restore stdout.
    sys.stdout = old_stdout

    # Save result to pep8.txt.
    result = mystdout.getvalue()
    output = open('pep8.txt', 'w')
    output.write(result)
    output.close()

    # Return Pep8 result
    if result:
        return result
    else:
        return 'PEP8 Correct.'

def runtests(test_suite):
    module = test_suite.split('.')[0]
    init(test_suite)

    from django.test.simple import run_tests
    # Start coverage.
    cov = coverage()
    cov.start()

    # Run tests.
    failures = run_tests((module,), verbosity=1, interactive=True)
   
    # Stop and generate coverage report.
    cov.stop()
    print "\nCoverage Report:"
    cov.report(include=['%s*' % module,])
    cov.xml_report(include=['%s*' % module,])

    print "\nPEP8 Report:"
    print runpep8(module)

    sys.exit(failures)

