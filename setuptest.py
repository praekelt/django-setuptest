import sys
import pep8

import unittest
from coverage import coverage
from distutils import log
from StringIO import StringIO


class SetupTestSuite(unittest.TestSuite):
    label = None

    def __init__(self, *args, **kwargs):
        from django.conf import settings
        from django.utils.importlib import import_module
        try:
            test_settings = import_module('%s.test_settings' % self.label)
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
            app = get_app(self.label)
            self.addTest(build_suite(app))
        self.old_config = self.test_runner.setup_databases()

    def run(self, *args, **kwargs):
        # Start coverage.
        verbose = '--quiet' not in sys.argv

        if verbose:
            cov = coverage()
            cov.start()

        result = super(SetupTestSuite, self).run(*args, **kwargs)

        if verbose:
            # Stop and generate coverage report.
            cov.stop()
            log.info("\nCoverage Report:")
            cov.report(include=['%s*' % self.label], omit=['*tests*'])
            cov.xml_report(include=['%s*' % self.label], omit=['*tests*'])

            # Generate PEP8 report.
            pep_result = self.runpep8(self.label)
            if pep_result:
                log.info("\nPEP8 Report:")
                log.info(pep_result)

        self.test_runner.teardown_databases(self.old_config)
        self.test_runner.teardown_test_environment()
        return result

    def runpep8(self, package):
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


def suite(name, test_label=None):
    if test_label is None:
        test_label = name
    suite_cls = type('%sSetupTestSuite' % name.capitalize(),
                     (SetupTestSuite,), {'label': test_label})
    return suite_cls()
