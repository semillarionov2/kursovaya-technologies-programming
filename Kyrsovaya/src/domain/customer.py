from __future__ import annotations


class Customer:
    def __init__(self, full_name: str, cash: float, bonus_points: float) -> None:
        self.full_name = full_name
        self.cash = cash
        self.bonus_points = bonus_points
        self.purchases: list[str] = []

    def can_pay_cash(self, amount: float) -> bool:
        return self.cash >= amount

    def can_pay_bonus(self, amount: float) -> bool:
        return self.bonus_points >= amount

    def pay_cash(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Сумма не может быть отрицательной")
        if self.cash < amount:
            raise ValueError("Недостаточно наличных")
        self.cash -= amount

    def pay_bonus(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Сумма не может быть отрицательной")
        if self.bonus_points < amount:
            raise ValueError("Недостаточно бонусов")
        self.bonus_points -= amount

    def add_purchase(self, receipt: str) -> None:
        self.purchases.append(receipt)
