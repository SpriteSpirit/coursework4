import json
import os

from src.vacancy import Vacancy
from storage.data_saver import DataSaver


class JSONSaver(DataSaver):

    def __init__(self):
        self.user_list = []

    def add_vacancy(self, vacancy):
        """ Добавляет вакансию в список пользователя """

        self.user_list.append(vacancy.cast_to_json_format())
        return self.user_list

    def delete_vacancy(self, index: int, filename: str):
        """ Удаляет вакансию из списка пользователя """

        data = self.load_json(filename)

        if data['items'] != 0:
            data['items'].pop(index - 1)

            self.save_json(data['items'], filename)

    @staticmethod
    def get_full_json_address_by_filename(filename: str) -> str:
        """ Получает полный адрес к файлу по указанному имени"""

        root_folder = os.path.dirname(os.path.abspath(__file__))
        json_name = f'{filename}.json'
        full_address = os.path.join(root_folder, 'docs', json_name)

        return full_address

    @staticmethod
    def save_json(list_vacancies: list, filename: str) -> None:
        """ Сохраняет список вакансий в json-файл """

        address = JSONSaver.get_full_json_address_by_filename(filename)

        if os.path.exists(address):
            with open(address, 'w', encoding='utf-8') as file:
                json.dump(Vacancy.cast_to_parent_dict(list_vacancies), file, ensure_ascii=False)

        vacancies_count = len(list_vacancies["items"]) if isinstance(list_vacancies, dict) else len(list_vacancies)

        print(f'Вакансий в списке: {vacancies_count}')
        print(f'Список вакансий сохранен в {address}\n')

    @staticmethod
    def load_json(filename: str) -> dict:
        """ Выгружает из json-файла список вакансий """

        address = JSONSaver.get_full_json_address_by_filename(filename)

        with open(address, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data
