import os
import json


class Program:
    def __init__(self):
        self.directory = os.getcwd()

    def update_directory(self, _directory):
        self.directory = os.path.dirname(_directory)

    def get_directory_data(self):
        file_info = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                file_path = os.path.join(root, file)
                stat_info = os.stat(file_path)
                file_info.append({
                    "name": file,
                    "path": file_path,
                    "size": stat_info.st_size,
                    "last_modified": stat_info.st_mtime
                })
        return file_info

    @staticmethod
    def save_file_info(file_info):
        print('i save')
        with open("files_info.json", "w") as json_file:
            json.dump(file_info, json_file, indent=4)

    @staticmethod
    def get_binary_file_info():
        with open("files_info.json", "rb") as json_file:
            data = json_file.read()
            return data
