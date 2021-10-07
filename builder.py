from abc import ABC, abstractmethod


class Product:
    """объявляем сам продукт"""
    def __init__(self):
        # элементы продукта
        self.elements = list()

    # метод для вывода элементов, которые содержатся в экземпляре
    def __str__(self):
        result = f"this product contains: {self.elements}"
        return result

    # метод для добавления элементов
    def add_element(self, element) -> None:
        self.elements.append(element)


class Builder(ABC):
    """
    Абстрактный класс строителя с обязательными методами, которые будут содавать элементы
    """
    @abstractmethod
    def get_product(self) -> Product():
        pass

    @abstractmethod
    def make_walls(self, walls_number: int) -> None:
        pass

    @abstractmethod
    def make_roof(self, type_of_roof: str) -> None:
        pass

    @abstractmethod
    def make_windows(self, number_of_windows: int) -> None:
        pass


class SomeBuilderOne(Builder):
    """
    Реализация конкретного строителя с дополнительным методом для автоматического обнуления
    продукта после его выдачи (эту часть можно делегировать на пользователя).
    """
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.product_in_instance = Product()

    def get_product(self) -> Product:
        current_product = self.product_in_instance
        # можно не обнулять самостоятельно при выдаче, а делать это по запросу клиента
        self.reset()
        return current_product

    def make_walls(self, walls_number: int) -> None:
        self.product_in_instance.add_element(f"walls: {walls_number}")

    def make_roof(self, type_of_roof: str) -> None:
        self.product_in_instance.add_element(f"roof: {type_of_roof}")

    def make_windows(self, number_of_windows: int) -> None:
        self.product_in_instance.add_element(f"windows: {number_of_windows}")


class Director:
    """
    Класс директора, который по сути является чем-то вроде Фасада, скрывая весь процесс создания
    продуктов, но при этом самостоятельно реншает как эти продукты будут выглядеть.
    """
    def __init__(self) -> None:
        self.builder_in_instance = None

    def set_builder(self, builder: Builder) -> None:
        # устанавливаем строителя, которому директор будет выдавать задачи
        self.builder_in_instance = builder

    def build_minimal(self) -> None:
        self.builder_in_instance.make_walls(4)
        self.builder_in_instance.make_roof('wooden')
        self.builder_in_instance.make_windows('0')

    def build_maximum(self) -> None:
        self.builder_in_instance.make_walls(100)
        self.builder_in_instance.make_roof('solar panels')
        self.builder_in_instance.make_windows('50')


if __name__ == '__main__':
    # с директором
    builder = SomeBuilderOne()
    director = Director()
    director.set_builder(builder)

    print('min: ')
    director.build_minimal()
    print(builder.get_product())

    print("max: ")
    director.build_maximum()
    print(builder.get_product())

    # без директора
    print("custom: ")
    builder.make_roof('classic')
    builder.make_walls(77)
    builder.make_windows(11)
    print(builder.get_product())



