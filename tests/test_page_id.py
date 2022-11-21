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


class PageIdTestCase(TestCase):

    def test_default(self):
        self.pdf2djvu().check_result(testcase_object=self)
        r = self.ls()
        r.check_result(
            testcase_object=self,
            stdout=re.compile(
                r'\n'
                r'\s*1\s+P\s+\d+\s+p0001[.]djvu\s+T=1\n'
                r'\s*2\s+P\s+\d+\s+p0002[.]djvu\s+T=2\n'
            )
        )
        self.pdf2djvu('--pages', '2').check_result(testcase_object=self)
        r = self.ls()
        r.check_result(
            testcase_object=self,
            stdout=re.compile(
                r'\n'
                r'\s*1\s+P\s+\d+\s+p0002[.]djvu\s+T=2\n'
            )
        )

    def test_spage(self):
        def check(tmpl):
            self.pdf2djvu('--pages', '2', '--page-id-template', tmpl).check_result(testcase_object=self)
            r = self.ls()
            r.check_result(
                testcase_object=self,
                stdout=re.compile(
                    r'\n'
                    r'\s*1\s+P\s+\d+\s+p2[.]djvu\sT=2\n'
                )
            )

        check('p{page}.djvu')
        check('p{spage}.djvu')

    def test_dpage(self):
        self.pdf2djvu('--pages', '2', '--page-id-template', 'p{dpage}.djvu').check_result(testcase_object=self)
        r = self.ls()
        r.check_result(
            testcase_object=self,
            stdout=re.compile(
                r'\n'
                r'\s*1\s+P\s+\d+\s+p1[.]djvu\s+T=2\n'
            )
        )

    def test_minus(self):
        self.pdf2djvu('--page-id-template', 'p{page-1}.djvu').check_result(testcase_object=self)
        r = self.ls()
        r.check_result(
            testcase_object=self,
            stdout=re.compile(
                r'\n'
                r'\s*1\s+P\s+\d+\s+p0[.]djvu\s+T=1\n'
                r'\s*2\s+P\s+\d+\s+p1[.]djvu\s+T=2\n'
            )
        )

    def test_plus(self):
        self.pdf2djvu('--page-id-template', 'p{page+7}.djvu').check_result(testcase_object=self)
        r = self.ls()
        r.check_result(
            testcase_object=self,
            stdout=re.compile(
                r'\n'
                r'\s*1\s+P\s+\d+\s+p8[.]djvu\s+T=1\n'
                r'\s*2\s+P\s+\d+\s+p9[.]djvu\s+T=2\n'
            )
        )

# vim:ts=4 sts=4 sw=4 et
