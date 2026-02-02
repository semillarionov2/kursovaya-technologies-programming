from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from domain.cart import Cart
from domain.customer import Customer
from services.payment import PaymentStrategy, PaymentResult


# Исключение, возникающее при ошибке оформления покупки
class CheckoutError(Exception):
    pass


# Структура данных для хранения информации о чеке
@dataclass
class Receipt:
    text: str           # Текст чека
    total: float        # Итоговая сумма покупки
    payment: PaymentResult  # Результат оплаты


# Сервис оформления покупки
class CheckoutService:
    def checkout(self, customer: Customer, cart: Cart, payment: PaymentStrategy) -> Receipt:
        # Проверка, что корзина не пуста
        if len(cart.items) == 0:
            raise CheckoutError("Корзина пуста")

        # Проверка наличия невзвешенных товаров
        if cart.has_unweighed_items():
            raise CheckoutError("Есть товары, которые не взвешены")

        # Расчёт итоговой суммы
        total = round(cart.total(), 2)
        if total <= 0:
            raise CheckoutError("Сумма покупки некорректна")

        # Выполнение оплаты выбранным способом
        try:
            pay_res = payment.pay(customer, total)
        except Exception as e:
            raise CheckoutError(str(e))

        # Формирование текста чека
        receipt_text = self._build_receipt(cart, total, pay_res)

        # Добавление чека в историю покупок пользователя
        customer.add_purchase(receipt_text)

        return Receipt(text=receipt_text, total=total, payment=pay_res)

    def _build_receipt(self, cart: Cart, total: float, pay_res: PaymentResult) -> str:
        # Формирование текстового представления чека
        lines = []
        lines.append("====== ЧЕК ======")
        lines.append(datetime.now().strftime("Дата: %Y-%m-%d %H:%M:%S"))
        lines.append("")

        # Перечень товаров в корзине
        for i, ci in enumerate(cart.items, start=1):
            lines.append(f"{i}. {ci.item.name} — {ci.amount} — {ci.cost():.2f} ₽")

        lines.append("")
        lines.append(f"ИТОГО: {total:.2f} ₽")
        lines.append(f"Наличными: {pay_res.paid_cash:.2f} ₽")
        lines.append(f"Бонусами:  {pay_res.paid_bonus:.2f} ₽")
        lines.append("=================")

        return "\n".join(lines)
