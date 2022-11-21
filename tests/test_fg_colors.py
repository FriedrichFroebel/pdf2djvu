# encoding=UTF-8

# Copyright © 2010-2022 Jakub Wilk <jwilk@jwilk.net>
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


class ForegroundColorsTestCase(TestCase):
    """
    Bug: https://github.com/jwilk/pdf2djvu/issues/45
    Fixed in 0.7.2 [72be13a3bc33817030125301fa34df3ddef63a10]
    """

    def test(self):
        for method, expected_color_count in [
                ('default', 325),
                ('web', 43),
                ('black', 2)
        ]:
            with self.subTest(method=method):
                self._test(method=method, n=expected_color_count)

    def _test(self, method, n):
        self.pdf2djvu(
            '--dpi=72',
            f'--fg-colors={method}'
        ).check_result(testcase_object=self)
        image = self.decode()  # noqa: F841
        image = self.decode(mode='foreground')
        colors = self.count_colors(image)
        self.assertEqual(len(colors), n)

# vim:ts=4 sts=4 sw=4 et
