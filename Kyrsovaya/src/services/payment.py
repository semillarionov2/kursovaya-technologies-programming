from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.customer import Customer


@dataclass
class PaymentResult:
    paid_cash: float
    paid_bonus: float


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, customer: Customer, total: float) -> PaymentResult:
        pass


class CashOnlyPayment(PaymentStrategy):
    def pay(self, customer: Customer, total: float) -> PaymentResult:
        customer.pay_cash(total)
        return PaymentResult(paid_cash=total, paid_bonus=0.0)


class BonusOnlyPayment(PaymentStrategy):
    def pay(self, customer: Customer, total: float) -> PaymentResult:
        customer.pay_bonus(total)
        return PaymentResult(paid_cash=0.0, paid_bonus=total)


class MixedPayment(PaymentStrategy):
    """Часть бонусами, остаток наличными"""

    def __init__(self, bonus_to_use: float) -> None:
        self.bonus_to_use = max(0.0, bonus_to_use)

    def pay(self, customer: Customer, total: float) -> PaymentResult:
        bonus = min(self.bonus_to_use, total, customer.bonus_points)
        cash = total - bonus

        if cash > customer.cash:
            raise ValueError("Недостаточно средств для смешанной оплаты")

        if bonus > 0:
            customer.pay_bonus(bonus)
        if cash > 0:
            customer.pay_cash(cash)

        return PaymentResult(paid_cash=cash, paid_bonus=bonus)
