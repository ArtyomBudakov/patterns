from abc import ABC, abstractmethod
from datetime import datetime


class AbstractDatabase(ABC):
    """абстрактный класс для описания методов реального объекта"""
    @abstractmethod
    def request(self):
        pass


class TestDatabase(AbstractDatabase):
    """реальный объект, выполняющий логику"""
    def __init__(self, token, data):
        self.token = token
        self.data = data

    def request(self):
        print(f"Handle in request with token: {self.token} and data: {self.data}")


class Proxy(AbstractDatabase):
    """прокси объект, который ведёт логирование и проверяет доступность к реальному объекту"""
    def __init__(self, token, data):
        self._main_database = TestDatabase(token, data)
        self.token = token
        self.data = data

    def request(self):
        if self.check_token():
            self.logger()
            self._main_database.request()

    def check_token(self):
        if self.token in (1, 2, 3, 4, 5):
            return True
        else:
            print(f"Denied in access from proxy. token: {self.token}")
            return False

    def logger(self):
        print(f"Just logger logical with identification by {self.token} at {datetime.now()}")


if __name__ == '__main__':
    token = 2
    data = "one, two"

    # значально была идея передавать экземпляр класса TestDatabase при создании экземпляра класса proxy
    # но при такой реализации выглядит странно то, что клиенту нужно практически дублировать код, что, как
    # я считаю - плохо. поэтому в итоговой реализации сделал формирование реального класса в proxy, что
    # позволяет не дублировать код при использовании прокси. Плюс, не факт, что клиент должен знать о том, что
    # у нас используется прокси.
    # real_object = TestDatabase(token, data)
    # proxy = Proxy(real_object, token, data)

    proxy = Proxy(token, data)
    proxy.request()

    token = 7
    data = "aaa, bbbb"
    proxy = Proxy(token, data)
    proxy.request()
