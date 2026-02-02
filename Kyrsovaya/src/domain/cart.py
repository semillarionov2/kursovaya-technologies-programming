from __future__ import annotations
from typing import List

from domain.items import Purchasable, WeightedProduct


class CartItem:
    def __init__(self, item: Purchasable, amount: float, is_weighed: bool = True) -> None:
        self.item = item
        self.amount = amount
        self.is_weighed = is_weighed

    def cost(self) -> float:
        return self.item.calc_cost(self.amount)


class Cart:
    def __init__(self) -> None:
        self._items: List[CartItem] = []

    @property
    def items(self) -> List[CartItem]:
        return list(self._items)

    def add(self, item: Purchasable, amount: float, is_weighed: bool = True) -> None:
        if amount <= 0:
            raise ValueError("Количество/вес должно быть больше 0")

        if isinstance(item, WeightedProduct):
            self._items.append(CartItem(item, amount, is_weighed))
        else:
            self._items.append(CartItem(item, amount, True))

    def remove(self, index: int) -> None:
        if index < 0 or index >= len(self._items):
            raise IndexError("Нет товара с таким номером")
        self._items.pop(index)

    def total(self) -> float:
        return sum(ci.cost() for ci in self._items)

    def has_unweighed_items(self) -> bool:
        for ci in self._items:
            if isinstance(ci.item, WeightedProduct) and not ci.is_weighed:
                return True
        return False

    def weigh_item(self, index: int, weight_kg: float) -> None:
        if index < 0 or index >= len(self._items):
            raise IndexError("Нет товара с таким номером")

        if weight_kg <= 0:
            raise ValueError("Вес должен быть больше 0")

        ci = self._items[index]

        if not isinstance(ci.item, WeightedProduct):
            raise ValueError("Этот товар не нужно взвешивать")

        ci.amount = weight_kg
        ci.is_weighed = True
