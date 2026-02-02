from __future__ import annotations


# Класс, описывающий покупателя магазина
class Customer:
    def __init__(self, full_name: str, cash: float, bonus_points: float) -> None:
        self.full_name = full_name          # ФИО покупателя
        self.cash = cash                    # Баланс наличных средств
        self.bonus_points = bonus_points    # Баланс бонусных баллов
        self.purchases: list[str] = []      # История покупок (чеки)

    def can_pay_cash(self, amount: float) -> bool:
        # Проверка возможности оплаты наличными
        return self.cash >= amount

    def can_pay_bonus(self, amount: float) -> bool:
        # Проверка возможности оплаты бонусами
        return self.bonus_points >= amount

    def pay_cash(self, amount: float) -> None:
        # Оплата наличными средствами
        if amount < 0:
            raise ValueError("Сумма не может быть отрицательной")
        if self.cash < amount:
            raise ValueError("Недостаточно наличных")
        self.cash -= amount

    def pay_bonus(self, amount: float) -> None:
        # Оплата бонусными баллами
        if amount < 0:
            raise ValueError("Сумма не может быть отрицательной")
        if self.bonus_points < amount:
            raise ValueError("Недостаточно бонусов")
        self.bonus_points -= amount

    def add_purchase(self, receipt: str) -> None:
        # Добавление чека в историю покупок
        self.purchases.append(receipt)
