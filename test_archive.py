import os
import shutil
import unittest

import exif

from archiver import Archiver

"""
Format description:

                Size
Name            128
Type            1       (0 for files, 1 for folders)
Checksum        16      (only for files)
MetaDataSize    2       (only for files)
MetaData        ...     (only for files)
DataSize        4       (only for files)
Data            ...     (only for files)
"""


class ArchiveTest(unittest.TestCase):

    def setUp(self) -> None:
        self.archiver = Archiver()
        os.mkdir('result')

    def tearDown(self) -> None:
        shutil.rmtree('result', ignore_errors=True)

    def test_file_archivation(self):
        expected = b"helloworld.py\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00g\x7f\xbd\xfa\xb6ze\xefu&\xc0)" \
                   b"\xc5V\xb7\xe2\x00\x00\x00\x00\x00\x14print('hello world')"
        zipped = self.archiver.zip([os.path.join('test_data', 'helloworld.py')])[0]
        self.assertEqual(zipped, expected)
        self.archiver.unzip(zipped, 'result')
        actual = os.walk('result')
        self.assertEqual(next(actual)[2], ['helloworld.py'])
        with open(os.path.join('test_data', 'helloworld.py')) as file1:
            with open(os.path.join('result', 'helloworld.py')) as file2:
                self.assertEqual(file1.read(), file2.read())

    def test_empty_folder_archivation(self):
        os.mkdir(os.path.join('test_data', 'empty_folder'))
        expected = b'empty_folder\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
        zipped = self.archiver.zip([os.path.join('test_data', 'empty_folder')])[0]
        self.assertEqual(zipped, expected)
        self.archiver.unzip(zipped, 'result')
        actual = os.walk('result')
        self.assertEqual(['empty_folder'], next(actual)[1])
        shutil.rmtree(os.path.join('test_data', 'empty_folder'))

    def test_folder_archivation(self):
        zipped = self.archiver.zip(['test_data'])[0]
        self.archiver.unzip(zipped, 'result')
        expected = os.walk(os.path.join('test_data'))
        actual = os.walk(os.path.join('result', 'test_data'))
        for i in actual:
            e = next(expected)
            self.assertEqual(i[1], e[1])
            self.assertEqual(i[2], e[2])

    def test_metadata_archivation(self):
        zipped = self.archiver.zip([os.path.join('test_data', 'EC7A7633.jpg')])[0]
        self.archiver.unzip(zipped, 'result')
        with open(os.path.join('test_data', 'EC7A7633.jpg'), 'rb') as file1:
            with open(os.path.join('result', 'EC7A7633.jpg'), 'rb') as file2:
                expected = exif.Image(file1).get_all()
                actual = exif.Image(file2).get_all()
                self.assertDictEqual(expected, expected)