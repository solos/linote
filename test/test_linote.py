#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import codecs
from linote import Linote
from path import path
from utils import clean_style, clean_note
from encoding import (to_unicode,
                      html_to_unicode,
                      html_body_declared_encoding,
                      read_bom,
                      http_content_type_encoding,
                      html_body_declared_encoding)
from evernote.edam.type.ttypes import Note
from utils import get_config

cur_dir = path(__file__).abspath().split('/')[:-2]
par_dir = '/'.join(cur_dir)
sys.path.append(par_dir)

import linote
import unittest
import pyshould.patch


class DefaultTestCase(unittest.TestCase):
    def setUp(self):
        self.linote = Linote('test_token', 'http://abc.com')

    def tearDown(self):
        pass

    def test_utils_clean_style(self):
        """Linote for utils clean_style"""
        clean_style("hello").should.eq("<p>hello</p>")

    def test_utils_clean_note(self):
        """Linote for utils clean_note"""
        clean_note("<h1>hello</h1>").should.eq("hello")

    def test_to_unicode(self):
        """Linote to_unicode function"""
        "abc".should_not.be_a(unicode)
        to_unicode("abc", "utf-8").should.be_a(unicode)

    def test_html_to_unicode(self):
        """Linote html_to_unicode function"""
        html_to_unicode(
            'charset=("zh_cn")',
            '<html><h1>漢字汉字</h1></html>').should.eq(
                ('utf8',
                 u'<html><h1>\u6f22\u5b57\u6c49\u5b57</h1></html>'))

    def test_html_body_declared_encoding(self):
        """Linote html_body_declared_encoding function"""
        html_body_declared_encoding(
            '<meta http-equiv="Content-Type" '
            'content="text/html;charset=ISO-8859-8">').should.eq(
                'iso8859-8')
        html_body_declared_encoding(
            '<meta http-equiv="Content-Type" '
            'content="text/html; charset=utf-8">').should.eq(
                'utf-8')

    def test_linote_checkdir(self):
        """Linote checkdir"""
        self.linote.checkdir("/xxx/yyy/zzz").should.be_false()
        path("/xxx/yyy/zzz").exists().should.be_false()
        existing_path = path.getcwd().joinpath('testingdir')
        self.linote.checkdir(existing_path).should.be_true()
        path(existing_path).exists().should.be_true()
        path(existing_path).rmdir_p()

    def test_linote_clean(self):
        """Linote clean function"""
        self.linote.clean("hello<br>").should.eq(
            u'hello\n')

    def test_linote_clean_note(self):
        """Linote clean_note function"""
        self.linote.clean_note(
            "<h1>hello</h1><br>").should.eq('hello')

    def test_linote_clean_style(self):
        """Linote clean_style function"""
        self.linote.clean_style(
            "<h1 type='text/css'>hello</h1>").should.eq(
                '<h1>hello</h1>')

    def test_linote_make_note(self):
        """Linote make_note function"""
        note = self.linote.make_note('a', 'abc')
        note.should.be_a(Note)
        note.title.should.eq('a')
        note.content.should.eq(
            '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE '
            'en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
            '<en-note> abc </en-note>')

    def test_linote_config_object(self):
        """Linote linote object works"""
        import kaptan
        linote_config = get_config("config.ini.sample")
        linote_config.should.be_a(kaptan.Kaptan)
        linote_config.get("linote.dev_token").should.eq(
            "fill_in_your_dev_token_here")
        linote_config.get("linote.notedir").should.eq("notes")
        linote_config.get("logging.log_name").should.eq("linote")

    def test_read_bom(self):
        """Linote read_bom function"""
        read_bom(codecs.BOM_UTF8).should.eq(
            ('utf-8', '\xef\xbb\xbf'))
        read_bom("hello").should.eq((None, None))

    def test_http_content_type_encoding(self):
        """Linote: http_content_type_encoding"""
        http_content_type_encoding(
            'Content-type: application/json; '
            'charset=utf-8').should.eq('utf-8')
        
    def test_html_body_declared_encoding(self):
        """Linote: html_body_declared_encoding"""
        html_body_declared_encoding(
            '<meta http-equiv="Content-Type"'
            ' content="text/html; charset=utf-8">').should.eq(
                'utf-8')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(DefaultTestCase('test_version'))
    suite.addTest(DefaultTestCase('test_utils_clean_style'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite', verbosity=2)
