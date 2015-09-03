__author__ = 'lowks'

import unittest
import local
from mock import Mock, patch, call


class LocalFunctionTests(unittest.TestCase):

    @patch("local.path")
    @patch("os.environ")
    def test_gen_filelist(self, mock_environ, mock_path):

        with patch.dict(local.local_files, {"onefile": "onefile"}, clear=True):
            mock_path.mkdir_p.return_value = True
            mock_path.write_text.return_value = True
            mock_environ["HOME"].return_value = "guda"
            local.gen_filelist("testingxx")
            self.assertIn(call('testingxx'), mock_path.mock_calls)
            self.assertIn(call('guda'), mock_path.mock_calls)

    @patch("local.path.stat")
    def test_statfile(self, mock_file):
        mock_file.st_mtime.side_effect = 100
        mock_file.st_ctime.side_effect = 100
        local.local_files = {}
        local.statfile("setup-setup-setup-setup-setup.enml")
        self.assertEqual(local.local_files,
                         {u'setup-setup-setup-setup-setup.enml':
                          {'ctime': 1,
                           'file': 'setup-setup-setup-setup-setup.enml',
                           'mtime': 1}})


if __name__ == '__main__':
    unittest.main()
