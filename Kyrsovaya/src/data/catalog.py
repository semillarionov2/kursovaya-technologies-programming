from __future__ import annotations

from domain.items import Product, WeightedProduct, Service, Purchasable


def get_catalog() -> list[Purchasable]:
    # Каталог магазина техники
    return [
        Product("Смартфон", 24999.0),
        Product("Ноутбук", 69999.0),
        Product("Монитор 27\"", 17999.0),
        Product("Клавиатура", 2999.0),
        Product("Мышь", 1499.0),
        Product("Наушники", 4999.0),

        # Взвешиваемые товары (для выполнения требования задания)
        WeightedProduct("Кабель (на отрез, кг)", 1200.0),
        WeightedProduct("Термопаста (на отрез, кг)", 15000.0),

        # Услуги
        Service("Доставка", 900.0),
        Service("Настройка ноутбука", 1500.0),
        Service("Расширенная гарантия", 3500.0),
    ]
