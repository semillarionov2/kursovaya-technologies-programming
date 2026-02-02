from __future__ import annotations

from domain.items import Product, WeightedProduct, Service, Purchasable


def get_catalog() -> list[Purchasable]:
    # Каталог продуктового магазина
    return [
        # Штучные товары
        Product("Хлеб", 49.0),
        Product("Молоко", 89.0),
        Product("Яйца (10 шт.)", 129.0),
        Product("Сахар", 79.0),
        Product("Масло сливочное", 199.0),

        # Взвешиваемые товары
        WeightedProduct("Мясо", 599.0),          # ₽ за кг
        WeightedProduct("Куриное филе", 449.0),  # ₽ за кг
        WeightedProduct("Картофель", 39.0),      # ₽ за кг
        WeightedProduct("Яблоки", 99.0),          # ₽ за кг

        # Услуги
        Service("Пакет", 10.0),
        Service("Доставка", 299.0),
    ]
