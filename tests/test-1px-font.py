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

from tools import (
    case,
)

class test(case):
    # Bug: https://bitbucket.org/jwilk/pdf2djvu/issue/5
    # + fixed in 0.4.10 [1a39024ea13a]

    def test(self):
        self.pdf2djvu().assert_()

# vim:ts=4 sts=4 sw=4 et
