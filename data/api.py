from abc import ABC, abstractmethod


class JobAPI(ABC):
    @abstractmethod
    def get_vacancies(self, city: str, search_query: str):
        pass
