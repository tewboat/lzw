from lzw_encoder import LzwEncoder


if __name__ == '__main__':
    encoder = LzwEncoder()
    encoder.encode('C:\\Users\\zdrav\\PycharmProjects\\lzw\\input_file',
                   'C:\\Users\\zdrav\\PycharmProjects\\lzw\\output_file')
