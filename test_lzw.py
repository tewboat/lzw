import unittest
from lzw import Lzw


class LzwTest(unittest.TestCase):

    def test_compression_1(self):
        lzw = Lzw()
        data = b'\x00\x00\x00\x00\x00'
        encoded_data = lzw.encode(data)
        self.assertEqual(b'\x00\x00\x01\x00\x01\x00', encoded_data)

    def test_compression_2(self):
        lzw = Lzw()
        data = b'\x00\x01\x02\x03\x04'
        encoded_data = lzw.encode(data)
        self.assertEqual(b'\x00\x00\x00\x01\x00\x02\x00\x03\x00\x04', encoded_data)

    def test_compression_3(self):
        lzw = Lzw()
        data = b'\x00\x01\x00\x01\x02\x00\x01\x02'
        encoded_data = lzw.encode(data)
        self.assertEqual(b'\x00\x00\x00\x01\x01\x00\x00\x02\x01\x02', encoded_data)

    def test_decompression(self):
        lzw = Lzw()
        data = 'Hello world!'.encode()
        encoded_data = lzw.encode(data)
        decoded_data = lzw.decode(encoded_data)
        self.assertEqual(data, decoded_data)

    def test_decompression_russian(self):
        lzw = Lzw()
        data = 'Привет мир! ЁёЁёЁ'.encode()
        encoded_data = lzw.encode(data)
        decoded_data = lzw.decode(encoded_data)
        self.assertEqual(data, decoded_data)

    def test_compressing_and_decompressing_big_data(self):
        lzw = Lzw()
        with open('test_data/data.txt', 'rb') as test_data:
            data = test_data.read()
            encoded_data = lzw.encode(data)
            decoded_data = lzw.decode(encoded_data)
            self.assertEqual(data, decoded_data)


if __name__ == '__main__':
    unittest.main()
