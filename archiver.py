import os.path
import struct
import hashlib


class Archiver:
    NAME_BLOCK = 128
    TYPE_BLOCK = 1
    SIZE_BLOCK = 4
    MAX_FILE_SIZE = 2 ** (SIZE_BLOCK * 8)
    TYPE_FOLDER = b'\01'
    TYPE_FILE = b'\00'
    CHECKSUM_BLOCK = 16

    """
    Format description:
    
                Offset      Size
    Name        0           128
    Type        128         1       (0 for files, 1 for folders)
    Size        129         4       (only for files)
    Checksum    133         16      (only for files)
    """

    def zip(self, paths):
        archive = []
        for path in paths:
            if os.path.isdir(path):
                local_root = path.split(os.sep)[-1]
                for root, _, files in os.walk(path):
                    folder_name = root.split(os.sep)[-1]
                    if folder_name != local_root:
                        folder_path = os.sep.join((local_root, folder_name))
                    else:
                        folder_path = folder_name
                    folder_block = self.__get_folder_block(folder_path)
                    archive.append(folder_block)
                    for file in files:
                        file_block = self.__get_file_block__(os.sep.join((root, file)),
                                                             os.sep.join((folder_path, file)))
                        archive.append(file_block)
            else:
                file = path.split(os.sep)[-1]
                file_block = self.__get_file_block__(path, file)
                archive.append(file_block)
        return b''.join(archive)

    def __get_file_block__(self, absolute_path, local_path):
        block = b''
        with open(absolute_path, 'rb') as file:
            data = file.read()
            block += self.__encode_name__(local_path)
            block += self.TYPE_FILE
            if len(data) > self.MAX_FILE_SIZE:
                raise FileSizeException(f"File size is greater than {self.MAX_FILE_SIZE}")
            block += struct.pack('>I', len(data))
            hash = hashlib.md5(data).digest()
            block += hash
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
            checksum = archive[cursor: cursor + self.CHECKSUM_BLOCK]
            cursor += self.CHECKSUM_BLOCK
            data = archive[cursor: cursor + size]
            if checksum != hashlib.md5(data).digest():
                print(f"Ошибка контрольной суммы в {name}")
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
