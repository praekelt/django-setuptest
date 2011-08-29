from setuptools.command.test import test

def run_tests(self):
    from setuptest.runtests import runtests
    return runtests(self.test_suite)

test.run_tests = run_tests
