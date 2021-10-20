import os.path
import struct


class Archiver:
    NAME_BLOCK = 128
    TYPE_BLOCK = 1
    SIZE_BLOCK = 4
    MAX_FILE_SIZE = 2 ** (SIZE_BLOCK * 8)
    TYPE_FOLDER = b'\01'
    TYPE_FILE = b'\00'

    def zip(self, path):
        if os.path.isdir(path):
            local_root = path.split(os.sep)[-1]
            archive = b''
            for root, _, files in os.walk(path):
                folder_name = root.split(os.sep)[-1]
                if folder_name != local_root:
                    folder_path = os.sep.join((local_root, folder_name))
                else:
                    folder_path = folder_name
                archive += self.__get_folder_block(folder_path)
                for file in files:
                    archive += self.__get_file_block__(os.sep.join((root, file)), os.sep.join((folder_path, file)))
            return archive
        return self.__get_file_block__(path, path.split('/')[-1])

    def __get_file_block__(self, absolute_path, local_path):
        block = b''
        with open(absolute_path, 'rb') as file:
            data = file.read()
            block += self.__encode_name__(local_path)
            block += self.TYPE_FILE
            if len(data) > self.MAX_FILE_SIZE:
                raise FileSizeException("File is too big")
            block += struct.pack('>I', len(data))
            block += data
        return block

    def __get_folder_block(self, path):
        block = b''
        block += self.__encode_name__(path)
        block += self.TYPE_FOLDER
        return block

    def __encode_name__(self, name):
        encoded = name.encode()
        for _ in range(self.NAME_BLOCK - len(encoded)):
            encoded += b'\x00'
        return encoded

    def unzip(self, archive, path):
        cursor = 0
        while cursor < len(archive):
            name = self.__decode_name__(archive[cursor: cursor + self.NAME_BLOCK])
            cursor += self.NAME_BLOCK
            type = archive[cursor: cursor + self.TYPE_BLOCK]
            cursor += self.TYPE_BLOCK
            if type == self.TYPE_FOLDER:
                os.mkdir(os.sep.join((path, name)))
                continue
            size = archive[cursor: cursor + self.SIZE_BLOCK]
            size = struct.unpack('>I', size)[0]
            cursor += self.SIZE_BLOCK
            data = archive[cursor: cursor + size]
            with open(os.sep.join((path, name)), 'wb') as file:
                file.write(data)
            cursor += size

    def __decode_name__(self, name: bytes):
        cursor = 0
        while name[cursor] != 0:
            cursor += 1
        return name[0: cursor].decode()


class FileSizeException(Exception):
    pass

