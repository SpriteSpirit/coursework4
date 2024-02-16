import json
import os

from src.vacancy import Vacancy
from storage.data_saver import DataSaver


class JSONSaver(DataSaver):

    def __init__(self):
        self.user_list = []

    def add_vacancy(self, vacancy):
        """  """
        self.user_list.append(vacancy.cast_to_json_format())
        return self.user_list

    def delete_vacancy(self, index: int, filename: str):
        """  """
        data = self.load_json(filename)

        if data['items'] != 0:
            data['items'].pop(index - 1)

            self.save_json(data['items'], filename)

    @staticmethod
    def get_full_json_address_by_filename(filename: str) -> str:
        """  """

        root_folder = os.path.dirname(os.path.abspath(__file__))
        json_name = f'{filename}.json'
        full_address = os.path.join(root_folder, 'docs', json_name)

        return full_address

    @staticmethod
    def save_json(list_vacancies: list, filename: str):
        """  """
        address = JSONSaver.get_full_json_address_by_filename(filename)

        if os.path.exists(address):
            with open(address, 'w', encoding='utf-8') as file:
                json.dump(Vacancy.cast_to_parent_dict(list_vacancies), file, ensure_ascii=False)

        vacancies_count = len(list_vacancies["items"]) if isinstance(list_vacancies, dict) else len(list_vacancies)

        print(f'Вакансии в списке: {vacancies_count}')
        print(f'Список вакансий сохранен в {address}\n')

    @staticmethod
    def load_json(filename: str):
        """  """
        address = JSONSaver.get_full_json_address_by_filename(filename)

        with open(address, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data

# # testing data (need to delete)
# from data.hh_api import HeadHunterAPI
#
#
# hh = HeadHunterAPI()
# vacancies = hh.get_vacancies('москва', 'java')
# test_json = JSONSaver()
# hh_vacancies = Vacancy.cast_to_object_list(vacancies, 350000)
#
# for vacancy in hh_vacancies:
#     # print(vacancy.cast_to_json_format_format())
#     test_json.add_vacancy(vacancy)
#
# test_json.save_json(test_json.user_list, 'favourite_vacancies')
#
# test_json.delete_vacancy(1, 'favourite_vacancies')
# test_json.delete_vacancy(1, 'favourite_vacancies')
# test_json.delete_vacancy(2, 'favourite_vacancies')