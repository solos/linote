#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
from utils import clean_style, clean_note
from encoding import (to_unicode,
                      html_to_unicode,
                      html_body_declared_encoding)

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

    def test_to_unicode(self):
        """Testing to_unicode function"""
        self.assertNotIsInstance("abc", unicode)
        self.assertIsInstance(to_unicode("abc", "utf-8"), unicode)

    def test_html_to_unicode(self):
        """Testing html_to_unicode function"""
        self.assertEqual(
            html_to_unicode('charset=("zh_cn")', '<html><h1>漢字汉字</h1></html>'),
            ('utf8', u'<html><h1>\u6f22\u5b57\u6c49\u5b57</h1></html>'))

    def test_html_body_declared_encoding(self):
        """Testing html_body_declared_encoding function"""
        self.assertEqual(
            html_body_declared_encoding(
                '<meta http-equiv="Content-Type" content="text/html;charset=ISO-8859-8">'),
            'iso8859-8')
        self.assertEqual(
            html_body_declared_encoding(
                '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'),
            'utf-8')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(DefaultTestCase('test_version'))
    suite.addTest(DefaultTestCase('test_utils_clean_style'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite', verbosity=2)
