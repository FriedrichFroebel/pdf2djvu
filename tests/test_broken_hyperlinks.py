# encoding=UTF-8

# Copyright © 2016-2017 Jakub Wilk <jwilk@jwilk.net>
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


class BrokenHyperlinksTestCase(TestCase):

    def check(self, page, message, empty_stdout=True):
        r = self.pdf2djvu('-p', str(page), quiet=False)
        kwargs = dict(
            stderr=re.compile(f'- Warning: {re.escape(message)}\n')
        )
        if not empty_stdout:
            kwargs.update(
                stdout=re.compile('')
            )
        r.check_result(testcase_object=self, **kwargs)

    def test_no_action(self):
        self.check(1, 'Unable to convert link without an action')

    def test_lookup_error(self):
        self.check(
            2, 'Cannot find link destination',
            empty_stdout=False  # https://bugs.freedesktop.org/show_bug.cgi?id=81513
        )

    def test_remote_goto_action(self):
        self.check(3, 'Unable to convert link with a remote go-to action')

    def test_named_action(self):
        self.check(4, 'Unable to convert link with a named action')

    def test_launch_action(self):
        self.check(5, 'Unable to convert link with a launch action')

    def test_movie_action(self):
        self.check(6, 'Unable to convert link with a multimedia action')

    def test_sound_action(self):
        self.check(7, 'Unable to convert link with a multimedia action')

    def test_rendition_action(self):
        self.check(8, 'Unable to convert link with a multimedia action')

    def test_js_action(self):
        self.check(9, 'Unable to convert link with a JavaScript action')

    def test_set_ocg_state_action(self):
        self.check(10, 'Unable to convert link with a set-OCG-state action')

    def test_unknown_action(self):
        self.check(11, 'Unknown link action')

# vim:ts=4 sts=4 sw=4 et
