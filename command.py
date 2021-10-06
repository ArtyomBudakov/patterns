from abc import ABC, abstractmethod


class Command(ABC):
    """
    Абстрактный класс Команды, который объявляет методы для выполнения команд.
    """

    @abstractmethod
    def do_something(self):
        pass


class BaseOperation(Command):
    """
    Наследуется от Астрактного класса Command, потому что должен содержать методы
    команды (абстрактного класса)

    Класс может выполнять базовые операции самостоятельно, получая только необходимые
    данные для выполнения.
    """

    def __init__(self, data):
        self._data = data

    def do_something(self):
        print(f"базовый класс, выполняющий базовую операцию с данными: {self._data}")


class BusinessLogic:
    """
    НЕ(!) наследуется от ABC потому что фактически не относится к команде, а просто
    выполняет поставленные задачи бизнес логики
    """

    def do_something_one(self, data):
        print(f"BusinessLogic: do_something_one: {data}")

    def do_something_two(self, data):
        print(f"BusinessLogic: do_something_two: {data}")


class ComplicatedCommand(Command):
    """
    Наследуется от Астрактного класса Command, потому что должен содержать методы
    команды (абстрактного класса)

    Команды, которые передают выполнение объектам другого класса. Тем самым логику
    выполняют другие методы, а в этом классе описывается логика взаимодействия с этими
    методами других классов
    """

    def __init__(self, recipient: BusinessLogic, data_one, data_two):
        """
        Через конструктор указывается объекты получателей (BusinessLogic) и данные,
        которые необходимы для выполнения операций
        """

        # получатель, который будет выполнять бизнес логику. должен быть экземпляром класса
        # BusinessLogic в данном случае
        self._recipient = recipient
        self._data_one = data_one
        self._data_two = data_two

    def do_something(self):
        """
        Метод из астрактного класса, который описывает процесс делегирования выполнения команд
        вызывает функции выполнения у получателя, который выполняет бизнес логику на основе
        полученных данных
        """

        print("ComplicatedCommand: сложная бизнес логика должна выполняться 'получателем'")
        self._recipient.do_something_one(self._data_one)
        self._recipient.do_something_two(self._data_two)


class Invoker:
    """
    НЕ(!) наследуется от ABC потому что фактически не относится к команде, хранит ссылки на
    объекты команд и обращается к ним, если нужно выполнить какое-от действие
    """

    _on_start = None
    _on_finish = None

    # параметр должен быть командой абстрактного класса. иначе говоря, должен
    # быть наследником от этого класса
    def set_on_start(self, command: Command):
        self._on_start = command

    def set_on_finish(self, command: Command):
        self._on_finish = command

    def do_something_important(self):
        """
        Отправитель не зависит от классов конкретных команд и получателей.
        Отправитель передаёт запрос получателю косвенно, выполняя команду.
        """

        if isinstance(self._on_start, Command):
            print("Invoker: выполняется команда, установленная в self._on_start")
            self._on_start.do_something()

        print("Сам 'Invoker' что-то выполняет")

        if isinstance(self._on_finish, Command):
            print("Invoker: выполняется команда, установленная в self._on_finish")
            self._on_finish.do_something()


if __name__ == "__main__":

    # можно самостоятельно вызвать команду
    b1 = BaseOperation('можно самостоятельно вызвать команду')
    b1.do_something()

    # определяем сложную команду, указывая класс, который выполняет бизнес логику,
    # которую мы хотим выполнить и данные с которыми должно произойти выполнение
    cc1 = ComplicatedCommand(BusinessLogic(), "какие-то данные раз", "какие-то данные два")
    # выполнить команду
    cc1.do_something()

    invoker = Invoker()
    # определяем команду для Отправителя и передаём ему данные, с которыми будет работать команда
    invoker.set_on_start(BaseOperation("Say Hi!"))

    # определяем команду для Отправителя и передаём ему данные, с которыми будет работать команда
    # в этом случае указываем команду и данные, а Отправитель сам решает как это передать выбранной
    # команде, причём выбранная команда будет использовать класс бизнес логики для выполнения задач
    invoker.set_on_finish(ComplicatedCommand(
        BusinessLogic(), "действие 1", "действие 2"))

    # выполняет команды и данные, которые уже установлены в нём
    invoker.do_something_important()

