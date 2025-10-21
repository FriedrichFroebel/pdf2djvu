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


class NfkcTestCase(TestCase):
    """
    Fixed in 0.4.9 [8af81b21de1d8c43bb7585b5318938cde52e30a2]
    Fixed in 0.4.11 [670a11dc9680cb4dac088d269f08f16f8ec0da7c]
    """

    text = '¾'
    text_nfkc = '3⁄4'
    text_no_nfkc = text

    def test_nfkc(self):
        self.pdf2djvu().check_result(testcase_object=self)
        r = self.print_text()
        r.check_result(testcase_object=self, stdout=re.compile(f'^{self.text_nfkc} *$', re.M))

    def test_no_nfkc(self):
        self.pdf2djvu('--no-nfkc').check_result(testcase_object=self)
        r = self.print_text()
        r.check_result(testcase_object=self, stdout=re.compile(f'^{self.text_no_nfkc} *$', re.M))

# vim:ts=4 sts=4 sw=4 et
