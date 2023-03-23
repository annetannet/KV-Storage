
## Локальное хранилище

Реализация KV-Storage. По умолчанию данные сохраняются в файл storage.txt.

### Features

- добавление сразу нескольких пар ключ - значение
- возможность создания нескольких экземпляров хранилищ
- устойчивость к перезапуску

### Запуск

```commandline
python3 kv_stor.py -k key1 key2 -v value1 value2 -f file1 file2
```

usage: kv_stor.py [-h] [-k [KEY ...]] [-v [VALUE ...]] [-f [FILE ...]]

optional arguments:

* `-h, --help`            show this help message and exit
* `-k, --key`             The key by which the value is stored
* `-v, --value`           The value that is stored in the database
* `-f, --file`            The file that contains the database
