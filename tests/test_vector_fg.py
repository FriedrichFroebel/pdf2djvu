# Copyright © 2015-2022 Jakub Wilk <jwilk@jwilk.net>
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


class VectorForegroundTestCase(TestCase):
    """
    Bug: https://github.com/jwilk/pdf2djvu/issues/115
    Introduced in 0.7.1 [a9440040faf697bc11370e8012ba586e88e4dca4]
    Introduced in 0.7.10 [da7cd2524b329a80581b939037f4d42801f3755d]
    Fixed in 0.9.3 [93f9032d99b75145a03ce64de9c3ae3e25314541]
    """

    def test(self):
        self.pdf2djvu()
        image = self.decode()  # noqa: F841
        image = self.decode(mode='foreground')
        colors = self.count_colors(image)
        self.assertGreater(colors.get(b'\xFF\0\0', 0), 5000)

# vim:ts=4 sts=4 sw=4 et
