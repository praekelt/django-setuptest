from setuptools.command.test import test as TestCommand


class test(TestCommand):
    user_options = TestCommand.user_options + [
        ('failfast', 'f', "Test suite will stop running after the first test failure is detected.")
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.test_suite = 'setuptest.setuptest.SetupTestSuite'
        self.failfast = 0
