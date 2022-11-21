# encoding=UTF-8

# Copyright © 2015-2018 Jakub Wilk <jwilk@jwilk.net>
#
# This file is part of pdf2djvu.
#
# pdf2djvu is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# pdf2djvu is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

import os
import re
from xml.etree import ElementTree

from tools import TestCase


HERE = os.path.dirname(__file__)
SRC_DIR = os.path.join(HERE, os.pardir)


class VersionTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        path = os.path.join(SRC_DIR, 'doc', 'changelog')
        with open(path) as fp:
            line = fp.readline()
        cls.changelog_version = line.split()[1].strip('()')

    def test_manpage(self):
        path = os.path.join(SRC_DIR, 'doc', 'manpage.xml')
        for dummy_event, elem in ElementTree.iterparse(path):
            if elem.tag == 'refmiscinfo' and elem.get('class') == 'version':
                self.assertEqual(elem.text, self.changelog_version)
                break
        else:
            self.fail("missing <refmiscinfo class='version'>")

    def test_executable(self):
        r = self.pdf2djvu('--version')
        r.check_result(testcase_object=self, stdout=re.compile(r'^pdf2djvu [0-9.]+\r?\n', re.M), rc=0)
        exec_version = r.stdout.splitlines()[0]
        _, exec_version = exec_version.split()
        self.assertEqual(exec_version, self.changelog_version)

# vim:ts=4 sts=4 sw=4 et
