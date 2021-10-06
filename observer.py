from abc import ABC, abstractmethod


class AbstractPublisher(ABC):
    """
    Абстрактный класс инициатора оповещения, чтобы были указаны обязательные методы
    """
    @abstractmethod
    def attach(self, observer):
        """метод для добавления наблюдателей"""
        pass

    @abstractmethod
    def detach(self, observer):
        """метод для удаления наблюдателей"""
        pass

    @abstractmethod
    def notify(self):
        """метод для оповещения наблюдателей"""
        pass


class StreamNotification(AbstractPublisher):
    """
    Класс для рассылки спама всем мазахистам, которые подписались на эту рассылку
    """

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.notify()


class AbstractSubscriber(ABC):
    """Абстрактный класс для каждого наблюдателя с обязательным методом для оповещения"""
    @abstractmethod
    def notify(self):
        pass


class Subscriber(AbstractSubscriber):
    def __init__(self, name):
        self.name = name

    def notify(self):
        print(f"Теперь {self.name} тоже получил оповещение")


class SpecialSubscriber(AbstractSubscriber):
    """
    Если нам нужно "особенное" поведение при оповещении, то его можно явно указать
    Также можно наследоваться от базового Subscriber и переопределять notify через super
    """
    def __init__(self, name):
        self.name = name

    def notify(self):
        print(f"Для таких как {self.name}, которым нужно \"особенное приглашение\" ")


if __name__ == '__main__':
    streamer = StreamNotification()

    subscriber_1 = Subscriber("subscriber_1")
    subscriber_2 = Subscriber("subscriber_2")
    subscriber_3 = Subscriber("subscriber_3")
    special_sub = SpecialSubscriber("special_sub")

    for sub in [subscriber_1, subscriber_2, subscriber_3, special_sub]:
        streamer.attach(sub)

    streamer.notify()

    streamer.detach(subscriber_2)
    streamer.notify()
