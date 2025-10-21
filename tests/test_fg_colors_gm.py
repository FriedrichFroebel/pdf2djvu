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

import re

from tools import TestCase


class ForegroundColorsGraphicsMagickTestCase(TestCase):

    def test(self):
        """
        Bug: https://github.com/jwilk/pdf2djvu/issues/47
        Fixed in 0.7.2 [a10cfc8ac94e8f3b7e01e089056bf6a371d1a68d]
        """
        def check(i, n):
            self.require_feature('GraphicsMagick')
            self.pdf2djvu(
                '--dpi=72',
                f'--fg-colors={i}'
            ).check_result(testcase_object=self)
            image = self.decode()  # noqa: F841
            image = self.decode(mode='foreground')
            colors = self.count_colors(image)
            if isinstance(n, tuple):
                self.assertIn(len(colors), n)
            else:
                self.assertEqual(len(colors), n)

        for foreground_colors, expected_color_count in [
                (1, 2),
                (2, 3),
                (4, 5),
                (255, 241),
                (256, (245, 256)),
                (652, (245, 325))
        ]:
            with self.subTest(foreground_colors=foreground_colors):
                check(foreground_colors, expected_color_count)

    def test_range_error(self):
        def check(i):
            self.require_feature('GraphicsMagick')
            r = self.pdf2djvu(f'--fg-colors={i}')
            msg = 'The specified number of foreground colors is outside the allowed range: 1 .. 4080'
            r.check_result(
                testcase_object=self,
                stderr=re.compile('^' + re.escape(msg) + '\n'),
                rc=1,
            )

        check('-1')
        check(0)
        check(4081)

    def test_bad_number(self):
        def check(i):
            self.require_feature('GraphicsMagick')
            r = self.pdf2djvu(f'--fg-colors={i}')
            r.check_result(
                testcase_object=self,
                stderr=re.compile(f'^"{i}" is not a valid number\n'),
                rc=1,
            )

        check('')
        check('1x')
        check('0x1')
        check(23 ** 17)

# vim:ts=4 sts=4 sw=4 et
