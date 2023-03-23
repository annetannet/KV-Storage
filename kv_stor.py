import os
from typing import Union
import argparse
import json


class KVS:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser. \
            add_argument('-k', '--key', nargs='*',
                         help='The key by which the value is stored in the db')
        self.parser. \
            add_argument('-v', '--value', nargs='*',
                         help='The value that is stored in the database')
        self.parser. \
            add_argument('-f', '--file', nargs='*', default=['storage.txt'],
                         help='The file that contains the database')

    def create_file(self, db: str) -> None:
        """Создает пустой файл"""
        with open(db, 'w'):
            pass

    def read_database(self, key: Union[str, None] = None, *,
                      db: str = 'storage.txt') -> Union[str, None]:
        """Читает файл.
        Если файла нет, создает его при помощи create_file().
        Если key == None, возвращает базу целиком.
        Если база пустая, возвращает None.
        Если key есть в базе, возвращает value.
        Если key нет в базе, возвращает None"""
        if not os.path.isfile(db):
            self.create_file(db)
        with open(db, 'r') as database:
            data = database.read()
            if not key:
                return data
            else:
                if not data:
                    return None
                else:
                    data = json.loads(data)
                    if key in data:
                        return data[key]
                    else:
                        return None

    def write_database(self, key: str, value: str,
                       db: list = ['storage.txt']) -> None:
        """Записывает в файл.
        Если база пустая, добавляет в нее {key: value}.
        Если ключ есть в базе, заменяет value.
        Если ключа нет в базе, добавляет data[key] = value"""
        data = self.read_database(db=db[0])
        if not data:
            data = {key: value}
        else:
            data = json.loads(data)
            data[key] = value
        for stor in db:
            with open(stor, 'w') as database:
                json.dump(data, database)

    def run(self, att):
        if att.key and att.value:
            if len(att.key) == len(att.value):
                for i in range(len(att.key)):
                    self.write_database(att.key[i], att.value[i], db=att.file)
            else:
                print('Invalid input. For one key, one value')
        elif att.key and not att.value:
            for key in att.key:
                print(self.read_database(key, db=att.file[0]))
        else:
            print("Invalid input")


if __name__ == "__main__":
    kvs = KVS()
    att = kvs.parser.parse_args()
    kvs.run(att)
