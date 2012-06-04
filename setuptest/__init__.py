from setuptools.command.test import test as TestCommand


class test(TestCommand):
    user_options = TestCommand.user_options + [
        ('failfast', 'f', "Test suite will stop running after the first test failure is detected.")
    ]
    failfast = 0
