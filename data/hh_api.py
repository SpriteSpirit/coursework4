from data.api import JobAPI
import requests


class HeadHunterAPI(JobAPI):
    def get_vacancies(self, city: str, search_query: str, page=0) -> dict:
        """
        Получает список вакансий для указанного города и поискового запроса.

        :param city : Название города.
        :param search_query: Поисковый запрос.
        :param page: Номер страницы результатов (по умолчанию 0).

        :return: Словарь с данными о вакансиях.
        """

        params = {
            'text': f'NAME:{search_query}',
            'area': city,
            'only_with_salary': True,
            'page': page,
            'per_page': 100,
        }

        response = requests.get("https://api.hh.ru/vacancies", params=params)
        assert isinstance(response.raise_for_status, object)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_areas() -> dict:
        """ Возвращает словарь стран """

        return requests.get('https://api.hh.ru/areas').json()

    @staticmethod
    def get_cities() -> dict:
        """ Возвращает словарь с информацией о городах. """

        cities = {}

        for country in HeadHunterAPI.get_areas():
            if country['id'] == '113':
                for region in country['areas']:
                    if region['areas'] is not None:
                        for city in region['areas']:
                            cities[city['name']] = int(city['id'])
                    cities[region['name']] = int(region['id'])
        return cities

    @staticmethod
    def get_city_id_by_name(city_name: str) -> int:
        """
        Получает числовой идентификатор города по его названию.
        :param city_name: Название города.
        :return: Числовой идентификатор города.
        """

        cities = HeadHunterAPI.get_cities()

        for city in cities.keys():
            if city_name.lower() in city.lower():
                return cities[city_name.title()]

    @staticmethod
    def get_city_name_by_id(city_id: int) -> str:
        """
        Получает название города по его числовому идентификатору.
        :param city_id: Числовой идентификатор города.
        :return: Название города.
        """

        cities = HeadHunterAPI.get_cities()

        for city_name in cities.keys():
            if city_id == cities[city_name]:
                return city_name
