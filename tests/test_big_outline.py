# Copyright © 2016-2022 Jakub Wilk <jwilk@jwilk.net>
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


ITEM_COUNT = 1000
ITEM_TEMPLATE = '''
  ("ipsum {0}"
   "#p0001.djvu" )
'''.strip('\n')
EXPECTED_OUTLINE_SEXPR = ('''\
(bookmarks
 ("Lorem"
  "#p0001.djvu"
''' + '\n'.join(ITEM_TEMPLATE.format(i) for i in range(0, ITEM_COUNT)) + ' ) )\n'
)


class BigOutlineTestCase(TestCase):

    def test_multi_page(self):
        self.pdf2djvu().check_result(testcase_object=self)
        self.print_outline().check_result(testcase_object=self, stdout=EXPECTED_OUTLINE_SEXPR)

# vim:ts=4 sts=4 sw=4 et
