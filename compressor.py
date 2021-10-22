import os
import argparse
from lzw import Lzw
from archiver import Archiver
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lzw compressor')
    parser.add_argument('-c', '--command', dest='command', required=True, help='Enter command: PACK or UNPACK')
    parser.add_argument('-i', '--input', dest='input_paths', nargs='+', required=True, help='Input file paths')
    parser.add_argument('-o', '--output', dest='output_path', required=True, help='Output file path')
    parser.add_argument('-n', '--name', dest='name', default='archive', help='Archive name')
    args = parser.parse_args()

    if args.command == 'PACK':
        input_paths, output_path = args.input_paths, args.output_path
        archiver = Archiver()
        lzw = Lzw()
        archive = archiver.zip(input_paths)
        lzw.encode(archive, args.name, output_path)

    elif args.command == 'UNPACK':
        input_paths, output_path = args.input_paths, args.output_path
        if len(input_paths) > 1:
            raise ValueError('There should be only one input path')
        archiver = Archiver()
        lzw = Lzw()
        decoded = lzw.decode(input_paths[0])
        archiver.unzip(decoded, output_path)

    else:
        print("Unknown command")
