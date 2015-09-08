# encoding=UTF-8

# Copyright © 2009-2015 Jakub Wilk <jwilk@jwilk.net>
#
# This file is part of pdfdjvu.
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
    # Bug: https://bugs.debian.org/508391
    # + fixed in 0.4.12 [f5d4727b2490]

    def test(self):
        self.pdf2djvu().assert_()
        self.print_outline().assert_()

# vim:ts=4 sts=4 sw=4 et
