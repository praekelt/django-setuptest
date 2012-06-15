import os
import sys

from setuptools.command.test import test as TestCommand
from setuptest import LabelException

class test(TestCommand):
    user_options = TestCommand.user_options + [
        ('autoreload', 'a', "Test suite will restart when code changes are detected."),
        ('failfast', 'f', "Test suite will stop running after the first test failure is detected."),
        ('label=', 'l', "Only run tests for specified label. Label should be of the form app.TestClass or app.TestClass.test_method."),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.test_suite = 'setuptest.setuptest.SetupTestSuite'
        self.autoreload = 0
        self.failfast = 0
        self.label = 0

    def run_tests(self):
        auto_reload = False
        if '-a' in sys.argv or '--autoreload' in sys.argv:
            auto_reload = True
        
        if auto_reload:
            from django.utils.autoreload import restart_with_reloader, reloader_thread
            if os.environ.get("RUN_MAIN") == "true":
                try:
                    TestCommand.run_tests(self)
                except LabelException:
                    sys.exit(1)
                except:
                    pass
                try:
                    reloader_thread()
                except KeyboardInterrupt:
                    pass
            else:
                try:
                    sys.exit(restart_with_reloader())
                except KeyboardInterrupt:
                    pass
        else:
            return TestCommand.run_tests(self)
