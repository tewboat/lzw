import os.path
import struct
import hashlib
import exif


class Archiver:
    NAME_BLOCK = 128
    TYPE_BLOCK = 1
    SIZE_BLOCK = 4
    METADATA_SIZE_BLOCK = 2
    MAX_FILE_SIZE = 2 ** (SIZE_BLOCK * 8)
    TYPE_FOLDER = b'\01'
    TYPE_FILE = b'\00'
    CHECKSUM_BLOCK = 16

    """
    Format description:
    
                    Size
    Name            128
    Type            1       (0 for files, 1 for folders)
    Checksum        16      (only for files)
    MetaDataSize    2       (only for files)
    MetaData        ...     (only for files)
    DataSize        4       (only for files)
    Data            ...     (only for files)
    """

    def zip(self, paths):
        archive = []
        offsets = {}
        offset = 0
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
                    offset += len(folder_block)
                    offsets[offset] = ""
                    archive.append(folder_block)
                    for file in files:
                        local_path = os.sep.join((folder_path, file))
                        file_block = self.__get_file_block__(os.sep.join((root, file)),
                                                             local_path)
                        archive.append(file_block)
                        offset += len(file_block)
                        offsets[offset] = local_path

            else:
                file = path.split(os.sep)[-1]
                file_block = self.__get_file_block__(path, file)
                archive.append(file_block)
                offset += len(file_block)
                offsets[offset] = file
        return b''.join(archive), offsets

    def __get_file_block__(self, absolute_path, local_path):
        block = b''
        with open(absolute_path, 'rb') as file:
            data = file.read()
            if len(data) > self.MAX_FILE_SIZE:
                raise FileSizeException(f"File size is greater than {self.MAX_FILE_SIZE}")
            block += self.__encode_name__(local_path)
            block += self.TYPE_FILE
            hash = hashlib.md5(data).digest()
            block += hash
            metadata = self.__get_metadata_block(file)
            block += struct.pack('>H', len(metadata))
            block += metadata
            block += struct.pack('>I', len(data))
            block += data
        return block

    def __get_folder_block(self, path):
        block = b''
        block += self.__encode_name__(path)
        block += self.TYPE_FOLDER
        return block

    def __get_metadata_block(self, file):
        block = []
        file = exif.Image(file)
        for tag in file.list_all():
            value = file.get(tag)
            if not value:
                continue
            if type(value) == tuple:
                value = self.__encode_tuple__(value)
            elif type(value) == str:
                value = value.encode()
            else:
                value = str(int(value)).encode()
            block.append(tag.encode() + b'=' + value)
        return b'&'.join(block)

    def __encode_tuple__(self, tuple):
        encoded = []
        for i in tuple:
            encoded.append(str(i).encode())
        return b'|'.join(encoded)

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
            checksum = archive[cursor: cursor + self.CHECKSUM_BLOCK]
            cursor += self.CHECKSUM_BLOCK
            metadata_size = archive[cursor: cursor + self.METADATA_SIZE_BLOCK]
            metadata_size = struct.unpack('>H', metadata_size)[0]
            cursor += self.METADATA_SIZE_BLOCK
            metadata = archive[cursor: cursor + metadata_size]
            metadata = self.__parse_metadata__(metadata)
            cursor += metadata_size
            size = archive[cursor: cursor + self.SIZE_BLOCK]
            size = struct.unpack('>I', size)[0]
            cursor += self.SIZE_BLOCK
            data = archive[cursor: cursor + size]
            if checksum != hashlib.md5(data).digest():
                print(f"Ошибка контрольной суммы в {name}")
            with open(os.sep.join((path, name)), 'wb+') as file:
                file.write(data)
                self.__set_metadata__(file, metadata)
            cursor += size

    def __decode_name__(self, name: bytes):
        cursor = 0
        while name[cursor] != 0:
            cursor += 1
        return name[0: cursor].decode()

    def __set_metadata__(self, file, metadata):
        file = exif.Image(file)
        for tag in metadata:
            file.set(tag, metadata[tag])

    def __parse_metadata__(self, bytes: bytes):
        if len(bytes) == 0:
            return {}
        metadata = {}
        pairs = bytes.split(b'&')
        for pair in pairs:
            print(pair)
            key, value = pair.split(b'=')
            value = value.split(b'|')
            if len(value) == 1:
                value = value[0]
            else:
                value = tuple(value)
            metadata[key] = value
        return metadata


class FileSizeException(Exception):
    pass
