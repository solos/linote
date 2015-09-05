__author__ = 'lowks'

import unittest
from mock import Mock, patch
import utils


class UtilsTests(unittest.TestCase):

    def test_clean_note(self):
        utils.cleaner = Mock()
        utils.cleaner.clean_html.return_value = "hulahoop"
        result = utils.clean_note("hulahoop")
        self.assertEqual(result, "hulahoop")

    def test_make_mdnote(self):
        result = utils.make_mdnote("* hulahoop *")
        self.assertEqual(
            result, u'<div><ul>\n<li>hulahoop *</li>\n</ul>\n<div style="display:none">* hulahoop *</div></div>')

if __name__ == '__main__':
    unittest.main()
