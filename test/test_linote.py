#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
from linote import Linote
from path import path
from utils import clean_style, clean_note
from encoding import (to_unicode,
                      html_to_unicode,
                      html_body_declared_encoding)

cur_dir = path(__file__).abspath().split('/')[:-2]
par_dir = '/'.join(cur_dir)
sys.path.append(par_dir)

import linote
import unittest


class DefaultTestCase(unittest.TestCase):
    def setUp(self):
        self.linote = Linote('test_token', 'http://abc.com')

    def tearDown(self):
        pass

    def test_version(self):
        """Linote ensure linote gives back correct version"""
        assert linote.__version__ == '0.0.1'

    def test_utils_clean_style(self):
        """Linote for utils clean_style"""
        assert clean_style("hello") == "<p>hello</p>"

    def test_utils_clean_note(self):
        """Linote for utils clean_note"""
        assert clean_note("<h1>hello</h1>") == "hello"

    def test_to_unicode(self):
        """Linote to_unicode function"""
        assert is_instance("abc", unicode) == False
        assert is_instance(to_unicode("abc", "utf-8"), unicode) == True

    def test_html_to_unicode(self):
        """Linote html_to_unicode function"""
        self.assertEqual(
            html_to_unicode('charset=("zh_cn")', '<html><h1>漢字汉字</h1></html>'),
            ('utf8', u'<html><h1>\u6f22\u5b57\u6c49\u5b57</h1></html>'))

    def test_html_body_declared_encoding(self):
        """Linote html_body_declared_encoding function"""
        self.assertEqual(
            html_body_declared_encoding(
                '<meta http-equiv="Content-Type" content="text/html;charset=ISO-8859-8">'),
            'iso8859-8')
        self.assertEqual(
            html_body_declared_encoding(
                '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'),
            'utf-8')

    def test_linote_checkdir(self):
        """Linote checkdir"""
        self.assertFalse(self.linote.checkdir("/xxx/yyy/zzz"))
        self.assertFalse(path("/xxx/yyy/zzz").exists())
        existing_path = path.getcwd().joinpath('testingdir')
        self.assertTrue(self.linote.checkdir(existing_path))
        self.assertTrue(path(existing_path).exists())
        path(existing_path).rmdir_p()

    def test_linote_clean(self):
        """Linote clean function"""
        self.assertEqual(self.linote.clean("hello<br>"), u'hello\n')

    def test_linote_clean_note(self):
        """Linote clean_note function"""
        self.assertEqual(self.linote.clean_note("<h1>hello</h1><br>"),
                         'hello')
    
    def test_linote_clean_style(self):
        """Linote clean_style function"""
        self.assertEqual(self.linote.clean_style("<h1 type='text/css'>hello</h1>"),
                         '<h1>hello</h1>')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(DefaultTestCase('test_version'))
    suite.addTest(DefaultTestCase('test_utils_clean_style'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite', verbosity=2)
