# encoding=UTF-8

# Copyright © 2015-2017 Jakub Wilk <jwilk@jwilk.net>
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


class LabelsTestCase(TestCase):
    """
    Bug: https://github.com/jwilk/pdf2djvu/issues/109
    Fixed in 0.9 [39920569549418038f1ffcefe65e3ddf78adacd2]
    """

    def test(self):
        def check(*args):
            self.pdf2djvu(*args).check_result(testcase_object=self)
            r = self.ls()
            r.check_result(
                testcase_object=self,
                stdout=re.compile(
                    r'\n'
                    r'\s*1\s+P\s+\d+\s+[\w.]+\s+T=one\n'
                    r'\s*2\s+P\s+\d+\s+[\w.]+\s+T=Αʹ\n'
                    r'\s*3\s+P\s+\d+\s+[\w.]+\s+T=i\n'
                    r'\s*4\s+P\s+\d+\s+[\w.]+\s+T=1\n'
                )
            )

        check()
        check('--page-title-template', '{label}')

    def test_arithmetic(self):
        def check(offset):
            r = self.pdf2djvu('--page-title-template', '{label' + offset + '}')
            r.check_result(
                testcase_object=self,
                stderr='Unable to format field {label}: type error: expected number, not string\n',
                rc=1
            )
        check('+1')
        check('-1')

    def test_auto_width(self):
        r = self.pdf2djvu('--page-title-template', '{label:0*}')
        r.check_result(
            testcase_object=self,
            stderr='Unable to format field {label}: unknown maximum width\n',
            rc=1
        )

    def test_page_id(self):
        """
        {label} can be used in --page-title-template, but not in --page-id-template.
        """
        r = self.pdf2djvu('--page-id-template', '{label}')
        r.check_result(
            testcase_object=self,
            stderr='Unable to format field {label}: no such variable\n',
            rc=1
        )

# vim:ts=4 sts=4 sw=4 et
