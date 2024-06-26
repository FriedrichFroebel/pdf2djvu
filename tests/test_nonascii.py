# encoding=UTF-8

# Copyright © 2019 Jakub Wilk <jwilk@jwilk.net>
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

import os
import shutil
import tempfile

from tools import TestCase


class NonAsciiTestCase(TestCase):
    """
    Bug: https://github.com/jwilk/pdf2djvu/issues/138
    """

    def test_nonascii(self):
        try:
            curr_sign = '\xA4'
        except UnicodeError:
            raise self.SkipTest('locale that can encode U+00A4 CURRENCY SIGN is required')
        tmpdir = tempfile.mkdtemp(prefix='pdf2djvu.test.')
        try:
            djvu_path = os.path.join(tmpdir, curr_sign + '.djvu')
            pdf_path = os.path.join(tmpdir, curr_sign + '.pdf')
            shutil.copy(self.get_pdf_path(), pdf_path)
            cmdline = (self.get_pdf2djvu_command() + (
                '-q',
                pdf_path,
                '-o', djvu_path
            ))
            r = self.run_command(*cmdline)
            r.check_result(testcase_object=self)
        finally:
            shutil.rmtree(tmpdir)

# vim:ts=4 sts=4 sw=4 et
