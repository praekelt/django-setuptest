import sys
import pep8

import unittest
from coverage import coverage, misc
from distutils import log
from StringIO import StringIO


class SetupTestSuite(unittest.TestSuite):
    label = None

    def __init__(self, *args, **kwargs):
        from django.conf import settings
        from django.utils.importlib import import_module
        try:
            test_settings = import_module('test_settings')
        except ImportError, e:
            log.info('ImportError: Unable to import test settings: %s' % e)
            sys.exit(1)

        setting_attrs = {}
        for attr in dir(test_settings):
            if '__' not in attr:
                setting_attrs[attr] = getattr(test_settings, attr)

        if not settings.configured:
            settings.configure(**setting_attrs)
        super(SetupTestSuite, self).__init__(*args, **kwargs)

        from django.db.models import get_app
        from django.test.simple import (DjangoTestSuiteRunner,
                                        build_test, build_suite)
        self.test_runner = DjangoTestSuiteRunner(verbosity=1,
                                                 interactive=True,
                                                 failfast=False)
        self.test_runner.setup_test_environment()
        if '.' in self.label:
            self.addTest(build_test(self.label))
        else:
            import sys
            f = sys._getframe()
            while f:
                if 'self' in f.f_locals:
                    locals_self = f.f_locals['self']
                    py_modules = getattr(locals_self, 'py_modules', None)
                    if py_modules:
                        for module in py_modules:
                            app = get_app(module)
                            self.addTest(build_suite(app))
                            break
                f = f.f_back

        self.old_config = self.test_runner.setup_databases()

    def run(self, *args, **kwargs):
        result = super(SetupTestSuite, self).run(*args, **kwargs)

        self.test_runner.teardown_databases(self.old_config)
        self.test_runner.teardown_test_environment()
        return result


def coverage_report(cov, test_label):
    verbose = '--quiet' not in sys.argv
    cov.stop()
    if verbose:
        log.info("\nCoverage Report:")
        try:
            omit = ['*tests*']
            cov.report(include=['%s*' % test_label], omit=omit)
            cov.xml_report(include=['%s*' % test_label], omit=omit)
        except misc.CoverageException, e:
            log.info("Coverage Exception: %s" % e)


def pep8_report(test_label):
    verbose = '--quiet' not in sys.argv
    if verbose:
        
        # Hook into stdout.
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        # Run Pep8 checks.
        pep8.options, pep8.args = pep8.process_options()
        pep8.options.repeat = True
        pep8.input_dir(test_label)

        # Restore stdout.
        sys.stdout = old_stdout

        # Save result to pep8.txt.
        result = mystdout.getvalue()
        output = open('pep8.txt', 'w')
        output.write(result)
        output.close()

        # Return Pep8 result
        if result:
            log.info("\nPEP8 Report:")
            log.info(result)


def suite(name, test_label=None):
    if test_label is None:
        test_label = name
    suite_cls = type('%sSetupTestSuite' % name.capitalize(),
                     (SetupTestSuite,), {'label': test_label})
        
    
    # Start coverage.
    cov = coverage()
    cov.start()

    result = suite_cls()
            
    # Generate coverage report.
    coverage_report(cov, test_label)
        
    # Generate PEP8 report.
    pep8_report(test_label)

    return result
