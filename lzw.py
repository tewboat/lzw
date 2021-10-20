import os
import struct


class Lzw:
    CHAR_SIZE = 8
    ALPHABET_SIZE = 2 ** CHAR_SIZE

    CHAR_EXTENSION_SIZE = 16
    MAX_ALPHABET_SIZE = 2 ** CHAR_EXTENSION_SIZE

    def encode(self, data: bytes, name, output_path):

        alphabet = {i.to_bytes(1, 'big'): i for i in range(self.ALPHABET_SIZE)}

        compressed_data = []
        extension = b""

        for char in data:
            byte = char.to_bytes(1, "big")
            temp = extension + byte
            if temp in alphabet:
                extension = temp
            else:
                compressed_data.append(alphabet[extension])
                if len(alphabet) <= self.MAX_ALPHABET_SIZE:
                    alphabet[temp] = len(alphabet)
                extension = byte

        if extension in alphabet:
            compressed_data.append(alphabet[extension])

        output_file_path = os.sep.join((output_path, name + '.lzw'))
        with open(output_file_path, 'wb') as file:
            for byte in compressed_data:
                file.write(byte.to_bytes(2, "big"))

    def decode(self, input_file_path):
        data: bytes
        compressed_data = []
        with open(input_file_path, 'rb') as file:
            while True:
                encoded = file.read(2)
                if len(encoded) != 2:
                    break
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

        result = b''
        for byte in decompressed_data:
            result += byte
        return result
