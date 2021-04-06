"""
test_head.py - tests for the HTTP metadata utilities module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.head import head

class TestHead(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_head(self):
        input = Mock(group=lambda x: 'https://vtluug.org')
        head(self.phenny, input)

        out = self.phenny.reply.call_args[0][0]
        m = re.match('^200, text/html, utf-8, \d{4}\-\d{2}\-\d{2} '\
                '\d{2}:\d{2}:\d{2} UTC, [0-9]+ bytes, [0-9]+.[0-9]+ s$', out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_head_404(self):
        input = Mock(group=lambda x: 'https://vtluug.org/trigger_404')
        head(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertEqual(out, '404')

    def test_header(self):
        input = Mock(group=lambda x: 'https://vtluug.org Server')
        head(self.phenny, input)

        self.phenny.say.assert_called_once_with("Server: nginx")

    def test_header_bad(self):
        input = Mock(group=lambda x: 'https://vtluug.org truncatedcone')
        head(self.phenny, input)

        self.phenny.say.assert_called_once_with("There was no truncatedcone "\
                "header in the response.")
