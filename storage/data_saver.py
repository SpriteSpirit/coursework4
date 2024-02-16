from abc import ABC, abstractmethod


class DataSaver(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, *args):
        pass

