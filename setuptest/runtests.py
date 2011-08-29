import sys
import pep8

from coverage import coverage
from distutils import log
from django.conf import settings
from importlib import import_module
from StringIO import StringIO

def init(test_suite):
    try:
        test_settings = import_module('%s.settings' % test_suite)
    except ImportError:
        log.info('ImportError: Unable to import %s.settings' % test_suite)
        sys.exit(1)

    setting_attrs = {}
    for attr in dir(test_settings):
        if '__' not in attr:
            setting_attrs[attr] = getattr(test_settings, attr)

    if not settings.configured:
        settings.configure(**setting_attrs)

def runpep8(package):
    # Hook into stdout.
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    # Run Pep8 checks.
    pep8.options, pep8.args = pep8.process_options()
    pep8.options.repeat = True
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
        return None

def runtests(test):
    test_suite = test.test_suite
    module = test_suite.split('.')[0]
    init(test_suite)

    from django.test.simple import run_tests
    # Start coverage.
    if test.verbose:
        cov = coverage()
        cov.start()

    # Run tests.
    failures = run_tests((module,), verbosity=1, interactive=True)
   
    if test.verbose:
        # Stop and generate coverage report.
        cov.stop()
        log.info("\nCoverage Report:")
        cov.report(include=['%s*' % module,], omit=['*tests*',])
        cov.xml_report(include=['%s*' % module,], omit=['*tests*',])

        # Generate PEP8 report.
        pep_result = runpep8(module)
        if pep_result:
            log.info("\nPEP8 Report:")
            log.info(pep_result)

    sys.exit(failures)

