# encoding=UTF-8

# Copyright © 2009-2022 Jakub Wilk <jwilk@jwilk.net>
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

import ast
import codecs
import collections
import inspect
import locale
import os
import pipes
import re
import signal
import subprocess as ipc
import sys
from unittest import SkipTest, TestCase as _TestCase


RE_TYPE = type(re.compile(''))

_PPM_RE = re.compile(r'P6\s+(\d+)\s+(\d+)\s+255\s(.*)\Z', re.DOTALL)
_PGM_RE = re.compile(r'P5\s+(\d+)\s+(\d+)\s+255\n(.*)\Z', re.DOTALL)

XML_NAMESPACE = dict(
    dc='http://purl.org/dc/elements/1.1/',
    xmpMM='http://ns.adobe.com/xap/1.0/mm/',
)

_UUID_REGEX = r'\Aurn:uuid:XXXXXXXX-XXXX-4XXX-[89ab]XXX-XXXXXXXXXXXX\Z'.replace('X', '[0-9a-f]')


def _get_signal_names():
    signame_pattern = re.compile('^SIG[A-Z0-9]*$')
    data = {
        name: getattr(signal, name)
        for name in dir(signal)
        if signame_pattern.match(name)
    }
    try:
        if data['SIGABRT'] == data['SIGIOT']:
            del data['SIGIOT']
    except KeyError:
        pass
    try:
        if data['SIGCHLD'] == data['SIGCLD']:
            del data['SIGCLD']
    except KeyError:
        pass
    return {no: name for name, no in data.items()}


class _IpcReturnCode(int):

    _signal_names = _get_signal_names()

    def __repr__(self):
        try:
            return '-' + self._signal_names[-self]
        except KeyError:
            return str(self)


class IpcResult:

    def __init__(self, stdout, stderr, rc):
        self.stdout = stdout
        self.stderr = stderr
        self.rc = rc

    def check_result(self, testcase_object: _TestCase, stdout=None, stderr=None, rc=0):
        if stderr is None:
            pass
        elif isinstance(stderr, RE_TYPE):
            testcase_object.assertRegex(self.stderr, stderr)
        else:
            testcase_object.assertMultiLineEqual(self.stderr, stderr)
        if rc is not None:
            testcase_object.assertEqual(_IpcReturnCode(self.rc), _IpcReturnCode(rc))
        if stdout is None:
            pass
        elif isinstance(stdout, RE_TYPE):
            testcase_object.assertRegex(self.stdout, stdout)
        else:
            testcase_object.assertMultiLineEqual(self.stdout, stdout)


def _get_locale_for_encoding(encoding):
    encoding = codecs.lookup(encoding).name
    candidates = {
        'utf-8': ['C.UTF-8', 'en_US.UTF-8'],
        'iso8859-1': ['en_US.ISO8859-1'],
    }[encoding]
    old_locale = locale.setlocale(locale.LC_ALL)
    try:
        for new_locale in candidates:
            try:
                locale.setlocale(locale.LC_ALL, new_locale)
            except locale.Error:
                continue
            locale_encoding = locale.getpreferredencoding(False)
            locale_encoding = codecs.lookup(locale_encoding).name
            if encoding == locale_encoding:
                return new_locale
    finally:
        locale.setlocale(locale.LC_ALL, old_locale)
    raise SkipTest(f'locale {str.join(" or ", candidates)} is required')


class TestCase(_TestCase):
    SkipTest = SkipTest
    maxDiff = None

    _pdf2djvu_command = os.getenv('pdf2djvu') or 'pdf2djvu'
    _feature_cache = {}
    _poppler_version = None

    def get_pdf2djvu_command(self):
        if re.compile(r'\A[a-zA-Z0-9_+/=.,:%-]+\Z').match(self._pdf2djvu_command):
            return (self._pdf2djvu_command,)
        return 'sh', '-c', self._pdf2djvu_command + ' "$@"', 'sh'

    def get_source_path(self, strip_py=False):
        result = inspect.getsourcefile(type(self))
        if strip_py and result.endswith('.py'):
            return result[:-3]
        return result

    def get_pdf_path(self):
        return self.get_source_path(strip_py=True) + '.pdf'

    def get_djvu_path(self):
        return self.get_source_path(strip_py=True) + '.djvu'

    def run_command(self, *commandline, **kwargs) -> IpcResult:
        env = dict(
            os.environ,
            MALLOC_CHECK_='3',
            MALLOC_PERTURB_=str(0xA5),
        )
        for key, value in kwargs.items():
            if key.isupper():
                env[key] = value
                continue
            if key == 'encoding':
                env['LC_ALL'] = _get_locale_for_encoding(value)
                continue
            raise TypeError(f'{key!r} is an invalid keyword argument for this function')
        env['LANGUAGE'] = 'en'
        cmd_array = [x if isinstance(x, str) else x.decode('UTF-8', 'surrogateescape') for x in commandline]
        print('$', str.join(' ', map(pipes.quote, cmd_array)))
        try:
            child = ipc.Popen(
                list(commandline),
                stdout=ipc.PIPE,
                stderr=ipc.PIPE,
                env=env,
            )
        except OSError as exc:
            exc.filename = commandline[0]
            raise
        stdout, stderr = child.communicate()
        return IpcResult(
            stdout=stdout.decode('UTF-8', 'surrogateescape'),
            stderr=stderr.decode('UTF-8', 'surrogateescape'),
            rc=child.returncode
        )

    def _pdf2djvu(self, *args, **kwargs) -> IpcResult:
        quiet = ('-q',) if kwargs.pop('quiet', True) else ()
        args = self.get_pdf2djvu_command() + quiet + (self.get_pdf_path(),) + args
        result = self.run_command(*args, **kwargs)
        if os.getenv('pdf2djvu_win32'):
            result.stderr = result.stderr.replace('\r\n', '\n')
        if sys.platform.startswith('openbsd'):
            # FIXME: https://github.com/jwilk/pdf2djvu/issues/108
            result.stderr = re.compile(
                r'Magick: Failed to close module [(]"\w*: Invalid handle\"[)].\n'
            ).sub('', result.stderr)
        return result

    def pdf2djvu(self, *args, **kwargs) -> IpcResult:
        return self._pdf2djvu('-o', self.get_djvu_path(), *args, **kwargs)

    def pdf2djvu_indirect(self, *args) -> IpcResult:
        return self._pdf2djvu('-i', self.get_djvu_path(), *args)

    def djvudump(self, *args) -> IpcResult:
        return self.run_command('djvudump', self.get_djvu_path(), *args)

    def djvused(self, expr, **kwargs) -> IpcResult:
        return self.run_command('djvused', '-e', expr, self.get_djvu_path(), **kwargs)

    def print_text(self) -> IpcResult:
        return self.run_command('djvutxt', self.get_djvu_path())

    def print_outline(self) -> IpcResult:
        return self.djvused('print-outline')

    def print_ant(self, page) -> IpcResult:
        return self.djvused(f'select {page}; print-ant')

    def print_meta(self) -> IpcResult:
        return self.djvused('print-meta')

    def ls(self) -> IpcResult:
        return self.djvused('ls', encoding='UTF-8')

    def _read_ppm(self, b):
        match = _PPM_RE.match(b)
        self.assertIsNotNone(match)
        (width, height, pixels) = match.groups()
        width = int(width)
        height = int(height)
        pixels = memoryview(pixels.encode('UTF-8', 'surrogateescape'))
        pixels = [
            [
                pixels[(i + j):(i + j + 3)].tobytes()
                for i in range(0, width * 3, 3)
            ]
            for j in range(0, len(pixels), width * 3)
        ]
        for line in pixels:
            self.assertEqual(len(line), width)
        self.assertEqual(len(pixels), height)
        return pixels

    def _read_pgm(self, b):
        match = _PGM_RE.match(b)
        self.assertIsNotNone(match)
        (width, height, pixels) = match.groups()
        width = int(width)
        height = int(height)
        pixels = memoryview(pixels.encode('UTF-8', 'surrogateescape'))
        pixels = [
            pixels[i:(i + width)]
            for i in range(0, len(pixels), width)
        ]
        for line in pixels:
            self.assertEqual(len(line), width)
        self.assertEqual(len(pixels), height)
        return pixels

    def decode(self, mode='color', fmt='ppm'):
        args = []
        r = self.run_command(
            'ddjvu',
            self.get_djvu_path(),
            f'-format={fmt}',
            f'-mode={mode}',
            '-subsample=1',
            *args
        )
        r.check_result(testcase_object=self, stdout=None)
        reader = dict(ppm=self._read_ppm, pgm=self._read_pgm)[fmt]
        return reader(r.stdout)

    def extract_xmp(self):
        r = self.djvused('output-ant')
        self.assertEqual(r.stderr, '')
        self.assertEqual(r.rc, 0)
        xmp_lines = [line for line in r.stdout.splitlines() if line.startswith('(xmp "')]
        if not xmp_lines:
            return None
        [xmp_line] = xmp_lines
        self.assertEqual(xmp_line[-2:], '")')
        xmp = xmp_line[5:-1]
        xmp = ast.literal_eval(xmp)
        return xmp

    def require_poppler(self, *version):
        if self._poppler_version is None:
            r = self.pdf2djvu('--version')
            r.check_result(testcase_object=self, stdout=re.compile('^pdf2djvu '), rc=0)
            print(r.stdout)
            match = re.compile('^[+] Poppler ([0-9.]+)$', re.M).search(r.stdout)
            self._poppler_version = tuple(int(x) for x in match.group(1).split('.'))
        if self._poppler_version < version:
            str_version = str.join('.', (str(v) for v in version))
            raise SkipTest(f'Poppler >= {str_version} is required')

    def require_feature(self, feature):
        try:
            feature_enabled = self._feature_cache[feature]
        except KeyError:
            if feature == 'POSIX':
                feature_enabled = not os.getenv('pdf2djvu_win32')
            else:
                r = self.pdf2djvu('--version')
                r.check_result(testcase_object=self, stdout=re.compile('^pdf2djvu '), rc=0)
                feature_enabled = feature in r.stdout
            self._feature_cache[feature] = feature_enabled
        if not feature_enabled:
            raise SkipTest(feature + ' support missing')

    @classmethod
    def count_colors(cls, image):
        result = collections.defaultdict(int)
        for line in image:
            for pixel in line:
                result[pixel] += 1
        return result

    @classmethod
    def xml_find_text(cls, xml, tag):
        [elem] = xml.findall('.//' + tag, XML_NAMESPACE)
        return elem.text

    def assert_uuid_urn(self, uuid):
        return self.assertRegex(uuid, _UUID_REGEX)


def rainbow(width, height):
    from PIL import Image
    from PIL import ImageColor
    image = Image.new('RGB', (width, height))
    pixels = image.load()
    for x in range(width):
        for y in range(height):
            hue = 255 * x // (width - 1)
            luminance = 100 * y // height
            color = ImageColor.getrgb(f'hsl({hue}, 100%, {luminance}%)')
            pixels[x, y] = color
    return image


def checkboard(width, height):
    from PIL import Image
    image = Image.new('1', (width, height))
    pixels = image.load()
    for x in range(width):
        for y in range(height):
            color = 0xFF * ((x ^ y) & 1)
            pixels[x, y] = color
    return image


__all__ = [
    # helper classes:
    'TestCase',
    # image handling:
    'rainbow',
    'checkboard',
    # XMP:
    'XML_NAMESPACE',
]

# vim:ts=4 sts=4 sw=4 et
