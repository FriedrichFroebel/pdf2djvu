# encoding=UTF-8

# Copyright © 2009-2016 Jakub Wilk <jwilk@jwilk.net>
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

from xml.etree import ElementTree

from tools import TestCase


class XmpMediatypeTestCase(TestCase):
    """
    Bug: https://github.com/jwilk/pdf2djvu/issues/12
    Fixed in 0.6.0 [1368c73c027d798bdbfe0ac61c26339206e747bc]
    """

    def test_verbatim(self):
        self.pdf2djvu('--verbatim-metadata').check_result(testcase_object=self)
        xmp = self.extract_xmp()
        xmp = ElementTree.fromstring(xmp)
        dc_format = self.xml_find_text(xmp, 'dc:format')
        self.assertEqual(dc_format, 'application/pdf')

    def test_no_verbatim(self):
        self.require_feature('Exiv2')
        self.pdf2djvu().check_result(testcase_object=self)
        xmp = self.extract_xmp()
        xmp = ElementTree.fromstring(xmp)
        dc_format = self.xml_find_text(xmp, 'dc:format')
        self.assertEqual(dc_format, 'image/vnd.djvu')
        instance_id = self.xml_find_text(xmp, 'xmpMM:InstanceID')
        document_id = self.xml_find_text(xmp, 'xmpMM:DocumentID')
        self.assertNotEqual(instance_id, document_id)
        self.assert_uuid_urn(instance_id)
        self.assert_uuid_urn(document_id)

# vim:ts=4 sts=4 sw=4 et
