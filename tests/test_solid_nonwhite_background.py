# encoding=UTF-8

# Copyright © 2009-2017 Jakub Wilk <jwilk@jwilk.net>
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


class SolidNonWhiteBackgroundTestCase(TestCase):
    """
    Fixed in 0.3.6 [79779eea4fccc83d126ba27408de16a1c5f35d11]
    """

    def test(self):
        self.pdf2djvu().check_result(testcase_object=self)
        r = self.djvudump()
        r.check_result(testcase_object=self, stdout=re.compile(r'BG44 \[[0-9][0-9]\] .* 75x75'))

# vim:ts=4 sts=4 sw=4 et
