import os
import sys

from setuptools.command.test import test as TestCommand


class test(TestCommand):
    user_options = TestCommand.user_options + [
        ('autoreload', 'a', "Test suite will restart when code changes are detected."),
        ('failfast', 'f', "Test suite will stop running after the first test failure is detected."),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.test_suite = 'setuptest.setuptest.SetupTestSuite'
        self.autoreload = 0
        self.failfast = 0

    def run_tests(self):
        auto_reload = False
        if '-a' in sys.argv or '--autoreload' in sys.argv:
            auto_reload = True
        
        if auto_reload:
            from django.utils.autoreload import restart_with_reloader, reloader_thread
            if os.environ.get("RUN_MAIN") == "true":
                try:
                    TestCommand.run_tests(self)
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
