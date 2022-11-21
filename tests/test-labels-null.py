# encoding=UTF-8

# Copyright © 2015-2017 Jakub Wilk <jwilk@jwilk.net>
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

import re

from tools import TestCase


class LabelsNullTestCase(TestCase):

    def test(self):
        self.pdf2djvu().check_result(testcase_object=self)
        r = self.ls()
        r.check_result(
            testcase_object=self,
            stdout=re.compile(
                r'\n'
                r'\s*1\s+P\s+\d+\s+[\w.]+\s+T=\uFFFDnul\uFFFDl\uFFFD\n'
                r'\s*2\s+P\s+\d+\s+[\w.]+\s+T=1\n'
            )
        )

# vim:ts=4 sts=4 sw=4 et
