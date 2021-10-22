Реализация алгоритма компрессии без потерь Лемпеля — Зива — Велча
=============================================================
Версия 0.2  
Автор: Илья Жданов  
###Требования  
- Python версии не ниже 3.6

###Состав
- lzw.py - реализация алгоритмов компрессии и декомпрессии
- archiver.py - реализация архивации файлов
- compressor.py - главный файл

###Использование
compressor.py [-h] -c COMMAND -i INPUT_PATHS [INPUT_PATHS ...] -o OUTPUT_PATH [-n NAME]

Optional arguments:     
- -h, --help          show this help message and exit
- -c COMMAND, --command COMMAND
                        Enter command: PACK or UNPACK   
- -i INPUT_PATHS [INPUT_PATHS ...], --input INPUT_PATHS [INPUT_PATHS ...]
                        Input file paths        
- -o OUTPUT_PATH, --output OUTPUT_PATH
                        Output file path
- -n NAME, --name NAME  Archive name



