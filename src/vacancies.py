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

    def to_json_format(self) -> dict:
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
    def to_parent_dict(list_vacancies: list) -> dict:
        """ Преобразует список вакансий в словарь с ключом 'items'
        - list_vacancies (list): Список объектов вакансий """

        return {'items': list_vacancies}