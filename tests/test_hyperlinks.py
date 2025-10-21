# Copyright © 2009-2022 Jakub Wilk <jwilk@jwilk.net>
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


class HyperlinksTestCase(TestCase):

    def check(self, page, url, border='(xor)'):
        result = self.print_ant(page=page)
        template = f'(maparea "{url}" "" (rect NNN NNN NNN NNN) {border})'
        regexp = re.escape(template).replace('NNN', '[0-9]+')
        result.check_result(testcase_object=self, stdout=re.compile(regexp))

    def test(self):
        """
        Bug: https://github.com/jwilk/pdf2djvu/issues/3
        Fixed in 0.4.10 [47cde6c195ac057c0061a5fa192c69c3373c14ec]
        Fixed in 0.4.12 [5e691b2b67b3f50275b12d2d262d38646dacda64]
        """
        self.pdf2djvu().check_result(testcase_object=self)
        self.check(1, '#p0002.djvu')
        self.check(2, '#p0001.djvu', '(border #ff7f00)')
        self.check(3, 'http://www.example.org/')

    def test_border_avis(self):
        def check(*args):
            self.pdf2djvu(*args).check_result(testcase_object=self)
            self.check(1, '#p0002.djvu', '(xor) (border_avis)')
            self.check(2, '#p0001.djvu', '(border #ff7f00) (border_avis)')
            self.check(3, 'http://www.example.org/', '(xor) (border_avis)')

        check('--hyperlinks', 'border-avis')
        check('--hyperlinks', 'border_avis')

    def test_border_color(self):
        self.pdf2djvu('--hyperlinks', '#3742ff').check_result(testcase_object=self)
        self.check(1, '#p0002.djvu', '(border #3742ff)')
        self.check(2, '#p0001.djvu', '(border #3742ff)')
        self.check(3, 'http://www.example.org/', '(border #3742ff)')

    def test_none(self):
        def check(*args):
            self.pdf2djvu(*args).check_result(testcase_object=self)
            for n in range(3):
                r = self.print_ant(page=(n + 1))
                r.check_result(testcase_object=self, stdout='')

        check('--hyperlinks', 'none')
        check('--no-hyperlinks')

    def test_bad_argument(self):
        r = self.pdf2djvu('--hyperlinks', 'off')
        r.check_result(testcase_object=self, stderr=re.compile('^Unable to parse hyperlinks options\n'), rc=1)

# vim:ts=4 sts=4 sw=4 et
