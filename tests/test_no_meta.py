# Copyright © 2009-2016 Jakub Wilk <jwilk@jwilk.net>
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

from tools import TestCase


class NoMetaTestCase(TestCase):
    """
    Fixed in 0.7.10 [b888a6035c600bb12855685389c488b35e4c868e]
    """

    def test(self):
        self.pdf2djvu('--no-metadata', '--dpi=72').check_result(testcase_object=self)
        self.print_meta().check_result(testcase_object=self)

# vim:ts=4 sts=4 sw=4 et
