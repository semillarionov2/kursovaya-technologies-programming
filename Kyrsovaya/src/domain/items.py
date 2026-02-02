from __future__ import annotations
from abc import ABC, abstractmethod


class Purchasable(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def calc_cost(self, amount: float) -> float:
        raise NotImplementedError


class Product(Purchasable):
    def __init__(self, name: str, unit_price: float) -> None:
        self._name = name
        self._unit_price = unit_price

    @property
    def name(self) -> str:
        return self._name

    def calc_cost(self, amount: float) -> float:
        return self._unit_price * amount


class WeightedProduct(Purchasable):
    def __init__(self, name: str, price_per_kg: float) -> None:
        self._name = name
        self._price_per_kg = price_per_kg

    @property
    def name(self) -> str:
        return self._name

    def calc_cost(self, amount: float) -> float:
        return self._price_per_kg * amount


class Service(Purchasable):
    def __init__(self, name: str, unit_price: float) -> None:
        self._name = name
        self._unit_price = unit_price

    @property
    def name(self) -> str:
        return self._name

    def calc_cost(self, amount: float) -> float:
        return self._unit_price * amount
