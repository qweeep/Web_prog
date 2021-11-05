import os
import shutil
import pathlib
from typing import Dict

class PathStorage:
    #Хранение информации о пути

    def __init__(self, sep : str) -> None:
        self.sep = sep
        self.__storage = ["storage"]

    def add_path(self, path: str) -> None:
        if ".." in path and len(self.__storage) != 1:
            self.__storage.pop(-1)
        # Если хотим выйти за пределы 
        elif ".." in path:
            print("Вы хотите выйти за пределы нашей границы!")
        # Значит хотим перейти на уровень ниже
        else:
            self.__storage.append(path)

    def file2path(self, file_name: str) -> str:
        """Возвращает указанный файл в текущей структуры каталогов"""
        locale_storage = self.__storage.copy()
        locale_storage.append(file_name)
        abs_path = pathlib.Path(__file__).parent.absolute()
        return str(abs_path) + self.sep + self.sep.join(locale_storage)

    @property
    def path(self):
        """Возвращает текущую структуру каталогов"""
        abs_path = pathlib.Path(__file__).parent.absolute()
        return str(abs_path) + self.sep + self.sep.join(self.__storage)

    @property
    def upper_path(self):
        """Возвращает директорию выше текущей"""
        abs_path = pathlib.Path(__file__).parent.absolute()
        print(self.__storage[1:])
        return str(abs_path) + self.sep + self.sep.join(self.__storage[:1])


class FileProcessing:
    """Работа с файлами"""

    @staticmethod
    def get_commands() -> Dict[str, str]:
        """Список всех команд"""

        commands_dict = {
            "cd": "Перемещение между папками",
            "ls": "Вывод содержимого текущей папки на экран",
            "mkdir": "Создание папки",
            "rmdir": "Удаление папки",
            "create": "Создание файла",
            "rename": "Переименование файла/папки",
            "read": "Чтение файла",
            "remove": "Удаление файла",
            "copy": "Копирование файла/папки",
            "move": "Перемещение файла/папки",
            "write": "Запись в файл",
        }

        return commands_dict

    def __init__(self) -> None:
        self.sep = os.sep
        self.storage = PathStorage(self.sep)

    def mkdir(self, filename: str):
        """Создание папки"""
        current_path = self.storage.file2path(filename)
        try:
            os.mkdir(current_path)
        except FileNotFoundError:
            os.makedirs(current_path)
        except FileExistsError:
            print(f"Директория {filename} уже существует")

    def rmdir(self, filename: str):
        """Удаление папки"""
        current_path = self.storage.file2path(filename)
        try:
            os.rmdir(current_path)
        except OSError:
            try:
                shutil.rmtree(current_path, ignore_errors=False, onerror=None)
            except FileNotFoundError:
                print(f"Директории {filename} не существует")
            except NotADirectoryError:
                print(f"Файл {filename} не является директорией")
        except FileNotFoundError:
            print(f"Директории {filename} не существует")
        except NotADirectoryError:
            print(f"Файл {filename} не является директорией")

    def cd(self, filename: str):
        """Перемещение между папками"""
        self.storage.add_path(filename)
        current_path = self.storage.path

        try:
            os.chdir(current_path)
        except FileNotFoundError:
            self.storage.add_path(f"..{self.sep}")
            print(f"Директории {filename} не существует")
        except NotADirectoryError:
            self.storage.add_path(f"..{self.sep}")
            print(f"Файл {filename} не является директорией")

    def ls(self):
        """Вывод содержимого текущей директории на экран"""
        current_path = self.storage.path
        filelist = os.listdir(current_path)
        for i in range(len(filelist)):
            if os.path.isdir(self.storage.file2path(filelist[i])):
                filelist[i] = f"[dir] {filelist[i]}"
            elif os.path.isfile(self.storage.file2path(filelist[i])):
                filelist[i] = f"[file] {filelist[i]}"

        r = "\n".join(filelist)
        print(f"Содержимое {current_path}:\n{r}")

    def touch(self, filename: str):
        """Создание пустых файлов с указанием имени"""
        current_path = self.storage.file2path(filename)
        try:
            open(current_path, "a").close()
        except IsADirectoryError:
            print(f"Файл {filename} уже был создан и это директория")

    def cat(self, filename: str) -> str:
        """Просмотр содержимого текстового файла"""
        current_path = self.storage.file2path(filename)
        try:
            with open(current_path, "r") as file:
                print(file.read())
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
        except IsADirectoryError:
            print(f"Файл {filename} является директорией")

    def rename(self, filename_old: str, filename_new: str):
        """Переименование файлов"""

        path_old = self.storage.file2path(filename_old)
        path_new = self.storage.file2path(filename_new)

        # Проверка на то, чтоб файл с новым именем не существовал
        try:
            if not os.path.isfile(path_new):
                os.rename(path_old, path_new)
            else:
                raise IsADirectoryError
        except FileNotFoundError:
            print(f"Указанного файла {filename_old} не существует")
        except IsADirectoryError:
            print(f"Файл с названием {filename_new} уже существует")

    def rm(self, filename: str):
        """Удаление файлов по имени"""
        path = self.storage.file2path(filename)
        if os.path.isfile(path):
            os.remove(path)
        else:
            print(f"Файла {filename} не существует")

    def cp(self, filename: str, path: str):
        """Копирование файлов из одной папки в другую"""
        path_old = self.storage.file2path(filename)
        if ".." in path:
            path_new = self.storage.upper_path + self.sep + filename
        else:
            buff = self.storage.file2path(path)

            if os.path.isdir(buff):
                path_new = self.storage.file2path(path + self.sep + filename)
            else:
                path_new = self.storage.file2path(path)
        try:
            shutil.copyfile(path_old, path_new)
        except IsADirectoryError:
            shutil.copytree(path_old, path_new)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")

    def mv(self, filename: str, path: str):
        """Перемещение файлов"""
        path_old = self.storage.file2path(filename)
        if ".." in path:
            path_new = self.storage.upper_path + self.sep + filename
        else:
            buff = self.storage.file2path(path)
            if os.path.isdir(buff):
                path_new = self.storage.file2path(path + self.sep + filename)
            else:
                path_new = self.storage.file2path(path)
        try:
            shutil.move(path_old, path_new)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")

    def write(self, filename: str, *data: str):
        """Запись текста в файл"""
        text = " ".join(data)
        path = self.storage.file2path(filename)
        try:
            with open(path, "a") as file:
                file.write(text)
        except IsADirectoryError:
            print(f"Указанный файл {filename} является директорией")

    def router(self, command: str):
        """Ассоциация между командами и методами"""

        commands = [
            self.cd,
            self.ls,
            self.mkdir,
            self.rmdir,
            self.touch,
            self.rename,
            self.cat,
            self.rm,
            self.cp,
            self.mv,
            self.write,
        ]
        item_dict = dict(zip(FileProcessing.get_commands().keys(), commands))
        return item_dict.get(command, None)


def main():
    file_processing = FileProcessing()

    while True:
        commands_str = "\n".join(
                [
                    f"{key} - {value}"
                    for (key, value) in FileProcessing.get_commands().items()
                ]
            )
        print(f"Список команд:\n{commands_str}")
        command = input("\nВведите команду -> ").split(" ")

        # Выход из программы
        if command[0] == "exit":
            break

        # Существование команды
        result = file_processing.router(command[0])
        # Наличие и корректность команды
        if result:
            try:
                result(*command[1:])
            except TypeError:
                print(f"Команда {command[0]} была вызвана с некорректными аргументами")

        else:
            
            print(f"Команда {command[0]} не найдена! Список команд:\n{commands_str}")

    print("Произведен выход из программы.")


if __name__ == "__main__":
    main()
