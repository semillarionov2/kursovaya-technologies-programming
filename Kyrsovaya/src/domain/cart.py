from __future__ import annotations
from typing import List

from domain.items import Purchasable, WeightedProduct


# Класс, описывающий одну позицию в корзине
class CartItem:
    def __init__(self, item: Purchasable, amount: float, is_weighed: bool = True) -> None:
        self.item = item          # Товар или услуга
        self.amount = amount      # Количество или вес
        self.is_weighed = is_weighed  # Признак того, что товар был взвешен

    def cost(self) -> float:
        # Расчёт стоимости позиции корзины
        return self.item.calc_cost(self.amount)


# Класс корзины покупателя
class Cart:
    def __init__(self) -> None:
        self._items: List[CartItem] = []

    @property
    def items(self) -> List[CartItem]:
        # Возвращает список товаров в корзине
        return list(self._items)

    def add(self, item: Purchasable, amount: float, is_weighed: bool = True) -> None:
        # Добавление товара или услуги в корзину
        if amount <= 0:
            raise ValueError("Количество/вес должно быть больше 0")

        if isinstance(item, WeightedProduct):
            self._items.append(CartItem(item, amount, is_weighed))
        else:
            self._items.append(CartItem(item, amount, True))

    def remove(self, index: int) -> None:
        # Удаление товара из корзины по индексу
        if index < 0 or index >= len(self._items):
            raise IndexError("Нет товара с таким номером")
        self._items.pop(index)

    def total(self) -> float:
        # Расчёт общей стоимости корзины
        return sum(ci.cost() for ci in self._items)

    def has_unweighed_items(self) -> bool:
        # Проверка наличия невзвешенных товаров
        for ci in self._items:
            if isinstance(ci.item, WeightedProduct) and not ci.is_weighed:
                return True
        return False

    def weigh_item(self, index: int, weight_kg: float) -> None:
        # Установка веса для взвешиваемого товара
        if index < 0 or index >= len(self._items):
            raise IndexError("Нет товара с таким номером")

        if weight_kg <= 0:
            raise ValueError("Вес должен быть больше 0")

        ci = self._items[index]

        if not isinstance(ci.item, WeightedProduct):
            raise ValueError("Этот товар не нужно взвешивать")

        ci.amount = weight_kg
        ci.is_weighed = True
