#!/usr/bin/env python

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["tests"]
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(name='misc',
      version='0.0.0',
      description='Miscellaneous',
      url='https://github.com/esesen/pymisc',
      packages=['misc'],
      tests_require=[
            'pytest>=2.7.2',
            'hypothesis>=1.10',
            'pytest-cache'],
      cmdclass={'test': PyTest})
