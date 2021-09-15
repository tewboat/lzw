class LzwEncoder:
    CHAR_SIZE = 8
    ALPHABET_SIZE = 2 ** CHAR_SIZE

    CHAR_EXTENSION_SIZE = 16
    MAX_ALPHABET_SIZE = 2 ** CHAR_EXTENSION_SIZE

    def encode(self, input_file_path, output_file_path):
        data: bytes
        with open(input_file_path, "rb") as file:
            data = file.read()

        alphabet_extension = {chr(i): i for i in range(self.ALPHABET_SIZE)}
        compressed_data = []
        stroke_index = 0

        i = 0
        while i < len(data):
            group = chr(data[i])
            j = i + 1
            while True:
                if j >= len(data):
                    compressed_data.append(alphabet_extension[group])
                    i += 1
                    break
                t = group + chr(data[j])
                if t not in alphabet_extension:
                    alphabet_extension[t] = stroke_index
                    stroke_index += 1
                    compressed_data.append(alphabet_extension[group])
                    i += 1
                    break
                i += 1
                j += 1
                group = t
        with open(output_file_path, 'wb') as file:
            for code in compressed_data:
                file.write(code.to_bytes(2, 'big'))
