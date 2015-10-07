# encoding=UTF-8

# Copyright © 2009-2015 Jakub Wilk <jwilk@jwilk.net>
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

import unicodedata

from tools import (
    case,
    re,
)

class test(case):
    # + fixed in 0.4.9 [18b2ae04de2f]
    # + fixed in 0.4.11 [fa7d4addf18e]

    text = u'bar\N{LATIN SMALL LETTER DZ}o'
    text_nfkc = unicodedata.normalize('NFKC', text).encode('UTF-8')
    text_no_nfkc = text.encode('UTF-8')

    def test_nfkc(self):
        self.pdf2djvu().assert_()
        r = self.print_text()
        r.assert_(stdout=re('^{s} *$'.format(s=self.text_nfkc), re.M))

    def test_no_nfkc(self):
        self.pdf2djvu('--no-nfkc').assert_()
        r = self.print_text()
        r.assert_(stdout=re('^{s} *$'.format(s=self.text_no_nfkc), re.M))

# vim:ts=4 sts=4 sw=4 et
