class Vacancy:

    def __init__(self, city: str, title: str, url: str, salary: int, description: str, experience: str, schedule: str):
        self.city = city
        self.title = title
        self.url = url
        self.salary = salary
        self.description = description
        self.experience = experience
        self.schedule = schedule

    def __le__(self, other):
        return self.salary <= other.salary

    def __lt__(self, other):
        return self.salary < other.salary

    def cast_to_json_format(self) -> dict:
        """ Преобразует объект вакансии в формат JSON """

        return {
            'city': self.city,
            'title': self.title,
            'url': self.url,
            'salary': self.salary,
            'description': self.description,
            'experience': self.experience,
            'schedule': self.schedule,
        }

    @staticmethod
    def cast_to_parent_dict(list_vacancies: list) -> dict:
        """ Преобразует список вакансий в словарь с ключом 'items'
        - list_vacancies (list): Список объектов вакансий """

        return {'items': list_vacancies}

    @staticmethod
    def cast_to_object_list(vacancies: dict) -> list:
        """ Преобразует словарь с вакансиями в список объектов Vacancy """

        vacancies_list = []

        for vacancy in vacancies['items']:
            salary_from = vacancy.get('salary').get('from')
            salary_to = vacancy.get('salary').get('to')
            salary = [salary_from if salary_from is not None else 'не указана',
                      salary_to if salary_to is not None else 'не указана']

            vacancies_list.append(Vacancy(
                vacancy['area']['name'],
                vacancy['name'],
                vacancy['alternate_url'],
                salary,
                vacancy['snippet']['requirement'] if vacancy['snippet']['requirement'] is not None
                else vacancy['snippet']['responsibility'],
                vacancy['experience']['name'],
                vacancy['schedule']['name'],
            ))
        return vacancies_list

    @staticmethod
    def cast_to_object_list_by_salary(vacancies: dict, salary: int = 0) -> list:
        """ Сортирует список вакансий и возвращает отсортированный список по зарплате """
        vacancies_list = []

        for vacancy in vacancies['items']:
            salary_from = vacancy.get('salary').get('from')

            if salary_from is not None:
                if salary <= salary_from:
                    vacancies_list.append(Vacancy(
                        vacancy['area']['name'],
                        vacancy['name'],
                        vacancy['alternate_url'],
                        salary,
                        vacancy['snippet']['requirement'] if vacancy['snippet']['requirement'] is not None
                        else vacancy['snippet']['responsibility'],
                        vacancy['experience']['name'],
                        vacancy['schedule']['name'],
                    ))

        return vacancies_list

    @staticmethod
    def get_sorted_vacancies(list_vacancies: list, is_reverse: bool = False, is_slice=False,
                             slice_num: int = 0) -> list:
        """ Сортирует список вакансий и возвращает отсортированный список """

        if is_slice:
            sorted_list = sorted(list_vacancies, reverse=is_reverse)[-slice_num:]
        else:
            sorted_list = sorted(list_vacancies, reverse=is_reverse)

        return sorted_list

    @staticmethod
    def get_founded_vacancies(list_vacancies: list) -> str:
        """ Возвращает строку с указанием количества найденных вакансий """

        return f'\nНайдено вакансий по запросу: {len(list_vacancies)}\n'
