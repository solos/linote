#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
from utils import clean_style, clean_note

cur_dir = os.path.abspath(__file__).split('/')[:-2]
par_dir = '/'.join(cur_dir)
sys.path.append(par_dir)

import linote
import unittest


class DefaultTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_version(self):
        self.assertIsNotNone(linote.__version__, '0.0.1')
    
    def test_utils_clean_style(self):
        assert clean_style("hello") == "<p>hello</p>"

    def test_utils_clean_note(self):
        assert clean_note("<h1>hello</h1>") == "hello"


def suite():
    suite = unittest.TestSuite()
    suite.addTest(DefaultTestCase('test_version'))
    suite.addTest(DefaultTestCase('test_utils_clean_style'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite', verbosity=2)
