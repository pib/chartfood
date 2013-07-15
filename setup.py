#!/usr/bin/python
#
# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup module for Google Visualization Python API."""

__author__ = "Misha Seltzer"

from setuptools import setup
import distutils.core
import unittest


class TestCommand(distutils.core.Command):
  """Class that provides the 'test' command for setup."""
  user_options = []

  def initialize_options(self):
    """Must override this method in the Command class."""
    pass

  def finalize_options(self):
    """Must override this method in the Command class."""
    pass

  def run(self):
    """The run method - running the tests on invocation."""
    from test import gviz_api_test
    suite = unittest.TestLoader().loadTestsFromTestCase(
        gviz_api_test.DataTableTest)
    unittest.TextTestRunner().run(suite)


setup(
    name="pyramid-charts",
    version="0.1",
    description="Python API for Google Visualization",
    long_description="""
The Python API for Google Visualization makes it easy to convert python data
structures into Google Visualization JS code, DataTable JSon construction
string or JSon response for Query object.
""".strip(),
    author="Amit Weinstein, Misha Seltzer",
    install_requires=['six'],
    license="Apache 2.0",
    url="https://github.com/pib/pyramid-charts",
    py_modules=["pyramid_charts"],
    cmdclass={"test": TestCommand},
)
