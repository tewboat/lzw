import os

from lzw import Lzw
from archiver import Archiver
import sys

if __name__ == '__main__':
    command = sys.argv[1]

    if command == '-h':
        print("""
        python compressor.py [command] [file_path] [destination_path]
        commands:
        -h help
        -p to pack files
        -u to unpack files
        """)
    elif command == '-p':
        input_path, output_path = sys.argv[2:4]
        archiver = Archiver()
        lzw = Lzw()
        archive = archiver.zip(input_path)
        lzw.encode(archive, input_path.split(os.sep)[-1], output_path)

    elif command == '-u':
        input_path, output_path = sys.argv[2:4]
        archiver = Archiver()
        lzw = Lzw()
        decoded = lzw.decode(input_path)
        archiver.unzip(decoded, output_path)

else:
    print("Unknown command")
