import os
import shutil
import unittest

from archiver import Archiver

"""
    Format description:

                Offset      Size
    Name        0           128
    Type        128         1       (0 for files, 1 for folders)
    Size        129         4       (only for files)
    Checksum    133         16      (only for files)
"""


class ArchiveTest(unittest.TestCase):

    def setUp(self) -> None:
        self.archiver = Archiver()
        os.mkdir('result')

    def tearDown(self) -> None:
        shutil.rmtree('result', ignore_errors=True)

    def test_file_archivation(self):
        expected = b"helloworld.py\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x14g\x7f\xbd\xfa\xb6ze\xefu&\xc0)\xc5V\xb7\xe2print('hello world')"
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
