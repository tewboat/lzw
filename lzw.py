import os
import struct


class Lzw:
    CHAR_SIZE = 8
    ALPHABET_SIZE = 2 ** CHAR_SIZE

    CHAR_EXTENSION_SIZE = 16
    MAX_ALPHABET_SIZE = 2 ** CHAR_EXTENSION_SIZE

    def encode(self, data, offsets=None):
        alphabet = {i.to_bytes(1, 'big'): i for i in range(self.ALPHABET_SIZE)}

        statistics = {}
        cur_stat = 0
        prev_offset = 0
        compressed_data = []
        extension = b""

        for i in range(len(data) + 1):
            if offsets and i in offsets and offsets[i] != '':
                statistics[offsets[i]] = cur_stat / (i - prev_offset)
                prev_offset = i
                cur_stat = 0
            if i == len(data):
                continue
            char = data[i]
            byte = char.to_bytes(1, "big")
            temp = extension + byte
            if temp in alphabet:
                extension = temp
            else:
                compressed_data.append(struct.pack('>H', alphabet[extension]))
                cur_stat += 2
                if len(alphabet) < self.MAX_ALPHABET_SIZE:
                    alphabet[temp] = len(alphabet)
                extension = byte

        if extension in alphabet:
            compressed_data.append(struct.pack('>H', alphabet[extension]))

        return b''.join(compressed_data), statistics

    def decode(self, data):
        compressed_data = []
        for i in range(0, len(data), self.CHAR_EXTENSION_SIZE // 8):
            encoded = data[i: i + self.CHAR_EXTENSION_SIZE // 8]
            value = struct.unpack('>H', encoded)
            compressed_data.append(value[0])
        alphabet = {i: i.to_bytes(1, 'big') for i in range(self.ALPHABET_SIZE)}
        extension_code = self.ALPHABET_SIZE
        extension = b''
        decompressed_data = []
        for code in compressed_data:
            if code not in alphabet:
                alphabet[code] = extension + extension[0].to_bytes(1, 'big')
            decompressed_data.append(alphabet[code])
            if len(extension) != 0:
                alphabet[extension_code] = extension + alphabet[code][0].to_bytes(1, 'big')
                extension_code += 1
            extension = alphabet[code]

        return b''.join(decompressed_data)
